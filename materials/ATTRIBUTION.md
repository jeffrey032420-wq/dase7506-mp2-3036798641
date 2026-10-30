# Reuse and attribution

- The official DASE7506 MP2 numeric parser, data interface, predictor and independent scorer are retained byte for byte in `code/`. Official source: https://github.com/xudongwu-0/DASE7506-MP2 . The original evaluator protocol is `dase7506-mp2-open-hard-verifier-v5`.
- Supplied questions/references derive from OpenAI GSM8K under its MIT license. The supplied candidate traces and fixed embeddings were prepared using Qwen3-0.6B, revision `c1899de289a04d12100db370d81485cdf75e47ca`. No Qwen model weights are included. Original notices are retained in `attribution/`.
- CaspianW's answer-group and training implementations informed same-answer subset augmentation and per-question/sample-count-invariant regularization: https://github.com/CaspianW/dase7506-mp2 .
- Bosco-lab's multi-correct training objective informed objective comparisons: https://github.com/Bosco-lab/DASE7506_MP2 .
- michaelleeoo's group/stack implementation informed heterogeneous expert comparisons: https://github.com/michaelleeoo/DASE7506-MP2 .
- Set Transformer and allRank sources were inspected to understand attention and ranking objectives. They were not imported as training dependencies. Inspected source URLs and Git blob hashes are recorded in `records/GITHUB_METHOD_SOURCES_2026-10-28.json`.

These methodological ideas were implemented locally. Peer self-reported scores were visible in inspected public READMEs; they were not independently reproduced. No external training questions or pretrained weights were downloaded for this method. The report states the scope of each comparison. AI assistance is separately disclosed in `AI_DISCLOSURE.md`.

Historical training source is intentionally duplicated in `training/archive/source/` to preserve the original SHA values. Those sources and the official tools retain their existing notices. This repository does not assign a new license to third-party material.


## Sources accompanying the report

Answer-group subset augmentation and sample-count-invariant regularization were informed by CaspianW's public implementation [2]; multi-correct objectives by Bosco-lab [3]; and heterogeneous experts by michaelleeoo [4]. These ideas were independently implemented. Public source inspection and self-reported aggregate scores are not independent reproductions. The source inventory records inspected URLs and blob hashes. Supplied questions derive from GSM8K, and supplied candidates/representations were prepared with Qwen3-0.6B; retained notices and licenses accompany the submission [1].

[1] DASE7506 MP2. [Project guide](https://github.com/xudongwu-0/DASE7506-MP2/blob/main/guide/GUIDE.md) and [running instructions](https://github.com/xudongwu-0/DASE7506-MP2/blob/main/code/README.md). Dataset attribution: [GSM8K](https://github.com/openai/grade-school-math) and [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B).

[2] CaspianW. [Answer groups](https://github.com/CaspianW/dase7506-mp2/blob/main/src/submission_answer_groups.py) and [training implementation](https://github.com/CaspianW/dase7506-mp2/blob/main/src/train.py). Static source inspection recorded 28 October 2026.

[3] Bosco-lab. [Training ranker](https://github.com/Bosco-lab/DASE7506_MP2/blob/main/code/train_ranker.py). Static source inspection recorded 28 October 2026.

[4] michaelleeoo. [Heterogeneous group/stack implementation](https://github.com/michaelleeoo/DASE7506-MP2/blob/main/code/stack_v2.py). Static source inspection recorded 28 October 2026.

**Local evidence:** `ROUND108_RESULTS.md`, `ROUND110_RESULTS.md`, `ROUND112_RESULTS.md`, `ROUND113_RESULTS.md`, `ROUND120_RESULTS.md`, `ROUND123_RESULTS.md`, `ROUND135_136_SUMMARY.md`, `ROUND137_LEARNING.md`, `FINAL_MODEL_FROZEN.json` and the corresponding official aggregate JSON. These are experimental records, not additional independent studies.
