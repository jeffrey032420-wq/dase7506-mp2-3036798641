# Training release integration summary

- Student: **3036798641 Liang Zefeng**.
- Intended repository mapping: this directory becomes `training/`; sibling `code/` contains frozen inference source and `code/checkpoint/`.
- Primary entry: `replay_round137.py --data-dir OFFICIAL_DATA`. Defaults to sibling `../code`, saved `parents/`, and new `training/runs/reproduction/round137/`.
- Copies exact original loss/optimizer/pair/metric/gradient/contract function bodies (7 functions) and retains 15 frozen feature-source files plus the 26-file full historical source import closure.
- Includes exact original full/fold0/fold1/fold2 center NPZs, fixed original folds, original Round123 train OOF, train-file SHA requirements, original train-only audit/training/selection records, and block-level source provenance.
- Original replay protocol is 18 outer fits (mix4/joint5180 × lambdas .01/.1/1 × three folds) + two full fits, with unchanged pair weighting, parent scales, optimizer, and selection rules.
- Optional `rebuild_parent_centers.py` reconstructs the **fixed selected** A→L→I→G chain in 25 fits from official train inputs before the 20-fit replay. It is explicitly **authored/statically inspected only, not executed or numerically validated after freezing**. It compares rebuilt centers only after fitting, and stops if mismatched. Do not claim all historic searches were repeated or that this optional wrapper is execution-verified.
- All outputs confined to fresh subdirectories of `training/runs/reproduction/`; no submitted checkpoint overwrite, no validation/test loading, no automatic prediction/scoring, no online access.
- Static assembly checks are recorded in `provenance/static-release-checks.json`. No new fits, predictions, or scores were performed in publication preparation.
- Required primary replay dependencies: NumPy2.5.3, SciPy1.18.1, threadpoolctl3.7.0; optional parent rebuild additionally scikit-learn1.9.1. Original Python3.12.14.
- `TRAINING_REPRODUCE.md` is the detailed reviewer-facing document; root may link it or copy its text into top-level reproduction instructions.
