"""Fixed 3-fold group subset study with sample-count-invariant regularization."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '4'
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.model_selection import StratifiedKFold
from threadpoolctl import threadpool_limits
from common import load_inputs
from features import answer_groups
from train_round1 import labels
from method_round108_group_subsets import tables, score_tables, candidate_scores, predict

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OUT = CODE/'runs/round108-group-subsets'
PLAN = ROOT/'ROUND108_GROUP_SUBSETS_PLAN.md'
LAMBDAS = (.003, .01)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def closure(names):
    pending, result = list(names), {}
    while pending:
        p = CODE/pending.pop()
        if p.name in result or not p.is_file():
            continue
        result[p.name] = digest(p)
        for node in ast.walk(ast.parse(p.read_text(encoding='utf-8'))):
            modules = ([a.name for a in node.names] if isinstance(node, ast.Import) else
                       [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            for m in modules:
                name = m.split('.')[0]+'.py'
                if (CODE/name).is_file():
                    pending.append(name)
    return result


def asset_inventory(folder):
    return {p.relative_to(folder).as_posix(): {'bytes': p.stat().st_size, 'sha256': digest(p)}
            for p in sorted(folder.rglob('*')) if p.is_file()}


def metrics(bank, y, scores):
    right = y[np.arange(len(y)), scores.argmax(1)]
    hard = np.array([len(set(v for v in g if v is not None)) >= 2 for g in answer_groups(bank)])
    return {'correct': int(right.sum()), 'n': len(y), 'accuracy': 100*float(right.mean()),
            'disagreement_correct': int(right[hard].sum()), 'disagreement_n': int(hard.sum()),
            'single_correct': int(right[y.sum(1) == 1].sum()), 'single_n': int((y.sum(1) == 1).sum())}


def scale_fit(data, fitting):
    x = np.stack([g['full'] for i in fitting for g in data[int(i)]])
    mean, scale = x.mean(0), x.std(0)
    scale[scale < 1e-8] = 1.
    return mean, scale


def design(data, y, fitting, scale, augmented):
    differences, origins, pmask, nmask, raw_weights = [], [], [], [], []
    for i in fitting:
        positive, negative = [], []
        for g in data[int(i)]:
            truth = y[i, g['members']]
            assert (truth == truth[0]).all()
            if augmented:
                variants = list(zip(g['variants'], g['masks']))
                assert len(variants) == 2**len(g['members'])-1
            else:
                variants = [(g['full'], sum(1 << j for j in g['members']))]
            (positive if truth[0] else negative).extend(variants)
        count = len(positive)*len(negative)
        if not count:
            continue
        for p, pi in positive:
            for n, ni in negative:
                assert pi & ni == 0
                differences.append((p-n)/scale)
                origins.append(int(i)); pmask.append(pi); nmask.append(ni); raw_weights.append(1/count)
    origin = np.asarray(origins, dtype=int)
    informative = np.unique(origin)
    weights = np.asarray(raw_weights)/len(informative)
    totals = np.bincount(origin, weights=weights, minlength=len(data))
    np.testing.assert_allclose(totals[informative], 1/len(informative), rtol=1e-12, atol=1e-14)
    assert abs(weights.sum()-1) < 1e-12 and set(informative) <= set(fitting)
    audit = {'origin': origin, 'positive_mask': np.asarray(pmask, dtype=np.uint8),
             'negative_mask': np.asarray(nmask, dtype=np.uint8), 'weights': weights, 'question_total_weights': totals}
    record = {'pairs': len(origin), 'informative_questions': len(informative), 'weight_sum': float(weights.sum()),
              'question_total_min': float(totals[informative].min()), 'question_total_max': float(totals[informative].max()),
              'scale_fit_augmented_subsets': False}
    x = np.asarray(differences)
    assert x.shape[1] == 1034 and np.isfinite(x).all()
    return x, weights, record, audit


def loss(weight, x, importance, penalty):
    margin = x@weight
    value = float(importance@np.logaddexp(0, -margin)+penalty/2*(weight@weight))
    gradient = x.T@(-importance*expit(-margin))+penalty*weight
    return value, gradient


def fit(x, importance, penalty):
    started = time.perf_counter()
    result = minimize(loss, np.zeros(x.shape[1]), args=(x, importance, penalty), jac=True,
                      method='L-BFGS-B', options={'maxiter': 1000, 'ftol': 1e-12, 'gtol': 1e-7, 'maxls': 40})
    value, gradient = loss(result.x, x, importance, penalty)
    assert result.success and np.isfinite(result.x).all(), result.message
    assert np.abs(gradient).max() < 1e-5, float(np.abs(gradient).max())
    return result.x, {'success': bool(result.success), 'iterations': int(result.nit), 'objective': value,
                      'gradient_inf_norm': float(np.abs(gradient).max()), 'seconds': time.perf_counter()-started}


def mathematical_checks(x, importance):
    probe = np.random.default_rng(20261029).normal(0, .001, x.shape[1])
    penalty, epsilon = .01, 1e-5
    value, grad = loss(probe, x, importance, penalty)
    errors = []
    for j in (0, 7, 1024, 1030):
        plus, minus = probe.copy(), probe.copy()
        plus[j] += epsilon; minus[j] -= epsilon
        numeric = (loss(plus, x, importance, penalty)[0]-loss(minus, x, importance, penalty)[0])/(2*epsilon)
        errors.append(abs(numeric-grad[j]))
    assert max(errors) < 1e-6
    duplicated = loss(probe, np.repeat(x, 2, axis=0), np.repeat(importance/2, 2), penalty)
    assert abs(duplicated[0]-value) < 1e-12
    np.testing.assert_allclose(duplicated[1], grad, rtol=1e-10, atol=1e-12)
    return {'finite_difference_max_error': max(errors), 'pair_duplication_loss_and_gradient_invariant': True}


def contracts(bank, arrays, path):
    s = candidate_scores(bank, arrays, path)
    pred = predict(bank, arrays, path)
    assert all(type(j) is int and 0 <= j <= 3 for j in pred)
    permutation = [2, 0, 3, 1]
    pb = [dict(r, candidates=[dict(r['candidates'][j], index=k) for k, j in enumerate(permutation)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb, {'embeddings': arrays['embeddings'][:, permutation]}, path),
                               s[:, permutation], rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1], {'embeddings': arrays['embeddings'][::-1]}, path),
                               s[::-1], rtol=1e-8, atol=1e-8)
    assert predict([dict(r, id=f'unseen108-{i}') for i, r in enumerate(bank)], arrays, path) == pred
    for n in (1, 7, 23):
        np.testing.assert_allclose(candidate_scores(bank[:n], {'embeddings': arrays['embeddings'][:n]}, path),
                                   s[:n], rtol=1e-8, atol=1e-8)
    assert predict([], {'embeddings': np.empty((0, 4, 1024))}, path) == []
    for i, group in enumerate(answer_groups(bank)):
        for a in set(v for v in group if v is not None):
            values = s[i, [j for j, v in enumerate(group) if v == a]]
            assert (values == values[0]).all()
    return {'strict_permutation': True, 'question_order': True, 'new_ids': True,
            'variable_batch': True, 'empty': True, 'python_integers': True, 'same_answer_same_score': True}


def name(augmented, penalty):
    return 'round108_'+('subsets' if augmented else 'full')+'_l'+str(penalty).replace('.', 'p')


def worker():
    started = time.perf_counter()
    hashes = closure(['train_round108_group_subsets.py', 'method_round108_group_subsets.py'])
    plan_hash = digest(PLAN)
    (OUT/'sources').mkdir()
    for n in hashes:
        shutil.copy2(CODE/n, OUT/'sources'/n)
    shutil.copy2(PLAN, OUT/'sources/PLAN.md')
    write(OUT/'pretraining-source-hashes.json', {'sources': hashes, 'plan_sha256': plan_hash})
    bank, arrays = load_inputs('train')
    y = labels(bank, 'train')
    data = tables(bank, arrays, include_subsets=True)
    folds = list(StratifiedKFold(3, shuffle=True, random_state=20261029).split(np.arange(len(bank)), y.sum(1)))
    write(OUT/'folds.json', [{'fold': f, 'fit': a.tolist(), 'held': b.tolist()} for f, (a, b) in enumerate(folds)])
    oof = {(a, p): np.zeros((len(bank), 4)) for a in (False, True) for p in LAMBDAS}
    records, numeric_checks = [], None
    for fold, (fitting, held) in enumerate(folds):
        assert not set(fitting) & set(held)
        mean, scale = scale_fit(data, fitting)
        held_data = [data[int(i)] for i in held]
        for augmented in (False, True):
            x, importance, description, audit = design(data, y, fitting, scale, augmented)
            np.savez_compressed(OUT/f'fold{fold}-aug{int(augmented)}-pair-audit.npz', **audit)
            if numeric_checks is None:
                numeric_checks = mathematical_checks(x[:100], importance[:100]/importance[:100].sum())
                write(OUT/'mathematical-checks.json', numeric_checks)
            for penalty in LAMBDAS:
                weight, report = fit(x, importance, penalty)
                scores = score_tables(held_data, mean, scale, weight)
                oof[augmented, penalty][held] = scores
                fold_path = OUT/'fold-models'/f'fold{fold}-{name(augmented, penalty)}'
                fold_path.mkdir(parents=True)
                np.savez(fold_path/'weights.npz', mean=mean, scale=scale, weight=weight)
                row = {'fold': fold, 'augmented': augmented, 'lambda': penalty, **description, **report,
                       'held': metrics([bank[int(i)] for i in held], y[held], scores)}
                records.append(row)
                write(OUT/'fit-progress.json', records)
                print('FOLD '+json.dumps(row), flush=True)
            del x, audit
    mean, scale = scale_fit(data, np.arange(len(bank)))
    models = []
    for augmented in (False, True):
        x, importance, description, audit = design(data, y, np.arange(len(bank)), scale, augmented)
        np.savez_compressed(OUT/f'full-aug{int(augmented)}-pair-audit.npz', **audit)
        for penalty in LAMBDAS:
            weight, report = fit(x, importance, penalty)
            path = OUT/'candidates'/name(augmented, penalty)
            path.mkdir(parents=True)
            np.savez(path/'weights.npz', mean=mean, scale=scale, weight=weight)
            cfg = {'schema': 'numeric_answer_group_1034_v1', 'augmented_training': augmented,
                   'lambda': penalty, 'objective': 'per_question_pair_mean_logistic_plus_l2',
                   'scaler_fit': 'original_complete_fitting_groups', 'dimensions': 1034, 'seed': 20261029,
                   'fit_split': 'train', 'unknown_answer_fallback': 0}
            write(path/'config.json', cfg)
            expected = score_tables(data, mean, scale, weight)
            check_bank, check_arrays = bank[:53], {'embeddings': arrays['embeddings'][:53]}
            actual = candidate_scores(check_bank, check_arrays, path)
            np.testing.assert_array_equal(actual, expected[:53])
            checks = contracts(check_bank, check_arrays, path)
            pooled = metrics(bank, y, oof[augmented, penalty])
            record = {'name': path.name, 'method': 'method_round108_group_subsets.py',
                      'checkpoint': path.relative_to(CODE).as_posix(), 'augmented': augmented, 'lambda': penalty,
                      'train_oof': pooled, 'train_resubstitution_not_oof': metrics(bank, y, expected),
                      'fit': {**description, **report}, 'checks': checks, 'assets': asset_inventory(path)}
            models.append(record)
            np.save(OUT/(path.name+'-oof-scores.npy'), oof[augmented, penalty])
            print('EXPORTED '+json.dumps({k: v for k, v in record.items() if k not in ('assets', 'checks')}), flush=True)
        del x, audit
    assert closure(['train_round108_group_subsets.py', 'method_round108_group_subsets.py']) == hashes
    assert digest(PLAN) == plan_hash
    write(OUT/'result.json', {'status': 'completed_train_only', 'models': models, 'fold_records': records,
                            'sources': hashes, 'plan_sha256': plan_hash, 'mathematical_checks': numeric_checks,
                            'model_fits': 16, 'threads_total': 4, 'seconds': time.perf_counter()-started,
                            'validation_used': False, 'test_used': False,
                            'numpy': np.__version__, 'scipy': scipy.__version__})
    print('TRAIN_COMPLETE '+json.dumps({'seconds': time.perf_counter()-started, 'model_fits': 16}), flush=True)


def main():
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(), 'Round108 already exists; no automatic retry or overwrite'
    OUT.mkdir(parents=True)
    tick = time.perf_counter()
    try:
        result = subprocess.run([sys.executable, '-X', 'utf8', str(Path(__file__).resolve()), '--worker'],
                                cwd=CODE, timeout=600, check=False)
        write(OUT/'process-monitor.json', {'exit_code': result.returncode, 'wall_seconds': time.perf_counter()-tick,
                                         'hard_timeout_seconds': 600, 'process_completed': True})
        if result.returncode:
            raise RuntimeError('Training failed; original sources and evidence preserved')
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json', {'status': 'hard_timeout', 'wall_seconds': time.perf_counter()-tick})
        raise


if __name__ == '__main__':
    main()
