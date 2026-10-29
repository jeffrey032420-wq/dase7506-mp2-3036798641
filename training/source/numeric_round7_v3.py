"""V3: distinguish math delimiters from unknown words/units at run boundaries."""
import ast
from fractions import Fraction
import re
import numpy as np
from common import parse_answer

NAMES=['checked_log','false_log','true_log','false_fraction','max_relative_error',
       'has_false','checked_coverage','distinct_result_log','any_result_matches_final',
       'last_result_matches_final','last_result_relative_error','has_result_and_final',
       'last_checked_true','unchecked_fraction']


def evaluate(expression):
    expression=expression.strip()
    if len(expression)>180 or not re.fullmatch(r'[0-9.()+*/\-\s]+',expression):
        raise ValueError('Unsupported expression')
    tree=ast.parse(expression,mode='eval')
    def visit(node,depth=0):
        if depth>12:
            raise ValueError('Depth limit')
        if isinstance(node,ast.Constant) and type(node.value) in (int,float):
            literal=ast.get_source_segment(expression,node)
            if len(literal)>40:
                raise ValueError('Literal limit')
            value=Fraction(literal)
        elif isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
            value=visit(node.operand,depth+1)*(-1 if isinstance(node.op,ast.USub) else 1)
        elif isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
            a,b=visit(node.left,depth+1),visit(node.right,depth+1)
            if isinstance(node.op,ast.Add): value=a+b
            elif isinstance(node.op,ast.Sub): value=a-b
            elif isinstance(node.op,ast.Mult): value=a*b
            else: value=a/b
        else:
            raise ValueError('Unsupported syntax')
        if abs(value)>10**15 or abs(value.numerator)>10**24 or value.denominator>10**24:
            raise ValueError('Magnitude limit')
        return value
    return visit(tree.body)


def normalize(text):
    text=text[:24000].replace('×','*').replace('÷','/').replace('−','-')
    text=re.sub(r'(?<=\d),(?=\d)','',text)
    for old,new in [(r'\times','*'),(r'\cdot','*'),(r'\div','/'),(r'\left',''),(r'\right','')]:
        text=text.replace(old,new)
    # Only constant arithmetic inside braces is transformed. Unknown LaTeX stays unknown.
    fraction=r'\\(?:d?frac)\{([0-9.()+*/\-\s]+)\}\{([0-9.()+*/\-\s]+)\}'
    for _ in range(6):
        new=re.sub(fraction,r'((\1)/(\2))',text)
        if new==text:
            break
        text=new
    text=re.sub(r'\\(?:text|mathrm)\{[^{}]*\}','|',text)
    text=re.sub(r'\\boxed\{[^{}]*\}','|',text)
    text=re.sub(r'(\d+(?:\.\d+)?)\s*%',r'((\1)/100)',text)
    return text.replace('$','#')


def relative_error(a,b):
    return float(abs(a-b)/max(Fraction(1),abs(a),abs(b)))


def evidence(text):
    text=normalize(text)
    records=[]
    total=min(text.count('='),64)
    # Runs never cross lines or textual/unit delimiters. Inspect each adjacent equality
    # in a chain, so a named left-hand side need not hide a later numeric equation.
    for match in re.finditer(r'[0-9(+\-][0-9.()+*/\-= \t]*',text):
        run=match.group()
        if '=' not in run:
            continue
        parts=run.split('=')
        prefix=text[:match.start()]
        suffix=text[match.end():]
        adjacent=bool(prefix and (prefix[-1].isalnum() or prefix[-1] in '^_\\'))
        suffix_of_algebra=bool(run[0] in '+-' and prefix.rstrip() and
                               (prefix.rstrip()[-1].isalnum() or prefix.rstrip()[-1] in '^_\\'))
        previous=prefix.rsplit('\n',1)[-1].rstrip()
        incomplete_left=bool(previous and (previous[-1].isalnum() or previous[-1] in '*/^_\\\\|)]}' or
                             (run[0] in '+-' and previous[-1] in ')]}|')))
        right_unsafe=bool(suffix and (suffix[0].isalnum() or suffix[0] in '^_\\'))
        for i,(a,b) in enumerate(zip(parts,parts[1:])):
            if i==0 and (adjacent or suffix_of_algebra or incomplete_left):
                continue
            if i==len(parts)-2 and right_unsafe:
                continue
            try:
                left=evaluate(a)
                right=evaluate(b.strip().rstrip('.'))
                error=relative_error(left,right)
                records.append((left,right,error))
            except (ValueError,SyntaxError,ZeroDivisionError,OverflowError,RecursionError):
                continue
            if len(records)>=64:
                return records,total
    return records,total


def candidate_features(text):
    records,total=evidence(text)
    errors=[r[2] for r in records]
    false=sum(e>1e-6 for e in errors)
    answer=parse_answer(text)
    final=Fraction(answer) if answer is not None else None
    final_errors=[relative_error(r[1],final) for r in records] if final is not None else []
    return [np.log1p(len(records)),np.log1p(false),np.log1p(len(records)-false),
            false/max(1,len(records)),max(errors,default=0),float(false>0),
            len(records)/max(total,len(records),1),np.log1p(len(set(r[1] for r in records))),
            float(any(e<=1e-6 for e in final_errors)),float(bool(final_errors) and final_errors[-1]<=1e-6),
            final_errors[-1] if final_errors else 0,float(bool(final_errors)),
            float(bool(errors) and errors[-1]<=1e-6),max(0,total-len(records))/max(total,1)]


def build(bank):
    return np.asarray([candidate_features(c['text']) for row in bank for c in row['candidates']],dtype=np.float64)
