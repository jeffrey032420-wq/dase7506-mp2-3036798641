"""Soft exact-value grounding/false-equation ancestry on the frozen R120 parent."""
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import re
import numpy as np
from common import parse_answer
from numeric_round7_v3 import normalize,evaluate
from method_round12_dependency import operand_values
from method_round108_group_subsets import tables,question_numbers
from method_round109_arithmetic_residual import close,anchored
from method_round120_question_interaction import candidate_scores as parent_scores

CONSTANTS = frozenset(map(Fraction,(0,1,2,7,10,12,24,60,100)))
NAMES = ('question_leaf_fraction','question_or_constant_leaf_fraction','prior_result_leaf_fraction',
         'final_has_scalar_equation','final_ancestor_count_log','final_ancestor_false_fraction',
         'strict_unknown_leaf_fraction','relaxed_unknown_leaf_fraction','strict_grounded_true_chain',
         'relaxed_grounded_true_chain','ancestor_question_value_coverage','equations_outside_final_ancestry_fraction')
COLUMNS = {'grounding':[0,1,2,12,13,14],
           'ancestry':list(range(3,12))+list(range(15,24)),
           'both':list(range(24))}


def graph_records(text):
    text = normalize(text)
    records = []
    for match in re.finditer(r'[0-9(+\-][0-9.()+*/\-= \t]*',text):
        run = match.group()
        if '=' not in run:
            continue
        parts = run.split('=');prefix,suffix = text[:match.start()],text[match.end():]
        adjacent = bool(prefix and (prefix[-1].isalnum() or prefix[-1] in '^_\\'))
        suffix_of_algebra = bool(run[0] in '+-' and prefix.rstrip() and (prefix.rstrip()[-1].isalnum() or prefix.rstrip()[-1] in '^_\\'))
        previous = prefix.rsplit('\n',1)[-1].rstrip()
        incomplete_left = bool(previous and (previous[-1].isalnum() or previous[-1] in '*/^_\\|)]}' or (run[0] in '+-' and previous[-1] in ')]}|')))
        right_unsafe = bool(suffix and (suffix[0].isalnum() or suffix[0] in '^_\\'))
        for i,(a,b) in enumerate(zip(parts,parts[1:])):
            if i==0 and (adjacent or suffix_of_algebra or incomplete_left):
                continue
            if i==len(parts)-2 and right_unsafe:
                continue
            # Graph outputs must be explicit scalar claims; do not turn an
            # expression on the RHS into an asserted intermediate result.
            if not re.fullmatch(r'\s*[-+]?(?:\d+(?:\.\d*)?|\.\d+)\s*',b):
                continue
            try:
                left,right = evaluate(a),evaluate(b.strip().rstrip('.'))
                operands = operand_values(a)
                if operands is None:
                    continue
                records.append((left,right,frozenset(operands)))
            except (ValueError,SyntaxError,ZeroDivisionError,OverflowError,RecursionError):
                continue
            if len(records)==64:
                return records
    return records


def candidate_features(question,text):
    source = frozenset(question_numbers(question));records = graph_records(text)
    total,q_known,relaxed_known,reused = 0,0,0,0
    for k,(_,_,operands) in enumerate(records):
        earlier = {r[1] for r in records[:k]}
        total += len(operands);q_known += len(operands&source)
        relaxed_known += len(operands&(source|CONSTANTS));reused += len((operands-source)&earlier)
    features = np.zeros(12)
    features[:3] = np.array([q_known,relaxed_known,reused])/max(total,1)
    parsed = parse_answer(text)
    roots = [k for k,r in enumerate(records) if parsed is not None and r[1]==Fraction(parsed)]
    if not roots:
        return features
    root = roots[-1]
    @lru_cache(None)
    def trace_node(k,relaxed):
        used,unknown,covered,terminals = {k},set(),set(),set()
        for value in records[k][2]:
            if value in source:
                covered.add(value);terminals.add(value)
            else:
                prior = [j for j in range(k) if records[j][1]==value]
                if prior:
                    u,b,c,t = trace_node(prior[-1],relaxed)
                    used.update(u);unknown.update(b);covered.update(c);terminals.update(t)
                elif relaxed and value in CONSTANTS:
                    terminals.add(value)
                else:
                    unknown.add(value);terminals.add(value)
        return frozenset(used),frozenset(unknown),frozenset(covered),frozenset(terminals)
    strict = trace_node(root,False);relaxed = trace_node(root,True)
    used = strict[0]|relaxed[0]
    false = sum(not close(records[k][0],records[k][1]) for k in used)
    features[3:] = [1,np.log1p(len(used)),false/max(len(used),1),len(strict[1])/max(len(strict[3]),1),
                    len(relaxed[1])/max(len(relaxed[3]),1),float(not strict[1] and false==0 and bool(strict[2])),
                    float(not relaxed[1] and false==0 and bool(relaxed[2])),
                    len(strict[2]|relaxed[2])/max(len(source),1),1-len(used)/len(records)]
    assert np.isfinite(features).all()
    return features


def feature_tables(bank,data,mode):
    columns = COLUMNS[mode];result = []
    for row,groups in zip(bank,data):
        features = np.stack([candidate_features(row['question'],c['text']) for c in row['candidates']])
        result.append([np.r_[features[g['members']].mean(0),features[g['members']].max(0)][columns] for g in groups])
    return result


def candidate_scores(bank,arrays,checkpoint):
    if not bank:
        return np.empty((0,4))
    path = Path(checkpoint);cfg = json.loads((path/'config.json').read_text(encoding='utf-8'))
    assert cfg['schema']=='grounded_chain_soft_residual_v1'
    base = parent_scores(bank,arrays,path/'parent');data = tables(bank,arrays)
    evidence = feature_tables(bank,data,cfg['mode'])
    with np.load(path/'chain.npz',allow_pickle=False) as z:
        return anchored(data,evidence,base,z['mean'],z['scale'],z['weight'])


def predict(bank,arrays,checkpoint):
    return [int(j) for j in candidate_scores(bank,arrays,checkpoint).argmax(1)] if bank else []


def contracts(bank,arrays,path):
    scores = candidate_scores(bank,arrays,path);choices = predict(bank,arrays,path)
    assert all(type(j) is int and 0<=j<4 for j in choices)
    perm = [2,0,3,1];pb = [dict(r,candidates=[dict(r['candidates'][j],index=k) for k,j in enumerate(perm)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb,{'embeddings':arrays['embeddings'][:,perm]},path),scores[:,perm],rtol=1e-8,atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1],{'embeddings':arrays['embeddings'][::-1]},path),scores[::-1],rtol=1e-8,atol=1e-8)
    assert predict([dict(r,id=f'unseen123-{i}') for i,r in enumerate(bank)],arrays,path)==choices
    for n in (1,7,23):
        np.testing.assert_allclose(candidate_scores(bank[:n],{'embeddings':arrays['embeddings'][:n]},path),scores[:n],rtol=1e-8,atol=1e-8)
    assert predict([],{'embeddings':np.empty((0,4,1024))},path)==[]
    for i,groups in enumerate(tables(bank,arrays)):
        for g in groups:
            same = scores[i,g['members']];assert (same==same[0]).all()
    return dict(strict_permutation=True,question_order=True,new_ids=True,variable_batch=True,empty=True,python_integers=True,same_answer_same_score=True)
