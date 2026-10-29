"""Frozen numeric-answer anchor plus a learned local arithmetic correction."""
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from common import parse_answer
from numeric_round7_v3 import evidence, relative_error
from method_round108_group_subsets import tables, score_tables


def close(a, b):
    return abs(a-b) <= Fraction(5, 1000)+Fraction(1, 10**6)*max(abs(a), abs(b))


def local_features(text):
    text = text[:24000]
    records, _ = evidence(text)
    mismatches = sum(not close(a, b) for a, b, _ in records)
    answer = parse_answer(text)
    known = bool(records and answer is not None)
    agrees = bool(known and close(records[-1][1], Fraction(answer)))
    equals = text.count('=')
    return np.array([float(equals > 0), np.log1p(equals), np.log1p(sum('=' in s for s in text.splitlines())),
                     float(bool(records)), np.log1p(len(records)), np.log1p(mismatches),
                     mismatches/max(len(records), 1), np.log1p(max((r[2] for r in records), default=0)),
                     float(known), float(agrees), float(known and not agrees)], dtype=np.float64)


def arithmetic_tables(bank, data):
    result = []
    for row, groups in zip(bank, data):
        features = np.stack([local_features(c['text']) for c in row['candidates']])
        result.append([np.r_[features[g['members']].mean(0), features[g['members']].max(0)] for g in groups])
    assert all(v.shape == (22,) and np.isfinite(v).all() for row in result for v in row)
    return result


def anchored(data, features, base, mean, scale, weight):
    scores = base.copy()
    for i, groups in enumerate(data):
        for g, feature in zip(groups, features[i]):
            scores[i, g['members']] += ((feature-mean)/scale)@weight
    assert np.isfinite(scores).all()
    return scores


def read_anchor(data, checkpoint):
    with np.load(Path(checkpoint)/'weights.npz', allow_pickle=False) as z:
        return score_tables(data, z['mean'], z['scale'], z['weight'])


def candidate_scores(bank, arrays, checkpoint):
    if not bank:
        return np.empty((0, 4))
    checkpoint = Path(checkpoint)
    config = json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    assert config['schema'] == 'group_anchor_local_arithmetic_22_v1'
    data = tables(bank, arrays)
    base = read_anchor(data, checkpoint/'anchor')
    features = arithmetic_tables(bank, data)
    with np.load(checkpoint/'residual.npz', allow_pickle=False) as z:
        return anchored(data, features, base, z['mean'], z['scale'], z['weight'])


def predict(bank, arrays, checkpoint):
    return [int(j) for j in candidate_scores(bank, arrays, checkpoint).argmax(1)] if bank else []
