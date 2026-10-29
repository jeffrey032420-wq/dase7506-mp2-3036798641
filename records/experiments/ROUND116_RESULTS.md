# Round116：题目数字与局部算术的分离消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。计划先于训练保存，模型及源冻结后全部官方验证。

## 假设与固定设置

依据115训练OOF的解析对齐收益提出H1：两个解析变化可能贡献不等；H2：该信号在原751的固定残差正则下是否仍成立。固定子集增强、基础lambda0.01、残差lambda0.1、嵌套OOF，只切换题目数字/解答算术两个定义，不搜索新参数。

|题目数字|解答算术|基础OOF/4755|完整OOF/4755|回代/4755|官方验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|legacy|4380|4392|4510|751|78|0/0|0.02592|1.857|
|legacy|aligned|4380|4395|4515|750|77|0/1|0.02592|2.053|
|aligned|legacy|4380|4392|4510|751|78|0/0|0.02593|1.930|
|aligned|aligned|4380|4395|4515|750|77|0/1|0.02593|2.117|

本批最佳round116_qlegacy_alegacy：751/798（94.1103%）。未超过原751，保留原研究候选；尚未最终测试。

## 两因子条件效应

|起点题目/算术|终点题目/算术|train OOF变化|三fold变化|验证变化|验证修复/新增错|
|---|---|---:|---|---:|---|
|legacy/legacy|aligned/legacy|+0|[0, 0, 0]|+0|0/0|
|legacy/aligned|aligned/aligned|+0|[0, 0, 0]|+0|0/0|
|legacy/legacy|legacy/aligned|+3|[1, 4, -2]|-1|0/1|
|aligned/legacy|aligned/aligned|+3|[1, 4, -2]|-1|0/1|

## 可靠性与限制

16次新残差拟合、0次新基础拟合，worker22.392秒，4线程、父进程600秒硬上限。基础全训练/outer/inner缓存逐个SHA核对；每题归一权重、scaler仅当前fit完整组，outer-held不参与训练；两legacy参数1e-12、OOF/验证分数1e-10重现原751。

所有候选收敛/梯度、缓存导出、零残差、候选重排分数1e-8、题序、新ID、变batch、空输入、Python整数、同答案同分通过；全部fresh官方validation预测+独立评分≤30秒，完整解压资产含嵌套基础、scaler/config≤16MiB。本机验证计时不是参考Xeon完整测试资格。

解析定义来源与剩余复现差异见ROUND115_RESULTS.md；没有执行外部源码或引入外部数据/权重。历史自身/他人测试汇总已知，本批不访问/哈希/预测/评分测试。长期开发复用train/validation，不能把微小验证优势当成独立泛化证明。遵照用户确认，每批最终候选均官方验证，测试留到方法冻结后。原751及原已测79模型保留；最终79指针不变。

复现：code目录先train_round116_factor_isolation.py，再evaluate_round116_factor_isolation.py。已有目录拒绝覆盖。训练证据runs/round116-factor-isolation/result.json、nested-partitions.json、pair-audit；验证证据runs/round116-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json及官方命令日志。
