# 2026-10-29：特征组合与嵌套条件选择结果

## Material Passport

academic-research-suite / experiment-agent；两轮均完成官方validation、来源/资产/接口核验。共69次新拟合、6个最终配置（含旧配置重现），没有新增测试。

|轮次/配置|训练外层OOF /4755|官方验证 /798|相对原751验证修复/新增错|
|---|---:|---:|---|
|118 legacy22，旧109重现|4392|751|0/0|
|118 legacy26，旧110重现|4398|751|1/1|
|118 aligned22，旧116重现|4395|750|0/1|
|118 aligned26，新组合|4399|750|1/2|
|119 confidence8条件选择|4387|751|1/1|
|119 evidence34条件选择|4389|751|1/1|

**没有超过原751/798（94.1103%）。** 原109冻结版本保留，其此前官方test记录391/467（83.7259%）未重跑，未据测试总分训练或选择上述配置。

## 这两轮新增的证据

1. 118把题目数值分词、基础模型、正则、margin来源全部固定，三旧控制参数和分数重现，检验的是局部算术定义与最终答案证据的匹配组合。新组合OOF比原模型+7题，但验证少1题；不能把训练提升当成验证突破。
2. 119没有简单在全训练专家OOF上拟合门控后报告同题成绩。它在outer-fit内部重新产生两个完整专家的inner-OOF，主模型的inner残差也使用inner-fit内部三折基础OOF。新增27基础、9主残差、9 CE专家、8门控，共53次拟合。
3. confidence8在嵌套外层切换62题，修复24、新增29错，净减5题；evidence34切换59题，修复22、新增25错，净减3题。两种门控的回代收益没有在嵌套外层保持。原专家可修复72个错误的oracle空间，未能被本批固定条件选择器可靠获取。
4. 两门控验证均为751，分别修复1/新增1；evidence34的单正确题79/117高于原78/117，但其他题损失抵消，不称总体改进。

## 测试条件与资源

训练前固定准入：官方validation>751、训练外层OOF>4392、全部实现/资源检查通过，才选唯一候选冻结并测试。118新组合验证未通过，119两门控外层OOF未通过，因此两批均未触发测试，也未按结果放宽门槛。

所有6配置完整解压推理资产≤55,921字节（54.61KiB），本机fresh官方validation预测+独立评分≤3.283秒。均在16MiB/30秒内，参考Xeon资格仍未验证。嵌套专家的全部权重、scaler/config和gate均计入；诊断训练参数不用于推理。

旧源、权重、数据、官方parser/scorer与冻结版本均保留。训练/验证不读取test输入、参考、预测或评分；历史已知测试汇总和长期适应性train/validation开发披露不变。

## 后续应如何推进

这两轮降低了继续堆叠现有算术统计或扫描同一门控阈值的优先级。若继续，应先提出能在训练内部区分“何时专家可靠”的新输入证据，例如具体题意数量关系；已有置信度和26维统计在本固定选择器下不足以证明稳定增益。需要新的训练侧可检验假设，不能以oracle或测试成绩代替。

## 文件

- ROUND118_EXECUTION_PLAN.md、ROUND118_RESULTS.md、ROUND118_LEARNING.md
- ROUND119_NESTED_SWITCH_PLAN.md、ROUND119_RESULTS.md、ROUND119_LEARNING.md
- code/runs/round118-evidence-factorial/result.json
- code/runs/round118-evaluation/all-results.json、integrity.json、selection-before-test.json
- code/runs/round119-nested-switch/result.json、innermost-partitions.json、gate-progress.json
- code/runs/round119-evaluation/all-results.json、integrity.json、selection-before-test.json

WORKLOG与AI_DISCLOSURE均已追加两轮完整结果；本汇总不代表已完成课程公开提交。
