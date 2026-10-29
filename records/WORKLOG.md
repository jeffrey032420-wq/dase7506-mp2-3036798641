# Development log

## 2026-10-28 Round105

两个旧系数组件输出最高747/798，未超过749/798（93.8596%），保留Round79。 两项零拟合旧系数组件消融完成；103–105共12输出，混合TRAIN与验证负结果均保留。组件归因只作开发解释，不把修复数或回代变化称突破。详见[ROUND105_RESULTS.md](ROUND105_RESULTS.md)。无新OOF、无测试使用；原交付快照保持。

## 2026-10-28 Round104

四个固定输出最高748/798，未超过749/798（93.8596%），保留Round79。 固定旧语义权重，2项数值组件消融+2项残差拟合；原权重精确冻结、全部控制与负结果见[ROUND104_RESULTS.md](ROUND104_RESULTS.md)。无新OOF、无测试使用。

## 2026-10-28 Round103

六个固定新输出最高748/798，未超过749/798（93.8596%），保留Round79。 既有numeric14/answer_context386在semantic分支联合分块正则，TRAIN预检覆盖267/316/316；六个固定输出与全部控制见[ROUND103_RESULTS.md](ROUND103_RESULTS.md)。没有新OOF或测试使用。

## 2026-10-27 Round102

验证最高749/798；当前最优749/798。未晋级，保留原模型。 两个无新拟合的严格格式对照；TRAIN覆盖与全部负结果见[ROUND102_RESULTS.md](ROUND102_RESULTS.md)。没有新OOF或测试使用。

## rounds99–101 completed (2026-10-27)

全部12个新输出均未超过749/798（93.8596%），保留Round79。 Three finite routes: local reference-step supervision, supervised/random second-moment axes, question-conditioned pair comparison; twelve fixed outputs. Train-only/descriptive resubstitution/no new OOF. Fixed79 and dynamic Round79/749 checked separately. Sources/assets through98, first-attempt failures and historical delivery snapshots preserved. See [ROUND99_101_RESULTS.md](ROUND99_101_RESULTS.md). No test or submission.

## rounds97–98 completed (2026-10-27)

全部10个新输出均未超过749/798（93.8596%），保留Round79。 Four frozen cosine-geometry and six diagonal-coordinate quadratic joint-ridge fits. Train-only/descriptive resubstitution/no new OOF. Fixed79 and dynamic Round79/749 audited separately. Sources/assets through96 and historical delivery snapshots preserved. See [ROUND97_98_RESULTS.md](ROUND97_98_RESULTS.md). No test or submission.

## round96 completed (2026-10-27)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four predeclared near/far×γ1/3 train-reference distance pair-weighted ridge fits, unit margin/equal question total weight. Train references supervise only training; inference unchanged/no references/no OOF. Fixed79 and dynamic Round79/749 checked separately. Sources/assets through95 and historical delivery snapshots preserved. See [ROUND96_RESULTS.md](ROUND96_RESULTS.md). No test or submission.

## round95 completed (2026-10-27)

全部6个新输出均未超过749/798（93.8596%），保留Round79。 Six fixed exact pair-Gram class-covariance ablations, train-only; no trace renormalization/no new OOF. Fixed79 and dynamic Round79/749 checked separately. All sources/assets through94 and historical delivery snapshots preserved. See [ROUND95_RESULTS.md](ROUND95_RESULTS.md). No test or submission.

## round94 completed (2026-10-27)

全部8个新输出均未超过749/798（93.8596%），保留Round79。 All4 frozen Round92 sources × strengths.1/.25,8 outputs; zero new fits/no new OOF. Adaptive follow-up from92 aggregate disclosed; no source filtering by scores. Fixed79 and dynamic Round79/749 checked separately. Sources/assets through93 and delivery snapshots preserved. See [ROUND94_RESULTS.md](ROUND94_RESULTS.md). No test or submission.

## round93 completed (2026-10-27)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four train-only original-quadratic-plus-all-candidate-BCE configs, free training intercept; 0 convergence failures,4 official validation outputs. Fixed training anchor79 and dynamic referenceRound79/749 checked separately. No new OOF; historical sources/assets through92 and delivery snapshots preserved. See [ROUND93_RESULTS.md](ROUND93_RESULTS.md). No test or public submission.

## round92 completed (2026-10-27)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four train-only learned low-rank embedding residuals (rank8/16 × λ.001/.01),40 fixed epochs. No new OOF; train resubstitution is descriptive. Historical sources/assets including89–91 and delivery snapshots preserved. See [ROUND92_RESULTS.md](ROUND92_RESULTS.md). No test or public submission.

## rounds89–91 completed (2026-10-27)

全部14个新输出均未超过749/798（93.8596%），保留Round79。 Three finite train-only semantic routes:6 block penalties,4 anchored objectives,4 query-variance metrics. 0 fixed convergence failures;14 official validation outputs. No new OOF; fulltrain values are resubstitution only. Sources/assets/history through88 and earlier delivery snapshots preserved. See [ROUND89_91_RESULTS.md](ROUND89_91_RESULTS.md). No test or submission actions.

## round88 completed (2026-10-26)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four fixed semantic coefficient averages, zero new fits/no OOF. Rounds86–88 total14 new validation outputs; finite scope complete, move to final materials. All histories/assets/audits passed. See [ROUND88_RESULTS.md](ROUND88_RESULTS.md). No test access.

## rounds86–87 completed (2026-10-26)

全部10个新输出均未超过749/798（93.8596%），保留Round79。 Six fixed semantic capacity settings and4 question-weighted semantic fits, train only/no new OOF; numeric1 and all protections fixed. All histories/assets/audits passed. See [ROUND86_87_RESULTS.md](ROUND86_87_RESULTS.md). No test access.

## round85 completed (2026-10-26)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four old full-numeric feature/stronger-ridge combinations with complete protections; no new OOF. Rounds81–85 total23 new validation outputs. All histories/assets/audits passed. See [ROUND85_RESULTS.md](ROUND85_RESULTS.md). No test access.

## round84 completed (2026-10-26)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four fixed convex numeric coefficient averages, zero new fits/no OOF. Explicit adaptive follow-up from aggregate Round83; source heads train-fitted only. Full audits/history hashes passed. See [ROUND84_RESULTS.md](ROUND84_RESULTS.md). No test access.

## round83 completed (2026-10-26)

全部4个新输出均未超过749/798（93.8596%），保留Round79。 Four fixed nongated fitting weights0/.1/.25/.5 compared with current r=1. All candidates trained only on train; no new OOF and no screening by resubstitution. Official/resource/interface audits passed. Historical sources/assets preserved. See [ROUND83_RESULTS.md](ROUND83_RESULTS.md). No test access.

## rounds81–82 completed (2026-10-26)

全部11个新输出均未超过749/798（93.8596%），保留Round79。 Numeric ridge7 outputs and arithmetic-subgroup penalty4 outputs were fixed before validation and officially audited against current749. All training used train only; Round82 fixed three-fold diagnostics did not select validation admission. Adaptive validation reuse disclosed. Historical sources/assets preserved. See [ROUND81_82_RESULTS.md](ROUND81_82_RESULTS.md). No test access.

## rounds79–80 completed (2026-10-25)

晋级Round79：验证749/798（93.8596%），较原748净增1题。 Complete protected semantic/numeric ridge grid17 outputs and local projection8 outputs were fixed before validation and officially audited. No new OOF; adaptive validation-development selection. All assets/time/interface checks passed; original sources/assets preserved. See [ROUND79_80_RESULTS.md](ROUND79_80_RESULTS.md). No test access.

## round77-78 completed (2026-10-25)

Codex and subagents audited support-dependent confidence loss, implemented strict nested two-action gates and two-parameter calibration, completed48expert/6gate/7calibration fits, and officially audited1frozen output. Validation746,8repairs/10new errors;best748retained. All failures preserved, no test access. See [ROUND77_78_RESULTS.md](ROUND77_78_RESULTS.md).

## round76 completed (2026-10-25)

本批没有超过748/798（93.7343%），保留Round11。 3train configurations; 3frozen outputs officially/resource/interface audited. See [ROUND76_RESULTS.md](ROUND76_RESULTS.md). No test access.

## round72-75 completed (2026-10-25)

Codex and delegated agents implemented four independent train-only routes,30held-screen records,42classifier fits plus3PCA. All failed fixed gates;no new validation/test or promotion. PyTorchCPU installed from official source, no pretrained weights/data. See [ROUND72_75_RESULTS.md](ROUND72_75_RESULTS.md).

## round71 completed (2026-10-24)

本批没有超过748/798（93.7343%），保留Round11。 1train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND71_RESULTS.md](ROUND71_RESULTS.md). No test access.

## round70 completed (2026-10-24)

本批没有超过748/798（93.7343%），保留Round11。 4train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND70_RESULTS.md](ROUND70_RESULTS.md). No test access.

## round68-69 completed (2026-10-24)

本批没有超过748/798（93.7343%），保留Round11。 10train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND68_69_RESULTS.md](ROUND68_69_RESULTS.md). No test access.

## round66-67 completed (2026-10-22)

Codex implemented question-only role-aligned symbolic transfer and supervised complete-program classification, with6fixed evaluation records and8classifier fold fits. Both failed train gates. No new validation/test or inference export;best748. See [ROUND66_67_RESULTS.md](ROUND66_67_RESULTS.md).

## round64-65 completed (2026-10-22)

Codex implemented disputed-clause extraction and matched sparse models, repaired numeric-signature plan mismatch before any validation, preserved both runs, and ran fresh train internal controls. OOF4324 tied cross/control; internal864 vsoldtail866, rejected. No new validation/test. Best748. See [ROUND64_65_RESULTS.md](ROUND64_65_RESULTS.md).

## round63 completed (2026-10-22)

本批没有超过748/798（93.7343%），保留Round11。 1train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND63_RESULTS.md](ROUND63_RESULTS.md). No test access.

## round62 completed (2026-10-22)

本批没有超过748/798（93.7343%），保留Round11。 6train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND62_RESULTS.md](ROUND62_RESULTS.md). No test access.

## round61 completed (2026-10-22)

Five frozen rule ablations; original4311, unitguard4313, period/combined4314 (one known fix, no new errors). No new validation/test. Best748/798. See [ROUND61_RESULTS.md](ROUND61_RESULTS.md).

## round58-60 completed (2026-10-22)

9configuration evaluation records,12fold-head fits; all rejected by frozen train gates. No new validation/test loaded. Best remains Round11=748/798. See [ROUND58_60_RESULTS.md](ROUND58_60_RESULTS.md).

## round48-57 completed (2026-10-22)

本批没有超过748/798（93.7343%），保留Round11。 23train configurations; 5frozen outputs officially/resource/interface audited. See [ROUND48_57_RESULTS.md](ROUND48_57_RESULTS.md). No test access.

## round44-47 completed (2026-10-22)

本批没有超过748/798（93.7343%），保留Round11。 14train configurations; 3frozen outputs officially/resource/interface audited. See [ROUND44_47_RESULTS.md](ROUND44_47_RESULTS.md). No test access.

## round41-43 completed (2026-10-21)

本批没有超过748/798（93.7343%），保留Round11。 8train configurations; 3frozen outputs officially/resource/interface audited. See [ROUND41_43_RESULTS.md](ROUND41_43_RESULTS.md). No test access.

## round37-40 completed (2026-10-21)

本批没有超过748/798（93.7343%），保留Round11。 30train configurations; 2frozen outputs officially/resource/interface audited. See [ROUND37_40_RESULTS.md](ROUND37_40_RESULTS.md). No test access.

## round33-36 completed (2026-10-21)

本批没有超过748/798（93.7343%），保留Round11。 41train configurations; 3frozen outputs officially/resource/interface audited. See [ROUND33_36_RESULTS.md](ROUND33_36_RESULTS.md). No test access.

## round30-32 completed (2026-10-21)

本批没有超过748/798（93.7343%），保留Round11。 21train configurations; 1frozen outputs officially/resource/interface audited. See [ROUND30_32_RESULTS.md](ROUND30_32_RESULTS.md). No test access.

## round26-29 completed (2026-10-21)

本批没有超过748/798（93.7343%），保留Round11。 17train configurations; 3frozen outputs officially/resource/interface audited. See [ROUND26_29_RESULTS.md](ROUND26_29_RESULTS.md). No test access.

## Rounds23–25 completed (2026-10-21)

Sixteen fixed train configurations: question-only program compatibility4321,
symmetric neural4344, randomized forest4321. Central validation747/743/743,
no promotion; retain748. All three official/resource/interface audits passed.
Independent audit found and archived float32 permutation failure; precision-only
repair keeps neural weights/config/OOF and all train choices unchanged. Complete
NPZ-expanded assets are counted. See ROUND23_25_RESULTS.md; no test access.

## Rounds20–22 completed (2026-10-21)

See [ROUND20_22_RESULTS.md](ROUND20_22_RESULTS.md). Eight correct-set/pairwise
loss configurations, ten structure-deletion configurations, six centered-PCA
neighbor configurations completed. Set-loss winner4322 validated748 (1fix/1new),
2.287sec; incumbent retained. Removing380cue/interaction dims ties full4335,
so no new validation; neighbor4314 gains in only one fold, not eligible.
All24training records and failures preserved. No test access. Rounds23–25 are
separate bounded train-only experiments, not yet claimed to improve accuracy.

## Rounds16–19 completed (2026-10-21)

See [ROUND16_19_RESULTS.md](ROUND16_19_RESULTS.md). Trained reference-operation
classifier, linear/bilinear residuals (including preserved collapse and active
repair), deterministic structured binary/ranking trees and frozen two-family
fusion. 67 OOF configuration records, seven frozen central validation outputs.
Highest OOF4359 did not transfer: operation748; linear747; collapsed747; active747;
binary744; LambdaRank741; fusion748. Retain Round11 at748/798. All seven official,
interface and local resource audits passed; maximum total8.945seconds. No test
access. Rounds20–22 separately planned and running: set losses, feature ablation,
and local centered-embedding neighbors. Failures and next actions preserved.

## Round15 completed: percentage parity and cumulative ablation

See [ROUND15_RESULTS.md](ROUND15_RESULTS.md), [main plan](ROUND15_PLAN.md),
and [debt amendment](ROUND15_AMENDMENT.md). Compared six percentage-factor graph
configurations, six explicit percentage-relation rules and two debt-omission
rules. Percentage parity changed21question features, but standalone best remained
4314(+1fix/0new). The142checked percentage relations were all locally correct,
so their six outputs made no changes. A scoped debt rule repaired train14 only;
both debt configurations stayed below the two-fix qualification gate.

The preplanned cumulative method combined prior algebra/discount corrections and
the frozen selected graph. Training OOF4319 fixes6/no new vs4313; without-graph
control4318 fixes5/no new, attributing one extra correction to the graph. Three
outputs including the incumbent passed official resource/interface audits. Both
new outputs scored748/798; the cumulative method changed two correct candidates
to other correct candidates. Round11 is retained. Largest assets1,678,384bytes,
longest local prediction-plus-scoring3.058sec. Reference-CPU eligibility pending.

After frozen results, train-reference inspection found4696/4755structured
intermediate computations. A separate Round16 train-only probe was launched to
learn question final-operation targets from this permitted supervision; its
outcome must be reported independently. No test inputs/references/scores used.

## Round14 completed: sufficiency gates, role audit and exact-chain repair

See [ROUND14_RESULTS.md](ROUND14_RESULTS.md), [main plan](ROUND14_PLAN.md),
and the [adaptive chain amendment](ROUND14_AMENDMENT.md). Stratified341 unknown
wrong OOF graphs:151 fail the minimum-three-input prerequisite,91 have no
supported correct arithmetic records,56 have no path to the official final,
40 have one supporting node,3 have an unparsed official answer. This prevents
attributing all unknowns to parser failure.

Nine sufficiency/legacy configurations stayed4313. Correct-selection penalties
fell53→7, but all9potential corrections were lost. Three closed-age-role modes
also stayed4313; only1question was recognized and already correct. Audit clarified
that row87already tracks the shared10-year offset: its multiplier4 was missing
because of a chained equality, correcting the prior incomplete diagnosis.

An explicitly planned follow-up compared six legacy/repaired-chain configurations.
Retaining exact numerical-expression RHS edges repaired one real omission error
(2669,rent/electricity280,1152→872), reaching4314 with no new errors. This remains
below the predeclared two-fix gate, so no validation was reopened. Round11 remains
best at748/798. Correct-selection penalties rose53→61 after chain recovery, so
format/role ambiguity remains. All cases, first-run gate-regex repair and lessons
were retained. The next proposed experiment tests ordinary/escaped percentages
and decimal-factor provenance parity under a fixed small grid. Integrity passed;
no validation/test inputs, scores or new reference-CPU eligibility claim this round.

## Round 13 completed: unit provenance repair and experiment-learning workflow

See [ROUND13_RESULTS.md](ROUND13_RESULTS.md), [main plan](ROUND13_PLAN.md),
[dependency plan](ROUND13_DEPENDENCY_PLAN.md), and the new persistent
[EXPERIMENT_LEARNING.md](EXPERIMENT_LEARNING.md). All experiment families now
leave evidence, failure mechanism, a next hypothesis, minimal ablation and stop
criteria; `runs/round13/lessons.json` and `next-experiment.json` make this concrete.

Compared six literal/unit-alias dependency configurations and eleven explicit
unit-evidence configurations. Aliases corrected the prior cents-to-dollars false
penalty, recovering4313/4755 from4312, but fixed no additional old errors. The
initial explicit-unit parser's apparent one-question gain depended on truncating
compound durations; after repairing the boundary, no choices changed. Initial
method and result snapshots are retained. Neither branch qualified, so validation
was not reopened and the Round11 best remains748/798.

Actionability audit: among442 wrong OOF selections, only10 are penalized by the
repaired dependency graph;9 have lower-penalty correct alternatives (6 graph-known
and complete), while53 correct selections are penalized.341 wrong selections have
unknown graphs, for multiple possible prerequisite/extraction reasons. This
motivates separating extraction sufficiency, irrelevant/canceling quantities and
actual omissions. All20 strength1 changes were manually reviewed (19 correct→
correct,1 wrong→wrong). Integrity passed. No new inference eligibility benchmark
was run because no model qualified; no validation/test inputs or scores were read.

## Round 12 completed: algebra, question relations and dependency evidence

See [ROUND12_RESULTS.md](ROUND12_RESULTS.md) and its linked plans. Train-only
branches compared 12 final-format configurations, 8 algebra/terminal-structure
rules, 4 strict discount relations and 3 numeric-dependency penalties. Format
extensions added no corrections. A frozen algebra penalty fixed 3 OOF errors;
discount relations fixed 2, with no new OOF errors. Their predetermined composition
reached 4,318/4,755 from 4,313. Neither individual rule nor the composition changed
validation choices: all remained 748/798. Four complete outputs including the
incumbent passed official local scoring/resource/interface checks. Round11 remains
selected and all previous source/asset hashes are preserved.

The dependency branch was rejected on training OOF (0 fixes, 1 new error at each
of three strengths). A correct cents-to-dollars conversion lost its literal input
in the graph, while a wrong unit-mixing computation appeared fully covered. This
motivates representing quantities with units before trusting dependency coverage;
that hypothesis has not yet been implemented or validated. A list-marker parsing
defect was fixed before structure freeze, and a constructed percentage example's
unsupported wording was corrected without extending the frozen parser. All
negative results and training audits remain available. No test inputs, labels or
scores were accessed; reference-CPU eligibility remains pending.

## Round 11 promoted: explicit final-answer/parser consistency, 748/798

See [ROUND11_RESULTS.md](ROUND11_RESULTS.md) and [plan](ROUND11_PLAN.md).
Training error inspection identified an actionable mismatch: intermediate ####
headings can make the official parser select a number different from the final
boxed conclusion. The new transfer rule chooses another existing candidate whose
official parsed answer matches the high-ranked candidate's explicit conclusion.
The supplied parser, scoring, data and all prior models remain unchanged.

Twelve training-OOF configurations covered transfer, clean-recipient transfer,
penalties and evidence voting. Four frozen family outputs all reached 748/798
validation (93.7343%), fixing one old error without new errors. The first transfer
rule is selected; its OOF improves from 4,310 to 4,313 with three fixes and no new
errors. It preserves the incumbent whenever no matching recipient exists.

Method: `code/method_round11.py`; assets:
`code/runs/round11/candidates/transfer/`. Total 1,678,154 bytes; official fresh local
validation prediction plus scoring 1.536 seconds. All five official audits and
constructed boundary/transfer checks passed. CURRENT_BEST.json now points to round
11. This is a small scoring-answer consistency gain, not a claim of improved
general reasoning. Repeated validation selection and narrow coverage are disclosed.
No test inputs, labels or scores were used; reference-CPU eligibility is pending.

## Round 10 completed: seven method families; round 7 retained

See [ROUND10_RESULTS.md](ROUND10_RESULTS.md), [main plan](ROUND10_PLAN.md),
[nested stacking amendment](ROUND10_AMENDMENT.md) and
[domain-rule amendment](ROUND10_DOMAIN_AMENDMENT.md).
Compared relative angular embeddings, extrema-based rival interactions, expected
feature-dropout regularization, and marginal correct-set likelihood. The main
search contained 54 fold records and 90 OOF options. A follow-up trained linear
and LightGBM meta selectors using nested cross-fitting (9 inner fitting groups),
with 15 outer fold records and 25 blend options. Four domain-rule configurations
were screened on training OOF; only the percentage rule qualified for validation.

Best selected OOF was 4,326/4,755, but angular fusion and tree stacking each scored
741/798 validation. The domain rule fixed two OOF errors with no new errors, yet
did not change validation choices. None exceeded the unchanged round 7 at 747/798.
Fourteen final outputs passed official local scoring, resource and interface
checks. Largest assets: 5,191,510 bytes; longest fresh prediction plus scoring:
6.396 seconds. Final reference-CPU eligibility remains unmeasured.

One synthetic pair-count assertion was corrected before training. Domain inference
initially also suppressed unparseable candidates; it was corrected to suppress
only confirmed violations, and the unchanged OOF/validation results were rerun.
Pre-audit results are retained. Nested base hyperparameters had already been
selected on full-training OOF, so residual selection bias is disclosed. No test
data, scores, external training data or pretrained weights were used.

## Round 9 completed: question alignment, conditioned embeddings and consensus

See [ROUND9_RESULTS.md](ROUND9_RESULTS.md), [plan](ROUND9_PLAN.md), and
[adaptive amendment](ROUND9_AMENDMENT.md). Four feature families generated 48
fold records and 64 training-OOF blend options; eight consensus conditions were
then compared using frozen heads. Eleven outputs including the incumbent were
officially scored and passed local resource/interface checks. Training vocabulary,
IDF, projections and scaling were fitted inside each training fold.

Best selected OOF improved from 4,310 to 4,320/4,755, but the corresponding
validation result was 746/798 (one fixed error, two new errors). Two- and three-head
consensus scored 746 and 745. Pure alignment-only-head selection scored 717;
this ablation removes embedding from the new head only, not the incumbent gate.
Shared errors include omitted tax and reversed subtraction despite high numeric
and unit overlap. These are descriptive development findings, not independent
generalization evidence. All negative results are retained.

CURRENT_BEST.json still selects unchanged round 7 at 747/798. Maximum audited
asset size was 4.252 MiB and maximum local fresh prediction-plus-scoring time was
5.017 seconds. Reference-CPU test eligibility remains unmeasured. No test data,
test labels, test scores, external datasets or pretrained weights were used.

## Round 8 completed: evidence adjustments and formatting; round 7 retained

See [ROUND8_RESULTS.md](ROUND8_RESULTS.md), [plan](ROUND8_PLAN.md), and
[amendment](ROUND8_AMENDMENT.md). Compared 57 training-OOF configurations for
candidate/group penalties, exact arithmetic repair support and selective gates;
froze one per family before validation. Added bounded numeric formatting support,
then repaired list-marker/currency/percentage ambiguities found in training cases.
Each formatting version used three training folds and three alphas (18 fold
records total). Ten frozen outputs, including the incumbent, were officially
reproduced and passed resource/interface checks.

No candidate exceeded 747/798 validation. Repair support reached 4,315 training
OOF correct but did not change validation choices. Formatting v1 reached 4,319
OOF, but contained identified extraction defects; its repaired v2 selected model
reached 4,314 OOF and only 745 validation. The incremental v2 scored 746 validation.
Both versions and all failures are retained. CURRENT_BEST.json still points to
the untouched round 7 checkpoint. No test inputs/references or test scores were used.

## Round 7 completed: controlled ablations and arithmetic-conflict gate

See [ROUND7_RESULTS.md](ROUND7_RESULTS.md), the initial [plan](ROUND7_PLAN.md),
and the adaptive [amendments](ROUND7_AMENDMENT.md). Ran 36 controlled ablations
across ranking objectives, embedding/context, numerical consistency and answer
agreement. Two arithmetic-boundary repairs added 18 configurations; two fixed
question-level gates brought the total to 56 validation configurations.
All intermediate failures, checkpoints and scores remain available.

The selected strict_core gate uses the numerical ranker only when a candidate
contains an explicit arithmetic conflict, and the round 2 baseline otherwise.
Official validation improved from 744/798 to **747/798 (93.6090%)**, fixing three
old errors without new validation errors. Frozen question-level training CV
improved from 4,300/4,755 to 4,310/4,755 (+2, +6, +2 across folds), with no retuning.
The gate was proposed after validation subgroup analysis, so these are development
results with selection bias, not independent generalization estimates.

Current method: `code/method_round7_gated.py`; checkpoint:
`code/runs/round7-gated/model_bundle/`. Assets total 1,678,126 bytes; fresh local
validation prediction plus independent scoring took 2.040 seconds, four threads.
Reference-CPU complete-test eligibility remains unmeasured. All 22 frozen output
audits passed. The original baseline is preserved. No test predictions or scores
were generated and no test labels were read during this work.

## Round 6 completed: broader comparison models; round 2 retained

See [ROUND6_RESULTS.md](ROUND6_RESULTS.md). Implemented directed pair-comparison
trees, exact quadratic-kernel training with compact matrix inference, conditional
support features, and Nyström kernel features compiled to landmark coefficients.
Also ran explicitly documented validation selection for limited blends, local
regularization, answer-score pooling, nested projection width and consensus blends.
Recorded 147 fold-level configuration scores and 60 validation entries including
repeated baselines. None exceeded 744/798; original model/checkpoint are retained.
Official reproduction, inference checks and integrity records are under
`code/runs/round6-verification/`. No test predictions or scores were generated.

## Round 5 completed: broader experiments; round 2 retained

See [ROUND5_RESULTS.md](ROUND5_RESULTS.md). Compared hard-question weighting,
squared hinge loss, absolute/relative RBF features, a 25,000-term sparse lexical
head, training-only score fusion, candidate resampling augmentation, and covariance
whitening. Used the same question-level training three-fold protocol; 171 fold
configuration scores and 35 fusion choices were recorded. None exceeded 744/798.
The best new model reached 742/798 and corrected no old errors. Fixed repeated
NPZ array loading in lexical inference without changing its mathematical output.
Official validation reproduction and inference checks are recorded under
`code/runs/round5-verification/`. No test predictions or scores were generated.

## Round 4 completed: more features and ranking trees; round 2 retained

See [ROUND4_RESULTS.md](ROUND4_RESULTS.md). Used three-fold training CV to compare
arithmetic/answer relations, train-fitted lexical features, PCA polynomial features,
score fusion and LightGBM LambdaRank. None exceeded the round2 validation score.
The initial arithmetic prototype had a suffix-parsing defect, was marked obsolete,
and was fully rerun after correction. Negative results and selection records remain
available. CURRENT_BEST.json identifies the recommended method and checkpoint.
No test predictions or scores were generated.

## Round 3 completed: round 2 remains best

See [ROUND3_RESULTS.md](ROUND3_RESULTS.md). All eight new validation results were
below 744/798, so round 2 remains the recommended method/checkpoint. Grouping,
alternative losses, larger projections, averaging and a small neural ranker were
evaluated. Negative results and all train-only selection records are retained.
No test score was computed. Family winners and grouped models passed official
validation reproduction and interface checks.

## Current status: round 2 completed

See [ROUND2_RESULTS.md](ROUND2_RESULTS.md). Current selected model is
`code/method_round2.py` with `code/runs/round2/model_bundle/`.
Official validation: 744/798 (93.23%), up from 723/798 (90.60%).
Three additional train-only holdouts also improve by 8/9/10 out of 951.
No test score was computed. Round 1 remains intact below.

## 2026-10-14: first development round

- Official data checker passed for 4,755 train, 798 validation, 467 test questions.
  This is a file/hash/alignment check, not a test prediction or score.
- Local Python 3.12.14; NumPy 2.5.3 installed in code/.venv.
- No test references used for training, tuning or error analysis.
- Implemented deterministic majority baseline and ridge correctness scoring.
- All four candidates receive binary correctness labels; multiple positives are retained.
- Standardization is fitted on training candidates only. Ridge minimizes mean
  squared error plus alpha times squared weight norm; outputs are ranking scores,
  not calibrated probabilities. Select the largest candidate score for each question.
- Fixed search: text / embeddings / combined; alpha = 0.01, 0.1, 1, 10, 100.
  Validation accuracy chooses the winner; ties use grid order.
- Simple text features capture length, formatting, answer parseability and agreement.
  They do not explicitly verify mathematical steps.

| Method | Best alpha | Validation correct | Accuracy |
|---|---:|---:|---:|
| First candidate | — | 624/798 | 78.20% |
| Majority answer | — | 688/798 | 86.22% |
| Text/answer features | 0.01 | 698/798 | 87.47% |
| Embeddings | 0.1 | 715/798 | 89.60% |
| Combined | 1 | 723/798 | 90.60% |

On 355 validation questions with at least two distinct parsed answers, majority
achieves 69.01% and combined achieves 78.87%. This subset is a development diagnostic,
not a substitute for the test bank. Whole-validation accuracy includes easier groups.

Combined beats majority by 35 validation questions (4.39 percentage points).
This is a selected validation result, not independent evidence of test improvement.
The best combined result beats the best embedding result by eight questions;
fixed-alpha ablations and robustness checks are still needed before strong claims.

Initial complete search took about 3.77 seconds locally, including data loading;
see code/runs/round1/experiments.json for the recorded environment and full grid.
Inference assets total 26,444 bytes including configuration. Weights are stored
uncompressed. Formal 30-second eligibility still depends on complete test evaluation
on the reference machine; local validation timing does not establish that eligibility.

Official validation scorer reproduced both results. Fresh prediction plus scoring
processes took 0.88 seconds for the selected method on the local Intel Core
i5-11400H (four BLAS threads). Interface checks passed for sizes 1, 7, 23,
new IDs, reversed question order and an empty bank. SHA-256 checks confirmed
the official runner, scorer, parser and data checker match the supplied release.

The supplied .gitignore excludes runs/. When preparing the final public repository,
explicitly package the experiment records and publish the matching checkpoint;
do not assume an ordinary git add will include these files.

## Next work

1. Examine training/validation failures and majority disagreements.
2. Ablate answer agreement and surface features at controlled regularization.
3. Compare candidate-ranking objectives with current pointwise regression.
4. Limit development iterations and use question-level training splits for robustness.
5. Freeze final method, then perform official complete test evaluation and timing.
6. Write the report (at most 10 pages), package versioned code/checkpoint and submit.
# 2026-10-24 Strategy reset

Responded to the user's request to change research direction. Audited36 historical
official outputs (25declines/11ties versusR11), then ran12fixed diagnostic fits
on three train-only splits at50%/90% fitting size. No ranking reversal observed
for the two representative model families; this does not establish a general cause.
No new validation/test evaluation or checkpoint promotion. Paused feature/rule/fusion
extensions. Proposed an independently trained raw-text sequence verifier with a
matched bag-of-words control; not implemented. See STRATEGY_RESET_FINDINGS.md.



## 2026-10-28 — Frozen Round79 final test

冻结模型后，运行一次官方测试预测和独立评分。未据测试结果改动模型或参数。

- 测试：**368/467 = 78.800857%**。
- 既有验证：749/798 = 93.859649%，为多轮开发选择后的验证指标。
- 配置：semantic alpha=0.3；numeric alpha=1；原算术门控与最终答案转交。
- 全部解压推理资产：1,678,154字节（1.6004 MiB）。
- 完整测试fresh预测＋独立评分：2.881274秒；四总CPU线程。
- 本机：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz，Python 3.12.14；参考Xeon资格未验证。
- 冻结前后代码和检查点SHA验证通过；未执行测试错题分析。
- 官方结果：`final_evaluation/round79-test-20261028/test-score.json`。
- 冻结快照与资源记录：同目录`FROZEN_MODEL.json`、`result.json`、`commands.json`及`code/`。
- 最终提交尚需同步报告/交付包、提供代码与checkpoint链接，并实际创建课程GitHub issue。

本次只新增正式最终测试记录，不增加开发轮次；历史1–105轮记录与旧交付快照保持。


## 2026-10-28 — Historical frozen-model test comparison

# 历史阶段最佳模型的固定测试比较

用户明确要求后的追加测试比较。Round79测试结果在本次清单形成前已可见；本批不属于测试前整体预注册。

|模型|验证正确数/798|测试正确数/467|测试准确率|预测＋评分秒|解压资产MiB|
|---|---:|---:|---:|---:|---:|
|Round2：上下文成对排序|744|366|78.3726%|1.459|0.8000|
|Round7：算术冲突门控|747|367|78.5867%|1.852|1.6004|
|Round11：最终答案转交|748|367|78.5867%|1.822|1.6004|
|Round79：验证选定最终模型|749|368|78.8009%|2.881|1.6004|

Round79引用之前的一次正式测试，本次不重跑。三个历史模型的检查点匹配既有验证资产SHA，推理源文件匹配首轮正式测试前的冻结版本。每个模型分别满足本机16MiB/30秒限制；四总CPU线程，参考Xeon资格尚未验证。

按验证集选定的最终模型仍为Round79。所有分数完整报告，不依测试结果改选、融合、调参或分析测试错题。当前比较不提供独立确认或显著性结论。开发轮次仍为105。

每个模型的官方评分JSON、预测、命令、完整运行输出、独立快照和资源记录位于`final_evaluation/historical-comparison-20261028/round{2,7,11}/`。固定清单和完整性记录位于同级`FROZEN_COMPARISON.json`及`integrity.json`。


## 2026-10-28 — Peer strategy review and validation difficulty audit

The student supplied Devin-Lo1/dase-7506-mp2/REPORT.md. Codex read the report and statically checked seven related public source files, compared their method with retained Rounds5/18/24/29/43/47/62 records, and summarized findings in PEER_STRATEGY_REVIEW_2026-10-28.md. Git blob hashes and links are recorded there. Peer scores are self-reported and were not independently reproduced. No peer checkpoint was downloaded or executed, and no peer code was integrated into inference.

A train/validation-only audit found 2114 training answer-disagreement groups, compared with 2513 mixed-correctness groups. Existing Round79 validation choices score 306/355 on answer-disagreement groups, with 43/49 errors in single-correct-candidate questions. The first audit utility failed because splitlines split Unicode separators inside JSON strings; switching to file-line iteration repaired the audit without changing official data/tools. The saved result includes source/data hashes.

The review proposes a finite 2x2 OOF-stacking/augmentation research comparison; this proposal has not been trained. No additional test prediction, scoring, per-question test analysis, parameter search or model selection was performed. Previously observed own/peer test totals are disclosed. The selected pointer and Round79 frozen source/assets remain unchanged.


# Round106：OOF堆叠与候选增强2×2结果

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION；四配置均完整报告，未运行测试。此前测试总分已知，不声称独立确认。

|候选增强|第二层|训练内部留出/951|验证/798|分歧验证/355|单正确验证/117|修复/新增错|解压MiB|fresh预测+评分秒|
|---|---|---:|---:|---:|---:|---|---:|---:|
|False|linear|876|741|298|70|10/18|0.6977|4.930|
|False|tree|870|743|300|71|10/16|2.3402|4.981|
|True|linear|871|739|296|70|12/22|0.6977|4.859|
|True|tree|869|739|296|66|10/20|2.3403|4.979|

当前Round79验证749/798、分歧306/355、单正确74/117。四配置最佳743/798，未超过当前最佳；不能称为突破。

2×2正确数差（描述性，非独立因果/显著性证明）：

```json
{
  "validation_correct_count": {
    "tree_minus_linear_without_aug": 2,
    "augmentation_effect_linear": -2,
    "augmentation_effect_tree": -4,
    "interaction": -2
  },
  "outer_held_correct_count": {
    "tree_minus_linear_without_aug": -6,
    "augmentation_effect_linear": -5,
    "augmentation_effect_tree": -1,
    "interaction": 4
  }
}
```

训练成本：48次基础logistic拟合、8次元模型拟合；训练worker墙钟234.367秒，四线程，1800秒硬预算。所有参数和四个输出在验证前固定。训练回代、基础OOF和外层留出区别记录，外层held中题目和副本均未参与该阶段学习。此训练集和验证集此前被多轮使用，存在适应性选择偏差。

参考公开同学方案的架构思想，自行实现；未使用其代码或权重。此次使用LightGBM shallow binary和三个基础模型，并非完整复现对方的CatBoost/attention集成。每个模型数值树导出与原生训练预测差<1e-10，训练缓存和checkpoint重载、严格重排/题序/新ID/变bank/空输入/整数均通过。资产按NPZ解压保守计数，完整fresh官方验证预测+独立评分<=30秒；本机结果不代表参考Xeon完整测试资格。

证据：`code/runs/round106-stack/result.json`、`outer-held-results.json`、`fold-proofs.json`；`code/runs/round106-evaluation/all-results.json`、`factorial-effects.json`、`integrity.json`及四个官方评分JSON。


# Round106：本轮发现与下一步

本轮未突破：最佳743/798，当前749/798仍更高。56次实际拟合产生四个最终配置，不能称56个独立实验。

## 配置差异的实际结果

- 未增强时，浅树验证比线性多2题，但内部留出少6题；两种评估未一致支持浅树优于线性。
- 增强使线性验证少2题、浅树少4题；内部留出也分别少5题、1题。此固定增强配方未显示收益。
- 最佳浅树修复旧模型10个错误，同时引入16个错误；单正确候选题71/117，低于原模型74/117。
- 全训练回代随增强/浅树提高到4536/4755，但未迁移到held/validation。回代提升不足以支持晋级；不能仅凭这些结果确定唯一过拟合原因。

## 基础模型的已有训练OOF诊断

|增强|表示|基础模型OOF正确数/4755|
|---|---|---:|
|False|raw|4336|
|False|context|4281|
|False|cluster|4295|
|True|raw|4321|
|True|context|4289|
|True|cluster|4282|

这些是基础模型的折外结果，不是第二层整体OOF，更不是未使用过的独立评估；不得与最终模型训练回代混用。

## 发现一个需要控制的训练混杂因素

原始pair数6516，增强后19200；正反pair同步增加，损失权重总量约变为2.9466倍。代码把pair权重归一化到均值1，且C固定；因此增强同时改变了训练分布、样本数量、缩放统计和有效正则，不能将下降完全归咎于候选重采样思想。若后续专门检验增强，需额外控制总损失权重（或按实际pair比例缩放C），再与原配方作对照；本轮没有事后修改或重跑。

## 下一步优先级

1. 先检查基础专家是否保留当前较强的语义表示。本轮三个基础模型没有使用原Round2的随机投影非线性块，也没有将当前父模型的合法OOF分数作为输入；整个新模型替换原模型后可能同时丢失已有优势。后续可固定比较加入旧强模型OOF信息的增量，而不是同时重做全部特征。
2. 本轮增强因子使全部基础模型替换为增强版本；对方最终方案同时保留原始与增强专家。原始+增强的联合输入尚未由本轮检验。若研究这种互补性，应固定一个线性元模型，避免再次同步扩学习器和权重网格。
3. 先控制上述差异，再决定是否训练attention；不因一次浅树失败就宣称所有非线性堆叠无效，也不承诺加attention即可提升。

本轮只用官方train/validation，无新测试评测或逐题测试诊断；Round79正式测试模型未替换。后续任何开发需保留既有测试已见的披露。


# Round107：保留当前模型的小权重融合

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。四个固定输出，零新增拟合；本次没有测试评测。

|donor|新模型权重|验证/798|分歧/355|单正确/117|修复/新增|解压MiB|fresh预测+评分秒|
|---|---:|---:|---:|---:|---|---:|---:|
|linear|0.1|748|305|73|0/1|2.2982|5.622|
|linear|0.25|747|304|73|0/2|2.2982|5.665|
|tree|0.1|748|305|73|0/1|3.9408|5.672|
|tree|0.25|746|303|73|1/4|3.9408|5.872|

最佳748/798（93.734336%）；原模型749/798。未超过原模型，不能称为突破。

本轮检验新模型纠错是否可在保留旧模型时保留下来；只有净正确数增加才称验证改进。按有效候选归一化、logit变换、掩码和单次R11转交都属于配方，不能把变化全归于一个特征。本次是106结果之后的顺序自适应验证开发；旧测试总分已知，不作独立泛化声明。

所有完整嵌套资产计入16MiB，fresh官方预测+独立评分四总线程<=30秒；本机测量不代表参考Xeon资格。0权重完整复现父模型，严格分数重排/题序/新ID/变bank/空输入/整数检查通过；源及模型SHA未变。

复现：从code目录运行run_round107_retain_parent.py，需保留原Round79和Round106训练产物；输出目录应不存在。固定清单、逐模型官方评分、资源和SHA见code/runs/round107-retain-parent/。


Round107 learning:

## 本轮结论与停止依据

四输出为748、747、748、746，均未超过749。0.1权重两个donor均为0修复/1新错；线性0.25为0/2，树0.25为1/4。更高的固定混合权重没有在本批带来净收益。新模型单独能修复10题，不代表简单分数平均能保留这些修复；还需要判断何时采用新模型。归一化及R11选择转交也可能影响改选，不能把全部变化归因于置信度或某个特征。

停止继续围绕这四项扩权重。若后续继续，优先在训练折外数据上学习原强模型与新专家的条件选择，并固定增量对照；不据测试结果调整。当前Round79正式测试模型保持；本次没有新增训练、测试评分或成绩提升。


## 2026-10-28 — Targeted GitHub methodology search

At the student's explicit request, Codex searched GitHub for additional relevant approaches. Repository search returned 13 student course repositories plus the official source; six student READMEs and related sources from three course repositories were inspected, together with primary Set Transformer/allRank/GSM8K sources and official CatBoost embedding documentation. The source record contains 22 GitHub files with blob SHAs and two documentation URLs. README aggregate test claims were visible and are not independently reproduced outcomes. No peer predictions, reference datasets, checkpoints or external training data were downloaded, and no remote code was executed.

GITHUB_METHOD_REVIEW_2026-10-28.md compares applicability and prior Rounds3/5/20/24/34/38/43/62/73/106/107, identifies within-answer nonempty-subset augmentation and sample-count-invariant regularization as a concrete follow-up, and distinguishes generic ranking losses from the multi-positive selection objective. NEXT_EXPERIMENT_GROUP_SUBSETS_2026-10-28.md is a four-configuration proposed experiment, not an executed round. No new training, validation prediction, test scoring, model selection or submission occurred. The frozen Round79 assets/source and latest completed round107 were verified unchanged.


# Round108：答案组子集增强与固定正则

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。先写计划，再自行实现；四配置完整报告。本轮未访问测试，既往自身及公开测试总分已知。

|组内增强|lambda|训练三折OOF/4755|验证/798|分歧/355|单正确/117|修复/新增错|资产MiB|fresh预测+评分秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|False|0.003|4364|739|296|71|11/21|0.02468|1.392|
|False|0.01|4387|741|298|71|10/18|0.02468|1.402|
|True|0.003|4369|746|303|74|15/18|0.02468|1.410|
|True|0.01|4380|746|303|74|13/16|0.02468|1.509|

本轮最佳round108_subsets_l0p01：746/798（93.4837%）；未超过既有749，不宣布突破。已完成测试的Round79模型和成绩仍保留。

## 消融解释

以下是正确题数差；共享划分、缩放和每题损失权重，只比较本轮固定表示内的条件：

```json
{
  "validation": {
    "augmentation_at_0p003": 7,
    "augmentation_at_0p01": 5,
    "stronger_regularization_full": 2,
    "stronger_regularization_subsets": 0
  },
  "train_oof": {
    "augmentation_at_0p003": 5,
    "augmentation_at_0p01": -7,
    "stronger_regularization_full": 23,
    "stronger_regularization_subsets": 11
  }
}
```

增强将全训练pair数从3058变为12200，但2114道有正负有效答案组的题目总权重保持一致；目标采用每题平均logistic损失加lambda/2*范数平方，因此排除了固定C随样本数改变有效正则的混杂。数值梯度与重复pair保持损失/梯度不变检查通过。

三折中每题及其所有子集处于同一侧；缩放只拟合该折原始完整组。OOF与训练回代分别记录，不把回代准确率作为泛化结果。训练数据和官方验证均已长期用于开发，不能视为全新独立确认。

16次拟合、四线程、worker墙钟11.769秒，600秒硬上限；训练停止后串行计时。全部模型资产按NPZ解压保守计数，包含权重/mean/scale/config。通过官方fresh预测及独立评分、严格分数重排、题序、新ID、变bank、空输入、Python整数和组内同分检查。本机验证计时不代表参考Xeon完整测试资格。

来源：CaspianW答案组内子集增强与显式正则思想，独立实现，不是其最终算术残差系统的复现。来源URL/版本见GITHUB_METHOD_SOURCES_2026-10-28.json。

复现：在code目录依次运行train_round108_group_subsets.py、evaluate_round108_group_subsets.py。已有输出目录时拒绝覆盖；完整计划见ROUND108_GROUP_SUBSETS_PLAN.md。

证据：code/runs/round108-group-subsets/result.json、folds.json、pair-audit和fold-models；code/runs/round108-evaluation/frozen-before-validation.json、all-results.json、factorial-effects.json、integrity.json及五组官方评分/命令/进程日志。


# Round108实验后的改进依据

本文件是四配置全部完成后的描述性分析，没有新训练、融合或追加验证配置。

## 已得到的结论

- 同一显式正则下，子集增强使验证正确数从739→746、741→746（+7、+5）；对应训练三折OOF为4364→4369（+5）、4387→4380（−7）。增强对验证有收益，但跨划分证据并不一致，不能宣称普遍稳定提升。
- lambda由0.003变0.01时，原始组的训练OOF+23、验证+2；增强组OOF+11、验证持平。两种训练条件下更强正则均提高本轮OOF；这支持约束模型的方向，而非继续增加拟合能力。两个正则点不足以确定最优范围。
- 最佳验证746仍低于原749。较强正则增强组修复13个旧错，却新增16个错；有互补信号，但直接替换会净损失3题。上一轮固定融合也已失败，不能仅凭互补就宣称融合必然有效。

## 错误分层与旧能力保留

|配置|真实数值答案改变|仅同答案内索引改变|单正确：新/旧|双正确：新/旧|三正确：新/旧|四正确：新/旧|算术门内：新/旧|旧最终答案转移修复：保留/总数|
|---|---:|---:|---|---|---|---|---|---|
|round108_full_l0p003|34|464|71/74|112/117|177/179|379/379|40/43|0/1|
|round108_full_l0p01|30|463|71/74|113/117|178/179|379/379|40/43|0/1|
|round108_subsets_l0p003|36|463|74/74|115/117|178/179|379/379|41/43|0/1|
|round108_subsets_l0p01|31|464|74/74|115/117|178/179|379/379|41/43|0/1|

原结果中的changed_choices包括同一数值答案组内的索引变化；上表将其拆开，避免把约500次索引变化误读为约500次数学决策改变。算术门由旧的固定规则计算，本次没有据此拟合或添加门控。分层仅用于说明得失，不是新的独立评价集。

## 下一轮应怎样改

1. 保留：原模型已有的显式算术检查和最终答案证据不应在新组模型中无意丢失。本轮六项numeric surface只描述答案/题目数值，不验证推理步骤，不能称为算术一致性验证器。
2. 可研究：将组表示作为训练得到的条件残差，而非全局固定融合或整体替换；残差的启用条件、权重和正则必须用训练原题的OOF确定，训练特征和残差拟合同样隔离。这只是后续假设，本轮未执行，不能保证改进。
3. 评价顺序：先要求多个训练折的净修复收益一致，再冻结一个有限候选池做官方验证。若仅验证涨、OOF降，完整报告冲突，不再从同一验证反馈连续追加融合参数。
4. 停止：按原计划完成四配置即结束本网格。原749保留，本轮不运行测试。

证据：同目录learning.json、all-results.json、factorial-effects.json；ROUND108_RESULTS.md及训练fold_records。


# Round109结果：固定答案组模型与局部算术残差

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。先保存计划，固定四配置，训练全程不加载验证或测试；全部模型冻结后验证。

|anchor增强|残差lambda|训练嵌套OOF/4755|anchor OOF|验证/798|anchor验证|分歧/355|单正确/117|修复旧错/新增错|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
|False|0.01|4386|4387|748|741|305|76|12/13|0.02616|1.955|
|False|0.1|4391|4387|747|741|304|76|11/13|0.02615|1.973|
|True|0.01|4390|4380|750|746|307|77|13/12|0.02615|1.979|
|True|0.1|4392|4380|751|746|308|78|14/12|0.02615|1.966|

最佳round109_subsets_r0p1：751/798（94.1103%）。超过原749；另存验证研究候选。已测Round79最终模型和历史测试成绩不变。

## 方法与来源

借鉴[CaspianW固定anchor与局部算术残差](https://github.com/CaspianW/dase7506-mp2/blob/main/src/train.py)，[组内mean/max聚合](https://github.com/CaspianW/dase7506-mp2/blob/main/src/quantity_flow_features.py)及[11项局部特征定义](https://github.com/CaspianW/dase7506-mp2/blob/main/src/arithmetic_features.py)。自行实现，不并入对方代码/权重；既有numeric_round7_v3有界解析器与来源解析器不完全相同。使用原始完整组残差pair、每题归一损失、显式L2。

不同于来源的同fit anchor margin，本轮使用inner-OOF offset。18次inner anchor拟合，12次outer残差拟合和4次全训练残差拟合，共34次新拟合。outer-held完全排除在inner fit和残差fit之外；scaler只拟合该fit原始组。最终残差用全train OOF offset，部署用full-train anchor。第108轮折模型与OOF数组逐分数精确一致，继承源/资产/折/OOF哈希均有记录。

四线程worker训练墙钟14.554秒，父进程硬timeout900秒。数值梯度、重复pair不变性、零残差严格等于anchor、缓存/导出一致、分数重排1e-8、题序、新ID、变bank、空输入、Python整数、同答案同分检查通过。完整资产包含anchor、scaler、残差权重和config，按NPZ解压保守计数；官方fresh预测+独立评分≤30秒。本机计时不代表参考Xeon完整测试资格。

历史自身与公开他人测试汇总分数已知；本轮不访问/哈希/预测/评分测试，不声称反复使用的训练或验证是独立确认。训练回代与OOF分开保存。

复现：code目录依次运行train_round109_arithmetic_residual.py与evaluate_round109_arithmetic_residual.py。已有目录拒绝覆盖。证据为runs/round109-arithmetic-residual/result.json、nested-partitions.json、residual-progress.json、pair-audit；runs/round109-evaluation/frozen-before-validation.json、all-results.json、integrity.json及每个官方评分和进程日志。


# Round109：为什么这次有提升，以及还缺什么

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成四配置后的描述性分析。没有新增拟合、配置或测试。

## 对照结果

|anchor|残差lambda|训练三折净增加|逐折净增加|验证相对anchor|验证相对原749|
|---|---:|---:|---|---:|---:|
|未增强|0.01|-1|[-4, 2, 1]|+7|-1|
|未增强|0.1|+4|[2, -1, 3]|+6|-2|
|增强|0.01|+10|[-2, 4, 8]|+4|+1|
|增强|0.1|+12|[2, 5, 5]|+5|+2|

最佳增强+0.1残差：train OOF 4380→4392，逐折+2/+5/+5；验证746→751。相对自身anchor修复5题、无新增错；相对旧Round79修复14题、新增12错，749→751。它既通过训练三折配对比较，也通过预定官方验证，证据强于只看训练回代。但两题增益很小，且数据长期用于开发，不能据此宣称显著性或独立测试提升。

## 可解释的变化

1. 上轮组模型仅有数值表面信息。本轮保留该组分数，再用局部等式和末个结果与答案关系学习修正。四配置相对各自anchor验证均提高6/7/4/5题；不过未增强弱正则的训练OOF−1，说明不是所有配置都跨划分一致。
2. 更强残差正则在两种anchor下均提高训练OOF；增强组验证750→751。未增强组验证则748→747，不能说更强正则对所有条件都更好。
3. 最佳相对anchor修复的5题中，算术特征贡献的新选项对旧选项分差为正有5题，格式特征贡献为正有1题。这是固定线性分数的精确分解，不是移除特征重训的因果消融；本轮没有新增这种消融配置。逐题分解在learning.json。
4. 相对原749，单正确题74→78，双正确117→116，三正确179→178，四正确379不变。净增益来自单正确题+4，另有两题净损失。旧最终答案/算术保护仍可能提供互补，不能把当前提升解释为已经解决所有旧错。

## 下一轮实验依据

- 保留本轮751研究候选和全部四配置；继续研究时以同折train OOF净修复为首要依据，再冻结小候选池验证。原已测Round79模型/测试记录仍保留。
- 如继续对照，应先区分格式与算术增量：在相同anchor、折和正则下比较“格式残差”与“格式+算术残差”，再判断收益是否来自真正的计算核对。不能把本轮分数贡献分解冒充这一实验。
- 在训练集分析剩余错例中解析不到的等式、已有检查但关系选错和最终答案格式冲突，根据覆盖率决定是否值得改解析器；不要直接编写针对验证题的规则。
- 本批按四配置完成即停止，不依据本轮验证结果追加融合权重或运行测试。

资源：最佳完整资产27423字节，含anchor与统计；本机四线程fresh官方预测+独立评分约1.966秒。这些是验证资源检查，非参考CPU完整测试复核。


# Round110：格式/算术消融与最终答案证据

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定四配置，训练不读取validation/test；四配置冻结后官方验证。

|模式|维数|训练三折OOF/4755|相对4392|验证/798|相对751|修复751错/新增错|单正确/117|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
|format|6|4386|-6|746|-5|0/5|74|0.02575|1.948|
|arithmetic|16|4389|-3|749|-2|0/2|77|0.02599|1.980|
|full|22|4392|+0|751|+0|0/0|78|0.02612|2.001|
|final_evidence|26|4398|+6|751|+0|1/1|78|0.02622|1.961|

本轮最佳round110_full：751/798（94.1103%）。未超过751，保留第109轮研究候选；full重复对照不计为新提升。原已测Round79最终模型及历史测试记录保持。

训练条件：固定增强组anchor lambda0.01，残差lambda0.1。仅格式6维、仅算术16维、完整22维和新增最终答案证据26维，均重训。最终答案证据沿用早期Round11解析定义，权重由训练学习，无人工指定答案转移。所有scaler只拟合各fit完整组。

16次新残差拟合，四线程，worker 19.838秒，父进程600秒硬上限。复用第109轮嵌套anchor，重新计算inner-OOF offset并逐pair验证与原审计一致；full模式统计/权重1e-12和OOF/验证分数1e-10重现原751控制。数值梯度、重复pair、缓存导出、零残差和严格重排/题序/新ID/变bank/空输入/Python整数/同组同分通过。

完整资产包含anchor、mean/scale、残差和config，按NPZ解压保守计数≤16MiB；训练停止后，fresh官方预测与独立评分合计≤30秒。以上本机验证计时不是参考Xeon完整测试资格。

历史自身及公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，不把长期开发使用的train或validation视为全新独立确认。

来源延续CaspianW固定anchor与局部算术残差思想（见第109轮计划的源码链接），本轮为自行实现的匹配消融与旧最终答案特征重用，没有引入外部代码/权重/数据。

复现：code目录train_round110_residual_ablation.py，然后evaluate_round110_residual_ablation.py；已有输出目录拒绝覆盖。证据：runs/round110-residual-ablation/result.json、fit-progress.json、nested-offset-proofs.json、pair-audit；runs/round110-evaluation/frozen-before-validation.json、all-results.json、integrity.json和所有官方评分/进程日志。


# Round110得失与下一轮依据

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；已完成匹配消融后的描述性分析。

|模式|train OOF|逐折相对full|验证|修复751错/新增错|
|---|---:|---|---:|---|
|format|4386|[4, -4, -6]|746|0/5|
|arithmetic|4389|[0, -2, -1]|749|0/2|
|full|4392|[0, 0, 0]|751|0/0|
|final_evidence|4398|[3, 0, 3]|751|1/1|

## 解释

1. 固定anchor、折外offset、缩放与lambda后，完整22维相对仅格式增加训练OOF6题、验证5题；相对仅算术增加训练OOF3题、验证2题。这支持格式和算术信息在本轮条件下互补，不能说只靠等号格式，也不能把格式信息全部删除。
2. 最终答案证据在训练OOF增加6题，逐折+3/0/+3；验证修复1题、新增1错，仍751。OOF改善没有转化为本次验证净增，不能宣称突破，也不能凭验证错例直接选择一个特征或手工开关。
3. full重训与第109轮统计/权重及OOF/验证分数严格重现。此结果减少了训练/缓存误差解释，但重复验证不是新的独立确认。

## 接下来只改参数

保留full和final_evidence两种表示，在训练三折比较少量预定正则；按训练OOF选每种表示一个候选，再一起冻结进入验证，避免把整个参数网格都暴露给验证集。保留751对照，不继续删除已证实互补的特征。

本轮16次新拟合，所有资源与接口通过；未运行测试。详情见ROUND110_RESULTS.md。


# Round111：固定表示的正则参数比较

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定2表示×4正则，只用训练三折为每种表示选一个候选；官方验证仅两个候选。

## 全部训练配置

|模式|lambda|训练三折OOF/4755|进入验证|
|---|---:|---:|---|
|full|0.03|4390|False|
|full|0.1|4392|True|
|full|0.3|4390|False|
|full|1.0|4385|False|
|final_evidence|0.03|4397|False|
|final_evidence|0.1|4398|True|
|final_evidence|0.3|4394|False|
|final_evidence|1.0|4391|False|

同分优先更强正则。lambda0.1为已知配置重现，不计新发现；未选出的六个配置没有运行验证。

## 两个训练选出候选的官方验证

|模式|lambda|验证/798|相对751|修复/新增错|单正确/117|资产MiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|---:|
|full|0.1|751|+0|0/0|78|0.02613|2.022|
|final_evidence|0.1|751|+0|1/1|78|0.02623|1.986|

最佳round111_full_r0p1：751/798（94.1103%）。没有超过751，保留第109轮研究候选。原已测Round79最终模型和历史测试记录保留。

32次新残差拟合，四线程，worker 15.903秒，600秒硬上限。复用第110轮验证过的嵌套anchor margin，按原题pair顺序、权重、哈希严格核对；每折统计只拟合fit，0.1参数严格重现。验证前全部源/模型/计划/训练结果SHA冻结。

全部8模型通过训练重载、零修正和接口检查；两个验证候选通过官方fresh预测+独立评分、严格分数重排/题序/新ID/变bank/空输入/Python整数/同组同分。完整解压资产含anchor/统计/残差/config≤16MiB，fresh预测与评分≤30秒。本机验证计时不是参考Xeon完整测试资格。

历史自身及公开他人测试总分已知。本轮不访问/哈希/预测/评分测试；train/validation长期自适应复用，不作独立确认或显著性承诺。未扩展预定参数网格，也未在结果后验证未入选配置。

复现：code目录train_round111_regularization.py，再evaluate_round111_regularization.py。输出存在则拒绝覆盖。证据：runs/round111-regularization/result.json、fit-progress.json、pair-audit；runs/round111-evaluation/frozen-before-validation.json、all-results.json、integrity.json及官方日志。


# Round111：训练折外错误的证据覆盖率

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；仅统计train OOF错误，不拟合、不读取验证或测试。

|训练OOF错误类型|full22|final_evidence26|
|---|---:|---:|
|错误总数|363|357|
|错选组无可检查等式|80|78|
|错选组有检查不匹配|3|3|
|错选组检查通过但末结果与答案冲突|97|93|
|错选组检查通过的其他错误|183|183|
|错选组与正确组都无可检查等式|39|39|
|错选组无检查、正确组有检查|41|39|
|正确组也含检查不匹配|8|8|
|错选组有late-box冲突|8|2|
|正确组收到组外冲突late-box支持|6|1|

前四个错误子类互斥；其余覆盖统计可重叠。“检查通过”只指有界解析器接受的局部等式，不意味着整条推理正确，更不自动证明语义错误。这里是已多轮使用的训练集诊断，不是独立确认。

下一轮可据这些计数判断优先级：无检查覆盖的部分需先审查解析边界；已有局部检查通过仍错的部分需要题意/运算关系信息；有矛盾仍胜出的部分再研究条件修正。不能简单规定“出现假等式就淘汰”，因为正确组也可能含检查不匹配。本文件只提出方向，没有新增规则、超参或验证配置。


# Round112：目标、集合交互与异质专家

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预定8专家+2固定集成完整报告；训练未读取验证或测试，全部冻结后验证。

|模型|目标|训练OOF/4755|验证/798|分歧/355|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---|---:|---:|
|linear|uniform_ce|4345|746|303|73|10/15|0.0254|1.971|
|linear|correct_set_mass|4337|745|302|79|9/15|0.0254|1.962|
|pointwise|uniform_ce|4305|724|281|55|10/37|0.2922|1.909|
|pointwise|correct_set_mass|4285|729|286|62|12/34|0.2922|2.008|
|deepsets|uniform_ce|4283|733|290|61|11/29|0.3079|1.904|
|deepsets|correct_set_mass|4301|730|287|72|17/38|0.3079|1.942|
|attention|uniform_ce|4291|735|292|63|7/23|0.3164|1.985|
|attention|correct_set_mass|4319|735|292|74|12/28|0.3164|1.903|
|diverse_mean|固定平均|4353|743|300|74|12/20|0.9423|4.238|
|protected_mean|固定平均|4398|746|303|75|0/5|0.9684|4.915|

最佳round112_linear_uniform_ce：746/798（93.4837%）。没有超过751，保留原751研究候选。原已测Round79模型与测试记录保持。

## 方法与实现边界

1. 组内子集与固定正则已在108及后续模型执行。本轮补充4结构×2多正确目标的匹配比较。同输入1053维、同折、同优化预算。非线性宽32；DeepSets在编码后聚合；attention四头候选自注意力，不是完整Set Transformer论文复现。参数量不同，不能把全部结构差异都归于注意力本身。
2. uniform_ce在正确候选上均分目标；correct_set_mass最大化整个正确候选集合的总概率。推理统一使用固定温度1的同答案概率求和；None不成有效组，组内同分，ID不作特征。没有直接套用allRank的默认ListNet或k=1 LambdaLoss。
3. 四个结构各自只用训练OOF选择一个损失，再等权平均组概率；protected_mean固定0.75父751+0.25异质平均。它们是预定概率集成，不是学习式堆叠。专家选择用过OOF标签，集成训练分数是开发指标，不称无偏meta-OOF。

来源：[Bosco训练源码](https://github.com/Bosco-lab/DASE7506_MP2/blob/main/code/train_ranker.py)、[Set Transformer作者源码](https://github.com/juho-lee/set_transformer/blob/master/modules.py)、[michaelleeoo异质专家](https://github.com/michaelleeoo/DASE7506-MP2)。独立实现，没有导入公开代码、权重、外部训练题目或在线模型调用。

## 训练与资源证据

32次新拟合，四CPU线程，worker 62.946秒，1800秒硬上限；PyTorch 2.14.1+cpu只训练，NumPy 2.5.3推理。Adam40epoch，lr0.003，batch128，显式L2=0.001，梯度clip5，固定seed。每折mean/std只拟合fit，原题分组隔离；未选择最佳验证epoch。训练回代、基础OOF和自适应集成指标区别记录。

训练前损失解析/有限差分梯度、torch-float64/NumPy前向预检通过；正式候选完整接口检查在拟合后执行。计划中的训练前排列预检没有单独留档；训练和验证端的正式严格重排检查均通过，作为此项流程差异披露。torch训练float32与float64导出误差另记，不假称位精度重现。float64原生/导出误差<1e-9。候选分数重排1e-8、题序、新ID、变bank、空输入、Python整数、同组同分通过。

全部部署资产含scaler、参数、嵌套专家与父模型，按NPZ解压保守计数≤16MiB；训练停止后逐个fresh官方预测+独立评分≤30秒。CPU本机验证不代表参考Xeon完整测试资格。

此前自身及公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，不将长期开发使用的train/validation视为独立确认。

复现：code目录train_round112_diverse_experts.py，随后evaluate_round112_diverse_experts.py；已有输出拒绝覆盖。证据在runs/round112-diverse-experts/result.json、fit-progress.json、mathematical-checks.json、fold参数、ensemble-members-selected-on-train.json；runs/round112-evaluation/frozen-before-validation.json、all-results.json、integrity.json及所有官方评分与进程日志。


# Round112：方法覆盖、消融解释与下一轮依据

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完整预定实验后的描述性分析。没有新拟合、额外验证候选或测试访问。

## 用户批注中的四条路线

|路线|实际工作|结果与边界|
|---|---|---|
|答案组内非空子集增强|108增强开/关×lambda对照，109/110/111使用增强anchor|108最佳746；109加局部残差751。不是仅复制候选。|
|增强保持正则尺度|108显式每题均值损失+lambda/2范数平方，scaler只fit完整原组|pair3058→12200，每题总权重不变；排除第106轮固定C样本数混杂。|
|结构/目标不同的专家|112线性、逐候选MLP、DeepSets、自注意力×两目标，及两种预定概率集成|32次新拟合、10部署候选完整验证；并非学习式堆叠或完整复现同学系统。|
|多正确答案损失适配|均分正确CE与正确集合概率质量匹配比较，梯度解析/有限差分一致|没有把多正确标签硬改为唯一类，没有直接套默认ListNet/k1 LambdaLoss。|

## 正确集合目标相对均分CE的变化

|结构|train OOF差|验证差|单正确差|双正确差|三正确差|
|---|---:|---:|---:|---:|---:|
|linear|-8|-1|+6|-6|-1|
|pointwise|-20|+5|+7|+1|-3|
|deepsets|+18|-3|+11|-7|-7|
|attention|+28|+0|+11|-12|+1|

集合质量目标在全部四结构上提高本轮单正确验证层，但整体正确数变化−1/+5/−3/0，不能说它总是更好。DeepSets和attention的训练OOF分别+18/+28，验证却−3/0；pointwise则训练OOF−20、验证+5。方向冲突必须保留，不能只展示一个有利指标。

## 结构与拟合差距

|结构|目标|训练回代/4755|训练OOF/4755|差距题数|其他候选raw logit扰动最大值|
|---|---|---:|---:|---:|---:|
|linear|uniform_ce|4507|4345|162|0|
|linear|correct_set_mass|4538|4337|201|0|
|pointwise|uniform_ce|4755|4305|450|0|
|pointwise|correct_set_mass|4755|4285|470|0|
|deepsets|uniform_ce|4755|4283|472|4.66045|
|deepsets|correct_set_mass|4755|4301|454|4.43405|
|attention|uniform_ce|4755|4291|464|1.49995|
|attention|correct_set_mass|4755|4319|436|5.34307|

六个非线性模型训练回代均4755/4755，训练OOF仅4283–4319，说明在这组固定训练条件下存在明显拟合差距。没有证据支持继续增加宽度/epoch。线性CE训练OOF4345也低于当前751模型的4392，说明这次不同表示/损失/聚合的重训并未整体取代原答案组增强+残差配方。

扰动诊断在固定规范化输入上只清零一个候选，不重新生成文本/组输入；线性和pointwise的其他候选raw logit不变，DeepSets/attention确实会改变。这证明新增网络交互被实际使用，不是没连上的模块；它不是同参数量控制，也不是推理概率归一化的变化。结构相对pointwise的差值见learning.json，不能把任意提升全部归因于注意力。

## 异质集成

训练选择成员为线性uniform_ce、pointwise uniform_ce、DeepSets correct_set_mass、attention correct_set_mass。异质平均训练开发4353、验证743；保留父模型的0.75/0.25固定平均训练开发4398、验证746。后者相对751验证没有修复旧错，却新增5错，不能部署为改进；父模型保留。这只检验了这组专家和两个固定权重方案，不否定所有异质集成，也不代表同学学习式堆叠已复现。

## 下一轮依据

1. 先修正非线性拟合差距：如继续，使用训练集内部早停或更小监督瓶颈，与固定40epoch/原宽度对照；不要从验证曲线挑epoch。此方向尚未执行，不保证提升。
2. 若要学习专家融合，保留强父模型，使用嵌套折外输入给第二层，并先检查专家在训练OOF的条件净修复；不能用本轮全训练回代概率训练融合器后称OOF，也不因验证失败追加手工权重。
3. 正确集合目标在单正确层有收益，应在训练折内研究多正确层的代价；任何分层策略都要用可由输入决定的条件，不能在推理时偷用正确候选数量。
4. 当前研究基准751保持，本轮不运行测试。全部10候选资产≤0.97MiB、fresh预测+评分≤4.92秒（本机验证）；资源满足不等于准确率改进。


# Round113：训练内部早停与embedding瓶颈

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定2×2四配置，训练不访问验证或测试，全部epoch/模型/源冻结后验证。

|输入|训练控制|全训练epoch|训练回代/4755|训练OOF/4755|验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|raw|fixed|40|4725|4267|722|62|9/38|0.0937|1.991|
|raw|early|10|4521|4315|740|70|6/17|0.0937|1.935|
|pca|fixed|40|4474|4275|735|73|13/29|0.5376|1.975|
|pca|early|6|4316|4288|734|63|8/25|0.5376|1.953|

最佳round113_raw_early：740/798（92.7318%）。未超过751，保留第109轮研究候选。原已测Round79最终模型和历史测试记录保持。

## 训练选择与实现

小型attention宽8/4头，correct_set_mass，显式L2=0.01。每个outer-fit再分80/20；selector最多60epoch，每2epoch按inner-held正确数选择、同分取最早，连续10次未提高停止。选好epoch后，重新在整个outer-fit拟合统计/PCA并从头训练，再预测outer-held。全训练也有独立内部选择后重训。selector的模型不是部署模型，所有原题划分、曲线和epoch见partition-proofs.json、selector-progress.json。

PCA64只在当前fit的标准化embedding拟合，投影后均值/缩放也只fit；保留29其他输入量，所有PCA/统计/网络参数写入部署包。raw与pca在本轮条件下匹配比较；相对112宽度和正则也变了，不把跨轮变化单独归因于早停。

24次新拟合、四CPU线程，worker 50.178秒、900秒硬上限。PyTorch只训练，NumPy/标准库推理；训练前损失梯度、小网络导出和重排预检留档。float64原生/NumPy前向<1e-9；训练float32误差另记；缓存重载与正式严格分数重排、题序、新ID、变bank、空输入、Python整数、同组同分通过。

完整解压资产含PCA/统计/网络≤16MiB，fresh官方预测+独立评分≤30秒；训练停止后串行计时。本机验证不代表参考Xeon完整测试资格。历史自身及公开他人测试总分已知，本轮未访问/哈希/预测/评分测试；反复开发的train/validation不是独立确认。

复现：code目录train_round113_earlystop.py，再evaluate_round113_earlystop.py；已有输出拒绝覆盖。证据：runs/round113-earlystop/result.json、preflight.json、partition-proofs.json、selector-progress.json、fit-progress.json；runs/round113-evaluation/frozen-before-validation.json、all-results.json、integrity.json和各官方评分/进程日志。


# Round113学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；预定四配置完整结果后的描述性分析。

## 匹配差异（正确题数）

```json
{
  "train_oof": {
    "early_minus_fixed_raw": 48,
    "early_minus_fixed_pca": 13,
    "pca_minus_raw_fixed": 8,
    "pca_minus_raw_early": -27
  },
  "validation": {
    "early_minus_fixed_raw": 18,
    "early_minus_fixed_pca": -1,
    "pca_minus_raw_fixed": 13,
    "pca_minus_raw_early": -6
  }
}
```

## 内部选择的epoch

|阶段|输入|选定epoch|实际selector轮数|inner-held最佳正确数|
|---|---|---:|---:|---:|
|0|raw|4|24|575|
|0|pca|22|42|573|
|1|raw|6|26|578|
|1|pca|10|30|569|
|2|raw|28|48|579|
|2|pca|16|36|570|
|全训练|raw|10|30|880|
|全训练|pca|6|26|867|

## 拟合差距

|输入/控制|回代−OOF题数|
|---|---:|
|raw/fixed|458|
|raw/early|206|
|pca/fixed|199|
|pca/early|28|

缩小回代与OOF差距本身不等于准确率提升，必须同时比较OOF与验证。PCA丢弃的方向可能含判别信息；若降维后更差，不应继续盲目压缩。内部选择的epoch不同是合法训练选择，不是从官方验证挑epoch。

下一轮依据：先看以上早停在两种输入中是否方向一致，再决定保留控制；若早停和瓶颈都未改善，不继续扩大同一神经网络网格，应返回已有效的答案组增强与局部残差，以训练折外净修复为依据引入新证据。完整四配置保留，不因结果继续扫epoch/正则。本轮未运行测试，751与原冻结最终模型保留。


# Round114：基础答案组正则的完整流水线对照

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。四个基础正则固定，均重新匹配嵌套折外算术残差；模型/源/结果冻结后才访问验证。

|基础lambda|基础train OOF|完整train OOF/4755|训练回代/4755|验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|0.003|4369|4380|4554|750|78|4/5|0.02612|2.019|
|0.01|4380|4392|4510|751|78|0/0|0.02612|2.024|
|0.03|4380|4387|4457|750|78|4/5|0.02599|2.121|
|0.1|4362|4374|4413|749|76|9/11|0.02598|2.012|

最佳round114_anchor_l0p01：751/798（94.1103%）。没有超过751，保留第109轮研究候选。0.01是原751严格重复对照，不算新提升；原已测Round79模型/测试记录保持。

固定子集增强、1034组表示、22维局部残差与残差lambda0.1；只比较基础lambda0.003/0.01/0.03/0.1。与111的残差正则网格不同。每种基础模型在outer-fit内部产生自己的inner-OOF margin，再学习自己的残差；没有直接给新基础分数套旧残差。所有缩放只拟合当前fit完整组。

51次新拟合，四线程，worker 21.499秒，父进程600秒硬上限。复用108/109已有模型均以源/折/参数/OOF SHA核对，0.01控制的统计/权重1e-12、OOF/验证分数1e-10重现。数学目标与108/109已核对函数相同；检查收敛/梯度、缓存重载、零修正等于基础模型与正式接口。

完整解压资产包含基础模型、均值/缩放、残差与config≤16MiB；训练停止后每个模型fresh官方预测+独立评分≤30秒，严格分数重排、题序、新ID、变bank、空输入、Python整数、同组同分均通过。本机验证计时不是参考Xeon完整测试资格。

历史自身和公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，长期开发的train/validation不是独立确认。四配置结束，不按验证反馈追加密集参数。

复现：code目录train_round114_anchor_regularization.py，再evaluate_round114_anchor_regularization.py。已有目录拒绝覆盖。证据：runs/round114-anchor-regularization/result.json、anchor-progress.json、fit-progress.json、pair-audit；runs/round114-evaluation/frozen-before-validation.json、all-results.json、integrity.json及官方进程日志。


# Round114学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成四配置后的描述性比较。

## 每折相对原0.01控制

```json
[
  {
    "fold": 0,
    "anchor_lambda": 0.003,
    "net_vs_0p01": 1
  },
  {
    "fold": 0,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 0,
    "anchor_lambda": 0.03,
    "net_vs_0p01": -1
  },
  {
    "fold": 0,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -13
  },
  {
    "fold": 1,
    "anchor_lambda": 0.003,
    "net_vs_0p01": -4
  },
  {
    "fold": 1,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 1,
    "anchor_lambda": 0.03,
    "net_vs_0p01": -5
  },
  {
    "fold": 1,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -4
  },
  {
    "fold": 2,
    "anchor_lambda": 0.003,
    "net_vs_0p01": -9
  },
  {
    "fold": 2,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 2,
    "anchor_lambda": 0.03,
    "net_vs_0p01": 1
  },
  {
    "fold": 2,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -1
  }
]
```

基础正则0.003/0.01/0.03/0.1的完整train OOF分别4380/4392/4387/4374。原0.01仍是这四点的训练OOF最好；不能仅因正则更强、回代差距更小就称泛化更好。

局部残差相对各自基础模型的train OOF增益分别+11/+12/+7/+12。这支持残差在本轮四条件下具有增量，但不意味着总能超过原751。本轮改变基础参数同时重新匹配残差，避免分数尺度与旧残差错配。

若验证和训练OOF排序不一致，完整报告，不能把验证赢家当成稳定泛化证明。本轮结束，不继续插值密集扫lambda；后续应优先训练OOF中尚未覆盖的题意数量关系和末结果/答案联系，先提出可复现的新信息特征，再做小型匹配消融。751与所有失败/持平配置保留，测试未运行。


# Round115：公开配方核对与四格匹配实验

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。计划保存后先审计训练输入，再冻结训练源码；四候选冻结后全部官方验证。

## 预设假设与固定配置

H1：按公开源码定义对齐题目数值与局部算术解析会改变残差可用信号。H2：残差用same_fit基础分数训练可能与nested_oof不同；两种都只在当前fit训练，outer-held始终排除。本轮固定子集增强、基础lambda0.01、残差lambda0.01。原751使用残差0.1，因此legacy/nested_oof应重现750而非751。

|特征|残差margin|基础OOF/4755|完整OOF/4755|训练回代/4755|官方验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|nested_oof|4380|4390|4504|750|77|0/1|0.02591|1.866|
|legacy|same_fit|4380|4390|4507|749|77|0/2|0.02591|1.909|
|aligned|nested_oof|4380|4397|4510|751|78|1/1|0.02592|2.087|
|aligned|same_fit|4380|4392|4516|751|78|1/1|0.02591|2.122|

本批最佳round115_aligned_same_fit：751/798（94.1103%）。未超过751，保留Round109研究候选；尚未测试。
原已测Round79（验证749、历史测试368/467）模型与最终指针不变。当前751研究模型未跑最终测试。

## 训练输入审计

4755题19020候选中，题目数字列表改变45题，局部11维向量改变7673候选；可检查算式候选由13932变为13141，含不一致算式候选由322变为314。这些覆盖差异不自动代表特征更好。人工算式、受限幂、变量边界、分数、Markdown、舍入与百分比拒绝样例通过。审计不用标签/验证/测试。

## 两因子匹配效应

|起点|终点|训练OOF变化|验证修复/新增错|验证净变化|
|---|---|---:|---|---:|
|legacy/nested_oof|aligned/nested_oof|+7|2/1|+1|
|legacy/same_fit|aligned/same_fit|+2|3/1|+2|
|legacy/nested_oof|legacy/same_fit|+0|0/1|-1|
|aligned/nested_oof|aligned/same_fit|-5|0/0|+0|

解析流程包含题目分词与局部算术两部分变化，不能单独归因于幂运算；分数变化只支持本固定配置下的条件效应。验证被长期开发复用，不是新的独立泛化证明。

## 可靠性、限制与复现

29次新拟合（aligned基础13、残差16），worker25.107秒、4线程、父进程600秒硬上限；legacy基础复用108/109 SHA核对资产，legacy/nested_oof的参数1e-12、OOF/验证分数1e-10复现原750。每题权重归一、仅fit完整组scaler、梯度/收敛、零残差、缓存导出、严格候选重排1e-8、题序、新ID、变bank、空输入、Python整数与同答案同分通过。

每个最终候选独立fresh官方validation预测+评分，总计≤30秒；完整解压资产包括嵌套基础权重、scaler及config≤16MiB。本机验证计时不等于参考Xeon完整测试资格。

公开参考静态来源为CaspianW/dase7506-mp2的src/train_surface.py、src/train.py、src/arithmetic_features.py与src/question_operation_features.py，URL/只读txt快照存reference_audit_20261028。独立实现按定义对齐，未执行外部源码、未引入外部权重/数据，也未用对方自报分数选择参数。基础求解器SciPy而非sklearn、保存scaler而非折入权重、并列选择规则仍有差别；不称最终提交方法或公开成绩的完整复现。

历史自身及他人测试汇总已知并披露；本轮未访问/哈希/预测/评分测试。按用户2026-10-28确认，每批最终候选都官方验证；测试留到方法冻结后。这四个配置结束，不按验证输赢追加参数。

复现：code目录依次运行audit_round115_features.py、train_round115_reference_alignment.py、evaluate_round115_reference_alignment.py。已有输出目录拒绝覆盖。证据：runs/round115-feature-audit/audit.json，runs/round115-reference-alignment/result.json、nested-partitions.json、pair-audit，runs/round115-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json和官方进程日志。


# Round115学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成固定四条件后的描述性解释。

## 此前安排需要纠正的地方

此前把思想借鉴与同配置复现混为一谈：修改算术解析器、改用OOF残差分数并改变正则，却没有先做匹配对照。这让失败实验难以定位原因；不是网络越复杂就必然更好，也不能归因于某工具品牌。此次明确四个固定条件并重现旧控制。

## 本批能支持的结论

- legacy/nested_oof → aligned/nested_oof：训练OOF+7题，验证+1题（修复2/新增1）。
- legacy/same_fit → aligned/same_fit：训练OOF+2题，验证+2题（修复3/新增1）。
- legacy/nested_oof → legacy/same_fit：训练OOF+0题，验证-1题（修复0/新增1）。
- aligned/nested_oof → aligned/same_fit：训练OOF-5题，验证+0题（修复0/新增0）。

两种训练margin都是合法训练选择。若same_fit提高回代而OOF/验证不提高，则回代拟合不能证明泛化；若OOF与验证排序不一致，必须同时报告。对齐解析改变覆盖与最后结果判定，不应把更多/更少已检查算式直接当质量提升。

## 下一轮具体改进点

先依据本批训练OOF确定哪个变化具有跨折收益，再把题目数值分词和算术解析拆成单因子，或在严格保持同配置的情况下补齐公开训练求解器与并列选择差异。只有训练证据支持才立下一批小规模计划，避免围绕验证个别题继续密集搜索；不能根据历史测试总分作方向选择。尚未核实更大公开成绩来自相同数据划分、相同提交配置及相同资源计量，因此不把对方成绩当作本实现必达保证。

继续保留全部成功/失败资产；研究候选是否提升只按真实官方验证记录判断。原751和冻结79均保留；本批无最终测试。


# Round116：题目数字与局部算术的分离消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。计划先于训练保存，模型及源冻结后全部官方验证。

## 假设与固定设置

依据115训练OOF的解析对齐收益提出H1：两个解析变化可能贡献不等；H2：该信号在原751的固定残差正则下是否仍成立。固定子集增强、基础lambda0.01、残差lambda0.1、嵌套OOF，只切换题目数字/解答算术两个定义，不搜索新参数。

|题目数字|解答算术|基础OOF/4755|完整OOF/4755|回代/4755|官方验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|legacy|4380|4392|4510|751|78|0/0|0.02592|1.857|
|legacy|aligned|4380|4395|4515|750|77|0/1|0.02592|2.053|
|aligned|legacy|4380|4392|4510|751|78|0/0|0.02593|1.930|
|aligned|aligned|4380|4395|4515|750|77|0/1|0.02593|2.117|

本批最佳round116_qlegacy_alegacy：751/798（94.1103%）。未超过原751，保留原研究候选；尚未最终测试。

## 两因子条件效应

|起点题目/算术|终点题目/算术|train OOF变化|三fold变化|验证变化|验证修复/新增错|
|---|---|---:|---|---:|---|
|legacy/legacy|aligned/legacy|+0|[0, 0, 0]|+0|0/0|
|legacy/aligned|aligned/aligned|+0|[0, 0, 0]|+0|0/0|
|legacy/legacy|legacy/aligned|+3|[1, 4, -2]|-1|0/1|
|aligned/legacy|aligned/aligned|+3|[1, 4, -2]|-1|0/1|

## 可靠性与限制

16次新残差拟合、0次新基础拟合，worker22.392秒，4线程、父进程600秒硬上限。基础全训练/outer/inner缓存逐个SHA核对；每题归一权重、scaler仅当前fit完整组，outer-held不参与训练；两legacy参数1e-12、OOF/验证分数1e-10重现原751。

所有候选收敛/梯度、缓存导出、零残差、候选重排分数1e-8、题序、新ID、变batch、空输入、Python整数、同答案同分通过；全部fresh官方validation预测+独立评分≤30秒，完整解压资产含嵌套基础、scaler/config≤16MiB。本机验证计时不是参考Xeon完整测试资格。

解析定义来源与剩余复现差异见ROUND115_RESULTS.md；没有执行外部源码或引入外部数据/权重。历史自身/他人测试汇总已知，本批不访问/哈希/预测/评分测试。长期开发复用train/validation，不能把微小验证优势当成独立泛化证明。遵照用户确认，每批最终候选均官方验证，测试留到方法冻结后。原751及原已测79模型保留；最终79指针不变。

复现：code目录先train_round116_factor_isolation.py，再evaluate_round116_factor_isolation.py。已有目录拒绝覆盖。训练证据runs/round116-factor-isolation/result.json、nested-partitions.json、pair-audit；验证证据runs/round116-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json及官方命令日志。


# Round116学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成固定四条件后的描述性比较。

## 实验学到了什么

- legacy/legacy → aligned/legacy：训练OOF+0题（三折[0, 0, 0]），官方验证+0题（修复0/新增错0）。
- legacy/aligned → aligned/aligned：训练OOF+0题（三折[0, 0, 0]），官方验证+0题（修复0/新增错0）。
- legacy/legacy → legacy/aligned：训练OOF+3题（三折[1, 4, -2]），官方验证-1题（修复0/新增错1）。
- aligned/legacy → aligned/aligned：训练OOF+3题（三折[1, 4, -2]），官方验证-1题（修复0/新增错1）。

这次分离了115合并变化带来的解释混杂。逐折变化可判断收益是否集中一折；若训练OOF提高而验证不提高，应报告这种不一致，不能通过继续围绕验证个别题调规则消除。

## 下一次的改进入口

对解析收益使用训练OOF错误覆盖审计：分别统计因变量边界拒绝、幂支持、最后数值与最终答案不一致产生的变化，再判断是否需要增加新信号。若只靠这些统计无法纠正剩余错误，下一方向应检验题意数量关系或具有互补OOF错误的真正不同专家；不继续密集搜索同一残差正则。所有下一批先立有限假设和训练筛选规则，再固定最终候选官方验证。公开分数不能替代相同输入/标签/资源/代码版本的可复现比较；本批不作工具品牌能力结论。


## 训练OOF错误覆盖补充（两批实验完成后）

```json
{
  "status": "completed_descriptive_train_oof_only",
  "selection_or_fitting_performed": false,
  "old_oof_correct": 4392,
  "aligned_oof_correct": 4395,
  "aligned_fixed_old_errors": 16,
  "aligned_new_errors": 13,
  "old_errors_with_any_group_feature_changed": 284,
  "feature_coverage_on_original_errors": {
    "legacy": {
      "original_oof_errors": 363,
      "invalid_selected_answer": 0,
      "all_groups_identical_full22": 8,
      "all_groups_identical_arithmetic16": 45,
      "all_correct_groups_match_selected_full22": 17,
      "chosen_has_checked_mismatch_and_some_correct_group_has_none": 2,
      "neither_selected_nor_any_correct_group_has_checked_equation": 39
    },
    "aligned": {
      "original_oof_errors": 363,
      "invalid_selected_answer": 0,
      "all_groups_identical_full22": 4,
      "all_groups_identical_arithmetic16": 41,
      "all_correct_groups_match_selected_full22": 10,
      "chosen_has_checked_mismatch_and_some_correct_group_has_none": 16,
      "neither_selected_nor_any_correct_group_has_checked_equation": 46
    }
  },
  "caveat": "Feature equality is a descriptive bound for corrections sharing this representation and a fixed anchor; it does not establish the performance of new semantic signals.",
  "validation_used": false,
  "test_used": false
}
```

这里不拟合/选择模型，也不查看验证个别错误。若正确答案组与已选错组的22维向量相同，仅改变该表示的残差权重无法改变二者基础margin；需要能区分这两个组的新信息。算式缺失是覆盖不足，不能直接标成正确或错误。


# Round109（验证751）冻结测试结果

2026-10-28，用户明确授权后，先冻结既有候选，再执行一次官方完整test预测与独立评分。没有新增训练、测试个题分析或测试选模。

- 模型：round109_subsets_r0p1；基础子集增强lambda0.01，22维局部算术残差lambda0.1，嵌套OOF训练margin。
- 官方测试：**391/467 = 83.725910%**。
- 既有官方验证：751/798 = 94.110276%；训练三折OOF：4392/4755。
- 全部解压推理资产：27,423字节（0.02615MiB）。
- 完整test fresh预测+独立评分：1.808351秒；4线程。
- 本机CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon Platinum8457C完整测试资格尚未验证。
- 冻结源码和参数前后SHA核对通过。历史其他模型及公开他人测试汇总已知，长期train/validation开发复用已披露。
- 官方JSON：final_evaluation/round109-test-20261028/test-score.json；冻结版本、命令、硬件和日志同目录。
- 原Round79最终模型与历史测试记录保留。此记录不据test输赢改变模型选择，不代表已提交GitHub issue。

精确复现命令见commands.json（使用同目录code/冻结源码与checkpoint，并显式指定项目code/data）。评估脚本拒绝覆盖已有目录。


# Round117：候选审计与研究清单

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；ANALYZED_FROM_FROZEN_CACHED_EVIDENCE。0训练、0新预测、0测试访问。已有候选的官方验证结果与训练OOF重新核算，不是新的泛化确认。

## 范围与证据

历史缓存扫描：355个有官方validation评分的输出，214种所选数值答案模式；0个输出缺少配对评分或未通过读取核对，逐项留档。统一审计108–116共46个全训练OOF配置，其中40个已有最终官方验证；38个满足同折个体OOF和资源/接口证据条件。

有验证的统一候选中，按train+validation所选数值答案去重，32种行为模式，8个重复项。同bank行为相同不代表模型在新bank函数相同；资产全部保留。111未入原验证名单的配置不补测；112两个自适应选成员集成单列，不能当独立meta-OOF。

## 按预设规则保留的研究清单

|用途|候选|训练OOF/4755|训练分歧/2114|验证/798|验证分歧/355|训练修复/新增错|验证修复/新增错|三折变化|资产KiB|既有fresh秒|
|---|---|---:|---:|---:|---:|---|---|---|---:|---:|
|existing_validation_control|round109_subsets_r0p1|4392|1751|751|308|0/0|0/0|[0, 0, 0]|26.78|1.966|
|individual_research_candidate|round110_final_evidence|4398|1757|751|308|8/2|1/1|[3, 0, 3]|26.85|1.961|
|individual_research_candidate|round115_aligned_nested_oof|4397|1756|751|308|25/20|1/1|[0, 5, 0]|26.54|2.087|
|complementary_expert_for_future_training_only|round112_linear_uniform_ce|4345|1704|746|303|72/119|10/15|[-14, -19, -14]|26.00|1.971|

控制是此前依据验证选定的109，清单是后续研究候选，不替换最终选择，也不将测试总分作为规则输入。个体候选最多2个且机制不同，要求验证≥749；互补专家要求训练OOF≥4342、验证≥741并优先训练修复数。阈值事先列明，不是外部性能保证。

## 候选之间的错误互补

```json
[
  {
    "a": "round109_subsets_r0p1",
    "b": "round110_final_evidence",
    "train_a_wrong_b_right": 8,
    "train_a_right_b_wrong": 2,
    "train_oracle_upper_bound": 4400,
    "train_answer_changes": 11,
    "validation_a_wrong_b_right": 1,
    "validation_a_right_b_wrong": 1
  },
  {
    "a": "round109_subsets_r0p1",
    "b": "round115_aligned_nested_oof",
    "train_a_wrong_b_right": 25,
    "train_a_right_b_wrong": 20,
    "train_oracle_upper_bound": 4417,
    "train_answer_changes": 53,
    "validation_a_wrong_b_right": 1,
    "validation_a_right_b_wrong": 1
  },
  {
    "a": "round109_subsets_r0p1",
    "b": "round112_linear_uniform_ce",
    "train_a_wrong_b_right": 72,
    "train_a_right_b_wrong": 119,
    "train_oracle_upper_bound": 4464,
    "train_answer_changes": 214,
    "validation_a_wrong_b_right": 10,
    "validation_a_right_b_wrong": 15
  },
  {
    "a": "round110_final_evidence",
    "b": "round115_aligned_nested_oof",
    "train_a_wrong_b_right": 27,
    "train_a_right_b_wrong": 28,
    "train_oracle_upper_bound": 4425,
    "train_answer_changes": 63,
    "validation_a_wrong_b_right": 2,
    "validation_a_right_b_wrong": 2
  },
  {
    "a": "round110_final_evidence",
    "b": "round112_linear_uniform_ce",
    "train_a_wrong_b_right": 66,
    "train_a_right_b_wrong": 119,
    "train_oracle_upper_bound": 4464,
    "train_answer_changes": 208,
    "validation_a_wrong_b_right": 9,
    "validation_a_right_b_wrong": 14
  },
  {
    "a": "round115_aligned_nested_oof",
    "b": "round112_linear_uniform_ce",
    "train_a_wrong_b_right": 81,
    "train_a_right_b_wrong": 133,
    "train_oracle_upper_bound": 4478,
    "train_answer_changes": 239,
    "validation_a_wrong_b_right": 11,
    "validation_a_right_b_wrong": 16
  }
]
```

oracle是假设预先知道标签、每题选择答对专家的不可部署上界。单模型修复数高也可能同时引入更多错；未经训练隔离的条件选择检验，不宣称能够获得这些上界。

## 指标解释与11项检查

|解释风险|检查结果|
|---|---|
|1 Simpson混合|总体/答案分歧/单正确均分开；不把固定容易题造成的高总体分当难题能力|
|2 生态谬误|只描述本bank候选表现，不由总分推断单题原因|
|3 选择样本偏差|短名单按公开阈值选择，属于开发复盘，不能推断总体模型优劣|
|4 Collider|未拟合因果或条件回归；短名单筛选不作因果证据|
|5 基率忽略|分歧分母train2114、validation355；总分与分歧排名相关，不能重复计为独立证据|
|6 均值回归|旧轮赢家由反复开发产生，微小差异不称稳定改进|
|7 幸存者偏差|缺少官方配对或未验证配置均列出，不只保留赢家|
|8 多重搜索|长期多轮适应性搜索，没有独立显著性声明|
|9 分叉路径|本轮筛选规则先保存，承认规则在已知历史开发结果后制定|
|10 相关不等于因果|不同训练配方的排名不能归因于单一组件|
|11 反向因果|不作因果推断；机制来自方法定义，不由成绩倒推|

## 完整性与复现

核对每个统一配置的当前源/训练记录/全checkpoint SHA、OOF数组和同一fold SHA；OOF数组无单独ID列，其原题顺序依据冻结训练源码及共享fold记录。资源是已有官方validation fresh记录，不是本轮新benchmark，也不是参考Xeon完整测试认证。

复现：code目录运行audit_round117_candidates.py；已有目录拒绝覆盖。证据位于runs/round117-candidate-audit，包含CSV、完整JSON、异常清单、短名单、互补表、源和证据SHA。未读取final_evaluation或test输入/参考/预测/评分；既有测试汇总已知的披露保留。


# Round118：算术解析 × 最终答案证据

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。16次新残差拟合、4最终候选全部官方验证。

## 假设与控制

H1：两个已有信号的组合可能具有互补增量；H2：也可能相互抵消。固定原109题目数值分词/子集增强anchor lambda0.01、残差lambda0.1、嵌套OOF margin。四格只切换局部算术legacy/aligned和4维最终答案证据；三旧条件参数/OOF/验证分数均数值重现，不把115的不同正则/题目分词当同配置对照。

|局部算术|最终答案证据|维数|训练OOF/4755|训练回代/4755|官方验证/798|分歧/355|单正确/117|修复751错/新增错|资产KiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|False|22|4392|4510|751|308|78|0/0|26.83|2.080|
|legacy|True|26|4398|4514|751|308|78|1/1|26.92|2.102|
|aligned|False|22|4395|4515|750|307|77|0/1|26.83|2.198|
|aligned|True|26|4399|4522|750|307|78|1/2|26.92|2.764|

本批最佳round118_legacy_final：751/798（94.1103%）。

## 固定条件测试准入

计划先于训练规定：官方验证>751、训练OOF>4392、全部资源/接口核验通过，才选唯一候选冻结测试。多候选按验证、OOF、资产、名称依次选择；不用测试总分选。

无人满足全部条件，本批不触发测试。原751模型与冻结测试记录保留，不因训练信号或验证持平而事后放宽门槛。

## 四格条件效应

```json
[
  {
    "from_condition": [
      "legacy",
      false
    ],
    "to_condition": [
      "aligned",
      false
    ],
    "train_oof_delta": 3,
    "fold_deltas": [
      1,
      4,
      -2
    ],
    "validation_delta": -1,
    "validation_fixed": 0,
    "validation_new_errors": 1
  },
  {
    "from_condition": [
      "legacy",
      true
    ],
    "to_condition": [
      "aligned",
      true
    ],
    "train_oof_delta": 1,
    "fold_deltas": [
      -1,
      3,
      -1
    ],
    "validation_delta": -1,
    "validation_fixed": 1,
    "validation_new_errors": 2
  },
  {
    "from_condition": [
      "legacy",
      false
    ],
    "to_condition": [
      "legacy",
      true
    ],
    "train_oof_delta": 6,
    "fold_deltas": [
      3,
      0,
      3
    ],
    "validation_delta": 0,
    "validation_fixed": 1,
    "validation_new_errors": 1
  },
  {
    "from_condition": [
      "aligned",
      false
    ],
    "to_condition": [
      "aligned",
      true
    ],
    "train_oof_delta": 4,
    "fold_deltas": [
      1,
      -1,
      4
    ],
    "validation_delta": 0,
    "validation_fixed": 1,
    "validation_new_errors": 1
  }
]
```

## 资源、来源与复现

16次新残差拟合，0新基础拟合；四线程worker26.451秒，父进程600秒硬上限。继承全训练/outer/inner基础参数、折划分、OOF及旧控制资产逐SHA核对；mean/scale/weight1e-12、OOF/验证分数1e-10重现三个旧条件。逐pair来源/归一权重/anchor margin与旧审计一致；scaler只fit当前fit原始完整组。

梯度/收敛、重复pair、零残差、导出、严格候选重排1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分均通过。每个候选完整解压资产含基础/残差权重和scaler/config≤16MiB，fresh官方validation预测+独立评分≤30秒。这是本机验证资源记录，参考Xeon资格未认证。

历史自身及公开他人测试总分已知；本轮训练/验证未读取测试输入/参考/预测/评分，长期train/validation适应性开发不作独立泛化声明。旧方法/模型/数据/官方parser/scorer均未改；不存在外部训练数据/权重或评估时API调用。

复现：code目录train_round118_evidence_factorial.py，再evaluate_round118_evidence_factorial.py。已有目录拒绝覆盖。证据：runs/round118-evidence-factorial/result.json、nested-partitions.json、pair-audit；runs/round118-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json、selection-before-test.json与官方日志。


# Round118学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；固定四格完成后的描述性分析。

三个控制数值重现，使新组合的增量可以在同基础模型、同正则、同折下比较。训练折外与验证分开报告，回代只描述拟合。

- ['legacy', False] → ['aligned', False]：训练OOF+3题（三折[1, 4, -2]），验证-1题（修复0/新增错1）。
- ['legacy', True] → ['aligned', True]：训练OOF+1题（三折[-1, 3, -1]），验证-1题（修复1/新增错2）。
- ['legacy', False] → ['legacy', True]：训练OOF+6题（三折[3, 0, 3]），验证+0题（修复1/新增错1）。
- ['aligned', False] → ['aligned', True]：训练OOF+4题（三折[1, -1, 4]），验证+0题（修复1/新增错1）。

若组合对齐后没有保留最终答案证据的原增量，说明两个信号在本线性残差表示下可能重复或产生权重折衷；不能仅按各自单独净增相加预测组合分数。若OOF提高但验证不提高，报告这种排序不一致，不继续围绕验证个别错题调权。

本四格结束不追加同参数网格。后续可独立检验“何时采用互补专家”的输入条件可分性；需要outer-fit内部产生专家OOF并学习门控，再评估outer-held。117的oracle只能表示潜在互补空间，不是可部署成绩，也不能把现成全OOF上的门控拟合叫无偏。

测试是否执行仅由上述事先门槛决定；历史已知测试汇总不参与配置选择。


# Round119：两种专家的嵌套条件选择

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。2个固定输出、53次新拟合。

## 假设与实现

主模型109的组pair-logistic算术残差与112的候选uniform-CE线性专家具有不同错误。检验只用置信度8维、或再加26维算术/最终答案差异，能否学习何时采用专家。选择器lambda0.1、阈值0.5固定；答案相同时不切换，两模型均错的分歧题对选择监督中性。scaler只fit当前fit专家分歧题。

outer-fit内重新产生两个完整专家的inner-OOF；主模型的inner残差又使用inner-fit内三折基础OOF margin。外层held标签不参与任何内层拟合，避免直接在同一全OOF上训练门控再声称其拟合分数为无偏评估。最终门控用全训练专家OOF拟合，部署用两个full-train专家。

|模式|嵌套OOF/4755|嵌套切换|训练修复/新增错|三折净变化|验证/798|分歧/355|验证切换|验证修复/新增错|资产KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|confidence8|4387|62|24/29|[-2, -5, 2]|751|308|3|1/1|54.00|2.786|
|evidence34|4389|59|22/25|[-2, -3, 2]|751|308|3|1/1|54.61|3.283|

最佳round119_evidence34：验证751/798，嵌套OOF4389/4755。

两条件均未通过预设的validation>751且嵌套OOF>4392门槛，本批不测试；不事后调阈值。

## 训练、来源与资源

worker40.434秒、4线程CPU、1800秒父进程硬限。新拟合计数：27 innermost基础、9 inner主残差、9 inner CE专家、6 outer选择器、2 full选择器，共53。CE固定40epoch/lr0.003/L2.001/batch128，seed按计划固定；不选验证epoch。原outer专家重放分数与已存OOF1e-10匹配。

源/计划/继承参数/分区SHA及拟合范围核对；数值梯度、收敛、重复样本不变、torch-float64/NumPy导出、零切换严格等于主模型、候选重排分数1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分通过。完整资产含两个专家及全部scaler/config/gate≤16MiB，各fresh官方validation预测+独立评分≤30秒。本机计时不是参考Xeon资格认证。

历史自身及公开测试汇总已知，长期train/validation开发复用披露。本训练/验证不访问test输入/参考/预测/评分，不按测试总分选模。全部旧源/资产、官方数据/parser/scorer和已有冻结版本保留。

复现：code目录train_round119_nested_switch.py，再evaluate_round119_nested_switch.py；已有目录拒绝覆盖。证据：runs/round119-nested-switch/result.json、innermost-partitions.json、inner-progress.json、gate-progress.json、pair-audit；runs/round119-evaluation/frozen-before-validation.json、all-results.json、integrity.json、selection-before-test.json和官方日志。


# Round119学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；固定两选择器完成后的描述性结论。

117审计的72个可修复错误是oracle互补空间，不是普通门控必能获取的增益。本批用完整嵌套专家评估实际可获取的修复，同时统计新增错误。

- confidence8：嵌套训练修复24/新增29，三折[-2, -5, 2]；验证修复1/新增1。
- evidence34：嵌套训练修复22/新增25，三折[-2, -3, 2]；验证修复1/新增1。

若门控几乎不切换，说明在固定正则和可观测特征下没有学到足够可靠的采用专家条件；若切换后新增错误更多，则互补空间不等于可识别空间。置信度不足、有限监督和专家从inner到full训练的数据规模变化，都可能影响门控迁移，不能仅凭本比较确定单一原因。

此批结束不追加阈值/正则；是否测试由训练前门槛决定。后续若研究条件选择，应先用训练侧错误机制与可观测信号证据说明新增特征，而非反复按验证错题修规则。


# Round110：验证751持平候选的冻结测试

2026-10-29，用户明确要求验证持平候选也可测试。测试前仅按既有train/validation选定round110_final_evidence并冻结，未使用其测试总分选模。

- 官方test：**391/467 = 83.725910%**。
- 官方validation：751/798；训练OOF4398/4755，相对109三折净增3/0/3。
- 配置：原109子集增强anchor lambda0.01，原算术22维+最终答案证据4维，残差lambda0.1，nested-OOF margin。
- 完整解压推理资产：27,493字节；四线程本机fresh完整test预测+独立评分1.887219秒。
- 本机CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon资格尚未验证。
- 预先选择记录selection-before-test.json、冻结源码/权重/SHA、命令、官方JSON和资源记录保存在final_evaluation/round110-test-20261029。
- 代码/资产前后SHA通过；无新训练、参数调整或测试个题分析。原109、79及其历史测试记录保留。
- 研究候选指针在测试前已按train/validation选择110，测试后只补记总分，不据输赢再更换。原79最终提交字段未改；未创建GitHub issue。

历史其他模型及公开他人test总分已知，长期train/validation适应性开发和此次额外冻结评价如实披露。此前118/119门槛属于代理自行设定的批次规则，不是课程要求；用户此次明确授权修正该规则用于此冻结候选。

## 启动记录补充

第一次启动在构造候选元数据时因重复status字段停止，发生在FROZEN_MODEL、预测/评分命令与进程创建之前，测试未开始。已核对不存在预测、评分或运行结果文件，将完整启动快照及PREFLIGHT_FAILURE.json保存在final_evaluation/round110-preflight-failed-20261029。修复仅将元数据合并改为显式覆盖，未改模型、特征、参数或评估配置；随后仅运行了一次官方完整测试预测及独立评分。


# Round120：题目词与答案组特征交互

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。12次新拟合、4最终输出全部官方验证。

## 假设与设计

固定完整110父模型，学习题目词与候选证据的显式交互。题目独立加性项在同题候选间会抵消，交互则能为不同题目条件学习不同候选证据权重。题目采用固定128维有符号BLAKE2b unigram/bigram哈希并L2归一；无词表/IDF/外部语料。候选证据为原6维答案数值、原26维格式/算术/最终答案、或两者合并32维。历史已有问题文本及语义尝试，本批不声称首次问题条件化。

scaler只fit当前fit原始组，新增残差按每题平均pair logistic，L2固定0.1。训练偏置来自当前fit父模型的回代margin；这是same-fit offset策略，outer-held完全排除，不假称inner-OOF offset。稀疏训练，NumPy推理。

|模式|系数数|训练OOF/4755|回代/4755|三折净变化|验证/798|分歧/355|单正确/117|修复751错/新增错|资产KiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|
|control|0|4398|4514|[]|751|308|78|0/0|27.12|1.997|
|question_numeric|768|4398|4515|[0, 0, 0]|751|308|78|0/0|33.95|2.741|
|question_evidence|3328|4394|4521|[-2, 0, -2]|752|309|79|1/0|54.27|2.836|
|question_both|4096|4396|4523|[-1, 1, -2]|752|309|79|1/0|60.36|2.806|

本批最佳round120_question_both：752/798。

无人满足训练前固定的validation≥751且OOF>4398及全部核验门槛，本批不触发测试。验证持平可以准入，但须有更好的训练折外证据；不事后改变门槛。

## 核验、资源与复现

训练worker15.826秒，4线程、父进程600秒硬限。三个交互各3outer+1full=12次新拟合；原110控制0新拟合。父fold held分数1e-10复现保存OOF；源/计划/旧参数/新资产SHA冻结核对，scaler及每题权重仅当前fit。梯度、重复pair、收敛、零交互严格等于父、导出、候选重排1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分通过。

全部资产包含父模型、scaler、交互权重和config≤16MiB；每个fresh官方validation预测+独立评分≤30秒。本机验证计时不是参考Xeon完整测试认证。本训练/验证未访问test输入/参考/预测/评分；历史测试汇总已知及长期自适应开发如实披露。旧模型、数据和官方parser/scorer均未改。

复现：code目录train_round120_question_interaction.py，再evaluate_round120_question_interaction.py。已有目录拒绝覆盖。证据：runs/round120-question-interaction/result.json、fit-progress.json、pair-audit；runs/round120-evaluation/frozen-before-validation.json、all-results.json、integrity.json、selection-before-test.json及官方日志。


# Round120学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；固定四输出后的描述性解释。

额外question×feature系数确实通过目标优化并影响输入分数，但训练目标下降或回代提升不能当作折外提升。问题词条件信息在此固定哈希/特征/正则/offset下是否有用，应看三折及官方验证。

- control：训练OOF4398、三折[]，验证751；相对751修复0/新增0。
- question_numeric：训练OOF4398、三折[0, 0, 0]，验证751；相对751修复0/新增0。
- question_evidence：训练OOF4394、三折[-2, 0, -2]，验证752；相对751修复1/新增0。
- question_both：训练OOF4396、三折[-1, 1, -2]，验证752；相对751修复1/新增0。

失败不能证明题目语义本身无用：哈希碰撞、词袋不能表达实体/关系、候选统计有限、稀疏条件监督及same-fit margin均可能限制本实现；本轮不能单独识别其原因。本四输出结束，不按验证追加词表或调整桶/正则。后续若延续，应先用训练OOF量化新修正的幅度、错误覆盖与表示碰撞，再决定是强度校准还是增加可验证的新关系信息。不通过测试逐个筛选这些模型，也不将旧测试总分用作训练方向依据。


# Round120验证752候选：追加冻结测试结果

2026-10-29。在看到四个官方验证结果后，按最高validation、同分最高训练OOF选择round120_question_both；测试之前写选择记录并冻结全部代码/参数。

- 官方test：**391/467 = 83.725910%**。
- 官方validation：752/798 = 94.235589%；训练OOF4396/4755，低于父110的4398。
- 方法：冻结110父模型+固定128维题目词哈希×32维数值/算术/最终答案证据交互，L2.1，same-fit父margin。
- 全部解压推理资产：61,805字节；4线程本机完整fresh test预测+独立评分2.296909秒。
- 本机CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon资格未验证。来源/资产/选择记录SHA前后核对通过。
- 原自动测试门槛OOF>4398未通过，原记录保持false。本次基于用户已有授权的追加冻结评价是看到验证结果后的开发决定，不称预注册准入成功，也不称稳定泛化提升。
- 未新增训练、改参、读取测试个题或按测试输赢再选模型；其他752/751候选未测。原110/109/79和历史结果保留。
- 官方JSON、完整冻结源/权重、命令、硬件与日志：final_evaluation/round120-test-20261029。研究候选在测试前已按train/validation选定120，测试后只补总分。原79最终提交字段保持，未创建GitHub issue。

历史测试汇总已知及长期自适应train/validation开发如实披露。评价本身不使一题验证增益变成独立统计证据。


# Round121：题目交互的正则参数消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。48新拟合，4个最终输出全部官方验证。

## 假设与训练诊断

120数值交互在训练OOF一道选择都未改变；证据交互改8题却修2/新增6，说明修正偏小和方向带噪声并存。固定110父模型、原三类特征及哈希，只比较λ=1/.1/.01/.001/.0001。训练OOF选每类一档，平分取较大λ；未选参数不看验证。

|特征|λ|训练OOF/4755|相对110修复/新增|三折净变化|训练选中|
|---|---:|---:|---|---|---|
|question_numeric|1.0|4398|0/0|[0, 0, 0]|是|
|question_numeric|0.1|4398|0/0|[0, 0, 0]|否|
|question_numeric|0.01|4393|2/7|[-2, -3, 0]|否|
|question_numeric|0.001|4383|17/32|[-7, -2, -6]|否|
|question_numeric|0.0001|4356|37/79|[-18, -10, -14]|否|
|question_evidence|1.0|4398|0/0|[0, 0, 0]|是|
|question_evidence|0.1|4394|2/6|[-2, 0, -2]|否|
|question_evidence|0.01|4389|15/24|[-1, -6, -2]|否|
|question_evidence|0.001|4348|49/99|[-19, -15, -16]|否|
|question_evidence|0.0001|4261|80/217|[-53, -40, -44]|否|
|question_both|1.0|4398|0/0|[0, 0, 0]|是|
|question_both|0.1|4396|3/5|[-1, 1, -2]|否|
|question_both|0.01|4380|14/32|[-2, -7, -9]|否|
|question_both|0.001|4344|49/103|[-20, -13, -21]|否|
|question_both|0.0001|4261|78/215|[-57, -43, -37]|否|

## 官方验证

|最终候选|λ|训练OOF|验证/798|分歧/355|单正确/117|相对752修复/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|0.1|4396|752|309|79|0/0|60.36|2.984|
|round121_question_numeric_l1p0|1.0|4398|751|308|78|0/1|33.95|2.818|
|round121_question_evidence_l1p0|1.0|4398|751|308|78|0/1|54.27|2.957|
|round121_question_both_l1p0|1.0|4398|751|308|78|0/1|60.36|2.885|

本轮开发选择：round120_question_both，验证752/798、训练OOF4396/4755。
只根据train/validation排序；新候选未胜出，保留120，不新增test。

## 解释与局限

网格包含比原设置强10倍和弱1000倍的正则；应结合完整表格判断更弱正则是否增加OOF净收益。训练目标下降、权重增大或回代上升均不等于泛化提升。本轮未分离哈希碰撞、语言关系不足及same-fit offset影响；不能把失败解释为题目语义无用。参数已用OOF选择，因此所选OOF是开发指标。长期train/validation适应及历史测试汇总已知如实披露，不做独立显著性或因果主张。

## 资源、核验与复现

45outer+3full=48新拟合，worker21.540秒，总4线程，600秒硬限。三个λ=.1严格复现120折外分数1e-10。fit-only scaler/每题权重/梯度/收敛/导出/零修正/重排/题序/新ID/变batch/空输入/Python整数/同答案同分核验通过。所有父参数和官方输入/解析/评估工具未修改，源/计划/参数SHA核对通过。全部资产≤16MiB，fresh validation预测+独立评分≤30秒；未做参考Xeon完整test认证。

复现：code目录train_round121_regularization.py，再evaluate_round121_regularization.py；存在证据目录则拒绝覆盖。证据位于runs/round121-train-diagnosis、round121-regularization、round121-evaluation。

## 统计解释检查（11/11）

1 Simpson：报告总体、分歧、单正确及三折，不以总体代替全部分组。2 Ecological：只推断本批题目表现。3 Berkson：数据固定且分歧分布不同，不能外推总体。4 Collider：无因果调整主张。5 Base rate：报告分母和容易的一致题占比。6 Regression to mean：小增益及自适应选择不称稳定提升。7 Survivorship：15训练配置含失败表现全部保留，4最终输出全验证。8 Look-elsewhere：有限参数搜索及全部结果披露，不报显著性。9 Forking paths：计划冻结、旧设置复现、未按验证追加。10 Correlation/causation：噪声和强度是当前实现的操作性解释，不推广为唯一因果。11 Reverse causality：无因果方向主张。


# Round122：答案组Embedding子集稳定性

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。10新拟合，2最终输出官方验证。

## 假设与设计

在完整120父模型上，学习相同答案组的非空子集Embedding评分稳定性。支持度/支持比例/答案组数固定为完整组，保留Embedding均值与离散度变化。六维为delta min/max/mean/std、singleton std及删一成员std。单例组全零。不是重做108训练增强。train覆盖：父359错中247题有多成员组，112题全单例，后者新增特征不能改变排序。只按train OOF从三档λ选一档，随后官方验证。

|λ|训练OOF/4755|修复父错/新增错|三折净变化|选中|
|---|---:|---|---|---|
|0.1|4392|2/6|[0, -3, -1]|False|
|0.01|4393|3/6|[0, -2, -1]|True|
|0.001|4393|4/7|[1, -2, -2]|False|

|最终候选|训练OOF|回代|验证/798|分歧/355|单正确/117|修复752错/新增错|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|4396|4523|752|309|79|0/0|60.36|2.757|
|round122_stability_l0p01|4393|4527|752|309|79|0/0|61.47|3.213|

开发选择：round120_question_both，验证752/798。保留原120，未新增test。

## 核验与局限

9outer+1full=10拟合，worker24.157秒，总4线程，600秒硬限。父held分数严格复现，梯度/重复pair/每题权重/fit-only scaler/收敛/导出/零修正/单例不改排序/重排等接口通过。全部资产≤16MiB；fresh validation预测+独立评分≤30秒，参考Xeon未验证。

same-fit frozen parent offset并非inner-OOF offset。子集信息只覆盖多成员组，且与旧离散度相关；覆盖不等于能够识别正确答案。全部3训练配置与2验证输出保留，不按验证追加网格。长期自适应开发、历史测试汇总已知如实披露，新测试不用于训练/选择。统计解释11/11检查：分层及三折防Simpson误读；不做生态/筛选/碰撞因果推断；报告分母；小增益与回归均值谨慎；全部失败保留；披露多重搜索与路径；不声称因果或反向因果。只作描述，不报独立显著性。

复现：code目录train_round122_subset_robustness.py，然后同脚本--evaluate；存在输出目录则拒绝覆盖。证据runs/round122-coverage、round122-subset-robustness、round122-evaluation。


# Round121–122学习记录与结论

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；完成两批有限实验，描述性解释。58新拟合、18训练配置、4个新最终候选、6次官方验证（含两次既有控制）。

## 121：参数不足是不是原因？

训练前OOF诊断显示数值交互修正很弱，但方向有噪声。比较λ=1/.1/.01/.001/.0001后，更弱正则没有产生训练折外净收益。
- 数值交互：λ.1→.0001，OOF4398→4356；最弱修复37/新增79。
- 证据交互：λ.1→.0001，OOF4394→4261；最弱修复80/新增217。
- 合并交互：λ.1→.0001，OOF4396→4261；最弱修复78/新增215。
- 按训练OOF选出的三类λ均为1，均OOF4398；官方验证均751，低于当前752。

这里能够排除“只要降低这套交互的正则就能提高准确率”这一具体猜测。无法证明其他参数或其他语义表示无用。不能因为更多错误被修复而忽略更多新错误。下一批不继续扩展当前词哈希×组统计的λ网格。

## 122：训练用过子集，推理稳定性是否还有增量？

在完整120父模型之上增加6维子集Embedding评分稳定性，固定支持度列，枚举非空组内子集。父训练OOF359错中247题有多成员组，112题全单例，无可用组内变化。
- λ.1 / .01 / .001的训练OOF分别4392 / 4393 / 4393；同分取较大λ，选择.01。
- 选中版修复父错3、增加6错，三折[0,-2,-1]；训练回代4523→4527没有转化为折外净收益。
- 官方验证752/798，与父同分；验证选择实际改变0题。新模型资产更大、OOF较低，按训练前规则保留原120。

子集稳定性是同一线性anchor产生的摘要，与既有Embedding离散度有相关性；本轮不能证明它带来了独立的新正确性信息。其盲区和修复/新增已明确，下一批不把这些摘要继续堆叠作为默认方向。

## 后续实验的证据要求

下批先检查训练错误是否需要目前输入摘要缺少的题目数量关系、实体对应或跨步骤一致性信号。固定一小组可自动验证的关系类型，用train量化覆盖与误触发后再设计消融；不根据验证个题硬编码规则。若只是重新组合旧分数，需要先有训练折外净收益，再进入官方验证。此处是下一步研究建议，不声称已实现关系验证器。

当前研究模型仍为120：验证752/798（94.235589%）。本批没有新test评价、没有test个题分析或test调参。历史测试汇总已知、自适应train/validation开发继续披露。

## 约束与复现状态

六次fresh官方validation预测+独立评分最慢3.213秒；全部推理资产最大62,942字节（61.47KiB），均小于30秒及16MiB。总4线程，两个训练worker各600秒硬限。参考Xeon资格未认证。
源/计划/旧参数/新资产完整性、严格父对照、导出与重排等接口已核验。旧研究120及原79提交候选保留。

完整结果：ROUND121_RESULTS.md、ROUND122_RESULTS.md；机器记录code/runs/round121-122-closeout/result.json。复现指令及每次拟合/官方预测/评分日志在各计划及runs目录；原目录拒绝覆盖。


# Round123：数字来源与最终计算链消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。21新拟合，4最终输出官方验证。

## 假设与输入审计

12/14等历史已有正确链/数量覆盖，本轮区分最终祖先中的真假运算并学习软修正。仅按训练信息设计和选择。grounding/ancestry/both对359训练错的差异覆盖300/256/308题；覆盖不是可修复数。最终祖先可见算术错的161候选中149错误，但父错仅1题选到此类候选，剩余简单算术空间很小。放宽来源的完整真链3904候选仍有752错误，因此不以真链证明题意正确。

|特征|λ|训练OOF/4755|修复父错/新增错|三折净变化|选中|
|---|---:|---:|---|---|---|
|grounding|0.1|4396|2/2|[-1, -1, 2]|False|
|grounding|0.01|4397|6/5|[1, -2, 2]|True|
|ancestry|0.1|4407|16/5|[4, 2, 5]|True|
|ancestry|0.01|4407|24/13|[3, 4, 4]|False|
|both|0.1|4403|15/8|[-1, 3, 5]|False|
|both|0.01|4404|26/18|[3, 4, 1]|True|

|最终候选|训练OOF|回代|验证/798|分歧/355|单正确/117|修复752错/新增错|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|4396|4523|752|309|79|0/0|60.36|2.860|
|round123_grounding_l0p01|4397|4524|752|309|79|0/0|61.59|3.626|
|round123_ancestry_l0p1|4407|4524|749|306|78|1/4|61.87|3.658|
|round123_both_l0p01|4404|4519|754|311|79|5/3|62.01|3.598|

开发选择：round123_both_l0p01，验证754/798。新候选按计划选出，须一次独立冻结test。

## 核验与局限

18outer+3full=21拟合，worker25.092秒，总4线程，600秒硬限。父held分数1e-10复现，纯输入缓存/梯度/重复pair/每题权重/fit-only scaler/收敛/导出/零修正/重排等接口通过。全部资产≤16MiB；fresh validation预测+独立评分≤30秒，参考Xeon未验证。

首次自检在数据/训练前发现通用常数遮蔽前序运算，已修正优先级，失败及原源码保留，完成审计输出新v2目录。same-fit frozen parent offset并非inner-OOF。数值相同不能确定实体，部分公式/文字未知；完整算术真链不能验证题意。六训练配置和四最终验证输出全部保留，未按验证追加网格。长期自适应train/validation及已知历史测试汇总如实披露，未用新test调参或分析个题。

## 统计解释检查11/11

1 Simpson：分歧/单正确及三折同时报告。2 Ecological：只对该固定题库作描述。3 Berkson：候选集筛选分布限制外推。4 Collider：不以条件子集作因果推断。5 Base rate：信号同时报告正确/错误计数和分母。6 Regression to mean：小变动与开发选择不称稳定收益。7 Survivorship：六训练配置含失败全部保留。8 Look-elsewhere：披露有限搜索和历史多次比较，不报显著。9 Forking paths：计划冻结、参数先按OOF选择。10 Correlation/causation与11 Reverse causality：不作因果方向主张。

复现：code目录audit_round123_grounded_chain.py、train_round123_grounded_chain.py，然后训练脚本--evaluate；原输出拒绝覆盖。证据runs/round123-train-audit（首次失败）、round123-train-audit-v2、round123-grounded-chain、round123-evaluation。


# Round123：验证754候选的冻结测试

2026-10-29。训练前规则已固定，按最高validation、同分OOF/资产选择round123_both_l0p01；新test预测前冻结全部代码、参数和选择。

- 官方validation：754/798 = 94.486216%；相对120修复5/新增3。
- 训练OOF：4404/4755，相对120净增8，三折[+3,+4,+1]。
- 官方test：**390/467 = 83.511777%**。
- 全部解压推理资产：63,495字节；总4线程，本机完整fresh test预测+独立评分2.778695秒。
- CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon资格未验证。源/参数/计划/选择记录SHA前后核对通过。
- 研究候选在test前已按train/validation选定；评分后只补总分，未训练、改参、分析test个题或根据test再选模型。其他123版本未测。原120/110/109及原79保留，未创建提交issue。
- 原训练前选择规则通过，无事后门槛更改；已知历史测试汇总与长期自适应开发继续披露。

官方JSON、冻结源/权重、命令、日志、硬件：final_evaluation/round123-test-20261029。


# Round123学习记录：计算链信号的收益与局限

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；21次新拟合、6训练配置、4个最终输出官方验证，1个按训练前规则选出的冻结test。

## 本轮实际改变与结果

固定120父模型，新增数字来源/最终计算链的软特征，不修改官方解析器。重点区分最终祖先节点与无关算式，并允许未知保持未知。

|输出|训练OOF/4755|相对父三折|验证/798|验证修复/新增|
|---|---:|---|---:|---|
|父120|4396|—|752|—|
|grounding .01|4397|+1/-2/+2|752|0/0|
|ancestry .1|4407|+4/+2/+5|749|1/4|
|both .01|4404|+3/+4/+1|754|5/3|

组合版按训练前validation/OOF/资产规则在test之前胜出，研究候选指针已选123；没有因为测试结果重新选模型。
组合版冻结test为390/467（83.511777%）；既有120测试391/467。验证净增2、训练OOF净增8，但本次test少1，不能称测试突破或稳定泛化提升。旧120及其资产/评价仍保留。

## 解释：哪些假设得到支持？

1. 题目数字来源和最终链的特征差异覆盖父359训练错中的308题，说明比只看显式坏算式有更广的机会。覆盖不等于识别正确答案的能力。
2. 最终链存在可见算术错的161训练候选中149错误，但父359错仅1题选到此类候选。旧模型已经避开绝大多数可见算术错，只强化该惩罚的空间很小。
3. 即使放宽数字来源并整条算术为真，3904训练候选仍有752错。它不能证明题目数量关系、实体、单位或目标正确。完整真链不应设为硬规则。
4. 仅ancestry训练三折都增益，官方验证仍下降3题；组合版反而验证增益。不能只按OOF最高或单个特征系数正负断言哪种解释最可靠。

## 测试前完成的训练贡献诊断

`runs/round123-contribution-diagnosis/result.json`在本次test前计算，未读validation/test、未拟合或选新输出，只将ancestry .1已有系数按块置零检查train OOF敏感度。

|置零块|OOF正确数|相对完整ancestry4407|
|---|---:|---:|
|最终匹配公式存在性|4409|+2|
|链长度及链外公式|4403|-4|
|祖先算术错|4407|0|
|未知叶子|4407|0|
|完整真链标志|4407|0|
|题目数字覆盖|4402|-5|

特征相关且没有重新拟合，以上是固定权重敏感度，不能解释为独立因果贡献，也不是新验证分数。未将这些置零输出送往validation/test。

## 下一次可检验改进

由上述**测试前训练诊断**提出：对ancestry/both做去掉“最终公式存在性”的匹配重训练消融，并保持父模型、折、正则和其他输入一致。先重新fit并看OOF修复/新增，再冻结最终输出官方验证，不能直接用置零4409当成新模型性能。还应单独核验链长度/链外公式和题目数字覆盖是否仅利用了表达风格。此处记录待研究假设，尚未执行这些新训练。

本次test仅记录已选冻结版本的汇总，不使用测试个题或输赢来改变上述方向。

## 资源、完整性与异常

4线程，训练worker25.10秒，600秒硬限；四个fresh validation最慢3.658秒；选中模型完整fresh test预测+独立评分2.779秒；全部推理资产最大63,495字节（62.01KiB），均满足30秒及16MiB。本机i5-11400H，参考Xeon未验证。
父fold复现、纯输入缓存、梯度、每题权重、重复pair、导出、零残差与重排/题序/ID/变batch等接口、源/计划/父新资产SHA通过。首次fixture失败发生于加载数据和拟合前，已保存原始源码/错误并修复常数优先级，完成审计写v2目录；没有test重试。
长期自适应train/validation及历史测试汇总已知披露，不做独立统计显著或唯一因果判断。原79最终提交字段不变，未提交GitHub issue。

完整报告ROUND123_RESULTS.md；冻结评价FINAL_TEST_ROUND123_RESULT_2026-10-29.md；机器闭环code/runs/round123-closeout/result.json。


# Round124：最终公式存在性匹配重训练消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。16新拟合、4最终输出官方验证。

## 假设与匹配设计

123测试前train-only置零诊断提示移除显式最终公式存在项可能有收益；本轮真正删除mean/max两列后重训练。固定120父、特征提取、折、scaler定义和same-fit offset；ancestry λ.1、both λ.01不扫参。其他链特征仍可编码存在性，因此只检验删除这两列的干预，不能称消除了该信息。

|条件|维度|λ|训练OOF/4755|回代/4755|修复匹配控制/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry_control|18|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.90|3.592|
|ancestry_drop_presence|16|0.1|4408|4525|2/1|[1, -1, 1]|749|306|78|2/7|61.84|3.954|
|both_control|24|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.09|3.684|
|both_drop_presence|22|0.01|4409|4522|9/4|[2, -1, 4]|751|308|79|1/4|62.03|4.361|

## 开发选择

两个新输出均未严格胜过当前(validation754, OOF4404)；保留123，不新增test，不根据验证扩展条件。

## 核验和局限

四条件各3outer+1full=16拟合；worker26.987秒，总4线程，600秒硬限。两个control全部fold/full mean/scale/weight及OOF按1e-10复现123；官方validation逐分数复现749/754。缓存纯输入、fit-only scaler、每题权重、梯度/重复pair、收敛、导出/零残差与重排等接口通过；官方源码、旧父/新资产、计划SHA核对。全部资产≤16MiB，fresh validation预测+独立评分≤30秒，本机不是参考Xeon资格。

训练前诊断依赖长期开发train，验证也长期适应。训练折外与验证变化需分别报告；不把置零未重训的4409当作本轮性能，不报独立显著或因果结论。已知历史test汇总披露；本批拟合/选择未读test输入、参考、预测或评分，未改官方解析和原始数据。

统计解释11/11：报告分层和三折（Simpson）；只对本题库推断（Ecological）；固定筛选分布（Berkson）；无因果调整（Collider）；报告分母（base rate）；小增益/开发选择不称稳定（regression to mean）；四输出全报（survivorship）；有限搜索及历史多比较披露（look-elsewhere）；计划冻结（forking paths）；不作因果及反向因果主张。

复现：code目录train_round124_presence_ablation.py，再加--evaluate。原证据目录拒绝覆盖。证据runs/round124-presence-ablation、round124-evaluation。


# Round124学习记录：固定系数诊断与重新拟合的区别

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16拟合、4官方验证，2新候选+2严格控制；未新增test。

## 本轮结果

|方法|原训练OOF→删列后|相对原三折|原验证→删列后|
|---|---|---|---|
|ancestry，λ.1|4407→4408|+1/-1/+1|749→749|
|both，λ.01|4404→4409|+2/-1/+4|754→751|

组合删列版在训练OOF修复9题、增加4错，但官方验证只修复原754的一题、增加4错。原123研究模型754/798保留，两个新版本未通过预先开发排序规则，未新增测试。删除的只是显式final_has_scalar_equation的mean/max，其他特征仍可能包含存在性信息，不称完全移除此信息。

## 学到了什么

1. 123测试前的固定系数置零诊断只能形成待验证假设。真正重训练后ancestry OOF是4408，不能拿之前未重训的4409当作本轮结果；组合重训练恰巧也为4409，属于不同模型。
2. 这项删除在训练划分有净收益，在验证未兑现；训练三折中也有一折下降。不能把该项简单认定为普遍有害，继续按验证删除小特征会增加自适应选择风险。
3. 两个控制fold/full mean/scale/weight、OOF和官方validation分数均严格复现，因而本次差异不是父模型、parser或不同正则的混杂。

## 补充训练诊断：父模型margin的乐观程度

新残差目前用same-fit frozen parent margin训练。以下只看train，没有新拟合、validation或test访问；比较描述当前差距，不证明它造成了验证下降。

|父120分数来源|题数|正确数|准确率%|每题归一pair logloss|平均pair margin|
|---|---:|---:|---:|---:|---:|
|full same-fit|4755|4523|95.1209|0.206198|2.949183|
|saved outer OOF|4755|4396|92.4501|0.302900|2.727199|
|fold0 same_fit|3170|3049|96.1830|0.181025|3.105511|
|fold0 outer_held|1585|1463|92.3028|0.309009|2.726168|
|fold1 same_fit|3170|3049|96.1830|0.179793|3.123739|
|fold1 outer_held|1585|1461|92.1767|0.305993|2.647429|
|fold2 same_fit|3170|3045|96.0568|0.183247|3.045271|
|fold2 outer_held|1585|1472|92.8707|0.293763|2.806761|

## 下一步可检验方向

固定原123保留全部特征的ancestry/both及各自正则，对比same-fit margin和真正inner-OOF父margin。只改变修正训练时看到的父分数，先做匹配训练折外比较，再冻结候选官方验证。这是由训练margin诊断形成的待检验假设，尚未执行，不声称已解决OOF/验证分歧。

**实现约束：**不能直接把全train保存的parent OOF抽出outer-fit行用于该折残差训练，因为其他折parent可能训练过当前outer-held。需要在每个outer-fit内部重新拟合或严格核对可复用的inner父模型及其scaler/训练索引，完整父120的各层也须排除held。最终full fit可使用父120对完整train的既有OOF，但新残差的外层OOF仍需上述嵌套过程。

## 资源与完整性

4线程，16拟合worker26.987秒；fresh官方validation预测+独立评分最慢4.361秒；全部推理资产最大63,577字节（62.09KiB）。满足本机30秒/16MiB约束，参考Xeon未认证。源/计划/父新资产SHA、缓存、每题权重、梯度/重复pair、导出/零修正、重排/题序/新ID/变batch等通过；旧123/120及原79提交字段保留。

长期自适应train/validation及已知历史测试汇总披露；本批没有test输入/预测/评分访问或测试驱动选择。统计解释11/11见ROUND124_RESULTS.md；只作描述，无显著性或唯一因果判断。

完整结果ROUND124_RESULTS.md；机器闭环code/runs/round124-closeout/result.json；训练margin诊断code/runs/round124-margin-gap/result.json。


# Round125：same-fit与真正嵌套OOF父margin

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。34新拟合、4最终输出官方验证；36个旧anchor核验复用。

## 假设与干预

124训练诊断显示父same-fit相对held更乐观；本轮只改变链残差训练margin来源，固定原123特征/正则及部署父120，不删列、不搜参数。same-fit为原配方；nested_parent_oof在每个outer-fit内构造完整120父模型的3-fold OOF，所有父层排除outer-held。

|特征|margin|λ|训练OOF/4755|回代/4755|相对匹配控制修复/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry|same_fit|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.77|3.657|
|ancestry|nested_parent_oof|0.1|4406|4522|5/6|[-2, 1, 0]|750|307|79|1/5|61.78|3.561|
|both|same_fit|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.91|3.625|
|both|nested_parent_oof|0.01|4399|4522|9/14|[1, -6, 0]|754|311|79|0/0|61.91|3.609|

## 选择

两个新输出未严格胜过当前(验证754, OOF4404)。保留原123，不新增test，不按验证追加网格。

## 嵌套与复用核验

109的9个inner anchor和119的27个innermost anchor按fit/predicted/outer-held索引核对，并重新计算fit-only scaler、增强pair、λ.01目标及梯度；36组均通过。新fit9个inner110的26维残差（使用innermost anchor OOF），再fit9个inner120交互（使用A-fit110 margin），每次只给inner-held B提供父分数。三份B覆盖当前outer-fit后训练链残差，部署在outer-held仍用原outer120。full链fit仅用原120完整train OOF。未将全局OOF直接切给outer-fit训练。

新增fit计数{'inner110': 9, 'inner120': 9, 'outer_chain': 12, 'full_chain': 4}，合计34；worker32.727秒、总4线程、600秒硬限。控制fold/full参数和OOF1e-10复现123，官方validation逐分数复现749/754。纯输入缓存、每题权重/梯度/重复pair、收敛/导出/零残差与重排等接口、源/计划/旧新资产SHA核对。全部解压推理资产≤16MiB，fresh官方validation预测+独立评分≤30秒；参考Xeon未认证。

## 解释边界

消除same-fit margin不等于性能一定提高：inner模型训练量较小，误差和校准也变化。这是原固定两种正则下的具体配方对比，不能单凭某一结果证明乐观偏差是或不是平台期唯一原因。OOF及validation已长期用于开发，历史test汇总已知继续披露。报告全部四条件，不报独立显著或因果效果；本批训练/选择未读取test输入、参考、预测、评分。

统计解释11/11：分层及三折检查Simpson误读；固定题库范围避免Ecological外推；候选筛选分布限定Berkson；不作Collider因果调整；报告分母防base-rate忽略；小变动与适应开发考虑regression-to-mean；四条件全报防survivorship；有限搜索与历史比较披露look-elsewhere；预先计划防forking-paths隐瞒；不作相关即因果或reverse-causality主张。

复现：code目录train_round125_nested_offsets.py，再evaluate_round125_nested_offsets.py；原证据目录拒绝覆盖。训练、索引证明/参数梯度、官方日志与选择保存在runs/round125-nested-offsets和round125-evaluation。


# Round125学习记录：嵌套margin不是当前提升的充分条件

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；34新拟合、36个核验复用anchor、4官方验证，未新增test。

|特征|same-fit OOF→nested OOF|相对控制三折|same-fit验证→nested验证|
|---|---|---|---|
|ancestry18 λ.1|4407→4406|-2/+1/0|749→750|
|both24 λ.01|4404→4399|+1/-6/0|754→754|

组合nested与原754在validation上选择完全相同，OOF较低；ancestry虽验证增1仍低于当前754。按预先规则保留原123研究候选，不新增test。

## 对假设的更新

训练margin乐观差距确实存在，但在此固定特征/正则下替换为真正嵌套OOF没有产生更好的最终开发候选。它不是当前平台期已经证实的唯一原因，也不能由此推断所有交叉拟合无用。
inner父模型只训练约2113题，比outer父3170题更少，分数质量、噪声及校准也会变化；本批没有分离这几个因素。不根据验证继续扫描offset混合系数。

## 完整嵌套与核验

每outer-fit内部3个inner分区，inner110残差的基础margin再来自3个innermost anchor；9个inner110与9个inner120均新拟合。链条层四条件12outer+4full=16拟合，共34。
36个已保存anchor逐个核对fit/held索引、当前fit-only scaler、增强pair、λ.01目标与梯度；119的22维残差没有被错误复用到110的26维残差。所有父层排除outer-held。
same-fit控制全部fold/full参数和OOF1e-10复现123，validation逐分数复现749/754。原始数据/parser/scorer及原父参数未改。

## 后续研究要求

下一步先核实组级标签结构及当前pair损失的权重分配，再考虑与组级softmax排序损失匹配比较。每题可能有多个正确候选，但同数值答案分组后可能只有一个正确组，不能把“多正确候选”和“多正确组”混为一谈。此处尚未进行新损失拟合。

## 资源与限制

4线程，worker32.727秒、600秒硬限；官方fresh validation预测+独立评分最慢3.657秒；全部资产最大63,400字节。满足本机30秒/16MiB，参考Xeon未认证。
长期自适应开发、已知历史测试汇总继续披露；本批未读取test输入/参考/预测/评分。原123/120及原79提交字段保留，未创建GitHub issue。统计解释11/11及全部结果见ROUND125_RESULTS.md；不作独立显著或因果结论。


# Round126：固定父模型的组级softmax损失

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4最终输出官方验证。

## 假设与标签核实

训练4755题按数值分组后均只有一个正确组；776题有多个错误组。pair损失将一题的权重平均分给各错误组；组级CE令所有错误组共同竞争。本批固定原123的ancestry/both、λ.1/.01、父120及same-fit offset，仅切换目标。它与112在原始结构上切换uniform/mass不同，不声称首次研究softmax。不引入候选支持度log先验。两种目标显式λ相同，不声称有效曲率等同。

|条件|维度|λ|训练OOF/4755|回代/4755|修复匹配控制/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry_pair|18|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.94|3.718|
|ancestry_group_ce|18|0.1|4405|4521|3/5|[-2, -2, 2]|749|306|78|1/6|61.95|3.641|
|both_pair|24|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.12|3.606|
|both_group_ce|24|0.01|4406|4518|5/3|[1, -1, 2]|751|308|78|0/3|62.13|3.646|

## 开发选择

新组级CE输出均未严格胜过当前(validation754, OOF4404)；保留123，不新增test，不按验证扩展网格。

## 核验与复现

四条件各3outer+1full=16拟合，worker27.046秒、4线程、600秒硬限。pair控制全部fold/full参数和OOF1e-10复现123；官方validation逐分数复现749/754。CE解析梯度、重复题归一、两组时与pair损失等价、组重排通过；每题权重/fit-only scaler/收敛/导出/零残差与候选重排等接口、源/旧新资产/计划SHA通过。全部推理资产≤16MiB，fresh完整validation预测+独立评分≤30秒；参考Xeon未认证。

生成器只创建新126驱动，未改124；首次两次替换次数保护在生成/数据读取前拒绝执行，修正计数并保存失败及源快照，无拟合或验证重试。精确替换和AST检查、模板/生成SHA保留于code/runs/round126-source-preparation.json。复现先prepare_round126_experiment.py，再train_round126_group_loss.py及其--evaluate；原目录拒绝覆盖。

## 解释边界

本实验切换优化目标，不增加输入数学/语义信息。若准确率不增，不能由此证明所有listwise损失无效；若有小增益，也不是独立确认。四条件全部披露，长期train/validation自适应和已知历史test汇总继续披露，不使用test个题或总分训练/选择。

统计解释11/11：同时报告分层/三折防Simpson；限定题库防Ecological；注意候选选择分布Berkson；无Collider因果调整；有分母防base-rate忽略；考虑小变化和regression-to-mean；全报防survivorship；披露look-elsewhere和forking-paths；不作相关即因果或reverse-causality主张。


# Round125–126学习记录：两项训练配方的匹配对照

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；50新拟合、36个验证复用anchor、8官方验证；本轮未新增test。

## 125：父margin由回代改为真正嵌套OOF

|特征|原OOF→嵌套OOF|相对控制三折|原验证→嵌套验证|
|---|---|---|---|
|ancestry18 λ.1|4407→4406|-2/+1/0|749→750|
|both24 λ.01|4404→4399|+1/-6/0|754→754|

嵌套父120所有层均排除outer-held，36个anchor经索引、scaler、pair、目标/梯度验证；9个inner110与9个inner120新拟合。组合验证选择完全相同，OOF较低。same-fit乐观差距存在，但替换为嵌套OOF不是本设置下已经证实的提升方案；inner训练量/噪声/校准也变化，未分离其影响。

## 126：pair平均与组级softmax

|特征|原OOF→group CE OOF|相对控制三折|原验证→group CE验证|
|---|---|---|---|
|ancestry18 λ.1|4407→4405|-2/-2/+2|749→749|
|both24 λ.01|4404→4406|+1/-1/+2|754→751|

组合CE折外修复5/新增3，验证修复0/新增3；ancestry CE折外修复3/新增5，验证总数与自己的749控制相同。全部结果保留，不因OOF小增益替换更好的验证版本。

## 标签与目标的核实

训练4755题都有且仅有一个正确数值组，多个正确候选只是同一正确组的多个成员。2114有信息题中1338（63.29%）只有两个答案组；在同一权重向量下，组CE与pair logistic对此类题逐题等价，等价性经数值/梯度检查。其余776题有多个错误组，才出现两种逐题目标的结构差异。共享系数重训练会影响全部题，因此不能说只有776题的选择可能变化。本批没有加入candidate multiplicity/support先验；那是不同的干预。

CE重新分配梯度但不增加输入语义/数学证据。本轮两个CE输出相对自己的pair控制只改变9和10个训练OOF选择，收益小且折间不一致；不能由此把一般listwise目标判为无用，也不能把目标重写当作已解决平台期。

|特征|pair与CE标准化权重余弦|pair范数|CE范数|差向量范数|
|---|---:|---:|---:|---:|
|ancestry|0.985718|0.126701|0.150973|0.033698|
|both|0.978516|0.399436|0.430376|0.091345|

系数比较只描述目标切换后的参数变化，特征相关且λ下有效曲率不同，不作独立因果贡献解释。

## 对下一次实验的约束

不继续追加offset混合系数、pair/CE混合权重或这一小组特征的验证网格。现有证据更支持先增加可区分题意/数量关系错误的输入信号，并在纯训练切片上核实实际覆盖、误触发和净收益，再进入验证。不能只增加“看起来更严谨”的训练环节就预告准确率会提升。此处是后续研究要求，尚未实现新的语义验证器。

## 开发选择、异常与资源

两个批次均按拟合前规则未选出胜过(754,4404)的新候选；保留原123研究模型754/798（94.486216%），未新增test、未分析test个题、未按历史测试成绩换模型。原120及79保留。126源生成器两次在生成/数据读取前因精确替换计数拒绝执行，失败与原源保留；修正计数后生成新驱动，旧124未改。未发生训练或官方评价重试。

50次新拟合由两个worker顺序执行，总4线程，各600秒硬限；8次fresh官方validation预测+独立评分最慢3.718秒；全部推理资产最大63,622字节（62.13KiB），均满足30秒/16MiB。本机i5-11400H，参考Xeon资格未认证。源/计划/旧新资产/生成模板SHA、控制参数/OOF/验证逐分数、梯度/重复题/两组等价与重排等接口通过。

长期自适应开发及已知历史测试汇总继续披露。统计解释11/11见两批结果，不报独立统计显著或唯一因果。官方数据/parser/scorer未改，未创建GitHub issue。

完整报告ROUND125_RESULTS.md、ROUND126_RESULTS.md；机器闭环code/runs/round125-126-closeout/result.json。


# Round127：计算链来源别名消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4最终输出官方验证。

## 假设与审计

按明确百分比p→p/100、同时存在美元语境的cent p→p/100增加原题来源的别名，不增加来源数或覆盖分母、不推断涨跌倍率。历史已有单位/百分比尝试，本批只修改当前123图的来源归一化。原始字面值匹配优先，未知保持未知。train新特征差异区分当前351错中percent31/cents1/both32题；新严格完整链仍含89/3/92错误候选，不能当硬证明。固定120父、24维图残差、λ.01、same-fit margin、三折、fit-only scaler和每题权重。

|模式|训练OOF/4755|回代/4755|修复754父错/新增（OOF）|相对父三折|验证/798|分歧/355|单正确/117|验证修复/新增|KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|legacy|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.94|3.796|
|percent|4399|4520|6/11|[-1, -2, -2]|754|311|79|0/0|61.94|3.821|
|cents|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.94|3.899|
|both|4400|4520|6/10|[0, -2, -2]|754|311|79|0/0|61.94|3.923|

## 开发选择

新输出未严格胜过当前(754,4404)；保留123，不新增test。

## 资源、核验及局限

4模式各3outer+1full=16拟合，worker28.076秒，4线程、600秒硬限。legacy全部fold/full参数、OOF和验证逐分数复现原123；无有效别名题原始特征全量严格不变，但全局重训练仍可改变这些题分数。源/计划/父新资产、缓存、梯度/重复pair/每题权重、导出/零修正及重排/题序/ID/变batch等核验通过；全部资产≤16MiB，fresh完整validation预测+独立评分≤30秒；参考Xeon未认证。

首次构造检查因float与Fraction精确比较失败，数据/拟合前已修复容差，原源/失败保留，新完成审计v2。来源仍按数值去重，不能证明实体/单位/题意；正确终值标签也不保证完整推理正确。训练错例查看驱动本批方向，属于自适应开发。未读取test输入/参考/预测/评分用于训练或选择；已知历史测试汇总继续披露，原123/120及79保留。

统计解释11/11：报告分层/三折防Simpson；限定题库防Ecological；注意筛选分布Berkson；无Collider因果调整；报告分母；考虑regression-to-mean；四模式全报防survivorship；披露look-elsewhere和forking-paths；不作相关即因果或reverse-causality主张。

复现：audit_round127_source_aliases.py，train_round127_source_aliases.py，再训练脚本--evaluate。证据runs/round127-train-audit（首次失败）、round127-train-audit-v2、round127-source-aliases、round127-evaluation；原输出拒绝覆盖。


# Round127学习记录：来源归一化与旧系数变化

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16拟合、4官方验证；未新增test。

|模式|训练OOF|修复原错/新增|相对原三折|验证|
|---|---:|---|---|---:|
|legacy|4404|0/0|0/0/0|754|
|percent|4399|6/11|-1/-2/-2|754|
|cents|4404|0/0|0/0/0|754|
|both|4400|6/10|0/-2/-2|754|

全部validation选择与原123完全相同。来源归一化在31/1/32个训练错上产生组间特征差异，但覆盖不保证迁移收益，继续保留原754模型。

## 训练组件分解（不作为新验证池）

固定原权重只换percent特征：OOF4403，修复3/新增4，均发生在特征变化题。
固定原特征只换percent新参数：OOF4402，修复4/新增6，新增6均发生在特征未变化题。
新特征+新参数：OOF4399，修复6/新增11；其中5个新错在特征变化题、6个在未变化题。
both同样有5个新错在特征未变化题。cents三种分量都未改变OOF选择。

这表明完整重训练会改变与别名无关的题目；还不能证明冻结旧系数后一定提高准确率，因为固定旧权重换新特征本身也净减1。组件分析仅使用train，各分量没有导出或送往validation/test，不作为独立因果估计。

## 下一步具体假设

保留原123完整模型与原特征作用，只把delta=新别名图特征−原图特征作为独立残差输入来学习。输入delta不减去均值，保证delta全零题的分数严格不变；依旧fit-only scale/每题权重，先做OOF和变化范围核验。
下一步必须区分“减少无关题误伤”和“真正修复相关题”，不能只报告零干预题不变而忽略有别名题上的新错。此处提出新批次假设，不称已经取得收益。

## 完整性与限制

legacy严格复现原参数/OOF/validation；无有效别名题原始特征严格相同。最初float/Fraction构造断言在数据/训练前修复，原源/失败保留。所有旧模型/官方数据和工具未改，资源与接口核验通过，参考Xeon未认证。
长期开发、训练错例驱动方向及历史test总分已知继续披露，test未用于本批训练或选择；不报独立显著。完整结果ROUND127_RESULTS.md，机器记录runs/round127-closeout与round127-component-audit。


# Round128：冻结754父模型的别名差值残差

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合、3官方验证输出（含原123控制）。

固定完整123；仅用percent/both别名图24维与原图的差值训练独立残差，λ.01，same-fit parent margin，原fold/每题归一权重/fit-only尺度。delta不减均值，未变化题的分数严格不动。127组件诊断发现完整重训在未变化题新增5–6错，但固定旧系数换新特征也净减1；本批检验减少无关误伤是否足够。

|模式|训练OOF|回代|训练修复/新增|三折|验证/798|分歧/355|单正确/117|验证修复/新增|delta零验证题|KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|---:|
|control|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|798|62.01|4.244|
|percent|4404|4523|6/6|[0, 2, -2]|754|311|79|0/0|728|63.16|5.553|
|both|4404|4522|6/6|[0, 2, -2]|754|311|79|0/0|726|63.15|5.601|

无人严格胜过当前(754,4404)，保留原123，不新增test。

8新拟合worker29.959秒、4线程、600秒硬限。父outer-held严格复现4404 OOF，delta零题的原分数在全train OOF、full回代与完整validation均逐值复现；零残差也严格复现父。梯度/重复pair/每题权重、缓存/fit-only尺度、导出/重排等接口、源/计划/父新资产SHA通过。全部资产≤16MiB，fresh完整官方validation预测+独立评分≤30秒，参考Xeon未认证。

训练仍包含全部有信息题的归一权重，没有active-only归一或新正则搜索。未变化题不动是设计约束，只有总体修复超过新增才是准确率提升。新来源仍不能证明题意/实体/单位；长期自适应开发与已知历史测试汇总如实披露，测试不用于训练/选择。

统计解释11/11：分层/三折（Simpson）；限定题库（Ecological）；候选分布（Berkson）；不作Collider调整；报告分母；小变化考虑regression-to-mean；全部输出保留（survivorship）；披露look-elsewhere/forking-paths；不作相关即因果或reverse-causality判断。

复现train_round128_alias_delta.py及--evaluate；证据runs/round128-alias-delta、round128-evaluation，旧证据拒绝覆盖。


# Round127–128：来源别名实验的结论

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。先固定各批假设，再训练和官方验证；两批共24次新拟合、7次官方验证，没有新增test。

|方案|训练OOF / 4755|训练修复 / 新增错误|官方验证 / 798|
|---|---:|---|---:|
|原Round123控制|4404|0 / 0|754|
|127百分比来源归一化，完整重训图残差|4399|6 / 11|754|
|127cent来源归一化，完整重训图残差|4404|0 / 0|754|
|127两者，完整重训图残差|4400|6 / 10|754|
|128冻结完整123，只训练百分比特征差值|4404|6 / 6|754|
|128冻结完整123，只训练两者的特征差值|4404|6 / 6|754|

## 每轮发现与下一轮依据

127发现百分比来源归一化在31个原训练错题上产生新的正确/错误答案组特征差异，但新出现的完整来源链中仍有错误答案候选，覆盖不等于可用判别。组件分解发现，percent新增11错中6错位于原特征没有变化的题上；全局系数重分配是可测的额外干预。同时，固定旧系数只换新特征仍净减1，不能把全局重训当成唯一原因。

128冻结完整123，只学习别名特征差值，不对差值减均值。percent训练4356题、both训练4349题的差值全零，原分数严格保持；对应validation为728和726题。两个版本均修复6个原训练错，同时新增6错，总数持平，三折净变化[0,+2,-2]。这消除了无关题的系数干预，但相关题上的得失仍互相抵消。

两批所有validation输出都与原123逐题选择相同，不能称为准确率突破。按预先固定的(validation, OOF)排序，没有新输出严格超过(754,4404)，保留123，不新增test。

## 本次得到的具体限制

数值写法归一化解决了部分来源漏匹配；它没有提供“这个数对应哪个实体、计算结果是否回答所问数量”的信息。正确终值标签也不保证中间推理正确。因此，不能继续把完整来源链当作正确性的硬证明，也没有证据支持继续围绕这两种别名扩展正则网格。

下一次实验前，应先在训练数据上核对剩余错误的目标数量/实体关系，量化一个新信号是否覆盖足够多的正确与错误答案组差异，同时审计已有单位、角色和目标运算实验的重复。只有获得新增覆盖证据后才制定有限训练消融；本记录不声称该方向一定能提高。

## 复现与完整性

完整单轮结果见ROUND127_RESULTS.md、ROUND128_RESULTS.md；127组件分解见runs/round127-component-audit/result.json。128按code目录train_round128_alias_delta.py，再同脚本--evaluate复现，旧证据拒绝覆盖。源、缓存、计划、父/新资产SHA、拟合梯度/每题权重、原父OOF复现、导出/重排/ID/batch/空输入等核验通过。127最初构造断言的float/Fraction比较失败发生在读数据和拟合前，修复容差后的原失败与源文件保留；128没有拟合或评估失败。

全部推理资产包含所有父模型和配置，低于16MiB；每次fresh完整validation预测及独立评分低于30秒，CPU总4线程。参考Xeon完整test运行未认证。长期自适应训练/验证开发、训练错例驱动方向和已知历史测试汇总继续披露，不声称独立显著或一般化提升；test没有参与本批拟合、调参或选择。原123、120和79均保留。

128本机最大未压缩资产64672字节，最大完整官方验证耗时5.601秒。


# Round129：上下文与计算链可靠性交互

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方验证输出。

完整123固定；原24维图特征分别与题目词语、四解答池平均嵌入固定投影、两者组合交互。λ.1，same-fit父margin，原三折、fit-only尺度、每题等权。嵌入上下文不是题目直接嵌入，不新增题意解析。

|模式|训练OOF/4755|回代|训练修复/新增|三折|验证/798|分歧/355|单正确/117|验证修复/新增|全部KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|control|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.01|3.917|
|words|4401|4527|3/6|[-1, -1, -1]|753|310|79|1/2|343.58|4.760|
|pooled_embedding|4402|4520|2/4|[1, -1, -2]|754|311|79|0/0|325.60|4.705|
|both|4406|4524|4/2|[1, 0, 1]|753|310|79|1/2|349.58|4.967|

无人严格胜过(754,4404)，保留123，不新增test。

12新拟合worker98.932秒，CPU共4线程，600秒硬限。每次fresh完整官方预测及独立评分≤30秒、全部递归资产≤16MiB。源/父/新资产SHA、父OOF逐分数复现、梯度/重复pair/每题权重、导出/零交互/重排/题序/ID/batch等核验通过；参考Xeon完整test未认证。

长期自适应开发，已知历史test汇总；test未用于本批训练或选择。覆盖不保证增益，回代不作OOF，题型可靠性不是数学证明。分层/三折与分母报告，全部配置保留，考虑regression-to-mean、look-elsewhere/forking-paths、候选筛选和生态外推；不作Collider调整或相关即因果/反向因果主张（11项解释检查）。

复现train_round129_conditional_chain.py及--evaluate；证据runs/round129-conditional-chain、round129-evaluation；原证据拒绝覆盖。


# Round129学习记录：条件可靠性与组合尺度

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方验证；全部结果保留。

## 训练前假设与证据

来源归一化不提供目标实体关系；历史已尝试角色/单位/词频，改为检验原24维图证据的条件可靠性。351个原训练OOF错误中300题存在正确/错误组图差异，但这些特征已在原模型里，覆盖不是新增可解题数。固定123，分别用词语、解答池嵌入、两者组合与图特征交互，λ.1，12拟合均按预先方案执行。

|方案|训练OOF / 4755|修复 / 新错|三折净变化|验证 / 798|验证修复 / 新错|
|---|---:|---|---|---:|---|
|control|4404|0 / 0|[0, 0, 0]|754|0 / 0|
|words|4401|3 / 6|[-1, -1, -1]|753|1 / 2|
|pooled_embedding|4402|2 / 4|[1, -1, -2]|754|0 / 0|
|both|4406|4 / 2|[1, 0, 1]|753|1 / 2|

## 性能变化的解释和边界

两种单输入训练OOF均下降；组合修复4题、新错2题，4406/4755，三折[+1,0,+1]。只说明当前组合在开发折上净增2，不证明普遍互补或可靠题意理解。解答池均值仍可能包含四份解答共享的错误信息；固定32维投影也会丢失信息。

**尺度混杂必须保留：** both上下文除sqrt(2)，两块在共同λ下各自的有效收缩强于单独输入。组合与单输入对比同时包含信息组合和收缩变化，不能把净增全归因于两种语义互补。本批不事后补参数，后续若研究该解释，需另立单输入λ.2的匹配收缩消融，再和原组合比较。

父模型和原图解析器全冻结；训练变化只来自新增条件残差。每个outer父分数复现原4404 OOF、同题pair等权、scaler仅当前fit题、零交互复现父、完整训练导出及候选重排等接口通过，源/计划/父新资产SHA保存。same-fit父回代offset及长期自适应开发仍是限制，不作独立显著主张。

## 开发选择

新输出未严格胜过预定(754,4404)，保留123，不新增test。训练改善与验证结果分别报告，不能把前者写作验证提升。

## 资源、记录及下一步

本机最大未压缩递归资产357974字节；最大完整官方validation预测+独立评分4.967秒；CPU总4线程，符合16MiB/30秒。参考Xeon完整test未认证。所有12拟合和4验证完成，无拟合/评估失败。

下一步只有在明确研究组合收益机制时，先做匹配收缩单输入对照；不应把更多投影seed、更多词哈希或更长网格当作既定提升。若新增信号目标仍是实体/所问数量，先对训练错题量化新覆盖，并与已有角色/目标运算实现对照，避免重复。

完整方案ROUND129_CONDITIONAL_CHAIN_PLAN.md；结果ROUND129_RESULTS.md；机器证据runs/round129-conditional-chain、round129-evaluation和round129-closeout。长期自适应train/validation、已知历史test总分、方向选择均披露，不作因果或显著性结论。


# Round130：上下文与计算链可靠性交互

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合、3官方验证输出。

完整123固定；原24维图特征分别与题目词语、四解答池平均嵌入固定投影交互；仅两个λ.2匹配收缩单输入，不重训组合。λ.2，same-fit父margin，原三折、fit-only尺度、每题等权。嵌入上下文不是题目直接嵌入，不新增题意解析。

|模式|训练OOF/4755|回代|训练修复/新增|三折|验证/798|分歧/355|单正确/117|验证修复/新增|全部KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|control|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.01|3.615|
|words|4405|4523|3/2|[1, 0, 0]|753|310|79|1/2|343.58|4.541|
|pooled_embedding|4404|4519|2/2|[1, 0, -1]|754|311|79|0/0|325.60|4.651|

无人严格胜过(754,4404)，保留123，不新增test。

8新拟合worker69.103秒，CPU共4线程，600秒硬限。每次fresh完整官方预测及独立评分≤30秒、全部递归资产≤16MiB。源/父/新资产SHA、父OOF逐分数复现、梯度/重复pair/每题权重、导出/零交互/重排/题序/ID/batch等核验通过；参考Xeon完整test未认证。

长期自适应开发，已知历史test汇总；test未用于本批训练或选择。覆盖不保证增益，回代不作OOF，题型可靠性不是数学证明。分层/三折与分母报告，全部配置保留，考虑regression-to-mean、look-elsewhere/forking-paths、候选筛选和生态外推；不作Collider调整或相关即因果/反向因果主张（11项解释检查）。

复现train_round130_matched_shrinkage.py及--evaluate；证据runs/round130-matched-shrinkage、round130-evaluation；原证据拒绝覆盖。


# Round129–130：条件计算链与匹配正则实验总结

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；两批共20次新拟合、7次官方验证。先分别固定方案，完整报告全部配置；无因验证结果追加网格。

## 结果

|轮次与方案|λ|训练OOF / 4755|训练修复 / 新错|相对123三折|官方验证 / 798|验证修复 / 新错|
|---|---:|---:|---|---|---:|---|
|123控制|—|4404|0 / 0|[0,0,0]|754|0 / 0|
|round129_words|0.1|4401|3 / 6|[-1, -1, -1]|753|1 / 2|
|round129_pooled_embedding|0.1|4402|2 / 4|[1, -1, -2]|754|0 / 0|
|round129_both|0.1|4406|4 / 2|[1, 0, 1]|753|1 / 2|
|round130_words|0.2|4405|3 / 2|[1, 0, 0]|753|1 / 2|
|round130_pooled_embedding|0.2|4404|2 / 2|[1, 0, -1]|754|0 / 0|

## 得到的可检验结论

129检验原24维计算链图特征的上下文可靠性，冻结完整123，不新增数量语法。题目词语128维、解答池平均嵌入固定32维投影、两者拼接归一化；解答池向量不是题目的直接嵌入。300/351个原训练错题有图特征差异，但这些特征原本就在123里，不能称新增覆盖300题。

129组合训练OOF4406，净增2，两个单输入4401/4402；官方validation组合753、词语753、嵌入754，均未超过754，不能把OOF增益写成验证提升。

130按尺度推导固定λ.2做两种单输入对照，词语OOF4405、嵌入4404。比原λ.1分别+4/+2，但比原123仅+1/0。组合与匹配词语只差1题，先前差距有相当部分可由收缩变化解释；这不是一般互补性或显著性证明。

使用原129实际3058个pair、保存权重、同一offset/每题权重，重新构建both目标0.19894820038182862，与未缩放两块、权重除sqrt(2)、λ.2目标逐值一致；最大margin差1.11e-16，梯度变换也相符。该数学核验0新拟合，不是一个额外训练配置。

## 开发选择

130没有新输出严格胜过预定(754,4404)。保留原123，未新增test；129准备的有条件冻结测试脚本未执行。

## 失败、资源和复现

130首次入口在导入时因生成器误改推理模块名而失败，尚未读数据或拟合；修复前源及失败保存在runs/round130-source-build/pre-import-failure。修复脚本第一次出现次数保护断言也在写入/数据/拟合前失败（误设3，实际2），已记录。修复只恢复已冻结129推理实现，未改实验配置。之后8次拟合和3次官方验证完成。129的12次拟合和4次验证均完成。

两批本机最大递归未压缩推理资产357974字节，最大完整官方validation预测+独立评分4.967秒；CPU总4线程，符合16MiB/30秒。参考Xeon完整test资格未认证。源/计划/父新资产/官方工具SHA、原父OOF、梯度/重复pair/每题权重、fit-only尺度、全训练导出/零交互及重排等接口核验通过。

code目录build_round130_matched_shrinkage.py生成新训练脚本，train_round130_matched_shrinkage.py训练，audit_round130_real_equivalence.py做实际pair等价核验，再训练脚本--evaluate；原证据拒绝覆盖。生成器已修正推理模块名，不需要在新工作副本重放导入失败。完整单轮方案/结果、机器证据与AI披露保留。

下一步应优先回答仍缺少什么输入关系，而非继续扩大哈希/seed/正则网格。当前交互只重加权旧数值图，没有显式表示所问实体与中间量的关系。若尝试实体/目标信号，必须先审计训练覆盖并与旧49/50/61/70等实现对照；本批不能保证此方向提高。长期自适应开发、已知历史test汇总、方向筛选继续披露，统计11项解释边界同单轮报告，不作独立显著或因果主张。


# Round129–130：五候选追加冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。用户明确要求全部测试；名单、顺序、所有源/参数在第一项新test预测前统一冻结。0新拟合，5项各一次fresh预测和独立官方评分。

|模型|λ|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|原123（引用已有记录）|.01|4404|754|390|83.5118%|0|—|—|
|原120（引用已有记录）|.1|4396|752|391|83.7259%|+1|—|—|
|round129_words|0.1|4401|753|391|83.7259%|+1|343.58|3.635|
|round129_pooled_embedding|0.1|4402|754|389|83.2976%|-1|325.60|3.316|
|round129_both|0.1|4406|753|391|83.7259%|+1|349.58|3.489|
|round130_words|0.2|4405|753|391|83.7259%|+1|343.58|3.434|
|round130_pooled_embedding|0.2|4404|754|390|83.5118%|+0|325.60|3.409|

## 与此前实验的关系

此前129/130报告的“不新增test”是当时的执行结果；本次用户后续明确授权扩大评价，未伪称通过原开发准入。旧报告、计划、选择、模型及元数据均保留。原123研究候选及79主交付没有按test自动替换。

五项全部报告，无依分数提前停止、追加模型、改参或重复运行，无test逐题错误分析。本批只提供这些固定模型在已暴露测试集上的分数；如后续按test最高分选模型，必须标明测试集参与选型，不能把赢家成绩当独立最终评估。长期自适应开发和已知历史test汇总继续披露；小幅计数差异不称显著提升。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz。总4线程，每项完整预测及独立评分共享30秒，各项递归未压缩资产≤16MiB；参考Xeon完整测试资格未认证。成功/失败、命令、stdout/stderr、官方JSON、冻结源/参数、全部SHA见final_evaluation/round129-130-all-test-20261029。

复现code/run_frozen_tests_round129_130_all.py，旧目录拒绝覆盖。未公开提交或创建issue。


# Round131：计算链组聚合子集增强

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4官方验证。

固定完整120父offset，只对24维图mean/max的训练输入做同答案组非空子集遮蔽。原组pair等权后均分subset-pair权重，每题总重一致；scaler仅当前fit原始完整组，λ.01，原三折。推理使用完整组。该干预不是整个父模型的候选删减增强。

|模式|训练OOF/4755|回代|训练修复/新增|三折|验证/798|分歧/355|单正确/117|验证修复/新增|KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|full|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.94|3.731|
|mean_subsets|4403|4517|4/5|[0, -1, 0]|751|308|79|0/3|61.95|3.710|
|max_subsets|4405|4521|2/1|[0, 0, 1]|751|308|79|0/3|61.95|3.692|
|both_subsets|4406|4520|4/2|[0, 0, 2]|750|307|79|0/4|61.95|3.668|

新输出未严格胜过(754,4404)，原123开发选择保留。

三个新增强版本按用户最近要求、预定名单全部冻结后各一次官方test；控制123已有test不重测。新test尚未在本脚本执行；其结果不改本批训练和开发选择。

16拟合worker89.345秒，4总线程，600秒硬限。原full控制参数/OOF/验证与123复现；原父120 OOF复现；每题/原pair权重、fit-only尺度、梯度/重复pair、全训练导出/零残差及重排等接口、源/计划/父新资产SHA核验通过。全部递归资产≤16MiB，完整官方validation预测+独立评分≤30秒，参考Xeon未认证。

没有新增题意语义，子集特征变动覆盖不等于可纠正数量。长期自适应train/validation、此前test汇总已知如实披露，本批训练和开发选择不使用test；不作独立显著或因果结论。统计解释11项关注分层/分母/全部配置、筛选与多次比较、生态外推、回归均值，不作Collider调整/相关即因果/反向因果主张。

复现train_round131_chain_subsets.py及--evaluate；证据runs/round131-chain-subsets、round131-evaluation，旧证据拒绝覆盖。


# Round131：三个新增强版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。三个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round131_mean_subsets|4403|751|391|83.7259%|+1|61.95|3.331|
|round131_max_subsets|4405|751|390|83.5118%|+0|61.95|2.848|
|round131_both_subsets|4406|750|391|83.7259%|+1|61.95|2.903|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round131-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round131-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round131学习记录：计算链子集增强

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4官方validation、3新最终版本各一次官方test；训练范围诊断0新拟合。

## 完整结果

|模式|训练OOF/4755|训练修复/新增|三折净变化|验证/798|验证修复/新增|测试/467|
|---|---:|---|---|---:|---|---:|
|full|4404|0/0|[0, 0, 0]|754|0/0|390（引用原123）|
|mean_subsets|4403|4/5|[0, -1, 0]|751|0/3|391|
|max_subsets|4405|2/1|[0, 0, 1]|751|0/3|390|
|both_subsets|4406|4/2|[0, 0, 2]|750|0/4|391|

## 本轮检验了什么

基础模型108已做所有同答案非空子集增强；本批只在123的计算链24维mean/max残差上做特征级遮蔽，完整120父offset固定，scaler从原fit完整组拟合，原组pair和每题总重不随子集数改变，λ.01。full控制逐参数/OOF/完整验证复现123。该方案没有模拟删去候选后重算整个父模型，也没有增加实体/目标数学知识。

三种增强在155个原训练错题上改变组特征，但覆盖不是可纠错数。均值增强OOF净减1，最大值净增1，二者净增2；后两者收益只来自第三折。官方validation所有新增强方案均下降，故不能称稳定或验证提升。三个版本按预定名单全部冻结后测试，最高391/467，与此前已记录的最高分持平，不按test重新选型。

## 训练范围和期望诊断

|模式|特征未变题|修复发生在未变题|新错发生在未变题|有期望偏移的答案组|最大期望偏移|
|---|---:|---:|---:|---:|---:|
|mean_subsets|1487|2|1|0|6.66134e-16|
|max_subsets|1595|0|0|3228|0.908091|
|both_subsets|1487|1|0|3228|0.908091|

所有非空子集均匀枚举时，子集均值的期望等于原完整均值（全train已逐组核验）；子集最大值的期望一般低于完整最大值。因此max/both增强不仅增加方差，也改变训练特征的期望与完整组推理之间的关系。固定scaler、每题权重和λ消除了样本量正则混杂，但不能消除这个分布偏移。这个数学事实与范围计数不能单独证明validation下降的原因。

新系数仍是全局的，所以即使一题没有子集输入变化，其分数也可能变化；上表完整报告这种修复和误伤，而不是只看增强覆盖内的收益。诊断只用train，不导出额外组件、不做新模型选型、没有额外validation或test。

## 下一步可检验改进

若继续检验增强机制，应另立匹配对照：将每组子集扰动减去其自身期望，再加回原完整特征，使训练扰动严格零均值；固定原scaler/权重/λ，对比未中心化max/both，分开检验噪声正则与期望偏移。该假设来自train输入的期望诊断，不来自test个题或输赢；尚未执行，不能预告提升。单纯增加遮蔽强度/正则/seed没有本批证据支持。

## 资源、完整性与复现

最大递归未压缩推理资产63436字节；本机完整官方validation预测+独立评分最长3.731秒，完整test最长3.331秒；CPU总4线程，符合16MiB/30秒。参考Xeon完整test未认证。16拟合、4验证、3测试全部完成，无失败或重试；源/计划/缓存/父新资产/官方工具SHA、父/控制复现、梯度/重复pair/原pair题权重、全训练导出/零修正/重排等接口通过。

code目录train_round131_chain_subsets.py及--evaluate，run_frozen_tests_round131.py，audit_round131_training_scope.py，closeout_round131.py。各证据目录拒绝覆盖。报告/AI披露保留全部配置和开发选择；无公开提交或issue，原123/120及79保留。长期自适应开发、已知test总分及测试池扩大如实披露；如将来依据test分数选模型，必须写明测试集参与选型，不作独立显著或因果主张。


# Round132：零均值计算链子集扰动

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合，3最终输出官方validation（控制复用0拟合）。

只对max/both子集扰动去掉每组期望偏移，保留方差；其他设置与131相同。每原pair加权增强期望逐值等于完整差值；加回去掉的偏移复现131设计。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|full|4404|0/0|[0, 0, 0]|754|0/0|61.94|3.706|
|max_centered|4404|1/1|[-1, 0, 1]|752|0/2|61.96|3.830|
|both_centered|4405|5/4|[-1, 1, 1]|752|0/2|61.96|3.693|

未严格胜过(754,4404)，保留123。

8拟合worker60.319秒，4总线程、600秒硬限。源/计划/缓存/父新资产、原pair权重/期望、梯度/重复pair、父/控制、全训练导出/零残差/重排等接口通过；全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒。参考Xeon未认证。

两个新输出按预定名单全部冻结后各一次官方test；本脚本未执行test，测试不改变本批开发选择或参数。长期自适应开发及既有test汇总披露，零均值扰动不是新增题意关系，增强值不一定落于原比例范围；不作独立显著或因果主张。统计11项解释边界沿用131，所有配置/分母/折/失败保留。

复现train_round132_centered_subsets.py及--evaluate，run_frozen_tests_round132.py；证据拒绝覆盖。


# Round132：两个新增强版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。两个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round132_max_centered|4404|752|391|83.7259%|+1|61.96|2.839|
|round132_both_centered|4405|752|392|83.9400%|+2|61.96|2.876|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round132-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round132-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round131–132：计算链子集增强及零均值对照

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；两批24次新拟合、7次官方validation、5个新增最终版本各一次官方test。每批均预先固定假设和名单，test不参与拟合/开发选择。

|模型|训练OOF/4755|训练修复/新增|三折净变化|官方验证/798|验证修复/新增|官方test/467|
|---|---:|---|---|---:|---|---:|
|原123控制|4404|0/0|[0,0,0]|754|0/0|390（已有记录）|
|round131_mean_subsets|4403|4/5|[0, -1, 0]|751|0/3|391|
|round131_max_subsets|4405|2/1|[0, 0, 1]|751|0/3|390|
|round131_both_subsets|4406|4/2|[0, 0, 2]|750|0/4|391|
|round132_max_centered|4404|1/1|[-1, 0, 1]|752|0/2|391|
|round132_both_centered|4405|5/4|[-1, 1, 1]|752|0/2|392|

## 131发现的问题与132如何检验

131保持完整120父分数、原图、原完整组fit-only scaler、每原pair/每题权重和λ.01，只遮蔽计算链mean/max训练特征。子集变化覆盖155/351个原训练错，覆盖不等于新增可解题。full重训严格复现123；max/both OOF净增1/2，但收益集中第三折，官方validation下降3/4题。

纯train期望审计发现：子集均值期望等于完整均值；子集max/both在3228/7813答案组改变期望，最大原始维度偏移0.908091。另有部分修复/新增发生于特征未变题，说明全局参数改变仍会影响非增强题。详见ROUND131_LEARNING.md及runs/round131-training-scope/result.json。

132仅去掉每组子集特征的平均偏移，保留零均值扰动，固定所有其他设置。每个原pair的增强差值期望逐值复现完整差值；加回所去偏移逐值复现131的pair设计。8拟合、3验证及2测试全部完成，无追加λ、噪声强度或seed。

去均值后的训练OOF为4404/4405，而原max/both为4405/4406；单看OOF，去偏移没有进一步提高。对validation和test是否有收益应以完整表分别判断，不能把消除一个数学混杂本身叫准确率提升。test只补充固定版本分数，不指导继续拟合/选择本批赢家。

## 开发选择与后续依据

所有新输出均未严格胜过预定(754,4404)，保留原123。原120等既有模型和成绩、79主交付均保留。

两批都没有提供新的实体、单位或所问数量关系，只对已有图信号重新加权/正则。若继续开发，应先在train上审计此前未表达的目标关系是否产生新的正确/错误组对比，并明确与旧角色、单位图、末步目标实验的差别。当前结果不支持继续扩展同一子集噪声的强度或seed网格；不把更多拟合次数当收益。

## 资源、失败及复现

最大递归未压缩推理资产63446字节；本机完整validation预测+独立评分最多3.830秒，完整test最多3.331秒；CPU总4线程，满足16MiB/30秒。参考Xeon完整test未认证。24拟合、7验证、5测试均完成，无实验失败或重试。源/计划/缓存/全部父新资产/官方工具SHA、原控制/父OOF、fit-only尺度、原pair权重/期望、梯度/重复pair、全训练导出/零修正和重排等接口通过。

code目录train_round131_chain_subsets.py及--evaluate、run_frozen_tests_round131.py；train_round132_centered_subsets.py及--evaluate、run_frozen_tests_round132.py。审计与closeout脚本、全部命令/日志/官方JSON/冻结源/参数保留，各证据目录拒绝覆盖。132测试脚本通过build_round132_test_runner.py生成，原131源保持原SHA。

长期自适应train/validation、已知历史和新test汇总均披露；全部版本报告，包括失败方向。若后续按test分选模型，需写明测试集参与选型，赢家分数不是独立最终估计。统计11项解释边界沿用单轮报告，不称显著、稳定泛化或因果机制。无公开提交/issue。


# Round133：跨候选错误传播复算支持

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation。

完整123固定，local/propagated/both分别4/4/8维残差，λ.1，same-fit完整父margin、原折/fit-only尺度/每题pair权重。整链复算差异覆盖8个原错、3个超出local，正确/错误接收支持答案组75/6；候选解析与123全train逐记录一致。跨候选支持不是题意证明，歧义producer/来源冲突拒绝。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|control|4404|0/0|[0, 0, 0]|754|0/0|62.01|3.681|
|local|4404|0/0|[0, 0, 0]|754|0/0|63.03|4.531|
|propagated|4404|0/0|[0, 0, 0]|754|0/0|63.03|4.625|
|both|4404|0/0|[0, 0, 0]|754|0/0|63.12|4.481|

未严格胜过(754,4404)，保留123。

12拟合worker89.082秒，4总线程，600秒硬限。原父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全训练导出/零修正/重排等接口和源/计划/父新资产SHA通过。全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒，参考Xeon未认证。

三个新版本按预先名单全部冻结后测试；本脚本未执行test，test不用于拟合或本批开发选择。长期自适应开发、已知test汇总披露，不作独立显著/稳定泛化/因果主张；11项解释边界沿用前轮，报告全部配置/分母/折与失败。

复现audit_round133_propagated_repair.py、train_round133_propagated_repair.py及--evaluate，再run_frozen_tests_round133.py；旧证据拒绝覆盖。


# Round131：三个复算支持版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。三个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round133_local|4404|754|391|83.7259%|+1|63.03|3.334|
|round133_propagated|4404|754|392|83.9400%|+2|63.03|3.378|
|round133_both|4404|754|392|83.9400%|+2|63.12|3.301|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round133-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round133-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round133学习记录：复算支持的总体精度与剩余错题方向

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation、3新最终版本各一次官方test；训练边际诊断0拟合。

|模式|训练OOF/4755|回代/4755|验证/798|官方test/467|
|---|---:|---:|---:|---:|
|原123控制|4404|4519|754|390（已有记录）|
|local|4404|4519|754|391|
|propagated|4404|4520|754|392|
|both|4404|4520|754|392|

传播/组合都在test得392/467，与132记录持平；它们validation754/798，而132_both_centered为752/798。它们没有超过原123的754，也没有超过既有test最高392，因此应分别报告“验证持平原最佳、测试持平新高”，不能声称新的test突破或稳定泛化。新模型的开发指标与123精确平分，按预定规则保留123；没有根据test成绩更换研究指针。

## 新信号及训练诊断

8的末步局部复算不能修正先前算错后继续沿用的中间量；本批保留原123数字等式语法和AST，纠正中间值并向最终root传播。不同producer、直接来源冲突和不安全运算拒绝；这仍不能证明实体/目标数量关系。local不是重放历史8参数，而是当前123父上的4维局部支持残差，另保留共享多步标志。

全训练解析逐记录与原123一致。传播支持命中正确答案组75个、错误答案组6个；新特征差异覆盖351个原错中的8题，3题超出local。该总体匹配计数看起来偏向正确，但不代表剩余错误中的信号也有利。

|模式|剩余错题特征有差异|修正方向有利/有害|达到原差距1/4|达到原差距|
|---|---:|---|---:|---:|
|local|5|1/4|0|0|
|propagated|8|2/6|1|0|
|both|8|2/6|1|0|

这8题中仅1题正确答案获得更强接收支持，4题反而是原错误首选获得更强支持，其余为该计数持平。学习后的传播/组合修正方向2题有利、6题有害，均不足以修复原排序；训练OOF全部与父逐题选择相同。回代多对1题不构成OOF增益。

因此，失败不只是“修正力度不够”：放大当前修正同时会放大更多错误方向。总体支持75/6与当前剩余错误上的1/5差异说明，覆盖审计必须区分“输入不同”“偏向正确组”“旧模型已经做对”；不能只用全训练总体精度和差异题数决定是否继续扩大λ网格。这里是描述性条件分解，不是独立因果估计。

## 下一轮应先验证什么

后续新信号审计需报告剩余错题中正确/错误首选支持方向，以及旧正确题的误导覆盖；优先寻找新的实体/所问数量关系，核对与旧单位图/数量角色/目标运算尝试的差别，再制定有限消融。本批证据不支持仅放大传播权重或扩大相同算术规则。若研究去掉donor惩罚，必须单独冻结对照，不能直接把某个置零诊断当已训练模型或按test选择。

## 失败、资源与复现

首次训练入口的负数构造用例不被原解析器的跨行边界支持，在训练数据加载和拟合前失败；原源和失败记录保留于runs/round133-propagated-repair。仅把用例改为原语法已支持的括号负数，未改解析器、已完成输入审计或实验配置，训练新输出使用runs/round133-propagated-repair-v2。随后12拟合、4验证、3测试均完成，无测试失败或重试。

最大递归未压缩资产64634字节；本机完整validation预测+独立评分最多4.625秒，完整test最多3.378秒；总4线程，符合16MiB/30秒，参考Xeon未认证。父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全部train导出/零修正/重排等接口及源/计划/旧新资产/官方工具SHA通过。

复现audit_round133_propagated_repair.py，train_round133_propagated_repair.py及--evaluate，run_frozen_tests_round133.py；训练诊断audit_round133_margin_signal.py；完整证据拒绝覆盖。三个新增版本统一冻结后全部测试，名单未按前面test分数调整，无test个题分析/训练/调参/本批重新选型。旧132记录模型及zip、123/120和79保持，未公开提交或创建issue。长期自适应开发与已知test汇总披露，不称独立显著或因果解释。


# Round134：跨答案组正文提及与结论语境

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation。

完整123固定，body/context/both分别4/4/8维残差，λ.1，same-fit完整父margin、原折/fit-only尺度/每题pair权重。正文数值提及可能代表中间量，结论/目标词/否定语境仍不是实体或题意证明。纯train预定审计全报两个方向，未据结果删特征或改变符号。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|control|4404|0/0|[0, 0, 0]|754|0/0|62.01|3.784|
|body|4402|9/11|[1, -5, 2]|754|0/0|63.03|4.920|
|context|4401|5/8|[-1, -2, 0]|754|0/0|63.03|4.960|
|both|4404|10/10|[2, -4, 2]|754|0/0|63.12|4.977|

未严格胜过(754,4404)，保留123。

12拟合worker95.739秒，4总线程，600秒硬限。原父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全训练导出/零修正/重排等接口和源/计划/父新资产SHA通过。全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒，参考Xeon未认证。

三个新版本按预先名单全部冻结后测试；本脚本未执行test，test不用于拟合或本批开发选择。长期自适应开发、已知test汇总披露，不作独立显著/稳定泛化/因果主张；11项解释边界沿用前轮，报告全部配置/分母/折与失败。

复现audit_round134_propagated_repair.py、train_round134_answer_mentions.py及--evaluate，再run_frozen_tests_round134.py；旧证据拒绝覆盖。


# Round134：三个正文提及版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。三个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round134_body|4402|754|391|83.7259%|+1|63.03|3.790|
|round134_context|4401|754|392|83.9400%|+2|63.03|3.717|
|round134_both|4404|754|391|83.7259%|+1|63.12|3.626|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round134-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round134-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round134学习记录：跨答案组正文提及与语境

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation、3个新最终候选统一冻结后各一次官方test。

|模式|训练OOF/4755|回代/4755|训练修复/新增|三折净变化|验证/798|验证修复/新增|官方test/467|
|---|---:|---:|---|---|---:|---|---:|
|原123控制|4404|4519|0/0|[0,0,0]|754|0/0|390（已有记录）|
|body|4402|4519|9/11|[1, -5, 2]|754|0/0|391|
|context|4401|4520|5/8|[-1, -2, 0]|754|0/0|392|
|both|4404|4520|10/10|[2, -4, 2]|754|0/0|391|

## 审计与为何不能把提及当正票

历史12/49/110已有末步转交、计算图祖先或末尾boxed冲突。本批原123父固定，只增加外国答案组正文数值出现、末尾位置、频次、非题目输入，以及结论/终问词邻近/否定语境。官方最终答案从原文本解析，特征文本则去掉最终####后缀与可识别boxed，避免把原final投票直接重复计数。无图可解析时仍可抽取文本；没有声称新的实体绑定或量纲验证。

|cue|剩余错：正确组更强|剩余错：错误首选更强|原正确：首选更强|原正确：其他错误组更强|
|---|---:|---:|---:|---:|
|foreign_body|56|51|191|633|
|foreign_tail|53|51|170|615|
|foreign_frequency|57|55|200|650|
|foreign_not_question_input|38|42|124|516|
|foreign_conclusion|29|24|97|333|
|foreign_target|40|41|146|489|
|foreign_negative|1|0|2|10|
|foreign_target_tail|37|40|123|457|

正文提及在107个剩余错误上有差异，但56偏向正确、51偏向错误首选；原正确题中更多其他错误组被提及（633对191），符合“提及可能只是中间量”的负向假设。结论词29/24，目标词40/41，目标+末尾37/40；这些词窗没有稳定地把信号变成正确答案支持。否定仅1个原错，不能据此扩展大量否定规则。

训练结果同样不稳定：body三折[+1,-5,+2]，context[-1,-2,0]，both[+2,-4,+2]。组合虽修复10个原错，同时新增10错，总体持平；不应只展示修复或两个有利fold。回代4519/4520不替代OOF4402/4401/4404。

## 拟合系数（描述性，不作因果贡献）

|模式|特征|标准化权重|原始特征斜率|
|---|---|---:|---:|
|round134_body|foreign_body|-0.019601|-0.0975675|
|round134_body|foreign_tail|-0.0516022|-0.273207|
|round134_body|foreign_frequency|-0.0101443|-0.0395288|
|round134_body|foreign_not_question_input|-0.100604|-0.61462|
|round134_context|foreign_conclusion|0.00407105|0.0378728|
|round134_context|foreign_target|-0.0436869|-0.262557|
|round134_context|foreign_negative|0.000790063|0.0570691|
|round134_context|foreign_target_tail|-0.0574601|-0.391409|
|round134_both|foreign_body|-0.0184559|-0.0918675|
|round134_both|foreign_tail|-0.0486641|-0.257652|
|round134_both|foreign_frequency|-0.00944123|-0.0367891|
|round134_both|foreign_not_question_input|-0.100218|-0.612258|
|round134_both|foreign_conclusion|0.028445|0.264622|
|round134_both|foreign_target|-0.010214|-0.061386|
|round134_both|foreign_negative|0.00339954|0.245561|
|round134_both|foreign_target_tail|-0.020498|-0.139629|

特征高度相关，单个系数正负不代表独立作用。权重只用于解释已有拟合，不据此再导出置零版本、选择新的符号或扩正则网格。带词窗的输入仍是关键词交集，无法确认提及数值的实体角色、时间范围或是否回答所问数量；这限制了将普通文本提及当作可靠推理证据。

## 开发选择、测试与后续依据

新输出未严格胜过(754,4404)，原123开发身份保留。此前132/133的392测试记录与133的754验证候选均保留，未依本批test成绩更换开发选择。

三个新最终版本按预定名单全部测试，test只记录分数，未用于本批拟合、参数或开发选择。下一步如果仍用文本，需要先验证提及数字与所问实体/时间角色的绑定是否产生真正新对比，并对照已有数量角色/单位/末步方案；当前结果不支持仅增加普通提及窗口、频次上限或同义词。新信号应同时报告剩余错题方向和旧正确的误导覆盖，不能再把大覆盖本身称为改进。

## 完整性、资源与复现

最大递归未压缩资产64635字节；本机完整validation预测+独立评分最多4.977秒，完整test最多3.790秒；CPU总4线程，符合16MiB/30秒。参考Xeon完整test未认证。12拟合、4验证、3测试全部完成。首次测试启动检查因记录仍写133而停止，尚未创建测试目录或执行预测；repair_round134_metadata.py按已完成证据修正轮号及旧文字，保留训练源/参数/分数，之后每项test仅执行一次。原源、parser/数据/官方工具、缓存、父/新资产SHA、父OOF、梯度/重复pair/每题权重/fit-only scaler、全训练导出/零修正/重排等接口通过。旧132及133压缩包SHA保持。

复现audit_round134_answer_mentions.py，build_round134_experiment.py，train_round134_answer_mentions.py及--evaluate，repair_round134_metadata.py，run_frozen_tests_round134.py，closeout_round134.py。旧目录拒绝覆盖。源生成只创建新文件，原133源保持原SHA；特征没有按审计或验证结果删改。测试runner的旧131报告标题在首次冻结前修正。所有原始分数、命令、日志、模型、计划与方向计数保留；无公开提交/issue。

同时核对133文字中的计数勘误：原机器行是1题正确组接收支持更强、4题错误首选更强、3题持平，旧一段误写1/5；当前133学习文档已加勘误，旧冻结源/模型/分数和历史zip不改。这不同于学习后分数变化的2有利/6有害。

长期自适应train/validation和已知test汇总继续披露；如果后续依据test分选择模型，必须说明测试集参与选型，不把最高分称独立最终估计。统计11项解释边界关注分层/分母/全部配置、条件筛选、生态外推、回归均值与多次比较，不作Collider调整或相关即因果/反向因果主张。


# Round135：数量标签、人名与明确状态的局部关联

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation。

完整123固定，label/role/both分别4/8/12维残差，λ.1，same-fit完整父margin、原折/fit-only尺度/每题pair权重。只抽取精确邻接数量标签、局部唯一明确人名和唯一状态词；仍是词面关联，不声称实体语义证明。纯train方向审计后未删列或改变符号。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|control|4404|0/0|[0, 0, 0]|754|0/0|62.01|4.962|
|label|4407|4/1|[2, 0, 1]|753|0/1|63.02|6.648|
|role|4404|3/3|[0, 1, -1]|754|0/0|63.12|5.886|
|both|4407|6/3|[2, 2, -1]|752|0/2|63.21|5.697|

未严格胜过(754,4404)，保留123。

12拟合worker123.487秒，4总线程，600秒硬限。原父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全训练导出/零修正/重排等接口和源/计划/父新资产SHA通过。全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒，参考Xeon未认证。

三个新版本按预先名单全部冻结后测试；本脚本未执行test，test不用于拟合或本批开发选择。长期自适应开发、已知test汇总披露，不作独立显著/稳定泛化/因果主张；11项解释边界沿用前轮，报告全部配置/分母/折与失败。

复现audit_round135_quantity_binding.py、train_round135_quantity_binding.py及--evaluate，再run_frozen_tests_round135.py；旧证据拒绝覆盖。


# Round135：三个数量关联版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。三个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round135_label|4407|753|390|83.5118%|+0|63.02|5.099|
|round135_role|4404|754|390|83.5118%|+0|63.12|4.676|
|round135_both|4407|752|389|83.2976%|-1|63.21|4.838|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round135-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round135-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round135学习记录：数量标签、人名与明确状态

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation、3个新最终候选统一冻结后各一次官方test。

## 全部结果

|模式|训练OOF/4755|回代/4755|训练修复/新增|三折净变化|验证/798|验证修复/新增|官方test/467|
|---|---:|---:|---|---|---:|---|---:|
|原123控制|4404|4519|0/0|[0,0,0]|754|0/0|390（已有记录）|
|label|4407|4524|4/1|[2, 0, 1]|753|0/1|390|
|role|4404|4522|3/3|[0, 1, -1]|754|0/0|390|
|both|4407|4522|6/3|[2, 2, -1]|752|0/2|389|

## 与旧方案的区别、审计及局限

14年龄关系、40角色审计、58时期换算、66跨题槽位匹配、70数字身份已做。135不产生新答案，而在同一题上区分数字紧邻标签、局部唯一显式人名、唯一状态词的匹配/冲突；按own与foreign提供者分开。官方final由原parser读取，特征正文遮蔽最终字段。相较134的宽词窗，此处要求数量标签直接邻接或label:number形式；人名/状态多义时未知。

训练4755题识别目标数量标签2857题、目标人名844题、状态1180题。未知不等于错误，识别数不等于正确率；数量标签集合仍是词面前缀，没有POS、代词消解、真实实体/时间推断。money/dollar统一不进行金额换算。

|cue|原错：正确组更强|原错：错误首选更强|原正确：首选更强|原正确：其他错误组更强|非零组|
|---|---:|---:|---:|---:|---:|
|label_own_match|20|23|120|138|745|
|label_foreign_match|6|6|27|80|148|
|label_own_mismatch|16|8|78|85|376|
|label_foreign_mismatch|15|7|47|83|180|
|entity_own_match|3|6|30|43|254|
|entity_foreign_match|2|0|5|37|55|
|entity_own_mismatch|0|1|9|12|47|
|entity_foreign_mismatch|3|0|3|22|34|
|state_own_match|14|15|106|89|634|
|state_foreign_match|1|5|10|60|93|
|state_own_mismatch|3|3|17|18|81|
|state_foreign_mismatch|1|1|7|20|38|

不能把match当正票、mismatch当负票：原错label_own_match为20对23，label_own_mismatch为16对8，foreign_mismatch为15对7。词面“不匹配”在正确组反而可能更强，可能来自题目标签截断、中间量、多个对象或不同提供者的描述；本批未按这些计数手选符号或删特征。人名相关原错覆盖很少，state_own_match14对15，也未显现单向可靠纠错。原正确的多错误组存在计数可重叠，不与单个错误首选的计数混作相同比例。

## 已拟合系数（描述性）

|模式|特征|标准化权重|原始特征斜率|
|---|---|---:|---:|
|round135_label|label_own_match|-0.0298435|-0.256982|
|round135_label|label_foreign_match|-0.050786|-0.856776|
|round135_label|label_own_mismatch|-0.00503382|-0.0499449|
|round135_label|label_foreign_mismatch|0.0334764|0.44758|
|round135_role|entity_own_match|-0.0376685|-0.515464|
|round135_role|entity_foreign_match|-0.0307945|-0.871396|
|round135_role|entity_own_mismatch|-0.0146941|-0.348698|
|round135_role|entity_foreign_mismatch|0.0130364|0.404972|
|round135_role|state_own_match|0.0187889|0.162138|
|round135_role|state_foreign_match|-0.0923412|-2.28063|
|round135_role|state_own_mismatch|-0.00107869|-0.033221|
|round135_role|state_foreign_mismatch|-0.0321595|-1.37165|
|round135_both|label_own_match|-0.0271634|-0.233905|
|round135_both|label_foreign_match|-0.0411626|-0.694426|
|round135_both|label_own_mismatch|-0.00413702|-0.041047|
|round135_both|label_foreign_mismatch|0.0410153|0.548376|
|round135_both|entity_own_match|-0.0353751|-0.484081|
|round135_both|entity_foreign_match|-0.032852|-0.929617|
|round135_both|entity_own_mismatch|-0.014808|-0.3514|
|round135_both|entity_foreign_mismatch|0.0099722|0.309784|
|round135_both|state_own_match|0.0202138|0.174434|
|round135_both|state_foreign_match|-0.0918095|-2.2675|
|round135_both|state_own_mismatch|0.00092216|0.0284004|
|round135_both|state_foreign_mismatch|-0.0302147|-1.28871|

系数存在相关性，不能当作独立因果贡献；没有据系数再删列、放大权重、扫正则或导出新版本。OOF修复和新增、全部三折、回代及验证同时保留，不把训练收益代称验证突破。

## 开发选择和测试边界

新输出未严格胜过(754,4404)，保留原123开发身份；先于新test已记录。

本批已观察test最高390/467，旧最高392/467；全部3个预定最终版本均测试，无test逐题分析或按中途成绩调整其余模型。test已反复暴露且长期自适应开发，不能把最高分当独立泛化估计；后续若据test挑提交版本须披露参与选型。

## 每轮给下一轮的依据

零拟合train诊断核对了全部25次OOF改选的逐特征margin贡献。发现具体的词面表示缺陷：目标gallons of gas被抽成(gallon,of,gas)，正文10 gallons只匹配较短(gallon)，被误标mismatch；ounces of fudge与ounces类似。4个label修复里包括利用这种伪冲突的情况：加油题10对8的修复来自mismatch贡献；另一题也用同类贡献把正确14改成错误6。因此训练净+3并非都来自正确数量标签，不能把它称为可靠单位绑定。完整cases和贡献位于runs/round135-train-diagnosis；未使用validation/test个题。

下一轮只对当前题目标签的严格前缀关系作unknown处理：一个完整标签与其短前缀不再计冲突，也不自动当精确match。此修正来自train表示审计，保持其他抽取、父模型、λ、fold、权重与尺度协议，比较修复前后。不同时修改人名词表、扩大窗口或增加单位换算，以区分表示修复和其他变化。

下一步应以本表的训练修复/新增和三折稳定性决定是否继续这个家族。单独label与role分支可区分精确数量标签和稀疏人名/状态是否互补；若组合新增错误抵消修复，不继续堆关键词。若标签有正向训练净收益但验证持平，也只算训练开发证据，需新保留数据确认。任何词法扩展必须先按train中的目标标签抽取失败/中间量混淆分层审计，独立列出旧正确反例，不按test个题修规则。

## 完整性、失败和复现

最大全部递归未压缩资产64728字节，完整fresh validation预测+独立官方评分最多6.648秒、test最多5.099秒；CPU总4线程，满足16MiB/30秒，本机资格不代替参考Xeon。训练600秒硬限，所有parser/原始数据/官方工具/父源资产、父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全train导出/零残差/重排/题序/新ID/变batch/空输入/同答案同分检查完成。旧132/133压缩包SHA通过。

失败记录：首次builder在拟合前因先替换answer_mentions后schema期望字符串过时而触发guard；原builder保存在runs/round135-source-build-repair，仅修正预期中间字符串，没有修改特征、计划、审计或模型。此时0拟合/0验证/0测试。之后12拟合、4验证、3测试完成，每项test一次。

复现：audit_round135_quantity_binding.py → build_round135_experiment.py → train_round135_quantity_binding.py → train_round135_quantity_binding.py --evaluate → run_frozen_tests_round135.py → closeout_round135.py；已有输出目录拒绝覆盖。所有原始聚合分数、拟合/命令/过程监控、冻结源与参数保留；无公开提交或issue。Codex实质参与实现、训练、评估与分析，AI_DISCLOSURE.md同步记录。

统计11项解释边界覆盖分母/分层、选择条件、生态外推、相关/因果/反向因果、混杂、回归均值、多次比较、假设与效应范围；不作独立显著或稳定提升主张，不作Collider调整。


# Round136：标签短前缀不计冲突

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合、3官方validation。

完整123固定，label/both分别4/12维残差，λ.1，same-fit完整父margin、原折/fit-only尺度/每题pair权重。唯一变化：目标和观察标签互为严格前缀时unknown，不计match/mismatch；人名/状态和其他词法保持135。不是单位换算或语义证明。纯train全量断言其他列不变。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|control|4404|0/0|[0, 0, 0]|754|0/0|62.01|4.045|
|label|4408|4/0|[2, 1, 1]|753|0/1|63.02|6.321|
|both|4407|6/3|[2, 2, -1]|752|0/2|63.21|6.489|

未严格胜过(754,4404)，保留123。

8拟合worker95.462秒，4总线程，600秒硬限。原父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全训练导出/零修正/重排等接口和源/计划/父新资产SHA通过。全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒，参考Xeon未认证。

两个新版本按预先名单全部冻结后测试；本脚本未执行test，test不用于拟合或本批开发选择。长期自适应开发、已知test汇总披露，不作独立显著/稳定泛化/因果主张；11项解释边界沿用前轮，报告全部配置/分母/折与失败。

复现audit_round136_prefix_unknown.py、train_round136_prefix_unknown.py及--evaluate，再run_frozen_tests_round136.py；旧证据拒绝覆盖。


# Round136：两个数量关联版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。两个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round136_label|4408|753|389|83.2976%|-1|63.02|4.411|
|round136_both|4407|752|388|83.0835%|-2|63.21|4.139|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round136-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round136-all-test-20261029，原模型与79主交付保留，未公开提交。


# Round136学习记录：标签短前缀不计冲突

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合、3官方validation、2个新最终候选统一冻结后各一次官方test。

## 全部结果

|版本|OOF/4755|回代/4755|相对123修复/新增|三折净变化|验证/798|验证修复/新增|test/467|
|---|---:|---:|---|---|---:|---|---:|
|原123控制|4404|4519|0/0|[0,0,0]|754|0/0|390（已有）|
|135_label|4407|4524|4/1|[2, 0, 1]|753|0/1|390（已有）|
|136_label|4408|4523|4/0|[2, 1, 1]|753|0/1|389|
|135_both|4407|4522|6/3|[2, 2, -1]|752|0/2|389（已有）|
|136_both|4407|4522|6/3|[2, 2, -1]|752|0/2|388|

135_role特征全量不变，其OOF4404、validation754、test390引用已有记录，不重新拟合/测试。

## 单一修正和配对输入审计

只把目标与观察标签互为严格前缀时记unknown，不把不完整标签提升为match；其他抽取、词表、窗口、人名、状态、数字及官方final解析保持。全部4755题断言精确match列、人名/状态列不变，只有两列label_mismatch下降。

共121题特征变化，原123错题11、原对题110；own冲突减少138个组cue，foreign减少35个。变化仅是表示修复，覆盖不代表纠错，组cue数量也不等于题数。

局限保持：following()在of处截断，因此正文明确写gallons of gas时仍可能只观察gallon，对长目标记unknown。没有把它偷换成完整短语识别，没有顺便过滤Then等伪人名或扩词表。初次构造预期误以为完整短语可被旧抽取器识别，读取数据前即失败；更正检查预期后，方法实现和计划均未改。

## 相对135的变化：区分局部输入与全局重拟合

|模式|分层|题数|改选|修复|新增|净变化|
|---|---|---:|---:|---:|---:|---:|
|label|all|4755|4|2|1|+1|
|label|changed_inputs|121|2|1|1|+0|
|label|unchanged_inputs|4634|2|1|0|+1|
|both|all|4755|0|0|0|+0|
|both|changed_inputs|121|0|0|0|+0|
|both|unchanged_inputs|4634|0|0|0|+0|

父模型、λ.1、同fit完整父margin、原折、每题pair权重及fit-only标准化协议固定。但特征分布改变会使拟合尺度和权重改变，因此未改变输入的题也可能变分/改选；不能把所有净收益归因于121题的局部表示修复。上表全报这一混杂。未再试λ、额外种子或组合强度。

## 开发选择和下一轮依据

没有新输出严格胜过(754,4404)，保留123开发身份。既有验证最高754、已观察test最高392的模型与包均保留。

本轮全部2个新最终候选按固定名单统一冻结测试，最高389/467；无test逐题分析、改参或按test选新研究身份。test已暴露，若后续据其挑最终提交模型须披露参与选型。

本轮可以否定“修正词面一致性必定提升准确率”的假设。下一次应先判断表中收益是否来自变化输入、是否两折以上一致、是否保住验证，而非继续扩大前缀或同义词规则。若修正仅恢复原754，就停止这个特征家族；规则一致性改进与选题准确率改进分别报告。

## 资源、完整性、失败、复现

最大全部递归未压缩资产64727字节，fresh完整validation预测+独立评分最多6.489秒、test4.411秒，4总CPU线程，符合16MiB/30秒；参考Xeon未认证。训练600秒硬限。原135及父源/资产/分数/计划、原132/133/135包SHA保留；缓存、原父OOF、梯度/重复pair/每题权重/fit-only尺度、全train导出/零残差/重排/题序/新ID/batch/空输入/同答案同分检查通过。

失败完整保留：1. 首次fixture错误预期完整of短语能被旧抽取器识别，0数据/0拟合即停止，原audit源与failure.json留在runs/round136-train-audit；实际审计-v2仅更正fixture。2. builder把只在train中的unseen135 token也要求在test替换，拟合前guard停止；原builder/部分生成源留在runs/round136-source-build-repair，修正guard并核对部分源完全一致，没有覆盖源或改特征。之后8拟合、3验证、2测试完成，每项test一次。

复现：audit_round136_prefix_unknown.py → build_round136_experiment.py → train_round136_prefix_unknown.py → train_round136_prefix_unknown.py --evaluate → run_frozen_tests_round136.py → closeout_round136.py。新目录拒绝覆盖。统计11项解释边界沿用135：自适应train/validation、多次比较、条件筛选、分层分母、回代/OOF、混杂、生态外推、回归均值和相关/因果范围；不作独立显著或稳定因果提升主张，无公开提交/issue。AI实质协助已披露。


# Rounds135–136：数量关联与前缀修正的完整记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；2轮、20新拟合、7次官方validation（含2次父控制）、5个新最终候选统一按批冻结后各一次官方test。

|候选|训练OOF/4755|验证/798|test/467|
|---|---:|---:|---:|
|原123控制|4404|754|390（已有）|
|round135_label|4407|753|390|
|round135_role|4404|754|390|
|round135_both|4407|752|389|
|round136_label|4408|753|389|
|round136_both|4407|752|388|

## 结论与后续决策

**没有新增验证或测试最高分。** 开发身份仍为123，validation754/798；此前132以及133传播/组合的已观察test最高392/467保持。两轮新输出全部保留但不晋级，无公开提交。

135增加精确邻接数量标签、人名与状态，label与both OOF均4407，但validation753/752；role OOF4404、validation754。抽取仍有歧义；不能把match当正票或把mismatch当错误证明。

135纯train逐特征margin诊断定位了具体误标：目标gallons of gas与正文gallons、ounces of fudge与ounces被当冲突。136仅把严格前缀关系记unknown，全量断言其他列不变；121题变化，其中11个原错。label OOF4408、修4/新增0、三折[+2,+1,+1]，validation仍753，test389；both OOF4407、validation752、test388。

相对135，136_label在121个输入变化题上修1/新增1，净0；其余4634题重拟合后的修1/新增0带来净+1。136_both训练选择完全不变。这说明仅看训练总分会把全局拟合波动当成局部表示修复的收益；没有证据把这种修正称准确率突破。

停止继续扩展当前词面数量标签家族，不据test个题、阈值或同义词扩表重试。若开启新路线，需能补充可靠的数量角色/算式关系或提供真正不同的学习信号，先在train对照旧正确反例及fold稳定性；不要把浅词窗升级为“语义推理”声称。规则一致性修复与准确率改进分别报告。

## 资源与完整性

两轮最大完整递归未压缩资产64728字节，fresh完整validation预测+独立评分最多6.648秒、test5.099秒，CPU总4线程，符合16MiB/30秒；参考Xeon未认证。原132/133/135/136包SHA核对，原135/父源资产保持。

拟合与5次实际test均完成，每项test一次。拟合前135builder schema guard、136fixture和builder guard，以及136打包计划文件名错误都保留原源和失败记录；均未据结果改特征/重训或重跑评分。136不完整首次打包目录另存output/round136-prefix-candidates-first-run；修正文档路径后重新打包，0新预测。136包元数据复制的three状态文字已单独纠正为通用文字，实际model_count一直为2，zip与源/资产/分数保持。

test按用户既有授权全报，未用于两批拟合、调参或开发选型；长期自适应开发与已暴露test汇总披露。若最终按test分选交付版本须说明测试参与选择，不称独立最终估计。11项解释边界见逐轮记录。

## 可复核文件

- [135完整学习与失败](ROUND135_LEARNING.md)、[136配对学习与失败](ROUND136_LEARNING.md)。
- [135官方测试](FINAL_TEST_ROUND135_ALL_RESULTS.md)、[136官方测试](FINAL_TEST_ROUND136_ALL_RESULTS.md)。
- [135全部3候选推理包](output/round135-quantity-candidates.zip)、[136全部2候选推理包](output/round136-prefix-candidates.zip)。
- 训练改选逐特征贡献：code/runs/round135-train-diagnosis；135/136计划在项目根目录，原始拟合/冻结/命令/评分/监控在各runs与final_evaluation目录。


# Round137：模块校准与联合更新

## Material Passport

academic-research-suite / experiment-agent；20次拟合、6个训练配置、2个train选λ最终候选、3次官方validation。计划和首次审计开始日期2026-10-29；精确过程时间见命令/冻结记录。

|配置|OOF/4755|修复/新增|三折净变化|选为最终输出|
|---|---:|---|---|---|
|round137_mix_l0p01|4401|11/14|[-1, -2, 0]|False|
|round137_mix_l0p1|4405|9/8|[-2, 0, 3]|False|
|round137_mix_l1p0|4406|4/2|[-1, 1, 2]|True|
|round137_joint_l0p01|4383|31/52|[-4, -17, 0]|False|
|round137_joint_l0p1|4398|17/23|[0, -8, 2]|False|
|round137_joint_l1p0|4406|9/7|[-1, 0, 3]|True|

|最终版本|OOF/4755|回代/4755|validation/798|验证修复/新增|KiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|
|round123_both_l0p01|4404|4519|754|0/0|62.01|3.768|
|round137_mix_l1p0|4406|4517|753|0/1|60.98|3.041|
|round137_joint_l1p0|4406|4519|752|0/2|60.99|3.121|

开发选择：保留123，先于新test。两候选会统一冻结后各一次test；本评价未运行test。

四块输入与123保持，mix训练4个系数偏移，joint同时更新5180个已有权重；λ均只在train OOF选，两种正则几何不同，不将差异全部归因于参数数量。旧fit-only中心/尺度逐fold重建held1e-10，零更新和独立导出检查通过。长期自适应train/validation和已知test汇总披露，OOF选λ后分数是开发指标。

全部原始源/父资产/官方工具/数据保持，候选完整接口及所有资产<=16MiB、完整fresh预测+独立评分<=30秒本机检查通过，4总线程；参考Xeon未认证。训练600秒硬限，验证全部输出而不按中途结果改名单/参数。复现audit_round137_joint_retrain.py → train_round137_joint_retrain.py → evaluate_round137_joint_retrain.py；原输出拒绝覆盖。


# Round137：两个最终版本的冻结测试

## Material Passport

两个版本在第一项新test前统一冻结，各一次完整fresh预测与独立官方评分，无新拟合、test个题分析或按test选型。

|版本|训练OOF/4755|验证/798|test/467|test准确率|完整KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---:|
|round137_mix_l1p0|4406|753|392|83.9400%|60.98|2.237|
|round137_joint_l1p0|4406|752|395|84.5824%|60.99|2.331|

test前开发选择：保留123；不按上述test分数更换。测试已经多次暴露，不能作独立最终估计。test只用于冻结评价，不用于训练、调参、选型或规则。

完整冻结源/资产/命令/日志/官方JSON见final_evaluation/round137-all-test-20261030。4总CPU线程、全部递归资产<=16MiB、完整预测+评分<=30秒，本机不代替参考Xeon认证；无公开提交/issue。


# Round137学习记录：模块校准与联合更新

## Material Passport

academic-research-suite / experiment-agent；计划/审计开始2026-10-29，冻结测试完成时戳见FROZEN_POOL与各result；20拟合、3官方validation、2项统一冻结测试。

## 全部训练配置

|家族|λ|OOF/4755|修复/新增|三折净变化|全train导出|
|---|---:|---:|---|---|---|
|mix|0.01|4401|11/14|[-1, -2, 0]|False|
|mix|0.1|4405|9/8|[-2, 0, 3]|False|
|mix|1.0|4406|4/2|[-1, 1, 2]|True|
|joint|0.01|4383|31/52|[-4, -17, 0]|False|
|joint|0.1|4398|17/23|[0, -8, 2]|False|
|joint|1.0|4406|9/7|[-1, 0, 3]|True|

## 官方完整评价

|版本|OOF/4755|回代/4755|验证/798|验证修复/新增|test/467|test准确率|
|---|---:|---:|---:|---|---:|---:|
|原123控制|4404|4519|754|0/0|390（既有）|83.5118%|
|round137_mix_l1p0|4406|4517|753|0/1|392|83.9400%|
|round137_joint_l1p0|4406|4519|752|0/2|395|84.5824%|

## 分数记录与开发身份分开

两版本均未在(validation,OOF)上严格胜过(754,4404)，故test前已记录保留123开发身份。joint的395/467（84.582441%）超过此前已观察392/467三题，增加0.642398个百分点；mix为392，持平旧已观察最高。这是按原名单全部冻结测试得到的观察记录，未按test选模型或改变开发身份。验证最高仍754，新joint为752，不能把test新记录称验证新高、稳定泛化提升或独立最终估计。

## 本轮检验了什么

保持原123四块输入：A1034、L26、I128×32、G24。先在full训练分数和三个held上精确重建原模型1e-10，零更新与独立NPZ导出一致；每折中心和尺度来自对应fit-only旧参数。mix更新4个模块系数，joint同时更新5180个已有权重，近端正则围绕原参数。更新使用完整组pair，没有重做A原训练子集增强。

两家族均在train OOF选λ1，未按validation/test改λ。mix修4/新增2、三折[-1,+1,+2]；joint修9/新增7、三折[-1,0,+3]，训练净收益各2题，尚不稳定。联合版目标/梯度收敛并不意味着0–1准确率必升。其验证新增2错而无修复，与test新记录方向不同，具体原因尚未证实；没有通过test个题反推规则。

原同fit父margin仍包含训练乐观性；本轮没有重做125嵌套margin。mix原分数尺度和joint标准化特征空间正则几何不同，不能把两者差异全归因于参数数目。每块尺度固定而权重允许更新，避免了135–136词法修复同时改变scaler的混杂，但使用既有自适应父中心仍限制独立解释。

## 权重更新描述（不作因果贡献）

|模型|模块|参数数|原权重L2|更新L2|相对L2|
|---|---|---:|---:|---:|---:|
|round137_mix_l1p0|A|1034|2.94246|0.177808|0.0604281|
|round137_mix_l1p0|L|26|0.229792|0.000274415|0.00119419|
|round137_mix_l1p0|I|4096|0.256041|0.00162652|0.00635255|
|round137_mix_l1p0|G|24|0.399436|0.000616768|0.0015441|
|round137_joint_l1p0|A|1034|2.94246|0.0358017|0.0121673|
|round137_joint_l1p0|L|26|0.229792|0.0091925|0.0400035|
|round137_joint_l1p0|I|4096|0.256041|0.0251963|0.098407|
|round137_joint_l1p0|G|24|0.399436|0.00450538|0.0112794|

mix完整train模块系数(A,L,I,G)=[1.0604281044408277, 1.001194187941217, 1.0063525475527484, 1.0015440985723953]。这些只是当前拟合描述，未据系数选择新版本/增大更新强度。

## 旧专家互补审计：有空间，不等于已能融合

|已有专家|OOF/4755|补回123错|错掉123原对|改选数|与123真值择优上限|
|---|---:|---:|---:|---:|---:|
|round108_subsets_l0p01|4380|24|48|85|4428|
|round110_final_evidence|4398|21|27|52|4425|
|round112_linear_uniform_ce|4345|71|130|221|4475|
|round112_linear_correct_set_mass|4337|61|128|207|4465|
|round112_pointwise_uniform_ce|4305|87|186|295|4491|
|round112_pointwise_correct_set_mass|4285|85|204|320|4489|
|round112_deepsets_uniform_ce|4283|90|211|329|4494|
|round112_deepsets_correct_set_mass|4301|85|188|302|4489|
|round112_attention_uniform_ce|4291|100|213|343|4504|
|round112_attention_correct_set_mass|4319|84|169|283|4488|

全部这些专家与123的真值择优并集为4618/4755，能覆盖351个123剩余错中的214个；这是使用真值选专家的上限，不是可部署精度，不是新模型或融合结果。注意力uniform专家可补100错、同时错掉213个原对题，不能据此直接平均。

本轮没有临时增加融合器。下一研究依据是train中的专家互补和误切换风险：用严格嵌套OOF检验能否从允许输入识别可靠专家；若只是放大平均分导致更多旧正确受损，应停止。不要根据本轮test395反向选择专家/λ/门槛，也不继续扩词法规则。

## 完整性、资源和复现

新版本最大全部递归未压缩资产62449字节，fresh完整validation预测+独立评分（含原控制）最多3.768秒，test最多2.331秒；总4CPU线程，满足16MiB/30秒，本机不代替参考Xeon认证。训练worker27.376秒、600秒硬限，20拟合全部完成。

本轮无运行失败/重试，2项test各一次。原123/父及135/136等源资产、旧132/133/135/136包、官方工具/数据/parser SHA保持；折中心/分区、四块分数、零更新、pair权重/抽样梯度/重复pair、缓存/全train导出及严格重排/题序/新ID/变batch/空输入/Python整数/同答案同分全部核验通过。独立导出不必读取嵌套父checkpoint，但源码重用和原权重来源仍披露。

复现：audit_round137_joint_retrain.py → train_round137_joint_retrain.py → evaluate_round137_joint_retrain.py → run_frozen_tests_round137.py → closeout_round137.py；训练复现依赖项目保留的原父折/全train参数与输入数据，便携推理包仅用于免重训复现。所有输出目录拒绝覆盖。完整源/资产/命令/评分/时戳/环境在runs/round137-*及final_evaluation对应目录；无公开提交/issue。

统计11项解释边界：同时全报总体/分歧/单正确及三折；不外推其他题库；条件筛选/候选分布不作因果调整；明确分母/回代/OOF/真值oracle；注意回归均值；保留全部6配置与2项test，披露多次比较和自适应路径；参数化/正则/父中心混杂；不把相关、系数、反向因果或最高暴露test记录当作独立稳定因果收益。AI实质协助已同步记录。


# Round137小结：联合更新得到新的已观察测试分数

## Material Passport

academic-research-suite / experiment-agent；计划开始2026-10-29，测试冻结/完成时戳2026-10-30（UTC+8）；20次拟合、6个训练配置、3次官方validation、2个最终候选统一冻结后各一次官方test。

|版本|训练OOF/4755|官方验证/798|官方test/467|test准确率|
|---|---:|---:|---:|---:|
|原123控制|4404|754|390（已有）|83.5118%|
|137模块校准λ1|4406|753|392|83.9400%|
|137联合更新λ1|4406|752|395|84.5824%|

## 已经确认的结果

- 新的已观察test最高395/467，比此前392多3题，增加0.642398个百分点；没有刷新验证最高754。395不是独立最终泛化估计。
- 两个家族均由训练OOF从λ=.01/.1/1选出λ1，随后全部官方验证；未通过预定开发排序，因此test前已保留123研究身份，test分数不改变它。
- 首次test前两个候选源/权重统一冻结，各一次完整预测+独立官方评分；没有test逐题分析、改参或按test选提交模型。
- 四块A/L/I/G保持原123输入，重新学习组合或同时更新5180个已有权重。每折只使用对应fit-only原参数/尺度为中心，精确重建原held与全train分数1e-10；独立导出不需要读取父checkpoint。
- mix与joint训练净收益都是2题，三折分别[-1,+1,+2]和[-1,0,+3]。验证分别少1和2题；test新分数的稳定性、原因尚未证实，不据此增加参数搜索。

## 下一步的训练依据

已有专家真值择优可覆盖123剩余351错中的214题，但许多专家也会损害更多原正确题。这是机会诊断，不能当可部署精度。下一独立计划应在严格嵌套OOF下验证“何时切换专家”是否可以从允许输入预测；依据是已预定的train互补审计，不能根据本轮test高低挑专家或调参数。

## 资源、交付与复现

两个新版本最大完整递归未压缩资产62,449字节，本机fresh完整test预测+独立评分最多2.332秒；总4CPU线程，满足16MiB/30秒。参考Xeon完整test资格未认证。20拟合worker27.379秒、600秒硬限；本轮无运行失败或重试，源/数据/parser/官方工具/父新资产、梯度/重复pair/每题权重/缓存/零更新/导出/接口检查通过。

- [完整六配置、分层结果与分析](ROUND137_LEARNING.md)
- [全部官方冻结测试](FINAL_TEST_ROUND137_ALL_RESULTS.md)
- [两个候选完整推理代码与checkpoint包](output/round137-joint-candidates.zip)
- [候选包及哈希元数据](ROUND137_CANDIDATE_BUNDLE.json)
- [已观察分数记录，包含全部候选](OBSERVED_TEST_RECORD_ROUND137.json)

原123开发候选、132及133等旧记录/资产包均保留，未公开提交或创建issue。便携包用于免重训复现，完整训练过程及历史父折参数在原项目code/runs中；命令见学习记录。AI实质协助及长期自适应train/validation、多次test暴露继续披露。


# 最终模型冻结与提交状态

用户已选定并冻结 **round137_joint_l1p0**，时间2026-10-30T00:24:58.993181+08:00。此版本停止训练与调参，后续训练需用户明确解除冻结。

|指标|最终模型|
|---|---|
|官方测试|395/467，84.58244111349036%|
|官方验证|752/798，94.23558897243107%|
|训练OOF|4406/4755（开发指标）|
|全部推理资产|62449字节|
|本机测试预测+独立评分|2.331497200008016秒，4总线程|
|正式提交|未提交|

[独立最终交付包](output/final-round137-joint-395.zip) · [冻结元数据与全部SHA](FINAL_MODEL_FROZEN.json) · [运行说明](output/final-round137-joint-395/README.md)。

最终模型指针CURRENT_BEST.json已由历史79切换为137；切换前完整指针另存，原79、123、所有其他候选及首次测试前清单/分数/历史包不改。研究开发选择仍123（验证754），与用户此次最终选定分开。

用户在测试成绩已知后选定最终版本，已明确记录测试参与最终人工选定，与课程要求测试不用于选型存在差异。报告须如实披露，不称395是独立最终泛化估计，也不能沿用旧阶段“测试完全未参与最终选择”的表述。原训练与λ选择仍只用train OOF。

模型冻结与SHA核验已完成，本次0训练、0预测、0评分。参考Xeon资格未认证。课程<=10页报告、公开代码与checkpoint链接、网站及实际GitHub issue提交仍待完成；无公开发布。
