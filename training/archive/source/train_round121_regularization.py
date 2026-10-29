"""Finite train-only R120 lambda ablation; select one lambda per family on OOF."""
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
from scipy.optimize import minimize
from threadpoolctl import threadpool_limits
from common import load_inputs
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,asset_inventory,metrics
from train_round109_arithmetic_residual import loss
from train_round120_question_interaction import scale_fit,pair_design,gradient_check
from method_round108_group_subsets import tables
from method_round109_arithmetic_residual import read_anchor,anchored
from method_round110_residual_ablation import candidate_scores as parent_scores
from method_round120_question_interaction import COLUMNS,question_hash,evidence_tables,add_interaction,candidate_scores,contracts

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
BASE = CODE/'runs/round108-group-subsets'
OLD = CODE/'runs/round110-residual-ablation'
PRIOR = CODE/'runs/round120-question-interaction'
PARENT = OLD/'candidates/round110_final_evidence'
OUT = CODE/'runs/round121-regularization'
PLAN = ROOT/'ROUND121_REGULARIZATION_PLAN.md'
PENALTIES = (1.,.1,.01,.001,.0001)


def fit_cross(x,offset,importance,penalty):
    tick = time.perf_counter()
    result = minimize(loss,np.zeros(x.shape[1]),args=(x,offset,importance,penalty),jac=True,method='L-BFGS-B',
                      options=dict(maxiter=1000,ftol=1e-12,gtol=1e-7,maxls=40))
    assert result.success and np.isfinite(result.x).all() and abs(result.jac).max()<1e-5
    return result.x,dict(lambda_value=penalty,iterations=int(result.nit),objective=float(result.fun),
                         initial_objective=loss(np.zeros(x.shape[1]),x,offset,importance,penalty)[0],
                         gradient_inf_norm=float(abs(result.jac).max()),seconds=time.perf_counter()-tick,
                         pairs=x.shape[0],dimensions=x.shape[1],nonzero_values=x.nnz,weight_norm=float(np.linalg.norm(result.x)))


def name(mode,penalty):
    return 'round121_'+mode+'_l'+str(penalty).replace('.','p')


def comparison(y,base,scores):
    a = y[np.arange(len(y)),base.argmax(1)].astype(bool)
    b = y[np.arange(len(y)),scores.argmax(1)].astype(bool)
    return dict(fixed_parent_errors=int((~a&b).sum()),new_parent_errors=int((a&~b).sum()),
                changed_choices=int((base.argmax(1)!=scores.argmax(1)).sum()))


def worker():
    tick = time.perf_counter()
    sources = closure(['train_round121_regularization.py'])
    prior = json.loads((PRIOR/'result.json').read_text(encoding='utf-8'))
    assert all(digest(CODE/n)==sha for n,sha in prior['sources'].items())
    assert all(digest(CODE/n)==sha for n,sha in prior['inherited'].items())
    inherited = dict(prior['inherited'])
    for p in [PRIOR/'result.json',CODE/'runs/round121-train-diagnosis/diagnosis.json',*[PRIOR/f'round120_{mode}-oof-scores.npy' for mode in COLUMNS]]:
        inherited[p.relative_to(CODE).as_posix()] = digest(p)
    parent_assets = asset_inventory(PARENT)
    (OUT/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    shutil.copy2(PLAN,OUT/'sources/PLAN.md');plan_sha = digest(PLAN)
    write(OUT/'pretraining.json',dict(sources=sources,plan_sha256=plan_sha,inherited=inherited,parent_assets=parent_assets,penalties=PENALTIES))
    bank,arrays = load_inputs('train');y = labels(bank,'train')
    data = tables(bank,arrays);evidence = evidence_tables(bank,data)
    q = np.stack([question_hash(r['question']) for r in bank])
    folds = json.loads((BASE/'folds.json').read_text(encoding='utf-8'))
    parent_oof = np.load(OLD/'round110_final_evidence-oof-scores.npy')
    assert metrics(bank,y,parent_oof)['correct']==4398
    oof = {(mode,p):np.zeros((len(bank),4)) for mode in COLUMNS for p in PENALTIES}
    records,checks,models,configs = [],{},[],[]
    fits = 0
    for fr in folds:
        f = fr['fold'];fitting,held = np.asarray(fr['fit']),np.asarray(fr['held'])
        assert not set(fitting)&set(held)
        base = read_anchor(data,BASE/f'fold-models/fold{f}-round108_subsets_l0p01')
        with np.load(OLD/f'outer{f}-final_evidence.npz',allow_pickle=False) as z:
            base = anchored(data,[[v[:26] for v in row] for row in evidence],base,z['mean'],z['scale'],z['weight'])
        np.testing.assert_allclose(base[held],parent_oof[held],rtol=1e-10,atol=1e-10)
        for mode,columns in COLUMNS.items():
            mean,scale = scale_fit(evidence,fitting,columns)
            x,offset,importance,audit = pair_design(data,evidence,q,y,fitting,columns,scale,base)
            np.savez_compressed(OUT/f'fold{f}-{mode}-pair-audit.npz',**audit)
            if mode not in checks:
                checks[mode] = gradient_check(x,offset,importance)
            for penalty in PENALTIES:
                weight,fit = fit_cross(x,offset,importance,penalty);fits += 1
                scores = add_interaction([data[i] for i in held],[evidence[i] for i in held],q[held],base[held],columns,mean,scale,weight)
                oof[(mode,penalty)][held] = scores
                np.savez(OUT/f'fold{f}-{name(mode,penalty)}.npz',mean=mean,scale=scale,weight=weight)
                records.append(dict(fold=f,mode=mode,lambda_value=penalty,fit=fit,held=metrics([bank[i] for i in held],y[held],scores),
                                    parent_held=metrics([bank[i] for i in held],y[held],base[held]),**comparison(y[held],base[held],scores)))
                write(OUT/'fit-progress.json',records)
                print('OUTER '+json.dumps(records[-1]),flush=True)
    for mode in COLUMNS:
        np.testing.assert_allclose(oof[(mode,.1)],np.load(PRIOR/f'round120_{mode}-oof-scores.npy'),rtol=1e-10,atol=1e-10)
        for penalty in PENALTIES:
            oo = oof[(mode,penalty)];np.save(OUT/(name(mode,penalty)+'-oof-scores.npy'),oo)
            configs.append(dict(name=name(mode,penalty),mode=mode,lambda_value=penalty,train_oof=metrics(bank,y,oo),
                                **comparison(y,parent_oof,oo),fold_deltas_vs_parent=[r['held']['correct']-r['parent_held']['correct'] for r in records if r['mode']==mode and r['lambda_value']==penalty]))
    selected = [min([r for r in configs if r['mode']==mode],key=lambda r:(-r['train_oof']['correct'],-r['lambda_value'])) for mode in COLUMNS]
    write(OUT/'selection-train-only.json',dict(status='selected_before_full_fit_and_validation',candidates=selected,all_configurations=configs,
                                             selection_rule='max train OOF correct, tie larger lambda',validation_used=False,test_used=False))
    full_base = parent_scores(bank,arrays,PARENT)
    for row in selected:
        mode,penalty = row['mode'],row['lambda_value'];columns = COLUMNS[mode]
        path = OUT/'candidates'/row['name'];path.mkdir(parents=True);shutil.copytree(PARENT,path/'parent')
        write(path/'config.json',dict(schema='question_evidence_interaction_v1',mode=mode,buckets=128,hash='blake2b_signed_l2_unigram_bigram_v1',
                                      lambda_value=penalty,fit_split='train',parent='round110_final_evidence',margin_mode='same_fit_frozen_parent'))
        mean,scale = scale_fit(evidence,np.arange(len(bank)),columns)
        x,offset,importance,audit = pair_design(data,evidence,q,y,np.arange(len(bank)),columns,scale,full_base)
        weight,fit = fit_cross(x,offset,importance,penalty);fits += 1
        np.savez(path/'interaction.npz',mean=mean,scale=scale,weight=weight)
        np.savez_compressed(OUT/f'{mode}-full-pair-audit.npz',**audit)
        expected = add_interaction(data,evidence,q,full_base,columns,mean,scale,weight)
        np.testing.assert_allclose(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},path),expected[:53],rtol=1e-10,atol=1e-10)
        np.testing.assert_array_equal(add_interaction(data,evidence,q,full_base,columns,mean,scale,np.zeros(len(weight))),full_base)
        contracts_result = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        contracts_result.update(export_agrees=True,zero_interaction_exact_parent=True,lambda_p1_oof_reproduces_round120=True)
        models.append(dict(**row,method='method_round120_question_interaction.py',checkpoint=path.relative_to(CODE).as_posix(),
                           train_resubstitution_not_oof=metrics(bank,y,expected),fit=fit,checks=contracts_result,assets=asset_inventory(path)))
        print('EXPORT '+json.dumps({k:v for k,v in models[-1].items() if k not in ('assets','checks')}),flush=True)
    assert fits==48 and len(records)==45 and len(models)==3
    assert closure(['train_round121_regularization.py'])==sources and digest(PLAN)==plan_sha
    assert all(digest(CODE/n)==sha for n,sha in inherited.items()) and asset_inventory(PARENT)==parent_assets
    write(OUT/'result.json',dict(status='completed_train_only',models=models,configurations=configs,fold_records=records,sources=sources,
                                plan_sha256=plan_sha,inherited=inherited,parent_assets=parent_assets,model_fits=fits,
                                mathematical_checks=checks,threads_total=4,seconds=time.perf_counter()-tick,validation_used=False,test_used=False))
    print('TRAIN_COMPLETE '+json.dumps(dict(fits=fits,seconds=time.perf_counter()-tick,selected=selected)),flush=True)


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
