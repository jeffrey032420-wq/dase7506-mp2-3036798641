# Training reproduction

Author: Liang Zefeng, student ID 3036798641.

## Scope and verification status

The submitted model is **proximal joint-update experiment joint, lambda 1**, a 5,180-weight proximal update of the fixed four-block grounded-chain control parent. The inference checkpoint is frozen. Numerical verification was completed on 30 October 2026 in the existing pinned local environment. The submitted weights were not overwritten. Both training routes reproduce the frozen parameter arrays exactly; the reconstructed model reproduces official validation and test scores. Evidence is in `../materials/reproduction/`.

There are three different reproduction tasks:

| Task | Entry and inputs | Status |
|---|---|---|
| Score the submitted frozen model without retraining | Repository inference instructions; `code/checkpoint/` | Uses the original frozen inference source and two-file checkpoint |
| Repeat the 20-fit proximal joint-update experiment experiment from the exact saved train-only parent centers | `training/replay_round137.py`, official train data, included `training/parents/` | Primary training reproduction route; mathematical helpers are exact AST copies of original source. Numerically verified: 20 fits, OOF 4,406/4,755, maximum frozen-array difference 0 |
| Rebuild the fixed selected parent chain from train inputs, then repeat proximal joint-update experiment | Optional `training/rebuild_parent_centers.py`, followed by replay with `--parents-dir` | Numerically verified: 25 parent fits plus 20 replay fits, maximum frozen-array difference 0; it does not repeat all historical searches |

Do not describe the saved-parent replay as training every historical component from scratch. The archived original records describe the original experiments; the separate `materials/reproduction/` records describe the fresh wrapper executions.

## Installation

Original training used Python **3.12.14**, NumPy **2.5.3**, SciPy **1.18.1**, scikit-learn **1.9.1**, and threadpoolctl **3.7.0**. Frozen inference needs NumPy only. The primary proximal joint-update experiment replay needs NumPy, SciPy, and threadpoolctl; optional parent rebuilding additionally needs scikit-learn.

From the repository root, install in a Python virtual environment:

```sh
python -m pip install -r training/requirements.txt
```

For optional parent rebuilding, install the full original numerical dependencies:

```sh
python -m pip install -r training/archive/requirements.txt
```

Obtain the unmodified official repository/data from <https://github.com/xudongwu-0/DASE7506-MP2>. Pass the **official `code/data` directory** to `--data-dir`. The training scripts open only `manifest.json`, `candidates/gsm8k_train.jsonl`, `candidates/gsm8k_train.npz`, and `gsm8k_train.jsonl`. Original train-file SHA-256 values are in `parents/train-data-manifest.json`; mismatches stop execution. The large official data files are not duplicated in this release.

## Primary route: exact saved-parent proximal joint-update experiment replay

Run from the repository root, replacing the example data path:

```sh
python -X utf8 training/replay_round137.py --data-dir /path/to/official/DASE7506-MP2/code/data
```

PowerShell example (use an actual local official data path):

```powershell
python -X utf8 .\training\replay_round137.py --data-dir 'D:\official-mp2\code\data'
```

`--code-dir` defaults to `../code` **relative to the script**. All inference feature source hashes are checked against the frozen originals before fitting. The primary helper functions in `source/replay_utils.py` are copied exactly from the original loss, optimizer, pair construction, metrics, comparison, gradient checks, and interface checks; the extraction mapping is in `provenance/manifest.json`.

Outputs go to the new directory `training/runs/reproduction/round137/`. Existing output directories are refused. To repeat independently, choose another directory under `training/runs/reproduction/`:

```sh
python -X utf8 training/replay_round137.py --data-dir /path/to/official/code/data --output runs/reproduction/round137-second
```

An optional read-only numerical parameter comparison with the submitted checkpoint can be requested:

```sh
python -X utf8 training/replay_round137.py --data-dir /path/to/official/code/data --output runs/reproduction/round137-compare --reference-checkpoint code/checkpoint
```

The replay writes both family candidates. It does not choose a new submission or overwrite `code/checkpoint/`:

```text
training/runs/reproduction/round137/
  selected-on-train-before-validation.json
  fit-progress.json
  result.json
  process-monitor.json
  candidates/
    round137_mix_l1p0/{config.json, parameters.npz}
    round137_joint_l1p0/{config.json, parameters.npz}
```

The displayed candidate names were confirmed by the fresh replay. A platform/library difference can alter the optimizer or selection; inspect the saved six-configuration table and convergence records. Compare arrays with tolerance rather than assuming a serialized NPZ SHA must match across versions. No official validation/test evaluation is automatically launched by this training script.

## What is repeated

The fixed original question folds are included in `parents/folds.json`. They were generated by three-fold `StratifiedKFold(shuffle=True, random_state=20261029)`, stratifying on the number of correct candidates.

The answer-group features and four blocks are unchanged:

| Block | Dimensions | Original source |
|---|---:|---|
| A: group Embedding, support, dispersion, and numerical features | 1,034 | subset-augmented group anchor subset-augmented ranker |
| L: local arithmetic and late boxed-answer evidence | 26 | local-evidence residual final-evidence residual |
| I: signed 128-bucket question unigram/bigram hash × 32 evidence features | 4,096 | question–evidence interaction model question-both interaction |
| G: numerical grounding and final-equation ancestry | 24 | grounded-chain control both residual |

The exact original full-train and three fit-only parent centers contain each block's weights, means, and scales. A fold center was trained without that fold's held questions. The replay recomputes input features, reproduces each held parent score within `1e-10`, and uses the corresponding frozen fold center. No full-train scaler is substituted into a fold.

For each training question, all good-answer-group versus bad-answer-group pairs are built; if there are `m` such pairs, each has raw weight `1/m`. Normalizing by the number of informative questions makes each informative question's total weight equal. Questions with no good/bad comparison contribute no ranking pairs.

Both families use weighted logistic ranking loss plus `lambda / 2 * ||delta||^2`:

- **mix:** four offsets modify original module coefficients from `1` to `1 + delta`.
- **joint:** a 5,180-dimensional update is added to the original standardized block weights.

The six predeclared configurations are two families × lambda `{0.01, 0.1, 1}`. Each is fitted on the same three outer folds: **18 fits**. Within each family, select by highest train OOF correct count, then fewer newly introduced parent errors, fewer changed choices, and larger lambda. Fit each selected family on all official train questions: **2 more fits, 20 total**. Updates start at zero. L-BFGS-B options are `maxiter=1000`, `ftol=1e-12`, `gtol=1e-7`, `maxls=40`; successful convergence, finite parameters, and gradient infinity norm below `1e-5` are required.

The original six OOF results were:

| Family | Lambda | OOF correct / 4,755 |
|---|---:|---:|
| mix | 0.01 | 4,401 |
| mix | 0.1 | 4,405 |
| mix | 1 | **4,406** |
| joint | 0.01 | 4,383 |
| joint | 0.1 | 4,398 |
| joint | 1 | **4,406** |

These are development metrics after selecting hyperparameters on those OOF results, not an independent final estimate. Original full-source and result evidence is preserved in `provenance/` and `archive/`.

## Optional from-data reconstruction of the fixed parent chain

This wrapper was **numerically executed and verified on 30 October 2026**. It reconstructs the fixed chosen chain from the official training data, without using saved learned parent arrays in fitting. Comparisons to the saved centers are made only after the 25 fits. It stops if the arrays/OOF do not agree within `1e-8` and preserves the comparison report. This is verification in the existing pinned environment; a newly provisioned clean environment was not used.

**Tolerance distinction:** the optional rebuild's array and OOF comparison uses `rtol=atol=1e-8`. The proximal joint-update experiment replay preserves the original, stricter held-parent score check of `rtol=atol=1e-10`, including when a rebuilt bundle is supplied. Passing the rebuild's `1e-8` check therefore does not guarantee that replay will accept its held scores at `1e-10`. If the latter check fails, replay stops before fitting the affected fold and preserves any earlier completed fold records; report the discrepancy rather than describing it as successful reproduction. The exact saved-parent route retains the original `1e-10` check unchanged.

```sh
python -X utf8 training/rebuild_parent_centers.py --data-dir /path/to/official/code/data
python -X utf8 training/replay_round137.py --data-dir /path/to/official/code/data --parents-dir runs/reproduction/rebuilt-parents/parents --output runs/reproduction/round137-rebuilt
```

The parent reconstruction does **25 fixed fits**:

1. subset-augmented group anchor A uses original full-group means/scales and all nonempty same-answer subsets, lambda `0.01`: three outer fits and one full fit.
2. Nine additional A fits produce three inner OOF partitions inside each outer fit, with seeds `20261030 + outer_fold`.
3. local-evidence residual L uses the 26 original final-evidence features, lambda `0.1`: three outer fits use the nested A OOF margin; the full fit uses global A OOF margins.
4. question–evidence interaction model I uses lambda `0.1` and the corresponding same-fit frozen A+L margin: three outer fits and one full fit.
5. grounded-chain control G uses the fixed selected 24-feature both family, lambda `0.01`, and the corresponding same-fit frozen A+L+I margin: three outer fits and one full fit.

It regenerates fixed folds, fits all scalers on their appropriate training indices, and writes a new `parents/` bundle. Adding the 20-fit replay gives **45 fits for the fixed selected chain**. This reconstructs the chosen model recipe; it does not repeat every historic search, failed branch, source-integrity audit, or later human final-model choice.

## Archived original sources and provenance

Historical plan documents are bundled in `materials/research-records.zip`, under `training/archive/plans/`. Extract those before following the original-layout inspection instructions below.

`archive/source/` contains the complete local Python import closure (26 files) rooted at the original subset-augmented group anchor/109/110/120/123/137 training and relevant audit entries. These are preserved for inspection, with original SHA-256s in `provenance/manifest.json`. `source/` holds the 15-file inference feature closure and the exact copied replay math helpers. Code duplication preserves old source bytes and is intentional.

For inspecting original entry points in their original relative layout, copy `archive/source/*.py` into a **separate research workspace `code/`**, copy `archive/plans/` into that workspace's parent, and obtain official `code/data/`. Do not overwrite this release's frozen inference files. The old entry points still expect historical `runs/...` metadata, feature caches, parent artifacts, and hash manifests; **merely copying the files is not a turnkey historical rerun**. The portable replay and optional fixed-chain reconstruction avoid those historical path requirements.

`provenance/manifest.json` identifies the four original A/L/I/G source artifacts for each full/fold center, their original repository-relative paths and hashes, and the saved-center hashes. Published center sizes plus fixed folds and parent OOF total **583,695 bytes**. These are **training-only artifacts**. At inference, `method_round137_joint_retrain.py` reads only `config.json` and `parameters.npz` from the submitted checkpoint; parent artifacts, OOF arrays, and training code are not loaded.

Both portable entries cap numerical libraries at **four total CPU threads** and use a **600-second worker timeout**. The assignment's 16 MiB / 30-second constraints concern the frozen inference assets and complete official prediction-plus-scoring run; training logs and parents are not runtime dependencies.

