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
