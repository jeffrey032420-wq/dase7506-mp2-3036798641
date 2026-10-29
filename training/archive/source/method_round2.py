"""Candidate comparison model; inference uses supplied inputs and explicit assets."""
import json
import numpy as np
from features import build_features


def transform(bank, arrays, state, mode):
    x = build_features(bank, arrays, 'combined')
    x = (x-state['base_mean'])/state['base_scale']
    if mode == 'linear':
        return x
    z = (x[:, :1024] @ state['projection']).reshape(-1, 4, state['projection'].shape[1])
    if mode == 'nonlinear':
        extra = np.concatenate([np.maximum(z, 0), z*z], axis=-1)
    elif mode == 'context':
        avg = z.mean(axis=1, keepdims=True)
        extra = np.concatenate([np.maximum(z, 0), z*z, z*avg, (z-avg)**2], axis=-1)
    else:
        raise ValueError(mode)
    return np.concatenate([x, extra.reshape(len(x), -1)], axis=1)


def score(bank, arrays, checkpoint):
    config = json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    with np.load(checkpoint/'weights.npz', allow_pickle=False) as asset:
        x = transform(bank, arrays, asset, config['mode'])
        x = (x-asset['mean'])/asset['scale']
        return (x @ asset['weight']).reshape(-1, 4)


def predict(bank, arrays, checkpoint):
    if not bank:
        return []
    if checkpoint is None:
        raise ValueError('An explicit round2 checkpoint is required')
    return [int(i) for i in score(bank, arrays, checkpoint).argmax(axis=1)]
