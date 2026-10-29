# round26-29：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round26-29_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批17条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round27_pointwise | 4327 | 742 | 3 / 9 | 1.7420 | 2.364 |
| round28_centered_forest | 4317 | 742 | 0 / 6 | 1.6282 | 4.431 |
| round29_valid_final | 4315 | 748 | 0 / 0 | 1.6005 | 1.655 |

## 实验假设与实际学习

### Round26：更多数字输入不等于更准确

固定原控制、英文整数词、题目明确提示的单位/关系常数、二者结合四表示；
保持7叶100轮、blend.1。控制4321、words4314、cued4316、both4315。
控制特征/原始头/OOF与Round23逐值完全一致。新增输入扩大覆盖，也增加偶然匹配：
错误目标可达率41.90%→48.35%/49.70%，正确39.17%→44.58%/45.74%。
原控制胜出，checkpoint=null，不重复验证。语义角色不能用更多算术输入替代。
同一全局重拟合还会改变输入未变化的问题，不能把所有变化归于局部parser。
详见[复盘](code/runs/round26-cued-program/FINDINGS.md)。

### Round27：同宽非线性与早期训练点

A固定同宽pointwise tanh去掉跨候选比较，40epochs、两个强度；best4327，
51修复/37新错，作为独立家族按原门槛验证，结果742（3修复/9新错）。
B同训练路径5/10/20epoch、两个强度；.25的OOF为4335→4338→4341，
旧40epoch4344仍最高。10/20epoch训练loss和Round24各折逐值一致，
排除了训练路径变化；早期最好相对40epoch为9修复/12新错，未合格不验证。
同宽pointwise比交互少17题且三折均低，支持这个开发配置里交互有用，
仍不能把训练优势称为独立泛化改进。所有新推理从开始使用float64严格重排。
详见[训练报告](code/runs/round27-nonlinear/TRAIN_ONLY_REPORT.md)。

### Round28：只改变森林监督目标

保持compact256、32树、depth4/8和两个融合权重，只将目标由binary改成
y减本题y均值，全正确2242题仍保留0目标。最佳4317（17修复/13新错，
各折+3/0/+1），验证742、无修复且新增6错。Matched binary对照：
depth4/.1是4315→4317，depth8/.1是4321→4314。浅树局部改善不能证明
中心化目标总体优于binary；总体不超过旧森林最佳，停止继续扩大同族网格。
导出概率逐折及最终19020候选与sklearn完全一致，NumPy推理不需要sklearn。
详见[森林复盘](code/runs/round28-centered-forest/LEARNING.md)。

### Round29：官方终值资格条件

单一固定规则：存在官方可解析候选时，将不可解析候选放到所有现有分数以下；
四候选全不可解析时保留原分数。没有重写官方parser或读取推理参考。
所有训练参考终值均可解析；在这个条件下，排除的候选不可能评分正确。
OOF改变3题、修复2/新错0，4315，按预先声明的逻辑条件门槛合格。
三个改选全文保留[changed-cases.json](code/runs/round29-valid-final/changed-cases.json)。
验证748，0修复/0新错，因此该条件没有新增验证纠错覆盖。
不能把训练中满足的有效参考假设宣称适用于所有任意数据源。

## 下一方向

正在另做Round30参考程序迁移、Round31问题预测答案量级、Round32数字masked样式控制。
这些使用不同信息或监督，拟合前写小网格计划；未完成前不预报准确率收益。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round26-29/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round26-29/frozen-selection.json)，
官方记录见[审计结果](code/runs/round26-29-verification/results.json)，
下一步见[经验](code/runs/round26-29/lessons.json)及[下一实验](code/runs/round26-29/next-experiment.json)。
