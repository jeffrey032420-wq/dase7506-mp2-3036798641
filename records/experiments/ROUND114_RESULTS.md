# Round114：基础答案组正则的完整流水线对照

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。四个基础正则固定，均重新匹配嵌套折外算术残差；模型/源/结果冻结后才访问验证。

|基础lambda|基础train OOF|完整train OOF/4755|训练回代/4755|验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|0.003|4369|4380|4554|750|78|4/5|0.02612|2.019|
|0.01|4380|4392|4510|751|78|0/0|0.02612|2.024|
|0.03|4380|4387|4457|750|78|4/5|0.02599|2.121|
|0.1|4362|4374|4413|749|76|9/11|0.02598|2.012|

最佳round114_anchor_l0p01：751/798（94.1103%）。没有超过751，保留第109轮研究候选。0.01是原751严格重复对照，不算新提升；原已测Round79模型/测试记录保持。

固定子集增强、1034组表示、22维局部残差与残差lambda0.1；只比较基础lambda0.003/0.01/0.03/0.1。与111的残差正则网格不同。每种基础模型在outer-fit内部产生自己的inner-OOF margin，再学习自己的残差；没有直接给新基础分数套旧残差。所有缩放只拟合当前fit完整组。

51次新拟合，四线程，worker 21.499秒，父进程600秒硬上限。复用108/109已有模型均以源/折/参数/OOF SHA核对，0.01控制的统计/权重1e-12、OOF/验证分数1e-10重现。数学目标与108/109已核对函数相同；检查收敛/梯度、缓存重载、零修正等于基础模型与正式接口。

完整解压资产包含基础模型、均值/缩放、残差与config≤16MiB；训练停止后每个模型fresh官方预测+独立评分≤30秒，严格分数重排、题序、新ID、变bank、空输入、Python整数、同组同分均通过。本机验证计时不是参考Xeon完整测试资格。

历史自身和公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，长期开发的train/validation不是独立确认。四配置结束，不按验证反馈追加密集参数。

复现：code目录train_round114_anchor_regularization.py，再evaluate_round114_anchor_regularization.py。已有目录拒绝覆盖。证据：runs/round114-anchor-regularization/result.json、anchor-progress.json、fit-progress.json、pair-audit；runs/round114-evaluation/frozen-before-validation.json、all-results.json、integrity.json及官方进程日志。
