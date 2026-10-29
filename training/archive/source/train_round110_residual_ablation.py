"""Sixteen matched residual fits with verified inherited nested anchor offsets."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
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
from features import answer_groups
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,asset_inventory,metrics
from train_round109_arithmetic_residual import residual_scale,residual_design,fit_residual,loss
from method_round108_group_subsets import tables,score_tables
from method_round109_arithmetic_residual import anchored,read_anchor
from method_round110_residual_ablation import feature_tables,DIMENSIONS,candidate_scores,predict

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OLD = CODE/'runs/round109-arithmetic-residual'
BASE = CODE/'runs/round108-group-subsets'
OUT = CODE/'runs/round110-residual-ablation'
PLAN = ROOT/'ROUND110_RESIDUAL_ABLATION_PLAN.md'
MODES = tuple(DIMENSIONS)


def contracts(bank,arrays,path):
    scores = candidate_scores(bank,arrays,path)
    pred = predict(bank,arrays,path)
    assert all(type(j) is int and 0 <= j <= 3 for j in pred)
    perm = [2,0,3,1]
    pb = [dict(r,candidates=[dict(r['candidates'][j],index=k) for k,j in enumerate(perm)]) for r in bank]
    np.testing.assert_allclose(candidate_scores(pb,{'embeddings':arrays['embeddings'][:,perm]},path),
                               scores[:,perm],rtol=1e-8,atol=1e-8)
    np.testing.assert_allclose(candidate_scores(bank[::-1],{'embeddings':arrays['embeddings'][::-1]},path),
                               scores[::-1],rtol=1e-8,atol=1e-8)
    assert predict([dict(r,id=f'unseen110-{i}') for i,r in enumerate(bank)],arrays,path) == pred
    for n in (1,7,23):
        np.testing.assert_allclose(candidate_scores(bank[:n],{'embeddings':arrays['embeddings'][:n]},path),
                                   scores[:n],rtol=1e-8,atol=1e-8)
    assert predict([],{'embeddings':np.empty((0,4,1024))},path) == []
    for i,group in enumerate(answer_groups(bank)):
        for a in set(v for v in group if v is not None):
            values = scores[i,[j for j,v in enumerate(group) if v == a]]
            assert (values == values[0]).all()
    return {'strict_permutation':True,'question_order':True,'new_ids':True,'variable_batch':True,
            'empty':True,'python_integers':True,'same_answer_same_score':True}


def gradient_check(x,offset,importance):
    w = np.random.default_rng(20261031).normal(0,.001,x.shape[1])
    eps = 1e-5
    value,grad = loss(w,x,offset,importance,.1)
    errors = []
    for j in range(x.shape[1]):
        plus,minus = w.copy(),w.copy()
        plus[j] += eps; minus[j] -= eps
        approximate = (loss(plus,x,offset,importance,.1)[0]-loss(minus,x,offset,importance,.1)[0])/(2*eps)
        errors.append(abs(approximate-grad[j]))
    assert max(errors) < 1e-6
    duplicated = loss(w,np.repeat(x,2,0),np.repeat(offset,2),np.repeat(importance/2,2),.1)
    assert abs(duplicated[0]-value) < 1e-12
    np.testing.assert_allclose(duplicated[1],grad,rtol=1e-10,atol=1e-12)
    return {'finite_difference_max_error':max(errors),'duplicate_pair_invariance':True}


def worker():
    tick = time.perf_counter()
    source = closure(['train_round110_residual_ablation.py','method_round110_residual_ablation.py'])
    prior = json.loads((OLD/'result.json').read_text(encoding='utf-8'))
    assert all(digest(CODE/n) == sha for n,sha in prior['sources'].items())
    assert all(digest(BASE/n) == sha for n,sha in prior['inherited_hashes'].items())
    selected = next(r for r in prior['models'] if r['augmented'] and r['lambda'] == .1)
    parent = CODE/selected['checkpoint']
    assert asset_inventory(parent) == selected['assets']
    inherited = {p.relative_to(OLD).as_posix():digest(p) for p in OLD.iterdir() if p.is_file()}
    base_hashes = {n:digest(BASE/n) for n in ['folds.json','round108_subsets_l0p01-oof-scores.npy']}
    (OUT/'sources').mkdir()
    for n in source:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    shutil.copy2(PLAN,OUT/'sources/PLAN.md')
    plan_sha = digest(PLAN)
    write(OUT/'pretraining.json',{'sources':source,'plan_sha256':plan_sha,'inherited_109':inherited,
                                 'inherited_108':base_hashes,'parent_assets':selected['assets']})
    bank,arrays = load_inputs('train')
    y = labels(bank,'train')
    data = tables(bank,arrays)
    features = {m:feature_tables(bank,data,m) for m in MODES}
    base_oof = np.load(BASE/'round108_subsets_l0p01-oof-scores.npy')
    prior_oof = np.load(OLD/'round109_subsets_r0p1-oof-scores.npy')
    assert int(y[np.arange(len(y)),prior_oof.argmax(1)].sum()) == 4392
    partitions = json.loads((OLD/'nested-partitions.json').read_text(encoding='utf-8'))
    folds = json.loads((BASE/'folds.json').read_text(encoding='utf-8'))
    oof = {m:np.zeros((len(bank),4)) for m in MODES}
    records,proof,checks = [],[],{}
    fits = 0
    for item in folds:
        fold = item['fold']
        fitting,held = np.asarray(item['fit']),np.asarray(item['held'])
        assert not set(fitting)&set(held)
        nested = np.zeros((len(bank),4))
        covered = []
        for row in [r for r in partitions if r['outer'] == fold and r['augmented']]:
            a,b = np.asarray(row['fit']),np.asarray(row['predicted'])
            assert set(a)|set(b) == set(fitting) and not set(a)&set(b)
            assert row['outer_held'] == held.tolist() and not (set(a)|set(b))&set(held)
            with np.load(OLD/f'outer{fold}-inner{row["inner"]}-aug1.npz',allow_pickle=False) as z:
                nested[b] = score_tables([data[int(i)] for i in b],z['mean'],z['scale'],z['weight'])
            covered.extend(b.tolist())
            proof.append({'outer':fold,'inner':row['inner'],'fit':a.tolist(),'predicted':b.tolist(),
                          'outer_held':held.tolist(),'verified_inherited_anchor':True})
        assert len(covered) == len(fitting) and set(covered) == set(fitting)
        for mode in MODES:
            mean,scale = residual_scale(features[mode],fitting)
            x,offset,importance,audit = residual_design(data,features[mode],y,fitting,scale,nested)
            with np.load(OLD/f'outer{fold}-aug1-residual-pair-audit.npz',allow_pickle=False) as old_audit:
                for key in ('origin','weights','anchor_margin','question_total_weights'):
                    np.testing.assert_array_equal(audit[key],old_audit[key])
            if mode not in checks:
                checks[mode] = gradient_check(x[:100],offset[:100],importance[:100]/importance[:100].sum())
            weight,report = fit_residual(x,offset,importance,.1)
            fits += 1
            predicted = anchored([data[int(i)] for i in held],[features[mode][int(i)] for i in held],
                                 base_oof[held],mean,scale,weight)
            oof[mode][held] = predicted
            if mode == 'full':
                with np.load(OLD/f'outer{fold}-round109_subsets_r0p1.npz',allow_pickle=False) as z:
                    for k,v in [('mean',mean),('scale',scale),('weight',weight)]:
                        np.testing.assert_allclose(v,z[k],rtol=1e-12,atol=1e-12)
                np.testing.assert_allclose(predicted,prior_oof[held],rtol=1e-10,atol=1e-10)
            np.savez(OUT/f'outer{fold}-{mode}.npz',mean=mean,scale=scale,weight=weight)
            np.savez_compressed(OUT/f'outer{fold}-{mode}-pair-audit.npz',**audit)
            row = {'fold':fold,'mode':mode,'dimensions':DIMENSIONS[mode],**report,
                   'held':metrics([bank[int(i)] for i in held],y[held],predicted),
                   'parent_held':metrics([bank[int(i)] for i in held],y[held],prior_oof[held])}
            records.append(row)
            write(OUT/'fit-progress.json',records)
            print('OUTER '+json.dumps(row),flush=True)
    write(OUT/'nested-offset-proofs.json',proof)
    models = []
    base = read_anchor(data,parent/'anchor')
    for mode in MODES:
        mean,scale = residual_scale(features[mode],np.arange(len(bank)))
        x,offset,importance,audit = residual_design(data,features[mode],y,np.arange(len(bank)),scale,base_oof)
        weight,report = fit_residual(x,offset,importance,.1)
        fits += 1
        path = OUT/'candidates'/('round110_'+mode)
        path.mkdir(parents=True)
        shutil.copytree(parent/'anchor',path/'anchor')
        np.savez(path/'residual.npz',mean=mean,scale=scale,weight=weight)
        np.savez_compressed(OUT/(mode+'-full-pair-audit.npz'),**audit)
        write(path/'config.json',{'schema':'matched_residual_features_v1','mode':mode,'dimensions':DIMENSIONS[mode],
                                  'anchor_lambda':.01,'augmented_anchor':True,'residual_lambda':.1,
                                  'offset':'nested_question_oof','fit_split':'train'})
        expected = anchored(data,features[mode],base,mean,scale,weight)
        np.testing.assert_array_equal(anchored(data,features[mode],base,mean,scale,np.zeros(len(weight))),base)
        if mode == 'full':
            with np.load(parent/'residual.npz',allow_pickle=False) as z:
                for k,v in [('mean',mean),('scale',scale),('weight',weight)]:
                    np.testing.assert_allclose(v,z[k],rtol=1e-12,atol=1e-12)
            np.testing.assert_allclose(oof[mode],prior_oof,rtol=1e-10,atol=1e-10)
        np.testing.assert_array_equal(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},path),expected[:53])
        cc = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        cc.update(cache_export_exact=True,zero_residual_exact_anchor=True)
        row = {'name':path.name,'mode':mode,'dimensions':DIMENSIONS[mode],'method':'method_round110_residual_ablation.py',
               'checkpoint':path.relative_to(CODE).as_posix(),'train_oof':metrics(bank,y,oof[mode]),
               'parent_train_oof':selected['train_oof'],'train_resubstitution_not_oof':metrics(bank,y,expected),
               'fit':report,'checks':cc,'assets':asset_inventory(path)}
        models.append(row)
        np.save(OUT/(path.name+'-oof-scores.npy'),oof[mode])
        print('EXPORTED '+json.dumps({k:v for k,v in row.items() if k not in ('checks','assets')}),flush=True)
    assert fits == 16 and len(records) == 12
    assert closure(['train_round110_residual_ablation.py','method_round110_residual_ablation.py']) == source
    assert digest(PLAN) == plan_sha and asset_inventory(parent) == selected['assets']
    assert all(digest(OLD/n) == sha for n,sha in inherited.items())
    assert all(digest(BASE/n) == sha for n,sha in base_hashes.items())
    write(OUT/'result.json',{'status':'completed_train_only','models':models,'fold_records':records,
                            'sources':source,'plan_sha256':plan_sha,'inherited_109':inherited,'inherited_108':base_hashes,
                            'mathematical_checks':checks,'full_control_reproduced':True,
                            'model_fits':fits,'threads_total':4,'seconds':time.perf_counter()-tick,
                            'validation_used':False,'test_used':False})
    print('TRAIN_COMPLETE '+json.dumps({'fits':fits,'seconds':time.perf_counter()-tick}),flush=True)


def main():
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(), 'Preserve evidence; no automatic retry'
    OUT.mkdir(parents=True)
    tick = time.perf_counter()
    try:
        r = subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--worker'],cwd=CODE,timeout=600)
        write(OUT/'process-monitor.json',{'exit_code':r.returncode,'wall_seconds':time.perf_counter()-tick,
                                         'hard_timeout_seconds':600,'process_completed':True})
        assert r.returncode == 0, 'Training failed; evidence retained'
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json',{'status':'hard_timeout','wall_seconds':time.perf_counter()-tick})
        raise


if __name__ == '__main__':
    main()
