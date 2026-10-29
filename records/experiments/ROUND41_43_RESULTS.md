# round41-43：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round41-43_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批8条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round41_budget | 4315 | 748 | 0 / 0 | 1.6004 | 1.695 |
| round42_profit | 4315 | 748 | 0 / 0 | 1.6004 | 1.718 |
| round43_crossfit | 4332 | 743 | 5 / 10 | 1.7424 | 2.307 |

## 假设、消融及失败后的判断

### Round41：预算角色反推只覆盖两个已研究训练错例

题目中唯一预算、购物后余额和穷尽的已知购买成本，给出未知商品金额
X=B−R−sum(cost)。只支持冻结的完整购买句法，所有钱额必须分配角色；
额外费用、多未知、单位/目标歧义均拒绝。transfer为4315，2修复0新错；
strict为4314，因为pair of shoes与shoes的有限容器共指被更严格规则拒绝。
自动接受仅1095/1884，结果11/41；15个预算问题全文保留，其余13个原本正确问题均拒绝。
因此没有已正确accepted训练样本，不能以0新错声称广泛可靠。
1884选中候选的终值正确，但正文仍有漏项笔误；题目金额验证不证明整条推理正确。

构造审计首版漏拒绝无$符号的文字运费，已保留first-run全部源码/结果，
收紧已解析子句以外的残文支付事件；12项最终构造检查通过，重跑原2配置结果不变。
完整验证748，0修复/0新错；没有独立验证净增。停止完整句式扩展，
不依据验证题目措辞扩语法。见[复盘](code/runs/round41-budget/FINDINGS.md)。

### Round42：带数量单位的净利润关系正确，但覆盖很小

固定Q×(sell/sell_basis−buy/buy_basis)，明确商品、买入/卖出角色及净利润目标。
单位each/dozen/pair/half-package、袋重量和cents/dollars按有界规则统一。
四类完整语法各接受1题，总4题，均与训练参考一致；其中2题原本正确。
transfer4315，2修复0新错；strict4314，因额外算术支持条件只修复1题。
拒绝库存未全部出售、收入目标、多价格/成本和未支持角色。
2081首先因a dollar超出显式数值钱额语法而拒绝，不能据此夸大语义库存识别能力。
完整验证748，0修复/0新错。此分支的自动覆盖全部来自已审阅anchors，
不足以验证宽泛泛化；停止完整句式模板分支。见[复盘](code/runs/round42-profit/LEARNING.md)。

### Round43：严格嵌套offset未优于历史匹配训练

旧残差训练使用合法的outerfit拟合内baseline offset；本轮只改为outerfit内3折OOF。
每个baseline子进程只收到outerfit输入与其innerfit标签，保存互斥全局索引证明，
没有复用含outerheld的已拟合统计。共9个内层fit、3个纯诊断fit，全部12个独立fit。
原1038维输入、40epochs及linear/competition网络保持匹配，2族×2strength共4项。

按预定pooled正确数选择competition/.25：4332，73修复54新错，各折+2/+2/+15；
相对旧同族同强度4344反而少12题（23修复35新错，各折−6/−4/−2）。
competition/.1相对旧同强度多6题，但不是本轮预定winner，不追改选择。
拟合内准确率约92.9–93.3%，nested约90.0–90.8%；softmax top及margin代理没有
支持旧offset更过自信的简单解释。inner模型训练量更小也是混杂因素。
按训练准入导出唯一winner后，正式验证743，5修复10新错；保留旧最佳。
总55.02秒，最终资产1,827,062字节，严格重排误差4.44e-16。
见[训练复盘](code/runs/round43-crossfit/TRAIN_ONLY_REPORT.md)。

## 下一入口

停止继续扩展上述完整句式或同族残差参数。另做题目级bootstrap方差控制、
Huber鲁棒成对损失、近邻binary监督与all-correct库消融，各自先冻结计划。
这些是假设，尚无验证收益；若失败继续保留748/798。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round41-43/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round41-43/frozen-selection.json)，
官方记录见[审计结果](code/runs/round41-43-verification/results.json)，
下一步见[经验](code/runs/round41-43/lessons.json)及[下一实验](code/runs/round41-43/next-experiment.json)。
