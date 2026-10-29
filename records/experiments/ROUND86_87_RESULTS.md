# Round86–87：完整保护下的语义容量与训练题目加权

Material Passport: academic-research-suite / experiment-agent；2026-10-26；VERIFIED_LOCAL_VALIDATION。

**全部10个新输出均未超过749/798（93.8596%），保留Round79。** 10个新输出在本批验证前固定；无新OOF。测试输入、参考、预测及成绩均未用于开发。

## 动机与固定假设

此前对Round79的汇总后分析显示，49个验证错误中43个在固定算术门外。这用于提出研究方向，
不是拟合输入、独立评估或逐题规则。新一批将semantic分支作为变化对象，numeric α=1、固定门控和R11格式转移保持原资产/实现。

1. **Round86容量：** semantic α=.3，固定context宽度32/64/128/192，以及linear宽度0、nonlinear宽度96，共6个配置。
   context宽度≤96截取原投影列；宽度128/192保留原96列，再拼接同一1024×96、seed20261025的新随机矩阵的前32/96列。
   因生成矩阵形状影响随机数排列，新128尾部不同于旧Round6形状较小的尾部；不能把两者当作相同随机方向上的纯复测。
   新宽度192扩展原范围；linear/nonlinear等为既有表示家族，本轮不是新特征发明。
   每个表示只在train重新拟合semantic特征均值/尺度和成对ridge，保留原base统计量。
2. **Round87题目权重：** 保留原1422维context和统计量、semantic α=.3，比较门内训练题权重0/.25/.5（门外=1），
   以及门外只有1个正确候选的题权重2（其余informative题=1），共4个配置。
   每题好坏候选差分等权，目标按informative题权重和归一化；全正确题没有成对差分。
   权重依train标签定义并固化在模型系数中，推理不读取参考答案或正确候选数。

原context96/全题等权控制必须复现原语义权重/完整train分数至1e−8。每路线1CPU线程、600秒硬预算；全部拟合停止后才作4总CPU线程官方审计。
Round86完成6候选＋1控制目标系统/解，耗时53.949秒；Round87完成3分区矩阵、5个ridge解（含控制），耗时31.562秒。

## 训练回代：不作持出或准入证据

|86表示|宽度|维数|完整train回代 /4755|非门回代 /4473|回代修复 / 新错（对当前）|
|---|---:|---:|---:|---:|---:|
|context|32|1166|4401|4152 / 4473|25 / 30|
|context|64|1294|4402|4153 / 4473|21 / 25|
|context|128|1550|4403|4154 / 4473|20 / 23|
|context|192|1806|4437|4188 / 4473|54 / 23|
|linear|0|1038|4393|4144 / 4473|24 / 37|
|nonlinear|96|1230|4398|4149 / 4473|21 / 29|

|87题目权重|informative权重和|完整train回代 /4755|非门回代 /4473|回代修复 / 新错（对当前）|
|---|---:|---:|---:|---:|
|gated fitting weight=0; nongated=1|2255.00|4412|4163 / 4473|19 / 13|
|gated fitting weight=0.25; nongated=1|2319.50|4407|4158 / 4473|10 / 9|
|gated fitting weight=0.5; nongated=1|2384.00|4404|4155 / 4473|6 / 8|
|nongated single-correct fitting weight=2; other informative=1|3114.00|4450|4201 / 4473|64 / 20|

这些值来自参与拟合的完整train，是回代描述；不是OOF、持出或独立泛化证据。全部10个固定配置均导出、全部进入验证，没有按回代数筛选。
完整缓存/直接checkpoint、门内分数保护、严格候选重排、新ID、空输入和整数检查记录保留。

## 冻结后的完整验证

|输出|配置|验证 /798|修复 / 新错（对Round79）|完整资产 MiB|fresh预测＋独立评分秒|
|---|---|---:|---:|---:|---:|
|round86_context_w32|context; width=32; dimensions=1166; semantic α=.3|742|1 / 8|1.0947|1.816|
|round86_context_w64|context; width=64; dimensions=1294; semantic α=.3|744|0 / 5|1.3476|1.895|
|round86_context_w128|context; width=128; dimensions=1550; semantic α=.3|744|1 / 6|1.8535|1.934|
|round86_context_w192|context; width=192; dimensions=1806; semantic α=.3|743|3 / 9|2.3593|1.868|
|round86_linear_w0|linear; width=0; dimensions=1038; semantic α=.3|741|2 / 10|0.8415|1.824|
|round86_nonlinear_w96|nonlinear; width=96; dimensions=1230; semantic α=.3|741|3 / 11|1.5961|1.850|
|round87_gate0p0|gated fitting weight=0; nongated=1; semantic α=.3|747|1 / 3|1.6005|1.856|
|round87_gate0p25|gated fitting weight=0.25; nongated=1; semantic α=.3|748|1 / 2|1.6005|1.960|
|round87_gate0p5|gated fitting weight=0.5; nongated=1; semantic α=.3|749|1 / 1|1.6005|1.805|
|round87_singleton2|nongated single-correct fitting weight=2; other informative=1; semantic α=.3|746|4 / 7|1.6005|1.860|

Round86最佳744/798；Round87最佳749/798。
这些语义容量与训练题目加权配置均未超过当前749。把研究重点移向非门区域并不自动产生收益：容量变化可能同时改变信号和拟合方差，拟合题目权重变化也可能降低原全题监督的帮助。本次有限比较不能确定唯一原因或证明模型上限；回代改善也不能替代持出证据。

## 选型、资源与交付边界

严格超过749且全部审计通过才晋级；与当前最佳同分保留当前最佳，新赢家同分按更小完整解压资产、再按名称字典序。
10个成功/失败输出均保留，停止本批固定范围，不在看到结果后扩大。多轮validation复用仅用于自适应开发与选型，不能称为无偏或显著提升。

所有输出通过fresh官方预测与独立完整验证798题评分、严格候选重排1e−8、题序、不同bank大小、新ID、空输入和Python整数检查。
完整解压资产882,382–2,473,937字节，均≤16MiB；fresh预测＋独立评分1.805–1.960秒，均≤30秒、4总CPU线程。
当前控制另fresh复核749/798，耗时2.059秒。本机完整验证计时不等于参考Xeon8457C完整测试资格认证。
原官方工具/train和validation文件、所有旧源码及原R11/当前R79资产哈希通过；没有读取或哈希测试文件。
最终≤10页课程报告、公开代码/checkpoint链接、最终冻结后的参考CPU完整测试与实际GitHub issue仍待完成。

证据：[冻结记录](code/runs/round86-87/frozen-selection.json)、[完整表](code/runs/round86-87/all-validation.csv)、
[官方审计](code/runs/round86-87-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
