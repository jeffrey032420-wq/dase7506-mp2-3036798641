# Round111：固定表示的正则参数比较

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定2表示×4正则，只用训练三折为每种表示选一个候选；官方验证仅两个候选。

## 全部训练配置

|模式|lambda|训练三折OOF/4755|进入验证|
|---|---:|---:|---|
|full|0.03|4390|False|
|full|0.1|4392|True|
|full|0.3|4390|False|
|full|1.0|4385|False|
|final_evidence|0.03|4397|False|
|final_evidence|0.1|4398|True|
|final_evidence|0.3|4394|False|
|final_evidence|1.0|4391|False|

同分优先更强正则。lambda0.1为已知配置重现，不计新发现；未选出的六个配置没有运行验证。

## 两个训练选出候选的官方验证

|模式|lambda|验证/798|相对751|修复/新增错|单正确/117|资产MiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|---:|
|full|0.1|751|+0|0/0|78|0.02613|2.022|
|final_evidence|0.1|751|+0|1/1|78|0.02623|1.986|

最佳round111_full_r0p1：751/798（94.1103%）。没有超过751，保留第109轮研究候选。原已测Round79最终模型和历史测试记录保留。

32次新残差拟合，四线程，worker 15.903秒，600秒硬上限。复用第110轮验证过的嵌套anchor margin，按原题pair顺序、权重、哈希严格核对；每折统计只拟合fit，0.1参数严格重现。验证前全部源/模型/计划/训练结果SHA冻结。

全部8模型通过训练重载、零修正和接口检查；两个验证候选通过官方fresh预测+独立评分、严格分数重排/题序/新ID/变bank/空输入/Python整数/同组同分。完整解压资产含anchor/统计/残差/config≤16MiB，fresh预测与评分≤30秒。本机验证计时不是参考Xeon完整测试资格。

历史自身及公开他人测试总分已知。本轮不访问/哈希/预测/评分测试；train/validation长期自适应复用，不作独立确认或显著性承诺。未扩展预定参数网格，也未在结果后验证未入选配置。

复现：code目录train_round111_regularization.py，再evaluate_round111_regularization.py。输出存在则拒绝覆盖。证据：runs/round111-regularization/result.json、fit-progress.json、pair-audit；runs/round111-evaluation/frozen-before-validation.json、all-results.json、integrity.json及官方日志。
