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
