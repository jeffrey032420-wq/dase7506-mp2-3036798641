# Round109结果：固定答案组模型与局部算术残差

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。先保存计划，固定四配置，训练全程不加载验证或测试；全部模型冻结后验证。

|anchor增强|残差lambda|训练嵌套OOF/4755|anchor OOF|验证/798|anchor验证|分歧/355|单正确/117|修复旧错/新增错|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
|False|0.01|4386|4387|748|741|305|76|12/13|0.02616|1.955|
|False|0.1|4391|4387|747|741|304|76|11/13|0.02615|1.973|
|True|0.01|4390|4380|750|746|307|77|13/12|0.02615|1.979|
|True|0.1|4392|4380|751|746|308|78|14/12|0.02615|1.966|

最佳round109_subsets_r0p1：751/798（94.1103%）。超过原749；另存验证研究候选。已测Round79最终模型和历史测试成绩不变。

## 方法与来源

借鉴[CaspianW固定anchor与局部算术残差](https://github.com/CaspianW/dase7506-mp2/blob/main/src/train.py)，[组内mean/max聚合](https://github.com/CaspianW/dase7506-mp2/blob/main/src/quantity_flow_features.py)及[11项局部特征定义](https://github.com/CaspianW/dase7506-mp2/blob/main/src/arithmetic_features.py)。自行实现，不并入对方代码/权重；既有numeric_round7_v3有界解析器与来源解析器不完全相同。使用原始完整组残差pair、每题归一损失、显式L2。

不同于来源的同fit anchor margin，本轮使用inner-OOF offset。18次inner anchor拟合，12次outer残差拟合和4次全训练残差拟合，共34次新拟合。outer-held完全排除在inner fit和残差fit之外；scaler只拟合该fit原始组。最终残差用全train OOF offset，部署用full-train anchor。第108轮折模型与OOF数组逐分数精确一致，继承源/资产/折/OOF哈希均有记录。

四线程worker训练墙钟14.554秒，父进程硬timeout900秒。数值梯度、重复pair不变性、零残差严格等于anchor、缓存/导出一致、分数重排1e-8、题序、新ID、变bank、空输入、Python整数、同答案同分检查通过。完整资产包含anchor、scaler、残差权重和config，按NPZ解压保守计数；官方fresh预测+独立评分≤30秒。本机计时不代表参考Xeon完整测试资格。

历史自身与公开他人测试汇总分数已知；本轮不访问/哈希/预测/评分测试，不声称反复使用的训练或验证是独立确认。训练回代与OOF分开保存。

复现：code目录依次运行train_round109_arithmetic_residual.py与evaluate_round109_arithmetic_residual.py。已有目录拒绝覆盖。证据为runs/round109-arithmetic-residual/result.json、nested-partitions.json、residual-progress.json、pair-audit；runs/round109-evaluation/frozen-before-validation.json、all-results.json、integrity.json及每个官方评分和进程日志。
