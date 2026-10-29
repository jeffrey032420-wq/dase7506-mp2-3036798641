"""Controlled ranking ablations and answer-conditioned embedding comparisons."""
import json
import numpy as np
from features import answer_groups
from features_round4 import equation_summary
from method_round2 import transform
import numeric_round7_v3 as numeric_round7


def answer_context(bank,base,state):
    z=(base[:,:1024]@state['projection']).reshape(len(bank),4,-1)
    same=np.empty_like(z)
    different=np.empty_like(z)
    present=np.zeros((len(bank),4,2))
    for n,answers in enumerate(answer_groups(bank)):
        for i,answer in enumerate(answers):
            peers=[j for j,a in enumerate(answers) if j!=i and answer is not None and a==answer]
            others=[j for j in range(4) if j!=i and j not in peers]
            same[n,i]=z[n,peers].mean(axis=0) if peers else z[n,i]
            different[n,i]=z[n,others].mean(axis=0) if others else z[n,i]
            present[n,i]=[bool(peers),bool(others)]
    extra=np.concatenate([z*same,z*different,(z-same)**2,(z-different)**2,present],axis=-1)
    return extra.reshape(4*len(bank),-1)


def features(bank,arrays,state,config):
    name=config['name']
    mode='nonlinear' if name in ('no_context','no_context_pointwise') else 'linear' if name=='linear' else 'context'
    base=transform(bank,arrays,state,mode)
    if name=='no_embedding':
        return base[:,1024:1038]
    if name=='embedding_only':
        return np.concatenate([base[:,:1024],base[:,1038:]],axis=1)
    if name=='no_agreement':
        return np.delete(base,[1031,1032],axis=1)
    blocks=[base]
    if name=='old_numeric':
        blocks.append(np.array([equation_summary(c['text']) for row in bank for c in row['candidates']]))
    if name=='strict_core':
        blocks.append(numeric_round7.build(bank)[:,:6])
    if name in ('strict_numeric','answer_context_numeric'):
        blocks.append(numeric_round7.build(bank))
    if name in ('answer_context','answer_context_numeric'):
        blocks.append(answer_context(bank,base,state))
    return np.concatenate(blocks,axis=1)


def candidate_scores(bank,arrays,checkpoint):
    config=json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    with np.load(checkpoint/'weights.npz',allow_pickle=False) as state:
        x=features(bank,arrays,state,config)
        return (((x-state['mean'])/state['scale'])@state['weight']+state['bias']).reshape(-1,4)


def predict(bank,arrays,checkpoint):
    if not bank:
        return []
    return [int(i) for i in candidate_scores(bank,arrays,checkpoint).argmax(axis=1)]
