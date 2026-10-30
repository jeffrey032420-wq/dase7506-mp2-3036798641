# Selecting Reliable LLM Answers with Group Ranking and Proximal Joint Updates

**DASE7506 Mini-project 2 · Final report**  
**Liang Zefeng · Student ID 3036798641**  
[Code repository](https://github.com/jeffrey032420-wq/dase7506-mp2-3036798641) · Frozen model: proximal joint ranker · 30 October 2026

## Abstract

This project selects one of four supplied language-model solutions. I investigate answer-group comparison, numerical evidence and coordinated training under a small CPU budget. The final selector groups equivalent answers and combines fixed embeddings, local arithmetic/final-answer evidence, question–evidence interactions and final-calculation ancestry. A proximal update adjusts 5,180 existing ranking weights, with regularization selected using training-only three-fold predictions. The frozen model obtains 752/798 validation answers and 395/467 official test answers (84.582441%). It requires 62,449 bytes of inference assets and 2.3315 seconds for complete local test prediction plus independent scoring. Validation is lower than the control's 754/798. Negative experiments explain why additional features and capacity did not reliably improve selection.

## 1. Task and research questions

The official data contain 4,755 training, 798 validation and 467 test questions, with four candidate texts and fixed 1,024-dimensional representations each. Every question has a correct candidate; multiple may be correct. Output is one candidate index. The unchanged scorer checks final numeric equivalence, not validity of every reasoning step.

**RQ1:** Does answer-group comparison use agreement and embeddings effectively? **RQ2:** Can numerical evidence improve selection without treating consistency as proof? **RQ3:** Does jointly adjusting sequentially added feature blocks improve their coordination?

The hypotheses were that grouping reduces redundant competition, numerical checks supply complementary evidence, and joint updating improves on frozen earlier weights. Alternatively, extra flexibility might damage more correct rankings than it repairs.

Fitting uses supplied training data only. Inference uses no external dataset, extra pretrained checkpoint, online generation, reference answers, ID lookup or cached predictions. Method sources, reuse acknowledgements and data licenses are listed in the repository appendix, `materials/ATTRIBUTION.md`.

## 2. Evaluation protocol and its limits

Evaluation uses the unmodified official parser, prediction runner and independent scorer. Historical methods share official splits, but early and later internal OOF diagnostics differ. The principal joint-update comparison shares three question-level folds.

These folds stratify by correct-candidate count with seed **20261029**. A question's candidates and subsets remain together. Each held fold uses its corresponding fit-only parent and statistics. Reconstructed parent held/full-training scores agree within 10⁻¹⁰.

Two families and three penalties were fixed before fitting. Six configurations received three outer fits; one winner per family received a full-training fit: **20 fits**. Selection used OOF correctness, then fewer new errors, fewer changed choices and larger regularization. Selected OOF accuracy is a development metric, not nested confirmation.

Both candidates and the control received validation. The development comparison retained the grounded-chain control; the two new candidates were frozen together and each evaluated once on test. This batch involved no test-case analysis or test-driven parameter changes.

Test aggregate scores were consulted in final model selection; the reported test accuracy is therefore descriptive performance on this bank, rather than an independent estimate.

## 3. Answer-group selector

### 3.1 Grouping and base representation

Candidates with the same officially parsed numeric answer form a group and receive exactly equal scores. Unparseable answers do not form a valid group. Prediction takes a highest-scoring candidate; reordered equivalent candidates can tie without changing the answer.

Block **A** has 1,034 dimensions: mean group embedding (1,024); support count/fraction, group count and embedding dispersion; and six numerical features. The latter encode sign, log magnitude, integer status, occurrence among question numbers, their count and relative magnitude. Statistics fit original complete groups in the relevant partition.

The original anchor trains on all nonempty group subsets: three supporting candidates yield seven. Each question retains equal total loss weight, preventing sample-count changes from changing effective regularization. The joint update retains this anchor as its center but updates complete groups only.

### 3.2 Numerical and question-conditioned blocks

Block **L** contains 26 bounded-arithmetic, formatting and final-answer features. Four describe conflicts with a later simple boxed conclusion and cross-candidate support. Unsupported expressions are unknown. All features are learned soft evidence, not rejection rules.

Block **I** interacts a fixed normalized 128-dimensional signed BLAKE2b question unigram/bigram hash with 32 evidence values: L plus six numerical features. Its matrix has 4,096 weights. Unlike a question-only additive term, which cancels within a question, this interaction changes evidence weights with wording. No external vocabulary is fitted.

Block **G** takes means/maxima of 12 numerical ancestry features. Extracted scalar equalities trace the final result through earlier calculations, describing question-value coverage, unknown leaves, reused results, false ancestors and unrelated equations. Strict grounding uses question numbers; relaxed grounding admits fixed common constants. Equal values need not identify the same entity, unit or time; this is numerical provenance, not semantic proof.

### 3.3 Proximal ranking objective

Let φ(q,g) concatenate the four blocks after their retained transformations, with the interaction flattened to 4,096 coordinates. The parent has weights θ₀ and score s₀(q,g). The final joint model uses

\[
s(q,g)=\phi(q,g)^\top(\theta_0+\delta),\qquad
1034+26+4096+24=5180.
\]

For each informative question q, form all correct–incorrect answer-group pairs Pq. With D the informative training questions, minimize

\[
\frac{1}{|D|}\sum_{q\in D}\frac{1}{|P_q|}
\sum_{(g^+,g^-)\in P_q}
\log\bigl(1+\exp[-(s(q,g^+)-s(q,g^-))]\bigr)
+\frac{\lambda}{2}\|\delta\|_2^2.
\]

Each question has equal total weight; questions without positive–negative pairs supply none. SciPy L-BFGS starts at zero update, retaining block scales and the parent center.

The **mix** comparison learns four offsets: s = Σb(1+db)sb, with penalty λ‖d‖²/2 on original block scores. Mix and joint therefore differ in regularization geometry as well as flexibility. Final joint regularization is **λ = 1**.

## 4. Experimental results

### 4.1 Development trajectory and key feature comparisons

Table 1 summarizes representative development results. The final method is not the highest-validation model.

| Method or stage | Validation correct /798 |
|---|---:|
| Initial independent correctness model | 723 |
| Contextual pairwise ranker | 744 |
| Selective arithmetic and final-answer transfer | 749 |
| Subset-augmented answer-group anchor | 746 |
| Local arithmetic and final-answer evidence | 751 |
| Question–evidence interaction | 752 |
| Numerical grounding and ancestry | **754** |
| Final proximal joint update | 752 |

Matched contextual-feature ablations, with fixed α=.3, obtained 722 with embeddings alone, 706 without embeddings, 734 without explicit agreement features and 744 with all features. They support complementary information in that earlier pipeline, not final-model block contributions.

The matched subset-augmentation comparison improves validation from 741 to 746 at λ=.01 and 739 to 746 at λ=.003, although OOF changes are −7 and +5. The local-evidence format-only, arithmetic-only, full and final-evidence variants obtain 746, 749, 751 and 751: four added final features yield no net gain. The grounded-chain grounding-only, ancestry-only and combined candidates obtain 752, 749 and 754 after training-only penalty selection. The combination repairs five validation errors of the question–evidence interaction model and introduces three.

### 4.2 Joint-update regularization comparison

Table 2 reports all configurations. “Repair/new” compares OOF outcomes with the grounded-chain control's 4,404 correct. Family-specific λ selection uses neither validation nor test.

| Family | λ | OOF /4755 | Repair/new | Fold net changes |
|---|---:|---:|---|---|
| mix | .01 | 4401 | 11/14 | −1, −2, 0 |
| mix | .1 | 4405 | 9/8 | −2, 0, +3 |
| **mix** | **1** | **4406** | **4/2** | **−1, +1, +2** |
| joint | .01 | 4383 | 31/52 | −4, −17, 0 |
| joint | .1 | 4398 | 17/23 | 0, −8, +2 |
| **joint** | **1** | **4406** | **9/7** | **−1, 0, +3** |

Both families select the strongest tested regularization. Joint λ=.01 repairs 31 but breaks 52. At λ=1, it repairs nine, breaks seven and changes 18 choices. Fold changes are not uniformly positive; objective convergence does not imply stable accuracy gains.

| Model | Train OOF /4755 | Validation /798 | Test /467 |
|---|---:|---:|---:|
| Grounded-chain control | 4404 | **754** | 390 |
| Module mixing, λ=1 | 4406 | 753 | 392 |
| **Final joint update, λ=1** | **4406** | **752** | **395** |

Final official accuracies are **94.235589% validation** and **84.582441% test**. Resubstitution is 4,519/4,755, distinct from OOF. Validation loses two correct answers without repairs. Test gains five versus the grounded-chain control and three versus the previous observed maximum, 392. No test-error explanation was attempted; these differences do not establish repeatable gains.

### 4.3 Negative results that changed the direction

| Experiment family | Representative validation /798 | Finding |
|---|---:|---|
| Linear / pointwise / DeepSets / attention | 746 / 729 / 733 / 735 | More expressive candidate interaction did not beat 751. |
| Raw attention, fixed / inner early stopping | 722 / 740 | Early stopping helped this network, but remained below the control. |
| PCA attention, fixed / early stopping | 735 / 734 | A 64-dimensional bottleneck did not resolve the deficit. |
| Quantity labels / role features / both | 753 / 754 / 752 | Lexical associations added ambiguous evidence. |
| Corrected quantity labels / both | 753 / 752 | Repairing an extractor inconsistency did not improve validation. |

The heterogeneous-expert comparison uses four architectures and two multi-correct objectives; its eight experts and two fixed ensembles remain below the incumbent. The early-stopping procedure chooses epochs inside each outer-fit partition before retraining, without validation-based stopping.

The initial quantity-label extractor incorrectly treats “gallons” and “gallons of gas” as conflicting. The corrected extractor makes strict prefixes unknown. Corrected labels reach 4,408 OOF, but among 121 changed-input questions repair one and break one relative to the initial quantity-label model. The net training increase arises elsewhere after refitting. This distinguishes extractor repair from accuracy improvement and motivates testing established-feature coordination.

## 5. What the results say about reliability

Validation mixes easy agreement and genuine selection: 355/798 questions have distinct answers, compared with all 467 test questions. Final validation performance is **309/355 (87.04%)** on disagreement and **78/117 (66.67%)** on single-correct questions; the grounded-chain control obtains 311 and 79. Overall validation and test accuracies therefore reflect different difficulty distributions. This does not explain why the joint update's changes have opposite directions across banks.

In the training audit preceding the grounded-chain control, relaxed complete true chains include **752 incorrect candidates among 3,904**: correct arithmetic can calculate the wrong quantity. Conversely, 149 of 161 candidates with a false final ancestor are wrong, yet the question–evidence parent model selects such a candidate in only one remaining error question. Global association need not provide remaining repair opportunity.

Older experts show complementarity and switching risk: attention repairs 100 parent OOF errors but loses 213 previously correct questions. A truth-based expert oracle could cover 214/351 remaining errors. This unavailable upper bound is not a deployable ensemble result.

Repairs, new errors, folds and strata must be examined together. Larger models and higher training scores did not provide a reliable shortcut. Final score margins have not been calibrated as correctness probabilities.

## 6. Resource use and reproduction

Local execution used Windows, **Intel Core i5-11400H @ 2.70 GHz**, Python 3.12.14 and NumPy 2.5.3. Training uses SciPy 1.18.1, scikit-learn 1.9.1 and threadpoolctl 3.7.0; historical neural experiments used PyTorch 2.14.1+cpu. Final inference requires NumPy/standard library only. Numerical workloads were serialized with four threads.

The final checkpoint includes all learned weights, transformations/statistics and configuration: **62,449 uncompressed bytes**, approximately 0.0596 MiB against the 16 MiB limit. It independently exports the four blocks; old parent checkpoints are unnecessary for inference. A fresh complete official test prediction process followed by a separate scoring process took **2.3314972 seconds**, including startup, imports, loading and preprocessing. This is below 30 seconds locally. Timing on the required **Xeon Platinum 8457C** has not been measured.

The joint-update comparison's 20 fits took **27.376 seconds** in its training worker; audit, evaluation, parent construction and previous searches are additional costs, not included in that number. The repository appendix retains their separate records rather than claiming an end-to-end project training time.

The repository provides exact installation/evaluation commands, training-only full/fold parent centers for final-stage training replay, and historical training sources. This supports final-stage replay; it does not claim one-command reconstruction of the entire historical search. Prediction uses `method_round137_joint_retrain.py`, the frozen checkpoint and independent `score_predictions.py`. Hashes, seeds and official JSON accompany the artifact. Parameter-file SHA-256: `61ff97395a049186e4f2887043d9e1b0755414a0fe42e34a81bba1584010e8fa`.

## 7. Limitations and conclusion

The project followed a long adaptive development path on reused training folds and validation data. Predeclaring individual batches does not make the whole search preregistered. A separate unseen audit bank is needed to assess generalization; no statistical significance or causal improvement is claimed here.

The final update also retains an adaptively developed parent and its scaling geometry. Same-fit parent margins used in updating are optimistic within training, despite properly excluded outer-held questions. The final method did not rebuild a fully nested parent-selection procedure. Comparisons of different feature blocks, penalties and architectures consequently have the stated local scope. Bounded parsers miss unsupported expressions and cannot resolve full entity, unit or temporal semantics. Correct final-answer selection is a narrower outcome than reliable reasoning.

The frozen artifact reproduces **395/467** on the official test bank within a small local resource budget. Answer-group ranking, soft numerical evidence and conservative joint adjustment form a compact implementation. The experiments' strongest methodological finding is the need to preserve correct decisions while adding evidence: many plausible changes merely exchanged errors. The final test improvement and validation regression are both retained in the comparison.

## 8. AI assistance

OpenAI Codex substantially assisted experimental planning, feature and loss implementation, execution, debugging, analysis, integrity/resource checks, packaging and report drafting. The author is responsible for understanding and reviewing the submission. Detailed assistance records accompany the repository. No additional pretrained model or outside training questions were imported.
