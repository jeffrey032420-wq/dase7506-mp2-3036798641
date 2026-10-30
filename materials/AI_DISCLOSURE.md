# AI assistance and responsibility

Author: Liang Zefeng, 3036798641.

OpenAI Codex provided substantive assistance with hypothesis formation, source inspection, implementation of features/losses/optimizers, execution and debugging of experiments, validation and test evaluation, result analysis, resource/hash checks, freezing, reproduction scripts, repository packaging, and English report drafting/typesetting. Multi-agent drafting and a separate evidence review were used for the final materials. AI use extended beyond code completion and language editing.

The author is responsible for reviewing, understanding and explaining the submitted implementation and conclusions. The chronological assistance record is retained in the historical assistance record in `research-records.zip`; statements there concern their dated development stages. The final selection disclosure below takes precedence for the final artifact.

The user selected proximal joint-update experiment joint after multiple official test aggregates were visible. Training and within-family lambda selection used training-only OOF, but final family/artifact selection was test informed. We do not claim independent test confirmation .

After the explicit final freeze, preparing the publication added documentation and portable reproduction wrappers, and performed static, hash and PDF layout checks only. It did not run new fitting, prediction or scoring, or modify the frozen inference source/checkpoint. The newly assembled training wrappers have not been numerically exercised after freezing; see `training/TRAINING_REPRODUCE.md`.
