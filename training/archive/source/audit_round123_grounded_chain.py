"""Train-only parser, grounding and error-opportunity audit before any new fit."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import time
import numpy as np
from common import load_inputs
from train_round1 import labels
from train_round108_group_subsets import digest,write
from method_round108_group_subsets import tables
from numeric_round7_v3 import evidence as local_evidence
from method_round123_grounded_chain import graph_records,candidate_features,NAMES,COLUMNS

CODE = Path(__file__).resolve().parent
OUT = CODE/'runs/round123-train-audit-v2'


def checks():
    a = candidate_features('There are 3 boxes with 4 items each. How many items?', '3 * 4 = 12\n12 - 2 = 10\n#### 10')
    b = candidate_features('There are 3 boxes with 4 items each. How many items?', '3 * 4 = 11\n11 - 2 = 9\n#### 9')
    c = candidate_features('There are 3 boxes with 4 items each. How many items?', '3 * 4 = 11\n3 * 4 = 12\n#### 12')
    assert a[9]==1 and a[8]==0 and a[5]==0 and a[2]>0
    assert b[5]>.4 and b[9]==0
    assert c[5]==0 and c[9]==1 and c[11]>.4
    assert not candidate_features('3 apples','No calculation. #### 5')[3:].any()
    for text in ('x^2 * 3 = 6','x + 3 = 6','3 * 4 = 12 apples','\\frac{x}{2} * 4 = 6'):
        assert not graph_records(text),text
    return dict(false_ancestor_detected=True,unrelated_false_equation_not_in_ancestry=True,
                strict_vs_relaxed_constants=True,unknown_not_forced_incorrect=True,unsupported_boundaries_refused=True)


def main():
    tick = time.perf_counter();assert not OUT.exists();OUT.mkdir()
    parser_checks = checks();bank,arrays = load_inputs('train');y = labels(bank,'train').astype(bool)
    features = np.array([[candidate_features(r['question'],c['text']) for c in r['candidates']] for r in bank])
    np.save(OUT/'candidate-features.npy',features)
    subset_of_local = True;record_count = false_count = 0
    for row in bank:
        for c in row['candidates']:
            old,_ = local_evidence(c['text']);old_pairs = {(a,b) for a,b,_ in old}
            for a,b,_ in graph_records(c['text']):
                subset_of_local &= (a,b) in old_pairs;record_count += 1;false_count += a!=b
    assert subset_of_local,'Graph must not invent equations beyond unchanged local parser'
    data = tables(bank,arrays);path = CODE/'runs/round120-question-interaction/round120_question_both-oof-scores.npy'
    scores = np.load(path);choice = scores.argmax(1);right = y[np.arange(len(y)),choice]
    group = [[np.r_[features[i,g['members']].mean(0),features[i,g['members']].max(0)] for g in gs] for i,gs in enumerate(data)]
    coverage = {}
    for mode,cols in COLUMNS.items():
        count = 0
        for i in np.flatnonzero(~right):
            gs = data[i];chosen = next(k for k,g in enumerate(gs) if choice[i] in g['members'])
            count += any(y[i,g['members'][0]] and np.max(abs(group[i][k][cols]-group[i][chosen][cols]))>1e-9 for k,g in enumerate(gs))
        coverage[mode] = int(count)
    profiles = {}
    for name,k in (('strict_true_chain',8),('relaxed_true_chain',9),('false_on_final_chain',5),('final_equation',3)):
        mask = features[:,:,k]>0
        profiles[name] = dict(candidates=int(mask.sum()),correct=int((mask&y).sum()),incorrect=int((mask&~y).sum()),
                              incorrect_parent_choices=int((mask[np.arange(len(y)),choice]&~right).sum()))
    report = dict(status='completed_train_only_audit',n=len(bank),parent_oof_correct=int(right.sum()),parent_errors=int((~right).sum()),
                  feature_names=NAMES,features_shape=list(features.shape),parser_checks=parser_checks,
                  graph_equations_subset_of_unchanged_local_evidence=True,retained_equations=record_count,exactly_false_equations=false_count,
                  error_opportunity_coverage=coverage,candidate_signal_profiles=profiles,seconds=time.perf_counter()-tick,
                  sources={n:digest(CODE/n) for n in ('audit_round123_grounded_chain.py','method_round123_grounded_chain.py')},
                  parent_oof_sha256=digest(path),feature_sha256=digest(OUT/'candidate-features.npy'),
                  note='All signals are soft. Grounded arithmetic is insufficient to establish semantic correctness; identical literal values do not identify entities.',
                  validation_used=False,test_used=False,new_fits=0)
    write(OUT/'audit.json',report);print(json.dumps(report,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
