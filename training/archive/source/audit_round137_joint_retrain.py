"""Train-only exact decomposition and existing-expert complementarity audit."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import time
import numpy as np
from threadpoolctl import threadpool_limits
from common import load_inputs
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,metrics,asset_inventory
from method_round123_grounded_chain import candidate_scores as parent_scores
from method_round137_joint_retrain import BLOCKS,DIMENSIONS,input_features,components,score_components,updated_parameters,candidate_scores

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
OUT = CODE/'runs/round137-train-audit'
PARENT = CODE/'runs/round123-grounded-chain/candidates/round123_both_l0p01'
PLAN = ROOT/'ROUND137_JOINT_RETRAIN_PLAN.md'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def parameter_paths(fold=None):
    if fold is None:
        return dict(A=PARENT/'parent/parent/anchor/weights.npz',L=PARENT/'parent/parent/residual.npz',
                    I=PARENT/'parent/interaction.npz',G=PARENT/'chain.npz')
    return dict(A=CODE/f'runs/round108-group-subsets/fold-models/fold{fold}-round108_subsets_l0p01/weights.npz',
                L=CODE/f'runs/round110-residual-ablation/outer{fold}-final_evidence.npz',
                I=CODE/f'runs/round120-question-interaction/fold{fold}-question_both.npz',
                G=CODE/f'runs/round123-grounded-chain/fold{fold}-round123_both_l0p01.npz')


def load_parameters(paths):
    p = {}
    for b,size,mean_size in zip(BLOCKS,DIMENSIONS,(1034,26,32,24)):
        with np.load(paths[b],allow_pickle=False) as z:
            for key in ('mean','scale','weight'):
                p[b+'_'+key] = np.asarray(z[key],dtype=float).ravel().copy()
        assert p[b+'_weight'].shape==(size,) and p[b+'_mean'].shape==(mean_size,)
        assert p[b+'_scale'].shape==(mean_size,) and np.all(p[b+'_scale']>0)
    assert all(np.isfinite(v).all() for v in p.values())
    return p


def main():
    tick = time.perf_counter();assert not OUT.exists();OUT.mkdir()
    sources = closure(['audit_round137_joint_retrain.py']);prior = read(CODE/'runs/round123-grounded-chain/result.json')
    assert all(digest(CODE/n)==s for n,s in prior['sources'].items())
    assert all(digest(CODE/n)==s for n,s in prior['inherited'].items())
    bank,arrays = load_inputs('train');y = labels(bank,'train').astype(bool)
    features = input_features(bank,arrays);data,local,ev,q,graph = features
    indptr = np.r_[0,np.cumsum([len(gs) for gs in data])]
    np.savez(OUT/'raw-features.npz',indptr=indptr,local=np.vstack([v for row in local for v in row]),
             evidence=np.vstack([v for row in ev for v in row]),questions=q,graph=np.vstack([v for row in graph for v in row]))
    p = load_parameters(parameter_paths());c = components(*features,p);base = score_components(data,c)
    original = parent_scores(bank,arrays,PARENT);np.testing.assert_allclose(base,original,rtol=1e-10,atol=1e-10)
    assert metrics(bank,y,base)['correct']==4519
    np.savez(OUT/'full.npz',**p);np.save(OUT/'full-components.npy',c)
    zero = OUT/'zero-control';zero.mkdir();write(zero/'config.json',dict(schema='joint_four_block123_v1',family='control'))
    np.savez(zero/'parameters.npz',**p)
    np.testing.assert_allclose(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},zero),base[:53],rtol=1e-10,atol=1e-10)
    for family,dim in (('mix',4),('joint',5180)):
        pp = updated_parameters(p,family,np.zeros(dim))
        assert all(np.array_equal(pp[k],p[k]) for k in p)
    ref_path = CODE/'runs/round123-grounded-chain/round123_both_l0p01-oof-scores.npy';ref = np.load(ref_path)
    folds = read(CODE/'runs/round108-group-subsets/folds.json');fold_checks = []
    inherited = dict(prior['inherited'])
    for path in (ref_path,CODE/'runs/round123-grounded-chain/result.json',CODE/'runs/round108-group-subsets/folds.json',
                 *[p for p in PARENT.rglob('*') if p.is_file()]):
        inherited[path.relative_to(CODE).as_posix()] = digest(path)
    for row in folds:
        f = row['fold'];fit,held = row['fit'],row['held'];assert not set(fit)&set(held)
        paths = parameter_paths(f);fp = load_parameters(paths);fc = components(*features,fp);fs = score_components(data,fc)
        np.testing.assert_allclose(fs[held],ref[held],rtol=1e-10,atol=1e-10)
        np.savez(OUT/f'fold{f}.npz',**fp);np.save(OUT/f'fold{f}-components.npy',fc)
        for path in paths.values():
            inherited[path.relative_to(CODE).as_posix()] = digest(path)
        fold_checks.append(dict(fold=f,fit=fit,held=held,old_held_exact=True,
                                held_correct=metrics([bank[i] for i in held],y[held],fs[held])['correct']))
    old_choice = ref.argmax(1);old_right = y[np.arange(len(y)),old_choice];assert old_right.sum()==4404
    experts = [CODE/'runs/round108-group-subsets/round108_subsets_l0p01-oof-scores.npy',
               CODE/'runs/round110-residual-ablation/round110_final_evidence-oof-scores.npy']
    experts += [CODE/f'runs/round112-diverse-experts/round112_{a}_{loss}-oof-scores.npy'
                for a in ('linear','pointwise','deepsets','attention') for loss in ('uniform_ce','correct_set_mass')]
    pool = old_right.copy();audit = []
    for path in experts:
        s = np.load(path);assert s.shape==ref.shape and np.isfinite(s).all()
        choice = s.argmax(1);right = y[np.arange(len(y)),choice]
        pool |= right;sha = digest(path);inherited[path.relative_to(CODE).as_posix()] = sha
        audit.append(dict(name=path.name.replace('-oof-scores.npy',''),correct=int(right.sum()),n=len(y),
                          recovered_parent_errors=int((~old_right&right).sum()),wrong_on_parent_correct=int((old_right&~right).sum()),
                          changed_choices=int((choice!=old_choice).sum()),pair_oracle_correct=int((old_right|right).sum()),source_sha256=sha))
    write(OUT/'expert-complementarity.json',dict(experts=audit,oracle_pool_correct=int(pool.sum()),parent_correct=4404,n=len(y),
           oracle_recovered_parent_errors=int((~old_right&pool).sum()),deployable_accuracy=False,
           note='Truth-selected model union is only an upper bound; no fusion is trained or selected.'))
    cached = [OUT/'raw-features.npz',OUT/'full.npz',OUT/'full-components.npy',
              *[OUT/f'fold{f}{suffix}' for f in range(3) for suffix in ('.npz','-components.npy')]]
    result = dict(status='completed_train_only_audit',n=len(bank),parent_oof_correct=4404,parent_full_resubstitution=4519,
                  block_weight_dimensions=dict(zip(BLOCKS,DIMENSIONS)),parameter_count=sum(DIMENSIONS),
                  exact_full_and_held_decomposition=True,zero_update_and_standalone_export=True,fold_centers=fold_checks,
                  sources=sources,inherited=inherited,parent_assets=asset_inventory(PARENT),
                  cache_sha256={p.name:digest(p) for p in cached},plan_sha256=digest(PLAN),
                  new_fits=0,validation_used=False,test_used=False,seconds=time.perf_counter()-tick)
    assert closure(['audit_round137_joint_retrain.py'])==sources
    assert all(digest(CODE/n)==s for n,s in inherited.items())
    write(OUT/'result.json',result)
    print(json.dumps(dict(status=result['status'],seconds=result['seconds'],exact_decomposition=True,
                          oracle_recovered_parent_errors=int((~old_right&pool).sum()),experts=audit)),flush=True)


if __name__=='__main__':
    with threadpool_limits(limits=4):
        main()
