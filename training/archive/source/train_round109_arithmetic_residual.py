"""Fixed 2x2 residual study with outer-held evaluation and inner-OOF offsets."""
import os
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.model_selection import StratifiedKFold
from threadpoolctl import threadpool_limits
from common import load_inputs
from features import answer_groups
from train_round1 import labels
from train_round108_group_subsets import (closure, digest, write, asset_inventory, metrics, scale_fit,
                                         design, fit as fit_anchor, name as anchor_name)
from method_round108_group_subsets import tables, score_tables
from method_round109_arithmetic_residual import arithmetic_tables, anchored, read_anchor, candidate_scores, predict

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OLD = CODE/'runs/round108-group-subsets'
OUT = CODE/'runs/round109-arithmetic-residual'
PLAN = ROOT/'ROUND109_ARITHMETIC_RESIDUAL_PLAN.md'
PENALTIES = (.01, .1)


def name(aug, penalty):
    return 'round109_'+('subsets' if aug else 'full')+'_r'+str(penalty).replace('.', 'p')


def residual_scale(features, indices):
    full = np.stack([g for i in indices for g in features[int(i)]])
    mean, scale = full.mean(0), full.std(0)
    scale[scale < 1e-8] = 1.
    return mean, scale


def residual_design(data, features, y, fitting, scale, offset):
    x, margin, raw_weights, origin = [], [], [], []
    for i in fitting:
        good, bad = [], []
        for k, group in enumerate(data[int(i)]):
            target = y[i, group['members']]
            assert (target == target[0]).all()
            (good if target[0] else bad).append(k)
        count = len(good)*len(bad)
        if not count:
            continue
        for p in good:
            for n in bad:
                x.append((features[i][p]-features[i][n])/scale)
                margin.append(offset[i, data[i][p]['members'][0]]-offset[i, data[i][n]['members'][0]])
                raw_weights.append(1/count)
                origin.append(int(i))
    origin = np.asarray(origin)
    informative = np.unique(origin)
    weights = np.asarray(raw_weights)/len(informative)
    totals = np.bincount(origin, weights=weights, minlength=len(data))
    np.testing.assert_allclose(totals[informative], 1/len(informative), rtol=1e-12, atol=1e-14)
    assert set(informative) <= set(fitting) and abs(weights.sum()-1) < 1e-12
    return np.asarray(x), np.asarray(margin), weights, {'origin': origin, 'weights': weights,
            'question_total_weights': totals, 'anchor_margin': np.asarray(margin)}


def loss(weight, x, offset, importance, penalty):
    margin = offset+x@weight
    return (float(importance@np.logaddexp(0, -margin)+penalty/2*(weight@weight)),
            x.T@(-importance*expit(-margin))+penalty*weight)


def fit_residual(x, offset, importance, penalty):
    tick = time.perf_counter()
    result = minimize(loss, np.zeros(x.shape[1]), args=(x, offset, importance, penalty), jac=True,
                      method='L-BFGS-B', options={'maxiter':1000, 'ftol':1e-12, 'gtol':1e-7, 'maxls':40})
    assert result.success and np.isfinite(result.x).all(), str(result.message)
    assert np.abs(result.jac).max() < 1e-5
    return result.x, {'success': bool(result.success), 'iterations': int(result.nit),
                     'objective': float(result.fun), 'initial_objective': loss(np.zeros(x.shape[1]), x, offset, importance, penalty)[0],
                     'gradient_inf_norm': float(np.abs(result.jac).max()), 'seconds':time.perf_counter()-tick,
                     'pairs':len(x), 'weight_sum':float(importance.sum())}


def check_gradient(x, offset, importance):
    weight = np.random.default_rng(20261030).normal(0, .001, x.shape[1])
    epsilon, penalty = 1e-5, .01
    value, grad = loss(weight, x, offset, importance, penalty)
    errors = []
    for j in (0, 3, 7, 10, 21):
        plus, minus = weight.copy(), weight.copy()
        plus[j] += epsilon; minus[j] -= epsilon
        numeric = (loss(plus,x,offset,importance,penalty)[0]-loss(minus,x,offset,importance,penalty)[0])/(2*epsilon)
        errors.append(abs(numeric-grad[j]))
    assert max(errors) < 1e-6
    duplicate = loss(weight, np.repeat(x,2,0), np.repeat(offset,2), np.repeat(importance/2,2), penalty)
    assert abs(duplicate[0]-value) < 1e-12
    np.testing.assert_allclose(duplicate[1], grad, rtol=1e-10, atol=1e-12)
    return {'finite_difference_max_error':max(errors), 'duplicate_pair_invariance':True}


def contracts(bank, arrays, path):
    scores = candidate_scores(bank, arrays, path)
    choices = predict(bank, arrays, path)
    assert all(type(i) is int and 0 <= i <= 3 for i in choices)
    perm = [2,0,3,1]
    pb = [dict(r, candidates=[dict(r['candidates'][j],index=k) for k,j in enumerate(perm)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb, {'embeddings':arrays['embeddings'][:,perm]}, path),
                               scores[:,perm], rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1], {'embeddings':arrays['embeddings'][::-1]}, path),
                               scores[::-1], rtol=1e-8, atol=1e-8)
    assert predict([dict(r,id=f'unseen109-{i}') for i,r in enumerate(bank)], arrays,path) == choices
    for n in (1,7,23):
        np.testing.assert_allclose(candidate_scores(bank[:n], {'embeddings':arrays['embeddings'][:n]},path),
                                   scores[:n], rtol=1e-8, atol=1e-8)
    assert predict([], {'embeddings':np.empty((0,4,1024))},path) == []
    for i,group in enumerate(answer_groups(bank)):
        for a in set(v for v in group if v is not None):
            ss = scores[i,[j for j,v in enumerate(group) if v == a]]
            assert (ss == ss[0]).all()
    return {'strict_permutation':True, 'question_order':True, 'new_ids':True,
            'variable_batch':True, 'empty':True, 'python_integers':True, 'same_answer_same_score':True}


def worker():
    started = time.perf_counter()
    sources = closure(['train_round109_arithmetic_residual.py','method_round109_arithmetic_residual.py'])
    prior = json.loads((OLD/'result.json').read_text(encoding='utf-8'))
    assert all(digest(CODE/n) == sha for n,sha in prior['sources'].items())
    inherited = {n:digest(OLD/n) for n in ['result.json','folds.json']}
    anchors = {}
    for aug in (False,True):
        r = next(r for r in prior['models'] if r['augmented'] == aug and r['lambda'] == .01)
        assert asset_inventory(CODE/r['checkpoint']) == r['assets']
        anchors[aug] = r
        f = r['name']+'-oof-scores.npy'
        inherited[f] = digest(OLD/f)
        for fold in range(3):
            f = f'fold-models/fold{fold}-{anchor_name(aug,.01)}/weights.npz'
            inherited[f] = digest(OLD/f)
    (OUT/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    shutil.copy2(PLAN,OUT/'sources/PLAN.md')
    plan_sha = digest(PLAN)
    write(OUT/'pretraining.json',{'sources':sources,'plan_sha256':plan_sha,'inherited_hashes':inherited})
    bank, arrays = load_inputs('train')
    y = labels(bank,'train')
    data = tables(bank,arrays,include_subsets=True)
    features = arithmetic_tables(bank,data)
    folds = json.loads((OLD/'folds.json').read_text(encoding='utf-8'))
    oof = {(a,p):np.zeros((len(bank),4)) for a in (False,True) for p in PENALTIES}
    base_oof = {a:np.load(OLD/(r['name']+'-oof-scores.npy')) for a,r in anchors.items()}
    proof, records, fits, gradient = [], [], 0, None
    for fold_row in folds:
        fold = fold_row['fold']
        fitting, held = np.asarray(fold_row['fit']), np.asarray(fold_row['held'])
        assert not set(fitting)&set(held)
        for aug in (False,True):
            original = OLD/'fold-models'/f'fold{fold}-{anchor_name(aug,.01)}'
            fold_score = read_anchor([data[int(i)] for i in held],original)
            np.testing.assert_array_equal(fold_score,base_oof[aug][held])
        nested = {a:np.zeros((len(bank),4)) for a in (False,True)}
        for inner,(a,b) in enumerate(StratifiedKFold(3,shuffle=True,random_state=20261030+fold).split(fitting,y[fitting].sum(1))):
            inner_fit, inner_held = fitting[a], fitting[b]
            assert not set(inner_fit)&set(inner_held) and not set(inner_fit)&set(held)
            mean, scale = scale_fit(data,inner_fit)
            for aug in (False,True):
                x, importance, description, audit = design(data,y,inner_fit,scale,aug)
                weight, report = fit_anchor(x,importance,.01)
                nested[aug][inner_held] = score_tables([data[int(i)] for i in inner_held],mean,scale,weight)
                np.savez(OUT/f'outer{fold}-inner{inner}-aug{int(aug)}.npz',mean=mean,scale=scale,weight=weight)
                fits += 1
                row = {'outer':fold,'inner':inner,'augmented':aug,'fit':inner_fit.tolist(),
                       'predicted':inner_held.tolist(),'outer_held':held.tolist(),'description':description,'fit_report':report}
                proof.append(row)
                write(OUT/'nested-partitions.json',proof)
                print('INNER '+json.dumps({'outer':fold,'inner':inner,'augmented':aug,**report}),flush=True)
                del x,audit
        mean, scale = residual_scale(features,fitting)
        for aug in (False,True):
            x, offset, importance, audit = residual_design(data,features,y,fitting,scale,nested[aug])
            np.savez_compressed(OUT/f'outer{fold}-aug{int(aug)}-residual-pair-audit.npz',**audit)
            if gradient is None:
                gradient = check_gradient(x[:100],offset[:100],importance[:100]/importance[:100].sum())
            for penalty in PENALTIES:
                weight, report = fit_residual(x,offset,importance,penalty)
                fits += 1
                hdata, hfeatures = [data[int(i)] for i in held], [features[int(i)] for i in held]
                predicted = anchored(hdata,hfeatures,base_oof[aug][held],mean,scale,weight)
                oof[aug,penalty][held] = predicted
                np.savez(OUT/f'outer{fold}-{name(aug,penalty)}.npz',mean=mean,scale=scale,weight=weight)
                row = {'fold':fold,'augmented':aug,'lambda':penalty,**report,
                       'held':metrics([bank[int(i)] for i in held],y[held],predicted),
                       'anchor_held':metrics([bank[int(i)] for i in held],y[held],base_oof[aug][held])}
                records.append(row)
                write(OUT/'residual-progress.json',records)
                print('OUTER '+json.dumps(row),flush=True)
    models = []
    mean, scale = residual_scale(features,np.arange(len(bank)))
    for aug in (False,True):
        x, offset, importance, audit = residual_design(data,features,y,np.arange(len(bank)),scale,base_oof[aug])
        np.savez_compressed(OUT/f'full-aug{int(aug)}-residual-pair-audit.npz',**audit)
        base = read_anchor(data,CODE/anchors[aug]['checkpoint'])
        for penalty in PENALTIES:
            weight, report = fit_residual(x,offset,importance,penalty)
            fits += 1
            path = OUT/'candidates'/name(aug,penalty)
            path.mkdir(parents=True)
            shutil.copytree(CODE/anchors[aug]['checkpoint'],path/'anchor')
            np.savez(path/'residual.npz',mean=mean,scale=scale,weight=weight)
            write(path/'config.json',{'schema':'group_anchor_local_arithmetic_22_v1','augmented_anchor':aug,
                                      'anchor_lambda':.01,'residual_lambda':penalty,'residual_dimensions':22,
                                      'offset':'train_question_oof','inference':'original_full_groups','fit_split':'train'})
            expected = anchored(data,features,base,mean,scale,weight)
            np.testing.assert_array_equal(anchored(data,features,base,mean,scale,np.zeros(22)),base)
            np.testing.assert_array_equal(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},path),expected[:53])
            checks = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
            checks.update(cache_export_exact=True, zero_residual_exact_anchor=True)
            r = {'name':path.name,'method':'method_round109_arithmetic_residual.py',
                 'checkpoint':path.relative_to(CODE).as_posix(),'augmented':aug,'lambda':penalty,
                 'train_oof':metrics(bank,y,oof[aug,penalty]),'anchor_train_oof':anchors[aug]['train_oof'],
                 'train_resubstitution_not_oof':metrics(bank,y,expected),'fit':report,'checks':checks,
                 'assets':asset_inventory(path)}
            np.save(OUT/(path.name+'-oof-scores.npy'),oof[aug,penalty])
            models.append(r)
            print('EXPORT '+json.dumps({k:v for k,v in r.items() if k not in ('assets','checks')}),flush=True)
    assert fits == 34 and len(records) == 12
    assert closure(['train_round109_arithmetic_residual.py','method_round109_arithmetic_residual.py']) == sources
    assert digest(PLAN) == plan_sha and all(digest(OLD/n) == sha for n,sha in inherited.items())
    assert all(asset_inventory(CODE/r['checkpoint']) == r['assets'] for r in anchors.values())
    write(OUT/'result.json',{'status':'completed_train_only','models':models,'fold_records':records,
                            'sources':sources,'plan_sha256':plan_sha,'inherited_hashes':inherited,
                            'mathematical_checks':gradient,'model_fits':fits,'threads_total':4,
                            'seconds':time.perf_counter()-started,'validation_used':False,'test_used':False})
    print('TRAIN_COMPLETE '+json.dumps({'seconds':time.perf_counter()-started,'fits':fits}),flush=True)


def main():
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(), 'Round109 exists; preserve evidence, no automatic retry'
    OUT.mkdir(parents=True)
    tick = time.perf_counter()
    try:
        r = subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--worker'],cwd=CODE,timeout=900)
        write(OUT/'process-monitor.json',{'exit_code':r.returncode,'wall_seconds':time.perf_counter()-tick,
                                         'hard_timeout_seconds':900,'process_completed':True})
        assert r.returncode == 0, 'Training failed; evidence retained'
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json',{'status':'hard_timeout','wall_seconds':time.perf_counter()-tick})
        raise


if __name__ == '__main__':
    main()
