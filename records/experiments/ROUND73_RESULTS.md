# Round73: all-correct supervision with class-conditional densities

2026-10-24. Completed train-only screen; no candidate passed admission, no
full-train model exported and no validation/test files opened.

The hypothesis was that the 2,242 all-correct training questions, dropped by
pairwise ranking, could improve the learned distribution of correct solutions.
This experiment used an independent Gaussian discriminant on question-relative
embeddings. It did not mix with Round11 or use old predictions as input.

Three fixed 90%/10% train splits each refitted PCA64 and a fresh Round2 context
pairwise ridge alpha0.3. Both QDA and matched simpler LDA compared
informative-only versus all-train class supervision. Class weights were balanced
within question and class, and covariance shrinkage0.2 was fixed before fitting.
The PCA retained86.53–86.60% of fitting relative-embedding variance.

|Model|seed20261024 /475|seed20261025 /475|seed20261026 /475|Sum of paired net vs freshR2|
|---|---:|---:|---:|---:|
|FreshR2|422|422|422|0|
|LDA informative-only|407|415|414|-30|
|LDA all-train|405|415|414|-32|
|QDA informative-only|398|406|398|-64|
|QDA all-train|388|395|398|-85|

These are overlapping, historically reused internal development splits. Their
sum is a paired diagnostic and cannot be interpreted as1,425 independent test
examples or compared directly with748/798 validation.

The all-train LDA fixed32 freshR2 errors but introduced64 errors across the three
held views; all-train QDA fixed39 and introduced124. All-train supervision lost
2 decisions versus matched informative LDA and21 versus informative QDA.
Neither head had a positive seed net versus freshR2, so both failed the frozen
admission rule. The simpler LDA clearly outperformed QDA and received identical
eligibility, but also failed the baseline comparison.

All-correct held questions were automatically correct under every selector.
For single-correct questions the seed scores were freshR2 32/29/37, LDA all-train
30/36/40 and QDA all-train16/17/23. LDA's gains in two single-correct subsets
were offset by errors elsewhere. This illustrates why subgroup improvements
alone are insufficient admission evidence.

The evidence does not support the proposed Gaussian use of all-correct
supervision. A plausible explanation is that correct-looking marginal density
also captures topic/style and the frequent easy agreement cases; those examples
provide no direct contrast identifying why a rare competing answer is wrong.
The higher covariance flexibility worsened discrimination in this experiment.
This is an interpretation, not proof that all-correct questions contain no useful
information or that every density model must fail. No shrinkage/rank grid follows.

Training used one CPU thread,17.222 seconds, with a600-second parent-enforced
hard timeout. It performed12 head fits,3 PCA fits and3 baseline fits. A separate
numerical audit of all12 frozen fold models passed strict candidate permutation
(maximum score error0), PCA means recomputed only from fit indices, projection
orthogonality and independently evaluated Gaussian quadratic scores. Fit/held
indices are disjoint. Empty-bank behavior passed. The first audit invocation
failed solely because its nested script directory did not include the code
directory in Python's import path; that auxiliary script was repaired without
changing any frozen fitting or method source, then passed.

No eligible inference checkpoint exists, so this round makes no16MiB/30-second
official eligibility claim. Fold artifacts are retained for reproducibility and
are not submission checkpoints. Source hashes were rechecked unchanged after
fitting and audit. Candidate rows for central validation are the empty list.

Evidence: `code/runs/round73-gaussian/training-results.json`, `splits.json`,
`fit-records.json`, `changed-cases.json`, `holdout-scores.npz`, `boundary-audit.json`
and `source-hashes.json`. Frozen plan: `ROUND73_GAUSSIAN_PLAN.md`. From `code/`,
run `.venv/Scripts/python.exe train_round73_gaussian.py` in a fresh output
directory; the script refuses to overwrite completed results.
