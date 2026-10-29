# Rounds97–98：显式几何与原坐标二次特征的联合排序

Material Passport: academic-research-suite / experiment-agent；2026-10-27；VERIFIED_LOCAL_VALIDATION。

**全部10个新输出均未超过749/798（93.8596%），保留Round79。** 四个几何配置和六个逐坐标二次配置在本批验证前固定；全部参数仅由给定train拟合，无外部数据或预训练权重。
不做新OOF/持出准入，全train回代仅作描述；validation反复用于自适应开发，不是独立泛化成绩。

## 预先提出的假设与消融

Round97假设：Embedding的同题相似度几何，以及在可解析答案组内/组外的相似度，可能补充原随机投影上下文排序。
比较4维同题cos几何和12维答案条件cos几何两个新特征块，各自新块alpha=.3/3，共四配置；原1422维表示的alpha保持.3。
Round98假设：随机投影的平方/交互可能未充分表示原1024个Embedding坐标的个别方向；直接加入逐坐标e²、e·同题均值或二者，可能提供互补。
固定self/context/both三种块，新块alpha=3/30，共六配置；旧块1422维alpha=.3。精确Schur补联合解同时更新旧/新系数，而非仅拟合固定父残差。
保持等题权成对平方目标、train拟合统计量、固定父79的numeric alpha1、原gate与一次R11格式转移。
不读取训练/验证/测试参考答案作为推理特征；所有变换统计量与系数均为显式推理资产。
历史已有核/二次/上下文表示，本轮是有限具体坐标与答案几何消融，不声称首次研究二次特征或候选间关系。
训练锚点固定父79，完整train回代为4406/4755；选型对照则为冻结的实际Round79/749，两者分别核验。

## 所有训练与控制

两个分支各1CPU线程/600秒硬预算，实际耗时Round97=71.263秒，Round98=57.359秒。
97有4个候选联合解和1个旧块控制解，共5次ridge求解；98有6个候选Schur解、1个旧块控制解及1次多右端交叉块求解，另保留6组小型Schur对直接联合求解的核对。零新增块控制不参与选型。
全部10个固定候选进入官方验证，不按回代筛选，未扩大本池。控制、求解残差、退化边界、导出等价性与完整计数见下方聚合原始记录。

|轮次|配置|完整train回代 /4755|回代修复 / 新错（对固定父79）|
|---|---|---:|---:|
|97|geometry; old α=.3; new-block α=0.3|4406|0 / 0|
|97|geometry; old α=.3; new-block α=3|4406|0 / 0|
|97|conditioned; old α=.3; new-block α=0.3|4368|16 / 54|
|97|conditioned; old α=.3; new-block α=3|4393|10 / 23|
|98|self; old α=.3; new-block α=3|4424|19 / 1|
|98|self; old α=.3; new-block α=30|4406|0 / 0|
|98|context; old α=.3; new-block α=3|4410|4 / 0|
|98|context; old α=.3; new-block α=30|4406|0 / 0|
|98|both; old α=.3; new-block α=3|4427|24 / 3|
|98|both; old α=.3; new-block α=30|4408|2 / 0|

训练聚合控制及资源记录（不是新OOF）：

```json
{
  "97": {
    "control": {
      "old_gram_weight_max_error": 2.040034807748725e-15,
      "old_gram_train_semantic_score_max_error": 5.039315303173268e-14,
      "synthetic_features": {
        "global_conditioned_expected_max_error": 0.0,
        "none_anchor_groups_empty": true,
        "none_participates_global": true,
        "zero_vectors_finite_cosine_statistics_zero": true,
        "norm_threshold_zero": true,
        "candidate_permutation_max_error": 0.0,
        "sorted_reductions": true,
        "population_std_ddof": 0
      },
      "zero_added_complete_pipeline_max_error": 5.040412531798211e-14,
      "zero_added_checkpoint": "runs\\round97-geometry\\zero_added_control",
      "zero_added_selectable": false
    },
    "population": {
      "train_questions": 4755,
      "training_candidates": 19020,
      "informative_questions": 2513,
      "weighted_pair_rows": 8271,
      "all_correct_questions": 2242,
      "all_incorrect_questions": 0,
      "gated_questions": 282,
      "unit_norm_zero_candidates": 0,
      "extra_scaler_fit_candidates": 19020,
      "constant_extra_features": [],
      "extra_feature_mean": [
        0.9846053434121801,
        0.976843549941477,
        0.9914318583806224,
        0.006316779222221166,
        0.7767102538069696,
        0.7804597724374357,
        0.416838482859168,
        0.41844062957640876,
        0.001353413284093527,
        0.0014950965075374012,
        0.78732912723449,
        0.4249211356466877
      ],
      "extra_feature_scale": [
        0.01105003520090428,
        0.01718040538609863,
        0.008072173804761114,
        0.0061997117298980215,
        0.40378362010549634,
        0.40570057085870004,
        0.4850185932903416,
        0.48687058239326625,
        0.008198579723766832,
        0.008479221582961298,
        0.4091967407526845,
        0.4943310268710375
      ],
      "same_group_present_candidates": 14975,
      "different_group_present_candidates": 8082
    },
    "fit_count": 4,
    "control_fit_count": 1,
    "gram_fit_count": 3,
    "ridge_solution_count": 5,
    "threads": 1,
    "new_OOF": false,
    "oof_estimate_available": false,
    "training_resubstitution_only": true,
    "validation_used": false,
    "test_used": false,
    "seconds": 71.2629406999913,
    "format_transfer_count": 1
  },
  "98": {
    "control": {
      "old_weight_max_error": 2.0660556598883772e-15,
      "old_train_semantic_score_max_error": 5.358665393546537e-14,
      "old_normal_equation_max_abs_residual": 6.661338147750939e-16,
      "parent_cached_direct_max_error": 0.0,
      "zero_new_complete_pipeline_max_error": 0.0,
      "zero_control_checkpoint": "runs\\round98-diagonal\\zero_new_block_control",
      "zero_control_selectable": false
    },
    "toy_direct_solve_audit": [
      {
        "family": "self",
        "new_block_alpha": 3.0,
        "direct_weight_max_error": 2.7755575615628914e-17,
        "full_normal_equation_max_abs_residual": 1.1102230246251565e-16
      },
      {
        "family": "self",
        "new_block_alpha": 30.0,
        "direct_weight_max_error": 2.7755575615628914e-17,
        "full_normal_equation_max_abs_residual": 1.1102230246251565e-16
      },
      {
        "family": "context",
        "new_block_alpha": 3.0,
        "direct_weight_max_error": 5.551115123125783e-17,
        "full_normal_equation_max_abs_residual": 2.220446049250313e-16
      },
      {
        "family": "context",
        "new_block_alpha": 30.0,
        "direct_weight_max_error": 5.551115123125783e-17,
        "full_normal_equation_max_abs_residual": 1.1102230246251565e-16
      },
      {
        "family": "both",
        "new_block_alpha": 3.0,
        "direct_weight_max_error": 5.551115123125783e-17,
        "full_normal_equation_max_abs_residual": 1.1102230246251565e-16
      },
      {
        "family": "both",
        "new_block_alpha": 30.0,
        "direct_weight_max_error": 2.7755575615628914e-17,
        "full_normal_equation_max_abs_residual": 1.1102230246251565e-16
      }
    ],
    "train_questions": 4755,
    "informative_questions": 2513,
    "weighted_pair_rows": 8271,
    "fit_count": 6,
    "control_old_solve_count": 1,
    "joint_gram_build_count": 1,
    "joint_schur_rhs_solve_count": 1,
    "new_OOF": false,
    "oof_estimate_available": false,
    "training_resubstitution_only": true,
    "validation_used": false,
    "test_used": false,
    "threads": 1,
    "seconds": 57.35911770001985,
    "format_transfer_count": 1,
    "fixed_training_parent": "runs\\round79-regularization\\candidates\\round79_s0p3_n1p0"
  }
}
```

## 冻结后的完整验证

|轮次|配置|验证 /798|修复 / 新错（对Round79）|改选数|完整资产 MiB|fresh预测＋独立评分秒|
|---|---|---:|---:|---:|---:|---:|
|97|geometry; old α=.3; new-block α=0.3|748|0 / 1|6|1.6124|3.149|
|97|geometry; old α=.3; new-block α=3|749|0 / 0|1|1.6124|2.746|
|97|conditioned; old α=.3; new-block α=0.3|743|1 / 7|54|1.6126|2.651|
|97|conditioned; old α=.3; new-block α=3|742|0 / 7|31|1.6126|2.857|
|98|self; old α=.3; new-block α=3|745|0 / 4|47|1.6359|2.207|
|98|self; old α=.3; new-block α=30|749|0 / 0|4|1.6359|2.014|
|98|context; old α=.3; new-block α=3|748|0 / 1|19|1.6359|2.773|
|98|context; old α=.3; new-block α=30|749|0 / 0|2|1.6359|2.055|
|98|both; old α=.3; new-block α=3|745|0 / 4|56|1.6594|2.314|
|98|both; old α=.3; new-block α=30|749|0 / 0|5|1.6594|2.339|

最佳新输出geometry; old α=.3; new-block α=3为749/798，修复0、新增0。同题/答案条件cos几何与逐坐标二次交互均未在这组正则强度下超过动态对照，新增表示容量没有自动转化为更可靠的排序。 回代不是OOF或持出；本批与既往实验相关且自适应，不能据此证明模型上限、唯一失败原因或独立泛化。

## 资源、完整性与交付边界

只有严格超过动态对照749且全部审计通过才晋级。同分保留 incumbent；多个新赢家同分时按更小完整解压资产、再按名称字典序。
完整解压资产1,690,758–1,739,982字节，均≤16MiB；fresh完整验证预测＋独立评分2.014–3.149秒，均≤30秒、4总CPU线程。
动态对照另fresh复核749/798，2.229秒。本地完整验证计时不等于参考Xeon8457C完整测试资格认定。
所有训练停止后执行官方计时；缓存/直接推理、一次格式转移、父gate/numeric一致、严格候选换序、题序、新ID、不同bank大小、空输入与Python整数输出均按训练及官方记录审计。
历史来源/资产（显式含89–96）、官方train/validation文件、固定父79、动态对照和全部新资产哈希通过；测试文件没有读取、评分或哈希。
历史ZIP、报告PDF与submission_ready保持冻结旧快照；本轮不自动同步或公开上传，没有完成最终测试或实际GitHub issue提交。

证据：[97训练](code/runs/round97-geometry/result.json)、[98训练](code/runs/round98-diagonal/result.json)、
[冻结](code/runs/round97-98/frozen-selection.json)、[全部验证](code/runs/round97-98/all-validation.csv)、
[官方审计](code/runs/round97-98-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
