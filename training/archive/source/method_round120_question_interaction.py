"""Input-only question-word × answer-group evidence residual, portable NumPy."""
import hashlib
import json
from pathlib import Path
import re
import numpy as np
from features import answer_groups
from method_round108_group_subsets import tables
from method_round110_residual_ablation import feature_tables,candidate_scores as parent_scores

BUCKETS = 128
COLUMNS = {'question_numeric':list(range(26,32)),'question_evidence':list(range(26)),'question_both':list(range(32))}


def question_hash(question):
    words = re.findall(r'[a-z]+',str(question)[:20000].lower())[:512]
    vector = np.zeros(BUCKETS)
    tokens = ['u:'+v for v in words]+['b:'+a+' '+b for a,b in zip(words,words[1:])]
    for token in tokens:
        code = int.from_bytes(hashlib.blake2b(token.encode('utf-8'),digest_size=8,person=b'MP2Q120').digest(),'little')
        vector[code%BUCKETS] += 1 if (code>>7)&1 else -1
    norm = np.linalg.norm(vector)
    return vector/norm if norm else vector


def evidence_tables(bank,data):
    local = feature_tables(bank,data,'final_evidence')
    return [[np.r_[v,g['full'][-6:]] for v,g in zip(row,groups)] for row,groups in zip(local,data)]


def add_interaction(data,evidence,questions,base,columns,mean,scale,weight):
    effective = questions@weight.reshape(BUCKETS,len(columns))
    result = base.copy()
    for i,groups in enumerate(data):
        for group,feature in zip(groups,evidence[i]):
            result[i,group['members']] += ((feature[columns]-mean)/scale)@effective[i]
    assert np.isfinite(result).all()
    return result


def candidate_scores(bank,arrays,checkpoint):
    if not bank:
        return np.empty((0,4))
    checkpoint = Path(checkpoint)
    cfg = json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    assert cfg['schema']=='question_evidence_interaction_v1'
    base = parent_scores(bank,arrays,checkpoint/'parent')
    if cfg['mode']=='control':
        return base
    data = tables(bank,arrays)
    evidence = evidence_tables(bank,data)
    q = np.stack([question_hash(r['question']) for r in bank])
    with np.load(checkpoint/'interaction.npz',allow_pickle=False) as z:
        return add_interaction(data,evidence,q,base,COLUMNS[cfg['mode']],z['mean'],z['scale'],z['weight'])


def predict(bank,arrays,checkpoint):
    return [int(j) for j in candidate_scores(bank,arrays,checkpoint).argmax(1)] if bank else []


def contracts(bank,arrays,path):
    scores = candidate_scores(bank,arrays,path)
    choices = predict(bank,arrays,path)
    assert all(type(j) is int and 0<=j<4 for j in choices)
    perm = [2,0,3,1]
    pb = [dict(r,candidates=[dict(r['candidates'][j],index=k) for k,j in enumerate(perm)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb,{'embeddings':arrays['embeddings'][:,perm]},path),scores[:,perm],rtol=1e-8,atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1],{'embeddings':arrays['embeddings'][::-1]},path),scores[::-1],rtol=1e-8,atol=1e-8)
    assert predict([dict(r,id=f'unseen120-{i}') for i,r in enumerate(bank)],arrays,path)==choices
    for n in (1,7,23):
        np.testing.assert_allclose(candidate_scores(bank[:n],{'embeddings':arrays['embeddings'][:n]},path),scores[:n],rtol=1e-8,atol=1e-8)
    assert predict([],{'embeddings':np.empty((0,4,1024))},path)==[]
    for i,groups in enumerate(answer_groups(bank)):
        for a in set(v for v in groups if v is not None):
            same = scores[i,[j for j,v in enumerate(groups) if v==a]]
            assert (same==same[0]).all()
    return dict(strict_permutation=True,question_order=True,new_ids=True,variable_batch=True,empty=True,python_integers=True,same_answer_same_score=True)
