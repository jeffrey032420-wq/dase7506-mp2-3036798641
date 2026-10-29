"""Conservative arithmetic and lexical features; no references or sample IDs."""
import ast
from collections import Counter
from fractions import Fraction
import math
import re
import numpy as np
from common import parse_answer

NUMBER = re.compile(r'(?<![\w.])[-+]?\d[\d,]*(?:\.\d+)?(?:/\d+)?')
WORDS = re.compile(r'[a-z]+')
MATH_NAMES = ['equations_checked','equations_false','equations_true','false_fraction',
              'max_relative_error','has_false_equation','answer_parsed','negative_answer',
              'noninteger_answer','log_answer_magnitude','answer_in_question',
              'question_number_coverage','answer_as_sum','answer_as_difference',
              'answer_as_product','answer_as_quotient','answer_greater_than_question_max',
              'log_answer_to_question_scale','question_word_coverage','answer_support',
              'answer_rank','question_asks_remaining','question_asks_total','question_asks_each']


def safe_number_expression(s):
    """Parse bounded literal arithmetic; never eval or execute candidate content."""
    s=s.strip()
    if len(s)>120 or not re.fullmatch(r'[\d.()+*/\-\s]+',s):
        raise ValueError('Unsupported arithmetic')
    tree=ast.parse(s,mode='eval')
    def visit(node,depth=0):
        if depth>12:
            raise ValueError('Expression too deep')
        if isinstance(node,ast.Constant) and type(node.value) in (int,float):
            value=float(node.value)
        elif isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            value=visit(node.operand,depth+1)*(1 if isinstance(node.op,ast.UAdd) else -1)
        elif isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
            a,b=visit(node.left,depth+1),visit(node.right,depth+1)
            if isinstance(node.op,ast.Add): value=a+b
            elif isinstance(node.op,ast.Sub): value=a-b
            elif isinstance(node.op,ast.Mult): value=a*b
            else: value=a/b
        else:
            raise ValueError('Unsupported syntax')
        if not math.isfinite(value) or abs(value)>1e15:
            raise ValueError('Arithmetic out of range')
        return value
    return visit(tree.body)


def equation_summary(text):
    text=text.replace(',','').replace('×','*').replace('÷','/').replace('−','-')
    for old,new in [(r'\times','*'),(r'\cdot','*'),(r'\div','/'),(r'\left',''),(r'\right','')]:
        text=text.replace(old,new)
    # Unsupported LaTeX remains unsupported; unknown expressions never count as false.
    text=re.sub(r'\\(?:d?frac)\{(-?\d+(?:\.\d+)?)\}\{(-?\d+(?:\.\d+)?)\}',r'(\1)/(\2)',text)
    text=re.sub(r'\\boxed\{([\d.()+*/\-\s]+)\}',r'(\1)',text)
    text=text.replace('$','')
    errors=[]
    pattern=r'(?<![\w.])([\d.()+*/\-][\d.()+*/\-\s]{0,100})=\s*([\d.()+*/\-][\d.()+*/\- ]{0,100})'
    for match in re.finditer(pattern,text):
        prefix=text[:match.start()].rstrip()
        # Do not interpret the numeric suffix of an unsupported algebraic expression.
        # E.g. the '+ 3' inside '2x + 3 = 7' must not be checked as a standalone sum.
        if prefix and (prefix[-1].isalnum() or prefix[-1] in '+-*/^\\'):
            continue
        try:
            a=safe_number_expression(match[1])
            b=safe_number_expression(match[2].strip().rstrip('.'))
            errors.append(abs(a-b)/max(1,abs(a),abs(b)))
        except (ValueError,SyntaxError,ZeroDivisionError,OverflowError,RecursionError):
            continue
    false=sum(e>1e-5 for e in errors)
    return [np.log1p(len(errors)),np.log1p(false),np.log1p(len(errors)-false),
            false/max(1,len(errors)),max(errors,default=0),float(false>0)]


def numbers(text):
    result=[]
    for s in NUMBER.findall(text):
        try:
            v=float(Fraction(s.replace(',','')))
            if math.isfinite(v) and abs(v)<1e12:
                result.append(v)
        except (ValueError,ZeroDivisionError,OverflowError):
            pass
    return result


def math_features(bank):
    rows=[]
    for row in bank:
        q=row['question'].lower()
        qnums=list(dict.fromkeys(numbers(q)))[:24]
        qw=set(WORDS.findall(q))
        answers=[parse_answer(c['text']) for c in row['candidates']]
        vals=[float(Fraction(a)) if a is not None else 0.0 for a in answers]
        scale=max([abs(v) for v in qnums]+[1])
        for j,c in enumerate(row['candidates']):
            t=c['text']
            v=vals[j]
            cn=set(numbers(t))
            operations=[False]*4
            if answers[j] is not None:
                for a in qnums:
                    for b in qnums:
                        candidates=[a+b,a-b,a*b,a/b if b else math.inf]
                        for k,value in enumerate(candidates):
                            operations[k] |= abs(v-value)<=1e-5*max(1,abs(v))
            rows.append(equation_summary(t)+[float(answers[j] is not None),float(v<0),
                float(v!=int(v)),np.log1p(abs(v)),float(any(abs(v-a)<1e-8 for a in qnums)),
                sum(a in cn for a in qnums)/max(1,len(qnums)),*map(float,operations),
                float(abs(v)>scale),np.log1p(abs(v)/scale),len(qw&set(WORDS.findall(t.lower())))/max(1,len(qw)),
                answers.count(answers[j])/4 if answers[j] is not None else 0,
                sum(v>a for a in vals)/4,float(bool(re.search(r'\b(left|remain|remaining)\b',q))),
                float(bool(re.search(r'\b(total|altogether|combined)\b',q))),
                float(bool(re.search(r'\b(each|per)\b',q)))])
    x=np.asarray(rows,dtype=np.float64)
    if x.shape[1]!=len(MATH_NAMES) or not np.isfinite(x).all():
        raise ValueError('Invalid math feature matrix')
    return x


def tokens(text):
    words=WORDS.findall(text.lower())
    return words+[a+' '+b for a,b in zip(words,words[1:])]


def fit_vocabulary(bank,limit=384):
    frequency=Counter()
    for row in bank:
        for c in row['candidates']:
            frequency.update(set(tokens(c['text'])))
    n=4*len(bank)
    selected=sorted(((word,count) for word,count in frequency.items() if 8<=count<=0.8*n),
                    key=lambda item:(-item[1],item[0]))[:limit]
    vocab=[word for word,count in selected]
    idf=np.array([np.log((1+n)/(1+count))+1 for word,count in selected])
    return vocab,idf


def lexical_features(bank,vocab,idf):
    index={word:i for i,word in enumerate(vocab)}
    x=np.zeros((4*len(bank),len(vocab)))
    for n,c in enumerate(c for row in bank for c in row['candidates']):
        for word,count in Counter(tokens(c['text'])).items():
            i=index.get(word)
            if i is not None:
                x[n,i]=np.log1p(count)*idf[i]
    return x
