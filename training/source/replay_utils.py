"""Exact function bodies extracted from the frozen original training sources.
Only imports were consolidated; extraction provenance is in provenance/manifest.json.
"""
import time
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from features import answer_groups
from method_round108_group_subsets import tables
from method_round137_joint_retrain import BLOCKS,SLICES,candidate_scores,predict

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


def metrics(bank, y, scores):
    right = y[np.arange(len(y)), scores.argmax(1)]
    hard = np.array([len(set(v for v in g if v is not None)) >= 2 for g in answer_groups(bank)])
    return {'correct': int(right.sum()), 'n': len(y), 'accuracy': 100*float(right.mean()),
            'disagreement_correct': int(right[hard].sum()), 'disagreement_n': int(hard.sum()),
            'single_correct': int(right[y.sum(1) == 1].sum()), 'single_n': int((y.sum(1) == 1).sum())}


def comparison(y,base,scores):
    a = y[np.arange(len(y)),base.argmax(1)].astype(bool)
    b = y[np.arange(len(y)),scores.argmax(1)].astype(bool)
    return dict(fixed_parent_errors=int((~a&b).sum()),new_parent_errors=int((a&~b).sum()),
                changed_choices=int((base.argmax(1)!=scores.argmax(1)).sum()))


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
