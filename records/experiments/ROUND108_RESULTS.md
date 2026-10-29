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
