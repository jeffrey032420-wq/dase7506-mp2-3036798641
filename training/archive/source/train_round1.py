"""Predefined 3 x 5 ridge search. Train fit; validation selection; no test access."""
import os
for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '4'

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
import numpy as np
from common import DATA, PROTOCOL, load_inputs, parse_answer, read_jsonl
from features import build_features, majority_choices, answer_groups, TEXT_NAMES

ALPHAS = [0.01, 0.1, 1.0, 10.0, 100.0]
MODES = ['text', 'embeddings', 'combined']


def labels(bank, split):
    refs = read_jsonl(DATA / f'gsm8k_{split}.jsonl')
    assert len(refs) == len(bank)
    out = []
    for r, b in zip(refs, bank):
        assert r['id'] == b['id'] and r['question'] == b['question']
        gold = parse_answer(r['answer'])
        out.append([float(gold is not None and parse_answer(c['text']) == gold) for c in b['candidates']])
    return np.asarray(out)


def metrics(y, choices, hard):
    right = y[np.arange(len(y)), choices]
    return {'correct': int(right.sum()), 'n': len(y), 'accuracy': float(100*right.mean()),
            'disagreement_n': int(hard.sum()),
            'disagreement_accuracy': float(100*right[hard].mean())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path('runs/round1'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    train, ta = load_inputs('train')
    val, va = load_inputs('validation')
    yt, yv = labels(train, 'train'), labels(val, 'validation')
    hard = np.array([len(set(x for x in a if x is not None)) >= 2 for a in answer_groups(val)])
    experiments = []
    for name, choices in [('first_candidate', [0]*len(val)), ('majority', majority_choices(val))]:
        record = {'method': name, **metrics(yv, choices, hard)}
        experiments.append(record)
        print(json.dumps(record), flush=True)
    best = None
    for mode in MODES:
        tick = time.perf_counter()
        x = build_features(train, ta, mode)
        xv = build_features(val, va, mode)
        mean, scale = x.mean(axis=0), x.std(axis=0)
        scale[scale < 1e-8] = 1
        x = (x - mean)/scale
        xv = (xv - mean)/scale
        y = yt.ravel()
        bias = y.mean()
        gram = x.T @ x / len(y)
        rhs = x.T @ (y-bias) / len(y)
        eig, vectors = np.linalg.eigh(gram)
        eig = np.maximum(eig, 0)
        projected = vectors.T @ rhs
        for alpha in ALPHAS:
            w = vectors @ (projected/(eig+alpha))
            choices = (xv @ w + bias).reshape(-1, 4).argmax(axis=1)
            record = {'method': mode, 'alpha': alpha, **metrics(yv, choices, hard)}
            experiments.append(record)
            print(json.dumps(record), flush=True)
            # Choose only by whole validation accuracy; deterministic first-in-grid tie.
            if best is None or record['correct'] > best['correct']:
                best = record.copy()
                bundle = args.output / 'model_bundle'
                bundle.mkdir(exist_ok=True)
                np.savez(bundle/'weights.npz', mean=mean, scale=scale, weight=w, bias=bias)
                config = {'feature_mode': mode, 'alpha': alpha, 'protocol': PROTOCOL,
                          'objective': 'mean_squared_error_plus_alpha_squared_weight_norm',
                          'seed': 0, 'tie_break': 'first_index', 'text_features': TEXT_NAMES}
                (bundle/'config.json').write_text(json.dumps(config, indent=2)+'\n', encoding='utf-8')
        print(f'{mode} training/search seconds: {time.perf_counter()-tick:.3f}', flush=True)
    assets = {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in bundle.iterdir() if p.is_file()}
    report = {'protocol': PROTOCOL, 'python': platform.python_version(), 'numpy': np.__version__,
              'platform': platform.platform(), 'processor': platform.processor(),
              'threads': 4, 'seed': 0, 'randomness': 'none; deterministic closed-form ridge',
              'test_used': False, 'search': {'modes': MODES, 'alphas': ALPHAS},
              'experiments': experiments, 'best_trained_model': best,
              'seconds_total': time.perf_counter()-start, 'assets': assets,
              'asset_bytes': sum(a['bytes'] for a in assets.values())}
    (args.output/'experiments.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'best': best, 'seconds': report['seconds_total'], 'asset_bytes': report['asset_bytes']}))


if __name__ == '__main__':
    main()
