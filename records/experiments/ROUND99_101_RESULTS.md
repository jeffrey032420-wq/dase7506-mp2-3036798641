# Rounds99–101：局部步骤监督、监督二阶矩与条件化候选比较

Material Passport: academic-research-suite / experiment-agent；2026-10-27；VERIFIED_LOCAL_VALIDATION。

**全部12个新输出均未超过749/798（93.8596%），保留Round79。** 三条路线各4配置，全部12项在本批验证前固定；仅由给定train拟合，无外部数据或预训练权重。
全train回代只是描述，不是OOF或持出准入；validation已反复用于自适应开发，不是独立测试成绩。

## 假设与匹配消融

**Round99：参考解的局部过程监督。** 从自然语言局部步骤提取经过精确算术检查的运算根，并清除数字、数学式与LaTeX后训练文本运算分类器。
last仅用每题最后一个有效参考步骤，all用全部有效步骤但保持每题监督总重1；词/相邻词TF-IDF最多6000项、min_df3、C1。
推理比较候选中已识别真算式根与文字预测的兼容度，按训练先验校正、裁剪并在已识别候选间中心化，未知候选中性；只有一项已知时不干预。
固定strength.1/.25乘原始分数标准差，保留原保护流程。这是局部算式/语言兼容监督，不等于验证完整推理或最终答案正确。
之前已有完整程序、目标运算、数值关系及参考全文增强；本轮不将这些统称为未尝试。

**Round100：监督基对匹配随机基。** 用父79标准化的1024维Embedding题内中心化，在2513信息题上逐题逐类等权，计算正确与错误的未扣类均值二阶矩差D。
取绝对特征值最大的16轴，对照固定seed20261027的16维QR正交随机基。将投影平方加入原1422维，新增统计量仅拟合train，联合成对ridge旧块alpha.3、新块alpha.3/3。
这是监督方向选择及匹配随机控制，不是新的二次函数表达能力；历史全二次、PCA-Gaussian、监督低秩失败提供负面先验。监督基仍可能过拟合。

**Round101：问题条件化的共同分歧跨度。** 匹配legacy候选成对表示与增加共同对齐首尾分歧、问题目标/条件/量词上下文的conditioned表示，各配线性分类器和小树。
两方向比较按题均衡，推理显式反对称并汇总固定比赛，strength.1。固定12尾句与通用单调对齐；不搜索早停或迭代数。
历史已有成对树、成对核及局部编辑；本轮检验条件化共同跨度在匹配表示/学习器控制下是否互补。

三路线训练锚点为父79，train回代4406/4755；正式选型对照是本批冻结的实际Round79/749，二者分别核验。
保留numeric alpha1与原gate，raw分数组合后仅一次格式转移，推理不读取参考答案。

## 完整训练、控制和失败记录

实际训练/导出审计耗时：99=83.093秒、100=66.906秒、101=250.446秒；各1线程、600秒硬限。
99有2个运算教师、4强度输出；100有1个监督基、1个随机基、4个联合候选解与旧块控制；101有4个固定表示/学习器输出。
零干预、数学/合成特征、模型导出、全训练缓存一致性及53题合同全部按记录核验。全部固定输出进入验证，没有按回代筛选或扩大本池。
首轮失败及验证前修复快照单独保留并核验；不得将零fit的读取失败算成一次模型实验，也不得丢弃真实数学/拟合失败。
99首次读取参考JSONL的实现失败发生在拟合前，0个完成模型；保留旧源码、失败、原始来源哈希与输入记录。
101在源码冻结前修正两个合成控制问题：等长目标词替换以保留legacy问题长度，及两方向统一C内存布局以消除相同成对输入的BLAS舍入差；两者均0fit、无验证反馈，不增加模型配置。

|轮次|配置|train回代 /4755|回代修复 / 新错（对固定父79）|
|---|---|---:|---:|
|99|reference-steps=last; strength=0.1|4406|4 / 4|
|99|reference-steps=last; strength=0.25|4401|6 / 11|
|99|reference-steps=all; strength=0.1|4407|3 / 2|
|99|reference-steps=all; strength=0.25|4405|6 / 7|
|100|basis=supervised; rank=16; new-block α=0.3|4420|41 / 27|
|100|basis=supervised; rank=16; new-block α=3|4411|16 / 11|
|100|basis=random; rank=16; new-block α=0.3|4409|17 / 14|
|100|basis=random; rank=16; new-block α=3|4405|5 / 6|
|101|pair=legacy; learner=linear; strength=.1|4407|3 / 2|
|101|pair=legacy; learner=tree; strength=.1|4402|7 / 11|
|101|pair=conditioned; learner=linear; strength=.1|4406|3 / 3|
|101|pair=conditioned; learner=tree; strength=.1|4402|7 / 11|

聚合训练/控制及修复记录（不是新OOF）：

```json
{
  "diagnostics": {
    "99": {
      "coverage": {
        "teacher_questions_known": 4558,
        "teacher_step_count": 13853,
        "teacher_reasons": {
          "known": 13853,
          "fewer_than_three_verbal_words": 223
        },
        "candidate_reasons": {
          "known": 28489,
          "fewer_than_three_verbal_words": 2395,
          "mixed_root_line": 133
        },
        "candidate_step_count": 28489,
        "candidate_known_count": 13024,
        "candidate_total": 19020,
        "questions_by_known_candidate_count": {
          "4": 1950,
          "3": 1048,
          "2": 763,
          "1": 554,
          "0": 440
        },
        "training_only": true,
        "before_classifier_fits": true
      },
      "control": {
        "raw_parent_format_once_max_error": 0.0
      },
      "classifier_fit_count": 2,
      "fixed_output_count": 4,
      "training_threads": 1,
      "threads": 1,
      "new_OOF": false,
      "oof_estimate_available": false,
      "training_resubstitution_only": true,
      "validation_used": false,
      "test_used": false,
      "seconds": 83.09348999999929,
      "format_transfer_count": 1,
      "fixed_training_parent": "runs\\round79-regularization\\candidates\\round79_s0p3_n1p0",
      "deadline_seconds": 600
    },
    "100": {
      "control": {
        "old_gram_weight_max_error": 2.040034807748725e-15,
        "old_gram_train_semantic_score_max_error": 5.039315303173268e-14,
        "synthetic_moments": {
          "explicit_outer_product_max_error": 4.440892098500626e-16,
          "class_mean_identity_max_error": 2.7755575615628914e-16,
          "uncentered_vs_centered_class_difference_Frobenius": 0.8867101076651037,
          "excluded_noninformative_change_max_error": 0.0,
          "candidate_permutation_max_error": 1.1102230246251565e-16,
          "toy_population": {
            "informative_questions": 3,
            "positive_class_total_mass": 3.0000000000000004,
            "negative_class_total_mass": 3.0,
            "positive_question_mass_max_error": 0.0,
            "negative_question_mass_max_error": 0.0,
            "signed_question_mass_max_error": 1.1102230246251565e-16,
            "positive_second_moment_Frobenius": 3.21078704382156,
            "negative_second_moment_Frobenius": 2.0078691351533364,
            "positive_second_moment_trace": 5.094099241504188,
            "negative_second_moment_trace": 3.2175112329491022,
            "positive_weighted_global_class_mean_L2": 0.5067428441609413,
            "negative_weighted_global_class_mean_L2": 0.6243606523733505,
            "class_means_subtracted": false
          },
          "does_not_subtract_class_means": true
        },
        "zero_added_complete_pipeline_max_error": 5.040412531798211e-14,
        "zero_added_checkpoint": "runs\\round100-moment-basis\\zero_added_control",
        "zero_added_selectable": false
      },
      "basis_diagnostics": {
        "population": {
          "informative_questions": 2513,
          "positive_class_total_mass": 2513.0,
          "negative_class_total_mass": 2513.0,
          "positive_question_mass_max_error": 0.0,
          "negative_question_mass_max_error": 0.0,
          "signed_question_mass_max_error": 1.1102230246251565e-16,
          "positive_second_moment_Frobenius": 20.752723744669076,
          "negative_second_moment_Frobenius": 23.190242047035635,
          "positive_second_moment_trace": 80.85635843381971,
          "negative_second_moment_trace": 90.28034924101908,
          "positive_weighted_global_class_mean_L2": 0.9808883443459109,
          "negative_weighted_global_class_mean_L2": 1.3302290422518839,
          "class_means_subtracted": false
        },
        "D_symmetry_max_error": 5.551115123125783e-17,
        "D_Frobenius_norm": 3.809170636499551,
        "D_trace": -9.42399080719936,
        "D_eigenvalue_min": -3.0110109644884706,
        "D_eigenvalue_max": 0.5504937769262652,
        "selected_eigenvalues": [
          -3.0110109644884706,
          -1.282747664165295,
          -1.0091040985008441,
          -0.6232444066079272,
          0.5504937769262652,
          0.45897662118243154,
          0.43832557037190634,
          -0.4048187759147223,
          -0.3612129886881357,
          -0.2991383096877962,
          0.2640568267680007,
          -0.25351894278068143,
          -0.23794610480114162,
          -0.22165331709106947,
          0.21715712342772373,
          0.20219894155879276
        ],
        "selected_eigen_indices": [
          0,
          1,
          2,
          3,
          1023,
          1022,
          1021,
          4,
          5,
          6,
          1020,
          7,
          8,
          9,
          1019,
          1018
        ],
        "selected_squared_eigenvalue_energy_fraction": 0.9328748928643157,
        "eigen_residual_relative_Frobenius": 1.6067887765878209e-15,
        "basis_checks": {
          "supervised": {
            "orthogonality_max_error": 1.5543122344752192e-15,
            "canonical_signs_positive": true,
            "rayleigh_diagonal": [
              -3.0110109644884706,
              -1.2827476641652946,
              -1.0091040985008455,
              -0.6232444066079265,
              0.5504937769262651,
              0.4589766211824318,
              0.4383255703719059,
              -0.4048187759147222,
              -0.36121298868813534,
              -0.29913830968779587,
              0.2640568267680007,
              -0.25351894278068143,
              -0.23794610480114192,
              -0.22165331709106967,
              0.21715712342772417,
              0.20219894155879267
            ]
          },
          "random": {
            "orthogonality_max_error": 8.881784197001252e-16,
            "canonical_signs_positive": true,
            "rayleigh_diagonal": [
              -0.01859967931903404,
              -0.008178021981462927,
              -0.010970743740413189,
              -0.007187596887575346,
              -0.0012758877701969748,
              -0.004585204352672043,
              -0.005190073247236933,
              -0.008460612664098923,
              -0.011431949940061333,
              -0.005390665292566084,
              -0.01359109000149153,
              0.0015031558214405618,
              -0.011506645964402245,
              -0.03272158746744465,
              -0.004246249271133691,
              -0.007859491289022247
            ]
          }
        },
        "rank": 16,
        "random_seed": 20261027
      },
      "population": {
        "train_questions": 4755,
        "training_candidates": 19020,
        "informative_questions": 2513,
        "weighted_pair_rows": 8271,
        "all_correct_questions": 2242,
        "all_incorrect_questions": 0,
        "gated_questions": 282,
        "extra_scaler_fit_candidates": 19020
      },
      "fit_count": 4,
      "control_fit_count": 1,
      "gram_fit_count": 3,
      "ridge_solution_count": 5,
      "supervised_basis_fit_count": 1,
      "random_basis_draw_count": 1,
      "rank": 16,
      "threads": 1,
      "new_OOF": false,
      "oof_estimate_available": false,
      "training_resubstitution_only": true,
      "validation_used": false,
      "test_used": false,
      "seconds": 66.90554569999222,
      "format_transfer_count": 1
    },
    "101": {
      "population": {
        "legacy": {
          "informative_questions": 2513,
          "directed_pair_rows": 16542,
          "per_question_weight_max_error": 1.1102230246251565e-16,
          "positive_class_weight": 1256.5,
          "negative_class_weight": 1256.5,
          "class_weight_max_abs_difference": 0.0,
          "total_pair_weight": 2513.0
        },
        "conditioned": {
          "informative_questions": 2513,
          "directed_pair_rows": 16542,
          "per_question_weight_max_error": 1.1102230246251565e-16,
          "positive_class_weight": 1256.5,
          "negative_class_weight": 1256.5,
          "class_weight_max_abs_difference": 0.0,
          "total_pair_weight": 2513.0
        }
      },
      "synthetic_controls": {
        "first_last_joint_disagreement": [
          [
            1,
            1
          ],
          [
            2,
            2
          ]
        ],
        "canonical_alignment_reversal": true,
        "question_target_feature_change": 1.0,
        "legacy_target_change_max_error": 0.0,
        "question_number_context_feature_change": 0.3333333333333333,
        "pair_reverse_feature_max_error": 0.0,
        "identical_text_head_max_abs": 0.0,
        "finite_double_threshold_boundary": true,
        "conditioned_dimensions": 271
      },
      "prefit_control_corrections": [
        {
          "stage": "unfrozen synthetic-only control",
          "failure": "Target replacement apples to dollars changed legacy log-question-length.",
          "correction": "Use equal-length apples/dollar, both already in condition and candidate texts; legacy control stays identical.",
          "fit_count": 0,
          "validation_used": false,
          "test_used": false
        },
        {
          "stage": "unfrozen synthetic-only control",
          "failure": "Identical feature pair exact-zero assertion exposed C/F BLAS summation-layout roundoff.",
          "correction": "Both directed standardized matrices are C-contiguous, with identical-pair preference exactly zero.",
          "fit_count": 0,
          "validation_used": false,
          "test_used": false
        }
      ],
      "strength0_control": {
        "checkpoint": "runs\\round101-question-pair\\strength0_control",
        "complete_parent_max_error": 0.0,
        "selectable": false,
        "assets": {
          "config.json": {
            "bytes": 388,
            "sha256": "14cf25c2fd2752c3e95a449c999d5aeb8d10746bb1124db4358b560d200973e2"
          },
          "weights.npz": {
            "bytes": 86218,
            "sha256": "bc71d0ffd47771d37e3298be7ce07f901aa4d5c65b9fe430392002df6c2f5aaa"
          },
          "incumbent\\config.json": {
            "bytes": 28,
            "sha256": "acdc8cdb3c198152f19ac79021fe424b303999f69b5e4945eeb63cc7f8238e91"
          },
          "incumbent\\incumbent\\config.json": {
            "bytes": 105,
            "sha256": "20cb6c8cc8db92f267ecc72cbae8b39314dbc28a779bd556e5fbf54a00da3a94"
          },
          "incumbent\\incumbent\\baseline\\config.json": {
            "bytes": 177,
            "sha256": "be93ceeeed3651d3e3ecb386775b2b6a9278d8007c5c0f74818bd8eed04227c6"
          },
          "incumbent\\incumbent\\baseline\\weights.npz": {
            "bytes": 838670,
            "sha256": "468d5dd5f8439b0d12d9fcf9c63ce5e0c895203d58212fcdc9799891523512c3"
          },
          "incumbent\\incumbent\\numeric\\config.json": {
            "bytes": 112,
            "sha256": "221b52a89ba53699e128270c2e61dac71cbb05ae1cf1f7fccaf2e18f40589855"
          },
          "incumbent\\incumbent\\numeric\\weights.npz": {
            "bytes": 839062,
            "sha256": "d47a8cf8c20381e4c71befca446355f9d81862baa7955550a6fea95c428b16c5"
          }
        }
      },
      "fit_count": 4,
      "logistic_fit_count": 2,
      "tree_fit_count": 2,
      "teacher_class_weight_balanced": true,
      "legacy_candidate_dimensions": 1062,
      "conditioned_dimensions": 271,
      "new_OOF": false,
      "oof_estimate_available": false,
      "training_resubstitution_only": true,
      "validation_used": false,
      "test_used": false,
      "format_transfer_count": 1,
      "numeric_alpha": 1.0,
      "strength": 0.1,
      "threads": 1,
      "seconds": 250.44564180000452,
      "fixed_training_parent": "runs\\round79-regularization\\candidates\\round79_s0p3_n1p0"
    }
  },
  "preserved_failure_archives": [
    {
      "round": 99,
      "directory": "runs\\round99-step-operation\\first-attempt-reader-failure",
      "files": 8,
      "failure_type": "RuntimeError",
      "message": "Traceback (most recent call last):\n  File \"<USER_PROFILE>\\Documents\\ChatGPT\\course work\\DASE7506-MP2\\code\\train_round99_step_operation.py\", line 257, in <module>\n    worker()\n  File \"<USER_PROFILE>\\Documents\\ChatGPT\\course work\\DASE7506-MP2\\code\\train_round99_step_operation.py\", line 95, in worker\n    refs = [json.loads(s) for s in Path(INPUTS[0]).read_text(encoding='utf8').splitlines()]\n            ^^^^^^^^^^^^^\n  File \"<USER_PROFILE>\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\Lib\\json\\__init__.py\", line 346, in loads\n    return _default_decoder.decode(s)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"<USER_PROFILE>\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\Lib\\json\\decoder.py\", line 338, in decode\n    obj, end = self.raw_decode(s, idx=_w(s, 0).end())\n               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"<USER_PROFILE>\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\Lib\\json\\decoder.py\", line 354, in raw_decode\n    obj, end = self.scan_once(s, idx)\n               ^^^^^^^^^^^^^^^^^^^^^^\njson.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 14 (char 13)\n",
      "completed_fit_records": 0,
      "source_snapshot_verified": true,
      "all_archive_files_hashed": true
    }
  ]
}
```

## 冻结后的官方完整验证

|轮次|配置|验证 /798|修复 / 新错（对Round79）|改选数|完整资产 MiB|fresh预测＋独立评分秒|
|---|---|---:|---:|---:|---:|---:|
|99|reference-steps=last; strength=0.1|747|0 / 2|8|1.7921|3.475|
|99|reference-steps=last; strength=0.25|747|0 / 2|24|1.7921|3.499|
|99|reference-steps=all; strength=0.1|748|0 / 1|4|1.9498|3.551|
|99|reference-steps=all; strength=0.25|748|0 / 1|21|1.9498|3.500|
|100|basis=supervised; rank=16; new-block α=0.3|741|1 / 9|106|1.7380|3.045|
|100|basis=supervised; rank=16; new-block α=3|746|0 / 3|42|1.7380|2.702|
|100|basis=random; rank=16; new-block α=0.3|745|0 / 4|56|1.7379|2.671|
|100|basis=random; rank=16; new-block α=3|746|0 / 3|20|1.7379|2.704|
|101|pair=legacy; learner=linear; strength=.1|749|0 / 0|13|1.6830|3.594|
|101|pair=legacy; learner=tree; strength=.1|744|0 / 5|35|1.6973|3.725|
|101|pair=conditioned; learner=linear; strength=.1|748|0 / 1|14|1.6934|9.202|
|101|pair=conditioned; learner=tree; strength=.1|744|0 / 5|35|1.7056|9.353|

最佳新输出pair=legacy; learner=linear; strength=.1为749/798，修复0、新增0。局部参考步骤监督、监督二阶矩方向与条件化共同分歧表示均未在这组预定设置下超过动态对照；不能把更丰富训练监督或回代收益直接当作可靠提升。 这是相关且自适应的开发证据；不能据此证明模型上限、唯一原因或独立泛化。

匹配控制的正确数量比较，仅描述本池，不是独立效应估计：

```json
[
  {
    "round": 100,
    "matched_new_block_alpha": 0.3,
    "supervised_correct": 741,
    "random_correct": 745,
    "difference_in_counts": -4
  },
  {
    "round": 100,
    "matched_new_block_alpha": 3.0,
    "supervised_correct": 746,
    "random_correct": 746,
    "difference_in_counts": 0
  },
  {
    "round": 101,
    "matched_learner": "linear",
    "legacy_correct": 749,
    "conditioned_correct": 748,
    "difference_in_counts": -1
  },
  {
    "round": 101,
    "matched_learner": "tree",
    "legacy_correct": 744,
    "conditioned_correct": 744,
    "difference_in_counts": 0
  }
]
```

## 资源、完整性和复现边界

严格超过动态对照749且全部审计通过才晋级；同分保留incumbent，多个同分新赢家按更小完整资产、再按名称选择。
完整解压资产1,764,760–2,044,528字节≤16MiB；fresh完整验证预测＋独立评分2.671–9.353秒≤30秒，4总CPU线程。
动态对照另fresh复核749/798，2.059秒。只有全部训练进程停止后才计时；本地完整验证时间不等于参考CPU完整测试资格。
源码/计划、所有训练输入引用、旧R11、固定父79、动态对照、全部候选及历史来源显式含89–98均通过哈希审计。
原官方文件仅复核train/validation；测试输入/参考/预测/成绩没有读取、评分或哈希。
历史ZIP、PDF、submission_ready保持冻结快照，本轮不自动同步、公开上传、运行最终测试或创建GitHub提交issue。

证据：[99训练](code/runs/round99-step-operation/result.json)、[100训练](code/runs/round100-moment-basis/result.json)、[101训练](code/runs/round101-question-pair/result.json)、
[冻结](code/runs/round99-101/frozen-selection.json)、[全部验证](code/runs/round99-101/all-validation.csv)、[官方审计](code/runs/round99-101-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
