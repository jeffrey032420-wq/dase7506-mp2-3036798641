# round30-32：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round30-32_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批21条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round32_masked_style | 4321 | 744 | 0 / 4 | 1.9473 | 5.465 |

## 训练假设、控制与实际结果

### Round30：参考计算程序迁移覆盖了什么

从训练参考结构化计算提取由题目数字槽与固定通用常数组成的短AST；至少真实依赖一个输入，
拒绝常数输出、变量完全抵消、含未支持字面量或歧义槽位的程序。原问题代入必须精确等于
参考官方终值。得到2314/4755程序；拒绝13个变量抵消、46个常数程序、679个重复槽、
1584个无支持终程序。折内masked问题TFIDF检索同槽数量模板，代入新题数值，
对候选终值投票；索引不存原题、ID或任意终值查表。K1/5×gate.3/.5×strength.1/.25共8项。

全部OOF4313、没有改选，selected=null。K5/.3有956题检索、98题输出匹配候选，
其中96题原本已正确，仅2旧错具有更高正确票；门槛.5的23匹配题全已正确。
另15题只支持错误候选，不能靠硬推或增权解决。数量角色/槽对齐仍不可靠；
先审计输入角色，不继续扩大K或权重。详见[复盘](code/runs/round30-template/FINDINGS.md)。

### Round31：教师数值误差更小，不等于选择更准

问题TFIDF与数值统计/固定关系特征预测参考signed-log终值，训练参考仅监督、推理不读取。
固定L2/median-quantile两头（7叶200轮）与折内目标中位数控制，各3个融合强度，共9项。
教师logMAE由常量1.541降到1.235/1.238，但最佳learned选择4315仍低于中位数控制4316，
按计划无导出/无验证。答案分歧子集单教师882/888对，也低于常量933；配对排序.495/.497
低于常量.519。回归误差改善不是候选排序改善的证据，不宣称题意理解提升。
详见[训练报告](code/runs/round31-magnitude/TRAIN_ONLY_REPORT.md)。

### Round32：数字masked结尾样式控制

每候选尾600字符，小写并将显式数字替为num；折内char_wb3–5 TFIDF12000/min_df3，
仅有对有错的问题拟合加权binary logistic，C.1/1×融合.1/.25共4项。
选C1/.1，OOF4321（23修复/15新错，折+5/−2/+5），验证744，无修复且新增4错。
纯head3888/3893远弱于原模型；最强正权重主要是boxed数字格式片段，负权重含粗体/approx，
因此最多称格式/措辞证据，不能称数学推理。各折及最终19020候选恢复transform/logit/probability
误差均0。普通JSON/NPZ导出，无pickle，推理依赖sklearn/SciPy；完整解压2,041,923字节。
详见[样式复盘](code/runs/round32-style/LEARNING.md)。

## 后续入口

继续检验完整context最大间隔排序、答案组新表示与目标问句运算监督。
前者发生代理恢复和根接手的并发写冲突，source-hash guard在验证前拦截；
旧33产物隔离归档，用相同冻结参数在独占新目录完整重跑后才允许验证。
这属于工程失败记录，不是新模型收益。其它分支命名与文件所有权独立。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round30-32/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round30-32/frozen-selection.json)，
官方记录见[审计结果](code/runs/round30-32-verification/results.json)，
下一步见[经验](code/runs/round30-32/lessons.json)及[下一实验](code/runs/round30-32/next-experiment.json)。
