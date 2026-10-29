# 第十轮：表示变换、正则化、集合损失与嵌套堆叠

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent，inline run。
- Origin Date: 2026-10-16。
- Verification Status: VERIFIED_LOCAL_VALIDATION；不是独立测试结论。
- Version Label: round10_results_v1。

## 结论

**本轮没有超过 747/798（93.6090%），保留第七轮模型。**
当前入口与 checkpoint 以 [CURRENT_BEST.json](CURRENT_BEST.json) 为准。
本轮进行了四类基础模型、两类跨模型选择器和取值域规则，共 14 个最终冻结验证输出，全部通过官方复算及本地资源/接口检查。
全部实验和旧最佳模型保留，没有读取测试输入、标签或成绩。

## 1. 主实验：先写假设，再做消融

运行前计划见 [ROUND10_PLAN.md](ROUND10_PLAN.md)。四种改变分别是：

- angular：每题 Embedding 减去候选均值，再逐候选缩放到长度 32；保留文本和 context 特征。
- rivals：原特征加 384 维与其他候选最小/最大投影值的差和乘积。
- dropout：成对平方损失增加特征缺失的期望对角惩罚，并保留普通 ridge 惩罚。
- marginal：优化全部候选 logsumexp 减正确候选 logsumexp，使多个正确解答可共享成功概率；ridge 初始化。

固定三折按题划分种子 20261018，投影种子 20261014。全部拟合统计量仅来自折内训练部分。
共 18 个配置、54 条折内记录，结合 5 个题内归一化融合比例产生 90 个 OOF 选项。
每族先选择纯模型与最佳融合，再在全训练集拟合，最后进行验证。旧算术冲突门控保持不变。
对照与新模型之间的比较包含每族不同超参数，不能归因于单一因素。

相对方向融合 OOF 从 4310 增至 4326，分折 1442/1443/1441，但验证只有 741。
dropout 纯模型 OOF 4325，验证 738；rivals OOF 4318，验证 741。
marginal 纯模型 OOF 4307、验证 735，融合后 OOF 4315、验证 742。
因此四类主假设均未取得验证净收益。纯 angular 修复 10 道旧错但新增 19 道，显示有互补信息也有明显代价。
所有九次主实验折内 marginal 优化及两个选中配置的完整重训都报告收敛；收敛不保证非凸目标的全局最优。
训练前构造检查曾把正负对数量误写为 20，修正为 21 后通过，算法未修改。

## 2. 补充：学习何时采用其他模型

主实验结束后写入 [ROUND10_AMENDMENT.md](ROUND10_AMENDMENT.md)，再运行两种 meta 模型：
成对 ridge 与 150 轮小型 LightGBM 二分类树。它们使用五个基础模型的分数、
分差、分数乘积、答案组投票、原文本和数值特征及分数—文本交互。
在非算术门控且正确/错误候选并存的训练题上拟合；推理继续保留旧算术门控。

采用嵌套 cross-fitting：外层每次保留三分之一训练题；外层训练部分再分三折，
重新拟合基础模型，为 meta 生成折外训练分数；外层 held 的基础分数只由外层训练部分拟合。
共九组内层重新拟合，每组包含原 baseline 和四个不同 head。
实现为简化复用了主实验 fit_all，因此内层还计算了未用于堆叠的其他配置；没有用内层 held 重新选参。
内层优化器状态未单独持久化，主实验及其完整重训的收敛记录可供检查。

基础 head 的超参数此前用全训练 OOF 选过，所以这里仍有超参数选择偏差。
嵌套方案隔离了 meta 训练所使用的基础分数，但不能称作完全无偏的独立评价。
最终 meta 用全训练 OOF 表拟合；推理基础 head 用完整训练集拟合。

5 个 meta 配置、15 条外层折内记录、25 个融合选项，冻结 4 个输出后才评估验证。
full 与 blend 相同时保留两个记录，不能算作两个独立实验。

| 方案 | alpha 或叶数 | meta 比例 | 外层 OOF /4755 | 各折正确数 |
|---|---:|---:|---:|---|
| ridge_full | 10.0 | 1.0 | 4324 | [1441, 1444, 1439] |
| ridge_blend | 10.0 | 1.0 | 4324 | [1441, 1444, 1439] |
| tree_full | 3 | 1.0 | 4321 | [1442, 1443, 1436] |
| tree_blend | 7 | 0.5 | 4326 | [1442, 1444, 1440] |

## 3. 补充：取值域约束与失败原因

第二次补充先保存 [ROUND10_DOMAIN_AMENDMENT.md](ROUND10_DOMAIN_AMENDMENT.md)，再检查训练 OOF。
非负计数、离散计数整数性、整体百分比范围及三者组合共四种配置。
仅允许训练 OOF 修复至少 2 题且新错为 0 的规则进入验证；最终选择百分比范围规则。
它在训练 OOF 修复 2 题、无新错（4312），验证仍为 747，候选选择没有变化。
另外两类单独规则均未修复训练旧错。组合也修复 2 题，但增加一次同为错误答案间的切换。

这些约束在本次数据中很少触发：旧模型已经避免了大部分明显违反取值域的答案。
有训练收益并不表示验证上有同类待修复错误。范围规则也不是通用数学证明，百分比可因问题含义超过 100。
实现审计发现初版还会压低无法解析的候选，与计划不符；修复为只压低已确认违规者，
重跑同一配置筛选后训练与验证成绩不变。初版结果保存为 pre-audit 文件；因此有一次额外验证执行，
14 是最终冻结输出数，不是历次脚本执行总数。

多种表示与集合目标的纯模型会纠正旧错，也会破坏更多旧正确选择；主实验中纯 angular 为修复10/新错19。
嵌套树融合缩小到43个选择变化，仍是修复2/新错8；选择器没有可靠地区分有益和有害的模型分歧。
这是观察到的失败机制，不能据此断言这些方法在其他任务上无效。
各方案训练 OOF 上的净收益没有转移到验证，可能与划分差异和反复选型有关；本轮未单独识别因果原因。

## 4. 所有冻结验证结果

修复/新错相对旧模型 747；选择变化还包含同为正确候选间的切换。
OOF 用于选型，是开发指标。验证已被多轮使用，选择偏差在最终报告中必须保留。

| 方案 | OOF /4755 | 验证 /798 | 修复 / 新错 | 选择变化 |
|---|---:|---:|---:|---:|
| round10/incumbent | 4310 | 747 | 0 / 0 | 0 |
| round10/angular_full | 4325 | 738 | 10 / 19 | 223 |
| round10/angular_blend | 4326 | 741 | 2 / 8 | 132 |
| round10/rivals_full | 4318 | 741 | 0 / 6 | 122 |
| round10/rivals_blend | 4318 | 741 | 0 / 6 | 122 |
| round10/dropout_full | 4325 | 738 | 2 / 11 | 94 |
| round10/dropout_blend | 4325 | 738 | 2 / 11 | 94 |
| round10/marginal_full | 4307 | 735 | 6 / 18 | 141 |
| round10/marginal_blend | 4315 | 742 | 1 / 6 | 57 |
| round10-stack/ridge_full | 4324 | 740 | 2 / 9 | 104 |
| round10-stack/ridge_blend | 4324 | 740 | 2 / 9 | 104 |
| round10-stack/tree_full | 4321 | 741 | 5 / 11 | 306 |
| round10-stack/tree_blend | 4326 | 741 | 2 / 8 | 43 |
| round10-domain/percent | 4312 | 747 | 0 / 0 | 0 |

## 5. 资源与复现

Intel Core i5-11400H，四线程；Python 3.12.14、NumPy 2.5.3；
训练损失优化使用 SciPy 1.18.1，树使用 LightGBM 4.7.0（树版本推理也需要）。
三个阶段最终训练/选择记录耗时合计 210.72 秒，不包括初版规则执行、官方审计与报告。
推理资产计入所有模型、词表/统计量（若有）、配置；没有按压缩体积折算。

| 输出 | 全部推理资产 MiB | 新进程预测＋评分秒 |
|---|---:|---:|
| round10/incumbent | 1.600 | 1.520 |
| round10/angular_full | 2.400 | 2.131 |
| round10/angular_blend | 2.400 | 2.162 |
| round10/rivals_full | 2.409 | 2.394 |
| round10/rivals_blend | 2.409 | 2.370 |
| round10/dropout_full | 2.400 | 2.173 |
| round10/dropout_blend | 2.400 | 2.114 |
| round10/marginal_full | 2.400 | 2.137 |
| round10/marginal_blend | 2.400 | 2.115 |
| round10-stack/ridge_full | 4.812 | 3.727 |
| round10-stack/ridge_blend | 4.812 | 3.709 |
| round10-stack/tree_full | 4.889 | 6.391 |
| round10-stack/tree_blend | 4.951 | 6.396 |
| round10-domain/percent | 1.600 | 1.603 |

所有输出通过官方评分、候选重排、题目逆序、新 ID、可变输入大小、空输入和 Python 整数返回检查。
预测与独立评分共用本地 30 秒截止时间；资产都低于 16 MiB。
**上述本地完整验证集计时不等于参考 Xeon Platinum 8457C 上完整测试集资格认证。**
官方工具与训练/验证数据、第七至九轮源代码、本轮已审计权重均通过哈希完整性核验。
未使用任何外部训练集、额外预训练模型或测试分数。

产物：

- [复现命令](REPRODUCE.md) 的 Round 10。
- [全部验证汇总](code/runs/round10/validation-summary.csv)。
- [主实验选型](code/runs/round10/oof-selection.json)、[嵌套堆叠选型](code/runs/round10-stack/oof-selection.json)。
- [取值域规则选型](code/runs/round10-domain/oof-selection.json)、[规则官方审计](code/runs/round10-domain-verification/results.json)。
- [配对与困难子集诊断](code/runs/round10/diagnostics.json)、[完整错例](code/runs/round10/paired-cases.json)。
- [主实验审计](code/runs/round10-verification/results.json)、[堆叠审计](code/runs/round10-stack-verification/results.json)。
- [完整性记录](code/runs/round10/final-integrity.json)。

本文件是开发记录。课程最终报告的 10 页排版、公开代码/checkpoint 链接、最终测试及 GitHub issue 提交仍待完成。
