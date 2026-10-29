"""Matched format/arithmetic residuals and learned final-answer evidence."""
import json
from pathlib import Path
import numpy as np
from common import parse_answer
from method_round11 import final_box
from method_round108_group_subsets import tables
from method_round109_arithmetic_residual import arithmetic_tables, anchored, read_anchor

FORMAT = [0,1,2,11,12,13]
ARITHMETIC = [i for i in range(22) if i not in FORMAT]
DIMENSIONS = {'format':6,'arithmetic':16,'full':22,'final_evidence':26}


def feature_tables(bank, data, mode):
    assert mode in DIMENSIONS
    local = arithmetic_tables(bank,data)
    result = []
    for row, groups, features in zip(bank,data,local):
        if mode in ('format','arithmetic'):
            columns = FORMAT if mode == 'format' else ARITHMETIC
            result.append([v[columns] for v in features])
        elif mode == 'full':
            result.append(features)
        else:
            official = [parse_answer(c['text']) for c in row['candidates']]
            late = [final_box(c['text'][:24000]) for c in row['candidates']]
            conflict = [v is not None and v != a for v,a in zip(late,official)]
            current = []
            for g,feature in zip(groups,features):
                members = g['members']
                answer = official[members[0]]
                extra = [sum(conflict[j] for j in members)/len(members),
                         sum(late[j] == answer for j in members)/len(members),
                         sum(v == answer for v in late)/4,
                         sum(conflict[j] and late[j] == answer for j in range(4) if j not in members)/4]
                current.append(np.r_[feature,extra])
            result.append(current)
    assert all(v.shape == (DIMENSIONS[mode],) and np.isfinite(v).all() for row in result for v in row)
    return result


def candidate_scores(bank,arrays,checkpoint):
    if not bank:
        return np.empty((0,4))
    checkpoint = Path(checkpoint)
    config = json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    assert config['schema'] == 'matched_residual_features_v1'
    data = tables(bank,arrays)
    base = read_anchor(data,checkpoint/'anchor')
    features = feature_tables(bank,data,config['mode'])
    with np.load(checkpoint/'residual.npz',allow_pickle=False) as z:
        return anchored(data,features,base,z['mean'],z['scale'],z['weight'])


def predict(bank,arrays,checkpoint):
    return [int(j) for j in candidate_scores(bank,arrays,checkpoint).argmax(1)] if bank else []
