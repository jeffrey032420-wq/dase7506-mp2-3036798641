# round62：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-22。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round62_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批6条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round62_joint | 4346 | 747 | 1 / 2 | 1.8127 | 11.447 |

## 联合语义与数学证据

此前数值结构树与embedding模型主要分别学习再融合。本轮假设联合树可以学习二者条件关系。
固定同一7叶100轮LambdaRank及原18其他设置，三表示：安全数学668维控制、
控制+1024原embedding、再加1024题内相对embedding；各融合.1/.25，共6项配置评估。
无新词表、PCA、外部数据或额外预训练权重，所有输入均为供应训练集。
候选按52固定规则规范顺序后计算相对量再还原，数据/官方解析/历史模型不改。
所有OOF只作开发选型，不输入训练offset；各题4候选同折，baseline仅用于融合评价。

控制/.25精确复现4341，是可比性检查，不是新收益。进入验证须超过同强度控制>=5题，
至少两折正增、>=15原错修复、<=15新增错误。只允许一个合格最佳输出重训/验证。
全部六项配置与逐题变化均保留，不追加树深/轮数/强度网格。

完整训练缓存与直接推理23题的特征/原始分数最大差均0；正式验证747，修复1/新增2，未晋级。

|配置|训练OOF/4755|修复/新增，对R11|折净增|
|---|---:|---|---|
|control-0.1|4324|17/6|[4, 1, 6]|
|control-0.25|4341|38/10|[8, 5, 15]|
|joint-0.1|4325|17/5|[4, 0, 8]|
|joint-0.25|4340|35/8|[8, 3, 16]|
|joint_relative-0.1|4333|23/3|[6, 3, 11]|
|joint_relative-0.25|4346|43/10|[6, 7, 20]|

最佳联合方案相对同强度控制：{"correct": 4346, "n": 4755, "fixed": 22, "new_errors": 17, "changed": 474, "fold_correct": [1447, 1446, 1453], "fold_net": [-2, 2, 5], "positive_folds": 2}。

完整单线程运行94.286秒；特征缓存属于训练中间产物，不是提交推理资产。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round62/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round62/frozen-selection.json)，
官方记录见[审计结果](code/runs/round62-verification/results.json)，
下一步见[经验](code/runs/round62/lessons.json)及[下一实验](code/runs/round62/next-experiment.json)。
