# AI assistance and responsibility

Author: Liang Zefeng, 3036798641.

OpenAI Codex provided substantive assistance with hypothesis formation, source inspection, implementation of features/losses/optimizers, execution and debugging of experiments, validation and test evaluation, result analysis, resource/hash checks, freezing, reproduction scripts, repository packaging, and English report drafting/typesetting. Multi-agent drafting and a separate evidence review were used for the final materials. AI use extended beyond code completion and language editing.

The author is responsible for reviewing, understanding and explaining the submitted implementation and conclusions.

After the explicit final freeze, publication work added documentation and portable reproduction wrappers, with static, hash and PDF layout checks. Numerical verification on 30 October 2026 then reproduced both the saved-parent training route and the fixed-chain reconstruction from official training data. Both reproduce the frozen parameter arrays exactly; the reconstructed model reproduces validation 752/798 and test 395/467. The submitted inference source and checkpoint were not modified. See `../training/TRAINING_REPRODUCE.md` and `reproduction/summary.json`.
