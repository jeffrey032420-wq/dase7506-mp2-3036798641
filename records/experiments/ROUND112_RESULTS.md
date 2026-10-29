# Round112：目标、集合交互与异质专家

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预定8专家+2固定集成完整报告；训练未读取验证或测试，全部冻结后验证。

|模型|目标|训练OOF/4755|验证/798|分歧/355|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---|---:|---:|
|linear|uniform_ce|4345|746|303|73|10/15|0.0254|1.971|
|linear|correct_set_mass|4337|745|302|79|9/15|0.0254|1.962|
|pointwise|uniform_ce|4305|724|281|55|10/37|0.2922|1.909|
|pointwise|correct_set_mass|4285|729|286|62|12/34|0.2922|2.008|
|deepsets|uniform_ce|4283|733|290|61|11/29|0.3079|1.904|
|deepsets|correct_set_mass|4301|730|287|72|17/38|0.3079|1.942|
|attention|uniform_ce|4291|735|292|63|7/23|0.3164|1.985|
|attention|correct_set_mass|4319|735|292|74|12/28|0.3164|1.903|
|diverse_mean|固定平均|4353|743|300|74|12/20|0.9423|4.238|
|protected_mean|固定平均|4398|746|303|75|0/5|0.9684|4.915|

最佳round112_linear_uniform_ce：746/798（93.4837%）。没有超过751，保留原751研究候选。原已测Round79模型与测试记录保持。

## 方法与实现边界

1. 组内子集与固定正则已在108及后续模型执行。本轮补充4结构×2多正确目标的匹配比较。同输入1053维、同折、同优化预算。非线性宽32；DeepSets在编码后聚合；attention四头候选自注意力，不是完整Set Transformer论文复现。参数量不同，不能把全部结构差异都归于注意力本身。
2. uniform_ce在正确候选上均分目标；correct_set_mass最大化整个正确候选集合的总概率。推理统一使用固定温度1的同答案概率求和；None不成有效组，组内同分，ID不作特征。没有直接套用allRank的默认ListNet或k=1 LambdaLoss。
3. 四个结构各自只用训练OOF选择一个损失，再等权平均组概率；protected_mean固定0.75父751+0.25异质平均。它们是预定概率集成，不是学习式堆叠。专家选择用过OOF标签，集成训练分数是开发指标，不称无偏meta-OOF。

来源：[Bosco训练源码](https://github.com/Bosco-lab/DASE7506_MP2/blob/main/code/train_ranker.py)、[Set Transformer作者源码](https://github.com/juho-lee/set_transformer/blob/master/modules.py)、[michaelleeoo异质专家](https://github.com/michaelleeoo/DASE7506-MP2)。独立实现，没有导入公开代码、权重、外部训练题目或在线模型调用。

## 训练与资源证据

32次新拟合，四CPU线程，worker 62.946秒，1800秒硬上限；PyTorch 2.14.1+cpu只训练，NumPy 2.5.3推理。Adam40epoch，lr0.003，batch128，显式L2=0.001，梯度clip5，固定seed。每折mean/std只拟合fit，原题分组隔离；未选择最佳验证epoch。训练回代、基础OOF和自适应集成指标区别记录。

训练前损失解析/有限差分梯度、torch-float64/NumPy前向预检通过；正式候选完整接口检查在拟合后执行。计划中的训练前排列预检没有单独留档；训练和验证端的正式严格重排检查均通过，作为此项流程差异披露。torch训练float32与float64导出误差另记，不假称位精度重现。float64原生/导出误差<1e-9。候选分数重排1e-8、题序、新ID、变bank、空输入、Python整数、同组同分通过。

全部部署资产含scaler、参数、嵌套专家与父模型，按NPZ解压保守计数≤16MiB；训练停止后逐个fresh官方预测+独立评分≤30秒。CPU本机验证不代表参考Xeon完整测试资格。

此前自身及公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，不将长期开发使用的train/validation视为独立确认。

复现：code目录train_round112_diverse_experts.py，随后evaluate_round112_diverse_experts.py；已有输出拒绝覆盖。证据在runs/round112-diverse-experts/result.json、fit-progress.json、mathematical-checks.json、fold参数、ensemble-members-selected-on-train.json；runs/round112-evaluation/frozen-before-validation.json、all-results.json、integrity.json及所有官方评分与进程日志。
