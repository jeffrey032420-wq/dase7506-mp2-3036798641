# DASE7506 MP2: Selecting Reliable LLM Reasoning

**Liang Zefeng · 3036798641**  
Frozen model: **proximal joint ranker** · 30 October 2026

[Report (PDF, 5 pages)](REPORT.pdf) · [Report source](REPORT.md) · [Training reproduction](training/TRAINING_REPRODUCE.md)

The model compares equivalent-answer groups using fixed supplied embeddings, support, local numerical evidence, question interactions and final-calculation ancestry. A conservative proximal update jointly adjusts 5,180 ranking weights. Inference uses NumPy and the standard library, with no API calls or LLM generation.

## Frozen result and limitations

| Record | Value |
|---|---:|
| Training 3-fold OOF, after lambda selection | 4,406 / 4,755 |
| Official validation | 752 / 798 = 94.23558897243107% |
| Official test | **395 / 467 = 84.58244111349036%** |
| All uncompressed additional inference assets | 62,449 bytes |
| Fresh complete local test prediction + separate scoring | 2.331497200008016 seconds |
| Local CPU / numerical threads | Intel Core i5-11400H / 4 total |

Official unchanged aggregate JSON: [`materials/validation-score.json`](materials/validation-score.json), [`materials/test-score.json`](materials/test-score.json). The limits are 30 seconds on the reference Xeon Platinum 8457C and 16 MiB of inference assets. The reported timing is measured locally; reference-machine assessment remains with the course evaluator.

## 1. Install and obtain the official data

Original environment: Python 3.12.14, NumPy 2.5.3. From this repository root:

```sh
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux instead: source .venv/bin/activate
python -m pip install -r materials/requirements-inference.txt
git clone https://github.com/xudongwu-0/DASE7506-MP2.git official-mp2
```

Keep the supplied official data, parser and scoring files unchanged. Data are not duplicated here. The evaluation commands require `official-mp2/code/data`, including its manifest, candidate inputs/representations and the appropriate split's scoring references. Prediction opens only the supplied inputs; the separate official scorer opens references.

## 2. Reproduce the frozen score without retraining

Run from this repository root:

```sh
python -X utf8 materials/evaluate_frozen.py --data-dir official-mp2/code/data --split test --output evaluation/test-reproduction
python -X utf8 materials/evaluate_frozen.py --data-dir official-mp2/code/data --split validation --output evaluation/validation-reproduction
```

Each invocation starts a fresh official prediction process and a separate official scoring process, serially. It sets numerical thread limits to four, checks the two checkpoint hashes and reports the combined wall time. It refuses to overwrite an existing output directory. The original records are preserved. A fresh reproduction on 30 October confirmed 395/467 test answers; complete frozen prediction plus independent scoring took 2.169209 seconds locally. See `materials/reproduction/summary.json`.

Equivalent direct commands, after setting `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS` and `BLIS_NUM_THREADS` to `4` in your shell:

```sh
python -X utf8 code/predict.py --method code/method_round137_joint_retrain.py --checkpoint code/checkpoint --data-dir official-mp2/code/data --split test --output evaluation/test-predictions.json
python -X utf8 code/score_predictions.py --split test --data-dir official-mp2/code/data --predictions evaluation/test-predictions.json --output evaluation/test-score.json
```

Both `code/checkpoint/config.json` and `code/checkpoint/parameters.npz` are required. No old parent checkpoint, training array, cached prediction or ID lookup is used during inference. 

## 3. Reproduce training

```sh
python -m pip install -r materials/requirements-train.txt
python -X utf8 training/replay_round137.py --data-dir official-mp2/code/data --reference-checkpoint code/checkpoint
```

This repeats the original **20-fit** proximal joint-update experiment comparison from the included exact full/fold **train-only parent centers**, recomputing supplied train features. Six fixed configurations use the original three-fold seed **20261029**; one lambda per family is selected by OOF before the two full fits. It does not launch validation/test evaluation or overwrite the frozen checkpoint.

For an optional reconstruction of the fixed parent chain directly from official training data:

```sh
python -X utf8 training/rebuild_parent_centers.py --data-dir official-mp2/code/data
python -X utf8 training/replay_round137.py --data-dir official-mp2/code/data --parents-dir runs/reproduction/rebuilt-parents/parents --output runs/reproduction/round137-rebuilt
```

This reference wrapper performs 25 fixed parent fits before the 20-fit replay. It does not repeat all historical searches. **Both routes were numerically executed on 30 October 2026.** The 20-fit saved-parent replay and the 45-fit from-data fixed-chain reconstruction both reproduce the frozen parameter arrays exactly (maximum absolute difference 0) and OOF 4,406/4,755. The reconstructed model reproduces validation 752/798 and test 395/467 using the unchanged official evaluator. This used the existing pinned local environment, rather than a newly provisioned clean environment. Evidence is in `materials/reproduction/`; detailed scope is in [`training/TRAINING_REPRODUCE.md`](training/TRAINING_REPRODUCE.md).

## 4. Repository layout and integrity

| Path | Contents |
|---|---|
| `REPORT.pdf`, `REPORT.md` | Final report and editable source |
| `code/` | Frozen inference implementation and complete checkpoint |
| `training/` | Training entries, saved parents and source provenance |
| `materials/` | Evaluation helper, pinned dependencies, official scores, disclosures, licenses and integrity manifest |

Final parameter SHA-256: `61ff97395a049186e4f2887043d9e1b0755414a0fe42e34a81bba1584010e8fa`. Config SHA-256: `041359516d344e57c53629a39aede6c30debb7d9aa97a2fdda690c8299b4fe41`.

Only `code/checkpoint/` is loaded as additional inference assets. Training parents and reports are not inference dependencies. The original 20-fit proximal joint-update worker took approximately 27.376 seconds; this excludes parent training, audits, evaluation and preceding searches.

The submitted code version is the Git commit at the linked repository URL; use an immutable `tree/<commit>` link for final submission. Use the checkpoint directory from that same commit. Any future documentation update must preserve this model's source/asset hashes.
