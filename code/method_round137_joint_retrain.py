"""Standalone four-block123 feature score, jointly exportable without parent assets."""
import json
from pathlib import Path
import numpy as np
from method_round108_group_subsets import tables
from method_round110_residual_ablation import feature_tables as local_tables
from method_round120_question_interaction import question_hash
from method_round123_grounded_chain import feature_tables as chain_tables

BLOCKS = ('A','L','I','G')
DIMENSIONS = (1034,26,4096,24)
SLICES = dict(zip(BLOCKS,(slice(0,1034),slice(1034,1060),slice(1060,5156),slice(5156,5180))))


def input_features(bank,arrays):
    data = tables(bank,arrays);local = local_tables(bank,data,'final_evidence')
    evidence = [[np.r_[v,g['full'][-6:]] for v,g in zip(row,gs)] for row,gs in zip(local,data)]
    questions = np.stack([question_hash(r['question']) for r in bank]) if bank else np.empty((0,128))
    graph = [list(row) for row in chain_tables(bank,data,'both')]
    return data,local,evidence,questions,graph


def components(data,local,evidence,questions,graph,p):
    out = np.zeros((len(data),4,4))
    effective = questions@p['I_weight'].reshape(128,32)
    for i,groups in enumerate(data):
        for g,l,e,z in zip(groups,local[i],evidence[i],graph[i]):
            v = np.array([((g['full']-p['A_mean'])/p['A_scale'])@p['A_weight'],
                          ((l-p['L_mean'])/p['L_scale'])@p['L_weight'],
                          ((e-p['I_mean'])/p['I_scale'])@effective[i],
                          ((z-p['G_mean'])/p['G_scale'])@p['G_weight']])
            out[i,g['members']] = v
    assert np.isfinite(out).all()
    return out


def score_components(data,c):
    scores = np.full((len(data),4),-1e100)
    for i,groups in enumerate(data):
        if not groups:
            scores[i] = 0.
        for g in groups:
            # Same group is assigned exactly the same Python-computed scalar.
            value = float(c[i,g['members'][0]].sum())
            scores[i,g['members']] = value
    return scores


def weight_vector(p):
    return np.concatenate([p[b+'_weight'].ravel() for b in BLOCKS])


def updated_parameters(p,family,delta):
    out = {k:v.copy() for k,v in p.items()}
    if family=='mix':
        assert delta.shape==(4,)
        for b,d in zip(BLOCKS,delta):
            out[b+'_weight'] = p[b+'_weight']*(1+d)
    else:
        assert family=='joint' and delta.shape==(5180,)
        for b in BLOCKS:
            out[b+'_weight'] = p[b+'_weight']+delta[SLICES[b]].reshape(p[b+'_weight'].shape)
    return out


def candidate_scores(bank,arrays,checkpoint):
    if not bank:
        return np.empty((0,4))
    path = Path(checkpoint);cfg = json.loads((path/'config.json').read_text(encoding='utf-8'))
    assert cfg['schema']=='joint_four_block123_v1'
    with np.load(path/'parameters.npz',allow_pickle=False) as z:
        p = {k:z[k].copy() for k in z.files}
    features = input_features(bank,arrays)
    return score_components(features[0],components(*features,p))


def predict(bank,arrays,checkpoint):
    return [int(j) for j in candidate_scores(bank,arrays,checkpoint).argmax(1)] if bank else []
