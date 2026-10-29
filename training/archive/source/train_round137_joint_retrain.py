"""Finite train-only module calibration and proximal joint updates around123."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits
from common import load_inputs
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,asset_inventory,metrics
from train_round109_arithmetic_residual import fit_residual,loss
from train_round121_regularization import comparison
from method_round108_group_subsets import tables
from method_round137_joint_retrain import BLOCKS,SLICES,input_features,components,score_components,updated_parameters,candidate_scores,predict

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OUT = CODE/'runs/round137-joint-retrain'
AUDIT = CODE/'runs/round137-train-audit'
PLAN = ROOT/'ROUND137_JOINT_RETRAIN_PLAN.md'
FAMILIES = ('mix','joint')
PENALTIES = (.01,.1,1.)


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def config_name(family,penalty):
    return 'round137_'+family+'_l'+str(penalty).replace('.','p')


def load_npz(path):
    with np.load(path,allow_pickle=False) as z:
        return {k:z[k].copy() for k in z.files}


def contracts(bank,arrays,path):
    s = candidate_scores(bank,arrays,path);choices = predict(bank,arrays,path)
    assert all(type(j) is int and 0<=j<4 for j in choices)
    perm = [2,0,3,1];pb = [dict(r,candidates=[dict(r['candidates'][j],index=k) for k,j in enumerate(perm)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb,{'embeddings':arrays['embeddings'][:,perm]},path),s[:,perm],rtol=1e-8,atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1],{'embeddings':arrays['embeddings'][::-1]},path),s[::-1],rtol=1e-8,atol=1e-8)
    assert predict([dict(r,id=f'unseen137-{i}') for i,r in enumerate(bank)],arrays,path)==choices
    for n in (1,7,23):
        np.testing.assert_allclose(candidate_scores(bank[:n],{'embeddings':arrays['embeddings'][:n]},path),s[:n],rtol=1e-8,atol=1e-8)
    assert predict([],{'embeddings':np.empty((0,4,1024))},path)==[]
    for i,groups in enumerate(tables(bank,arrays)):
        for g in groups:
            v = s[i,g['members']];assert (v==v[0]).all()
    return dict(strict_permutation=True,question_order=True,new_ids=True,variable_batch=True,empty=True,python_integers=True,same_answer_same_score=True)


def pair_design(data,local,evidence,q,graph,p,c,y,fitting):
    pairs,weights = [],[];informative = 0
    for i in fitting:
        good,bad = [],[]
        for k,g in enumerate(data[i]):
            truth = y[i,g['members']];assert (truth==truth[0]).all()
            (good if truth[0] else bad).append(k)
        count = len(good)*len(bad)
        if not count:
            continue
        informative += 1
        for a in good:
            for b in bad:
                pairs.append((int(i),a,b));weights.append(1/count)
    importance = np.array(weights)/informative;origins = np.array([r[0] for r in pairs])
    totals = np.bincount(origins,weights=importance,minlength=len(data));used = np.unique(origins)
    np.testing.assert_allclose(totals[used],1/informative,rtol=1e-12,atol=1e-14)
    assert set(used)<=set(fitting) and abs(importance.sum()-1)<1e-12
    mix = np.stack([c[i,data[i][a]['members'][0]]-c[i,data[i][b]['members'][0]] for i,a,b in pairs])
    joint = np.empty((len(pairs),5180))
    joint[:,SLICES['A']] = np.stack([data[i][a]['full']-data[i][b]['full'] for i,a,b in pairs])/p['A_scale']
    joint[:,SLICES['L']] = np.stack([local[i][a]-local[i][b] for i,a,b in pairs])/p['L_scale']
    joint[:,SLICES['G']] = np.stack([graph[i][a]-graph[i][b] for i,a,b in pairs])/p['G_scale']
    ed = np.stack([evidence[i][a]-evidence[i][b] for i,a,b in pairs])/p['I_scale']
    for start in range(0,len(pairs),256):
        end = min(start+256,len(pairs))
        joint[start:end,SLICES['I']] = (q[origins[start:end],:,None]*ed[start:end,None,:]).reshape(end-start,4096)
    assert np.isfinite(joint).all() and np.isfinite(mix).all()
    theta = np.concatenate([p[b+'_weight'].ravel() for b in BLOCKS])
    np.testing.assert_allclose(joint@theta,mix.sum(1),rtol=1e-10,atol=1e-10)
    return dict(mix=mix,joint=joint),mix.sum(1),importance,dict(origins=origins,weights=importance,question_total_weights=totals,
        positive_candidate=np.array([data[i][a]['members'][0] for i,a,b in pairs]),negative_candidate=np.array([data[i][b]['members'][0] for i,a,b in pairs]))


def gradient_check(x,offset,importance):
    x,offset,importance = x[:64],offset[:64],importance[:64]
    rng = np.random.default_rng(20261029);w = rng.normal(0,.001,x.shape[1]);penalty=.1;eps=1e-5
    value,gradient = loss(w,x,offset,importance,penalty)
    coords = list(range(4)) if x.shape[1]==4 else [0,17,1033,1034,1059,1060,1171,2017,3999,5155,5156,5179]
    errors = []
    for j in coords:
        plus,minus = w.copy(),w.copy();plus[j] += eps;minus[j] -= eps
        finite = (loss(plus,x,offset,importance,penalty)[0]-loss(minus,x,offset,importance,penalty)[0])/(2*eps)
        errors.append(abs(finite-gradient[j]))
    assert max(errors)<1e-6
    vv,gg = loss(w,np.repeat(x,2,0),np.repeat(offset,2),np.repeat(importance/2,2),penalty)
    assert abs(vv-value)<1e-12;np.testing.assert_allclose(gg,gradient,rtol=1e-10,atol=1e-12)
    return dict(checked_coordinates=coords,finite_difference_max_error=max(errors),duplicate_pair_invariance=True,checked_pairs=len(x))


def worker():
    tick = time.perf_counter();sources = closure(['train_round137_joint_retrain.py']);audit = read(AUDIT/'result.json')
    assert audit['exact_full_and_held_decomposition'] and audit['zero_update_and_standalone_export']
    assert not audit['validation_used'] and not audit['test_used'] and audit['new_fits']==0
    assert all(digest(CODE/n)==s for n,s in audit['sources'].items())
    assert all(digest(AUDIT/n)==s for n,s in audit['cache_sha256'].items()) and digest(PLAN)==audit['plan_sha256']
    inherited = dict(audit['inherited'])
    for p in (AUDIT/'result.json',*[AUDIT/n for n in audit['cache_sha256']]):
        inherited[p.relative_to(CODE).as_posix()] = digest(p)
    assert all(digest(CODE/n)==s for n,s in inherited.items())
    (OUT/'sources').mkdir();shutil.copy2(PLAN,OUT/'sources/PLAN.md')
    for n in sources:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    write(OUT/'pretraining.json',dict(sources=sources,inherited=inherited,plan_sha256=digest(PLAN),families=FAMILIES,penalties=PENALTIES,planned_fits=20))
    bank,arrays = load_inputs('train');y = labels(bank,'train');data = tables(bank,arrays);cached = load_npz(AUDIT/'raw-features.npz')
    ptr = cached['indptr'];assert np.array_equal(np.diff(ptr),[len(gs) for gs in data])
    def unpack(key):
        return [list(cached[key][ptr[i]:ptr[i+1]]) for i in range(len(data))]
    local,ev,q,graph = unpack('local'),unpack('evidence'),cached['questions'],unpack('graph')
    actual = input_features(bank[:13],{'embeddings':arrays['embeddings'][:13]})
    for left,right in ((actual[1],local[:13]),(actual[2],ev[:13]),(actual[4],graph[:13])):
        for a,b in zip(left,right):
            np.testing.assert_array_equal(a,b)
    np.testing.assert_array_equal(actual[3],q[:13])
    folds = read(CODE/'runs/round108-group-subsets/folds.json')
    ref = np.load(CODE/'runs/round123-grounded-chain/round123_both_l0p01-oof-scores.npy');assert metrics(bank,y,ref)['correct']==4404
    oof = {(f,p):np.zeros_like(ref) for f in FAMILIES for p in PENALTIES};records=[];math={};fits=0
    for fr in folds:
        f = fr['fold'];fitting,held = np.array(fr['fit']),np.array(fr['held']);assert not set(fitting)&set(held)
        p = load_npz(AUDIT/f'fold{f}.npz');c = np.load(AUDIT/f'fold{f}-components.npy');base = score_components(data,c)
        np.testing.assert_allclose(base[held],ref[held],rtol=1e-10,atol=1e-10)
        x,offset,importance,pa = pair_design(data,local,ev,q,graph,p,c,y,fitting)
        np.savez_compressed(OUT/f'fold{f}-pair-audit.npz',**pa)
        held_features = ([data[i] for i in held],[local[i] for i in held],[ev[i] for i in held],q[held],[graph[i] for i in held])
        for family in FAMILIES:
            if family not in math:
                math[family] = gradient_check(x[family],offset,importance)
            for penalty in PENALTIES:
                delta,fit = fit_residual(x[family],offset,importance,penalty);fits += 1
                parameters = updated_parameters(p,family,delta)
                scores = score_components(held_features[0],components(*held_features,parameters));oof[family,penalty][held] = scores
                np.savez(OUT/f'fold{f}-{family}-{penalty}.npz',delta=delta)
                row = dict(fold=f,family=family,lambda_value=penalty,fit=fit,held=metrics([bank[i] for i in held],y[held],scores),
                           current_held=metrics([bank[i] for i in held],y[held],ref[held]),**comparison(y[held],ref[held],scores))
                records.append(row);write(OUT/'fit-progress.json',records);print('OUTER '+json.dumps(row),flush=True)
        del x
    searches = []
    for family in FAMILIES:
        for penalty in PENALTIES:
            scores = oof[family,penalty];name = config_name(family,penalty);np.save(OUT/(name+'-oof-scores.npy'),scores)
            searches.append(dict(name=name,family=family,lambda_value=penalty,train_oof=metrics(bank,y,scores),
                current754_comparison=comparison(y,ref,scores),fold_deltas_vs_current=[r['held']['correct']-r['current_held']['correct'] for r in records if r['family']==family and r['lambda_value']==penalty]))
    selected = [min((r for r in searches if r['family']==family),key=lambda r:(-r['train_oof']['correct'],r['current754_comparison']['new_parent_errors'],
                      r['current754_comparison']['changed_choices'],-r['lambda_value'])) for family in FAMILIES]
    write(OUT/'selected-on-train-before-validation.json',dict(selected=selected,all_searches=searches,validation_used=False,test_used=False))
    p = load_npz(AUDIT/'full.npz');c = np.load(AUDIT/'full-components.npy');base = score_components(data,c)
    x,offset,importance,pa = pair_design(data,local,ev,q,graph,p,c,y,np.arange(len(bank)));np.savez_compressed(OUT/'full-pair-audit.npz',**pa)
    models = []
    for selected_row in selected:
        family,penalty = selected_row['family'],selected_row['lambda_value'];delta,fit = fit_residual(x[family],offset,importance,penalty);fits += 1
        parameters = updated_parameters(p,family,delta);path = OUT/'candidates'/selected_row['name'];path.mkdir(parents=True)
        write(path/'config.json',dict(schema='joint_four_block123_v1',family=family,lambda_value=penalty,fit_split='train',features='same_four_blocks_as123',standalone=True))
        np.savez(path/'parameters.npz',**parameters);np.savez(OUT/(selected_row['name']+'-update.npz'),delta=delta)
        expected = score_components(data,components(data,local,ev,q,graph,parameters))
        np.testing.assert_allclose(candidate_scores(bank,arrays,path),expected,rtol=1e-10,atol=1e-10)
        checks = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        checks.update(full_train_export_agrees=True,pure_input_cache_agrees=True,zero_update_exact_parent=True,fit_only_fold_center_and_scaler=True,all_parent_held_scores_reproduced=True)
        row = dict(**selected_row,method='method_round137_joint_retrain.py',checkpoint=path.relative_to(CODE).as_posix(),new_candidate=True,
                   train_resubstitution_not_oof=metrics(bank,y,expected),fit=fit,checks=checks,assets=asset_inventory(path),
                   update_l2=float(np.linalg.norm(delta)),module_coefficients=(1+delta).tolist() if family=='mix' else None)
        models.append(row);print('EXPORT '+json.dumps({k:v for k,v in row.items() if k not in ('assets','checks')}),flush=True)
    assert fits==20 and closure(['train_round137_joint_retrain.py'])==sources
    assert all(digest(CODE/n)==s for n,s in inherited.items()) and digest(PLAN)==audit['plan_sha256']
    write(OUT/'result.json',dict(status='completed_train_only',models=models,searches=searches,fold_records=records,mathematical_checks=math,
        model_fits=20,seconds=time.perf_counter()-tick,threads_total=4,sources=sources,inherited=inherited,plan_sha256=digest(PLAN),
        parent_assets=audit['parent_assets'],validation_used=False,test_used=False))
    print('TRAIN_COMPLETE '+json.dumps(dict(fits=fits,seconds=time.perf_counter()-tick)),flush=True)


def main():
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(),'Preserve evidence';OUT.mkdir();tick=time.perf_counter()
    try:
        process = subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--worker'],cwd=CODE,timeout=600)
        write(OUT/'process-monitor.json',dict(exit_code=process.returncode,wall_seconds=time.perf_counter()-tick,hard_timeout_seconds=600))
        assert process.returncode==0
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json',dict(status='hard_timeout',wall_seconds=time.perf_counter()-tick));raise


if __name__=='__main__':
    main()
