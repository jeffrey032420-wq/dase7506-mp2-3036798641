# Round96：训练参考数值距离提供额外成对权重监督

Material Passport: academic-research-suite / experiment-agent；2026-10-27；VERIFIED_LOCAL_VALIDATION。

**全部4个新输出均未超过749/798（93.8596%），保留Round79。** 预先固定near/far×γ1/3共四配置，全部导出后再进行本批验证。
只使用所给train候选、Embedding及训练参考答案；无外部数据或预训练权重。没有新OOF/持出筛选，回代只作描述，validation仅用于自适应开发。

## 假设与有限干预

假设：保持原表示与单位排序margin，仅用训练错误答案与训练参考的数值距离调整同题错误候选的关注程度，可能改善共享排序系数。
训练参考g、错误候选数值a，精确Fraction计算Δ=|a−g|、S=max(1,|g|)。只将有界h=S/(S+Δ)、f=Δ/(S+Δ)转换为float64，避免巨大数值比率溢出。
near原权重为1+γh，far为1+γf。无法解析的错误候选采用同题已解析错误候选权重均值；若全不可解析则用均匀权重，避免把解析能力自动当可靠性。
每个正确—错误对权重为`u_bad/(n_good·sum_bad u)`，每道信息题总权重1；目标margin仍为1，α=.3，统计量/投影/表示固定，不额外改变题权或加入全正确题排序对。
参考仅用于训练监督；导出只有semantic系数与描述配置，推理完全沿用method_round11.py，不需要训练/验证/测试参考答案。
历史已使用过训练参考文本、参考幅值教师及题权；本轮不声称首次使用参考，具体区别见[计划](ROUND96_PRIVILEGED_DISTANCE_PLAN.md)。

数值距离不一定反映推理错误程度，近错可能难学，远错可能稀释关键区分；S对小答案也有单位依赖。
只有一个错误候选或同题所有错误距离相同时，归一化使该题的干预无效；以下记录实际不等权覆盖，不能把2513分母误称全部受到干预。
固定训练父79及numeric α=1/门控/一次格式转移保持；动态选型对照则是本批冻结Round79/749，分别核验资产。

## 全部训练、覆盖与控制

实际4个候选ridge解、1个γ0控制，共5次求解；1CPU线程/600秒硬预算，耗时35.936秒。所有四配置均进入验证，不按回代筛选。
回代固定父79为4406/4755，不是OOF、持出或验证结果。

|距离偏重|γ|真正不等权题数 /2513|原错误候选权重范围|完整train回代 /4755|回代修复 / 新错|相对方程残差|
|---|---:|---:|---:|---:|---:|---:|
|near|1|757|1–1.99982|4403|1 / 4|6.87e-16|
|near|3|757|1–3.99946|4404|4 / 6|4.89e-16|
|far|1|757|1–1.99972|4406|0 / 0|5.52e-16|
|far|3|757|1–3.99917|4405|1 / 2|5.89e-16|

训练解析与覆盖聚合记录：

```json
{
  "train_questions": 4755,
  "informative_questions": 2513,
  "all_correct_questions": 2242,
  "all_incorrect_questions": 0,
  "reference_parsed_questions": 4755,
  "reference_unparsed_questions": 0,
  "reference_zero_questions_all": 0,
  "reference_zero_questions_informative": 0,
  "incorrect_candidates_informative": 4667,
  "parsed_incorrect_candidates_informative": 3796,
  "unparsed_incorrect_candidates_informative": 871,
  "partial_bad_parse_questions": 337,
  "no_parsed_bad_questions": 399,
  "single_bad_questions": 1070,
  "reference_and_wrong_distance_used_only_in_train": true,
  "parsed_near_signal_min": 0.0002777777777777778,
  "parsed_near_signal_max": 0.9998186434530286,
  "parsed_far_signal_min": 0.00018135654697134566,
  "parsed_far_signal_max": 0.9997222222222222,
  "weighted_pair_rows": 8271,
  "informative_gated_questions": 258,
  "informative_nongated_questions": 2255
}
```

γ0原模型控制及等题权检查：

```json
{
  "gamma0_weight_max_error": 2.040034807748725e-15,
  "gamma0_train_semantic_score_max_error": 5.039315303173268e-14,
  "gamma0_pair_weight_max_error": 0.0,
  "gamma0_normal_equation_max_abs_gradient": 8.881784197001252e-16,
  "question_weight_sums": {
    "distance_mode": "near",
    "gamma": 0,
    "question_weight_sum_min": 1.0,
    "question_weight_sum_max": 1.0,
    "question_weight_sum_max_abs_error": 0.0,
    "total_pair_weight": 2513.0,
    "raw_bad_weight_min": 1.0,
    "raw_bad_weight_max": 1.0,
    "pair_weight_min": 0.25,
    "pair_weight_max": 0.3333333333333333,
    "within_question_raw_max_min_ratio_max": 1.0,
    "unequal_weight_questions": 0,
    "equal_weight_questions": 2513,
    "unit_target_margin": 1.0
  },
  "gamma0_complete_pipeline_max_error": 5.040412531798211e-14
}
```

## 冻结后完整验证

|距离偏重|γ|验证 /798|修复 / 新错（对Round79）|改选数|完整资产 MiB|fresh预测＋独立评分秒|
|---|---:|---:|---:|---:|---:|---:|
|near|1|749|0 / 0|10|1.6006|1.887|
|near|3|748|0 / 1|16|1.6006|1.834|
|far|1|747|0 / 2|5|1.6006|1.868|
|far|3|747|0 / 2|10|1.6006|1.987|

最佳新输出distance=near; γ=1; margin=1; α=.3为749/798，修复0、新增0。这四种训练距离权重未超过动态对照；偏重近错或远错并不保证更可靠的推理排序。 数值距离不等于语义难度或推理质量，且题内归一化限制有效覆盖；训练回代不是持出，这些自适应比较不能识别唯一原因、证明模型上限或独立泛化。

## 资源、选型与材料边界

严格超过动态对照749且全部官方/资源/接口检查通过才晋级；同分保留当前最佳，新赢家同分按更小完整解压资产、再按名称字典序。
全部四行与失败保留，不按个别验证错题增加规则或扩大γ/距离定义。
完整解压资产1,678,336–1,678,337字节，均≤16MiB；fresh完整验证预测＋独立评分1.834–1.987秒，均≤30秒、4总CPU线程。
动态对照另fresh复核749/798，1.891秒；本机完整验证计时不等于参考Xeon8457C完整测试资格认证。
全部拟合停止后才执行官方计时；完整缓存/直接推理、门控父一致、严格重排、题序、不同bank大小、新ID、空输入、Python整数检查通过。
历史来源/资产（含89–95）、原官方工具/train与validation文件、新训练参考输入哈希、固定父79、动态对照及新资产均通过；未读取或哈希测试文件。
历史ZIP、报告PDF及submission_ready保持旧快照，不自动同步本轮成果；没有冻结测试、公开上传或实际GitHub issue提交。

证据：[训练](code/runs/round96-privileged-distance/result.json)、[冻结](code/runs/round96-evaluation/frozen-selection.json)、
[全部验证](code/runs/round96-evaluation/all-validation.csv)、[官方审计](code/runs/round96-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
