"""Train-only sparse question interactions on a fixed answer-group parent."""
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
from scipy.sparse import csr_matrix,vstack
from scipy.optimize import minimize
from threadpoolctl import threadpool_limits
from common import load_inputs
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,asset_inventory,metrics
from train_round109_arithmetic_residual import loss
from method_round108_group_subsets import tables
from method_round109_arithmetic_residual import read_anchor,anchored
from method_round110_residual_ablation import candidate_scores as parent_scores
from method_round120_question_interaction import BUCKETS,COLUMNS,question_hash,evidence_tables,add_interaction,candidate_scores,contracts

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
BASE = CODE/'runs/round108-group-subsets'
OLD = CODE/'runs/round110-residual-ablation'
PARENT = OLD/'candidates/round110_final_evidence'
OUT = CODE/'runs/round120-question-interaction'
PLAN = ROOT/'ROUND120_QUESTION_INTERACTION_PLAN.md'


def scale_fit(evidence,fitting,columns):
    x = np.stack([v[columns] for i in fitting for v in evidence[i]])
    mean,scale = x.mean(0),x.std(0)
    scale[scale<1e-8] = 1
    return mean,scale


def pair_design(data,evidence,q,y,fitting,columns,scale,base):
    values,indices,indptr,origin,margins,raw_weights,positives,negatives = [],[],[0],[],[],[],[],[]
    dim = len(columns)
    for i in fitting:
        good,bad = [],[]
        for k,g in enumerate(data[i]):
            truth = y[i,g['members']]
            assert (truth==truth[0]).all()
            (good if truth[0] else bad).append(k)
        count = len(good)*len(bad)
        if not count:
            continue
        qi = np.flatnonzero(q[i])
        for p in good:
            for n in bad:
                delta = (evidence[i][p][columns]-evidence[i][n][columns])/scale
                used = np.flatnonzero(delta)
                vv = (q[i,qi,None]*delta[used][None,:]).ravel()
                jj = (qi[:,None]*dim+used[None,:]).ravel()
                values.append(vv);indices.append(jj);indptr.append(indptr[-1]+len(vv))
                origin.append(int(i));raw_weights.append(1/count)
                a,b = data[i][p]['members'][0],data[i][n]['members'][0]
                positives.append(a);negatives.append(b);margins.append(base[i,a]-base[i,b])
    origin = np.asarray(origin,dtype=int)
    informative = np.unique(origin)
    importance = np.asarray(raw_weights)/len(informative)
    totals = np.bincount(origin,weights=importance,minlength=len(data))
    np.testing.assert_allclose(totals[informative],1/len(informative),rtol=1e-12,atol=1e-14)
    assert set(informative)<=set(fitting) and abs(importance.sum()-1)<1e-12
    x = csr_matrix((np.concatenate(values),np.concatenate(indices),np.asarray(indptr)),shape=(len(origin),BUCKETS*dim))
    assert np.isfinite(x.data).all()
    audit = dict(origin=origin,positive_candidate=np.asarray(positives),negative_candidate=np.asarray(negatives),
                 anchor_margin=np.asarray(margins),weights=importance,question_total_weights=totals)
    return x,np.asarray(margins),importance,audit


def fit_cross(x,offset,importance):
    tick = time.perf_counter()
    result = minimize(loss,np.zeros(x.shape[1]),args=(x,offset,importance,.1),jac=True,method='L-BFGS-B',
                      options=dict(maxiter=1000,ftol=1e-12,gtol=1e-7,maxls=40))
    assert result.success and np.isfinite(result.x).all() and abs(result.jac).max()<1e-5
    return result.x,dict(iterations=int(result.nit),objective=float(result.fun),initial_objective=loss(np.zeros(x.shape[1]),x,offset,importance,.1)[0],
                         gradient_inf_norm=float(abs(result.jac).max()),seconds=time.perf_counter()-tick,pairs=x.shape[0],dimensions=x.shape[1],nonzero_values=x.nnz)


def gradient_check(x,offset,importance):
    n = min(x.shape[0],100)
    x,offset,importance = x[:n],offset[:n],importance[:n]/importance[:n].sum()
    w = np.random.default_rng(20261029).normal(0,.001,x.shape[1])
    value,grad = loss(w,x,offset,importance,.1)
    errors = []
    for j in (0,len(w)//4,len(w)//2,3*len(w)//4,len(w)-1):
        a,b = w.copy(),w.copy();a[j] += 1e-5;b[j] -= 1e-5
        errors.append(abs((loss(a,x,offset,importance,.1)[0]-loss(b,x,offset,importance,.1)[0])/2e-5-grad[j]))
    duplicate = loss(w,vstack([x,x]),np.r_[offset,offset],np.r_[importance,importance]/2,.1)
    assert max(errors)<1e-6 and abs(duplicate[0]-value)<1e-12
    np.testing.assert_allclose(duplicate[1],grad,rtol=1e-10,atol=1e-12)
    return dict(finite_difference_max_error=max(errors),duplicate_pair_invariance=True)


def worker():
    tick = time.perf_counter()
    sources = closure(['train_round120_question_interaction.py','method_round120_question_interaction.py'])
    prior = json.loads((OLD/'result.json').read_text(encoding='utf-8'))
    assert all(digest(CODE/n)==sha for n,sha in prior['sources'].items())
    parent_row = next(r for r in prior['models'] if r['name']=='round110_final_evidence')
    assert asset_inventory(PARENT)==parent_row['assets']
    inherited = {}
    def remember(p):
        inherited[p.relative_to(CODE).as_posix()] = digest(p)
    for p in (OLD/'result.json',OLD/'round110_final_evidence-oof-scores.npy',BASE/'folds.json'):
        remember(p)
    for f in range(3):
        remember(OLD/f'outer{f}-final_evidence.npz');remember(BASE/f'fold-models/fold{f}-round108_subsets_l0p01/weights.npz')
    for p in PARENT.rglob('*'):
        if p.is_file():
            remember(p)
    (OUT/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    shutil.copy2(PLAN,OUT/'sources/PLAN.md')
    plan_sha = digest(PLAN)
    write(OUT/'pretraining.json',dict(sources=sources,plan_sha256=plan_sha,inherited=inherited,parent_assets=parent_row['assets']))
    assert np.array_equal(question_hash('How MANY apples?'),question_hash('how many apples'))
    assert not np.array_equal(question_hash('remaining apples'),question_hash('apples per box'))
    assert not question_hash('12345?!').any()
    bank,arrays = load_inputs('train');y = labels(bank,'train')
    data = tables(bank,arrays);evidence = evidence_tables(bank,data)
    q = np.stack([question_hash(r['question']) for r in bank])
    assert np.isfinite(q).all() and all(v.shape==(32,) for row in evidence for v in row)
    folds = json.loads((BASE/'folds.json').read_text(encoding='utf-8'))
    parent_oof = np.load(OLD/'round110_final_evidence-oof-scores.npy')
    assert metrics(bank,y,parent_oof)['correct']==4398
    oof = {mode:np.zeros((len(bank),4)) for mode in COLUMNS}
    records,models,math_checks = [],[],{}
    fits = 0
    for frow in folds:
        f = frow['fold'];fitting,held = np.asarray(frow['fit']),np.asarray(frow['held'])
        assert not set(fitting)&set(held)
        base = read_anchor(data,BASE/f'fold-models/fold{f}-round108_subsets_l0p01')
        with np.load(OLD/f'outer{f}-final_evidence.npz',allow_pickle=False) as z:
            base = anchored(data,[[v[:26] for v in row] for row in evidence],base,z['mean'],z['scale'],z['weight'])
        np.testing.assert_allclose(base[held],parent_oof[held],rtol=1e-10,atol=1e-10)
        for mode,columns in COLUMNS.items():
            mean,scale = scale_fit(evidence,fitting,columns)
            x,offset,importance,audit = pair_design(data,evidence,q,y,fitting,columns,scale,base)
            if mode not in math_checks:
                math_checks[mode] = gradient_check(x,offset,importance)
            weight,report = fit_cross(x,offset,importance);fits += 1
            prediction = add_interaction([data[i] for i in held],[evidence[i] for i in held],q[held],base[held],columns,mean,scale,weight)
            oof[mode][held] = prediction
            np.savez(OUT/f'fold{f}-{mode}.npz',mean=mean,scale=scale,weight=weight)
            np.savez_compressed(OUT/f'fold{f}-{mode}-pair-audit.npz',**audit)
            records.append(dict(fold=f,mode=mode,fit=report,held=metrics([bank[i] for i in held],y[held],prediction),parent_held=metrics([bank[i] for i in held],y[held],base[held])))
            write(OUT/'fit-progress.json',records)
            print('OUTER '+json.dumps(records[-1]),flush=True)
    full_base = parent_scores(bank,arrays,PARENT)
    for mode in ('control',*COLUMNS):
        path = OUT/'candidates'/('round120_'+mode);path.mkdir(parents=True)
        shutil.copytree(PARENT,path/'parent')
        write(path/'config.json',dict(schema='question_evidence_interaction_v1',mode=mode,buckets=128,hash='blake2b_signed_l2_unigram_bigram_v1',
                                      lambda_value=.1,fit_split='train',parent='round110_final_evidence',margin_mode='same_fit_frozen_parent'))
        if mode=='control':
            expected,oo,report = full_base,parent_oof,dict(new_fits=0)
        else:
            columns = COLUMNS[mode]
            mean,scale = scale_fit(evidence,np.arange(len(bank)),columns)
            x,offset,importance,audit = pair_design(data,evidence,q,y,np.arange(len(bank)),columns,scale,full_base)
            weight,report = fit_cross(x,offset,importance);fits += 1
            np.savez(path/'interaction.npz',mean=mean,scale=scale,weight=weight)
            np.savez_compressed(OUT/f'{mode}-full-pair-audit.npz',**audit)
            expected = add_interaction(data,evidence,q,full_base,columns,mean,scale,weight);oo = oof[mode]
            np.testing.assert_array_equal(add_interaction(data,evidence,q,full_base,columns,mean,scale,np.zeros(len(weight))),full_base)
        np.testing.assert_allclose(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},path),expected[:53],rtol=1e-10,atol=1e-10)
        checks = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        checks.update(export_agrees=True,zero_interaction_exact_parent=True)
        np.save(OUT/(path.name+'-oof-scores.npy'),oo)
        models.append(dict(name=path.name,mode=mode,method='method_round120_question_interaction.py',checkpoint=path.relative_to(CODE).as_posix(),
                           train_oof=metrics(bank,y,oo),train_resubstitution_not_oof=metrics(bank,y,expected),fit=report,checks=checks,assets=asset_inventory(path)))
        print('EXPORT '+json.dumps({k:v for k,v in models[-1].items() if k not in ('checks','assets')}),flush=True)
    assert fits==12 and len(records)==9 and len(models)==4
    assert closure(['train_round120_question_interaction.py','method_round120_question_interaction.py'])==sources and digest(PLAN)==plan_sha
    assert all(digest(CODE/n)==sha for n,sha in inherited.items()) and asset_inventory(PARENT)==parent_row['assets']
    write(OUT/'result.json',dict(status='completed_train_only',models=models,fold_records=records,sources=sources,plan_sha256=plan_sha,inherited=inherited,
                                parent_assets=parent_row['assets'],model_fits=fits,mathematical_checks=math_checks,threads_total=4,
                                seconds=time.perf_counter()-tick,validation_used=False,test_used=False))
    print('TRAIN_COMPLETE '+json.dumps(dict(fits=fits,seconds=time.perf_counter()-tick)),flush=True)


def main():
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(),'Preserve original evidence'
    OUT.mkdir(parents=True);tick = time.perf_counter()
    try:
        p = subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--worker'],cwd=CODE,timeout=600)
        write(OUT/'process-monitor.json',dict(exit_code=p.returncode,wall_seconds=time.perf_counter()-tick,hard_timeout_seconds=600))
        assert p.returncode==0,'Training failed; evidence retained'
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json',dict(status='hard_timeout',wall_seconds=time.perf_counter()-tick));raise


if __name__=='__main__':
    main()
