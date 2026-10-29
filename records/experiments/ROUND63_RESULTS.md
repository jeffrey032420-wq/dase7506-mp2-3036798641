# round63：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-22。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round63_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批1条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round63_conservative | 4333 | 748 | 0 / 0 | 1.8127 | 11.246 |

## 已有合格输出的保守选择

本轮没有新拟合或新系数。仅使用Round62原六项训练网格中的joint_relative/.1，
其4333/4755、23修复3新增，对同强度控制4324多9，折净增+2/+2/+5，
独立满足62运行前门槛。62按总OOF选了.25；本轮明确改为优先较少新错的合格输出。
这是在62验证汇总747后进行的一次自适应验证选型，偏差需披露；没有查看验证逐题
原文/标签设计条件，测试未访问。完整复制62模型，只改配置weight=.1。
一次比较后停止该强度家族，不追加更多值。缓存与模型未更改，官方资源接口另行审计。
本轮1条配置记录复用62拟合，不能称作新训练模型或独立实验数据。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round63/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round63/frozen-selection.json)，
官方记录见[审计结果](code/runs/round63-verification/results.json)，
下一步见[经验](code/runs/round63/lessons.json)及[下一实验](code/runs/round63/next-experiment.json)。
