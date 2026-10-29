# Round119：两种专家的嵌套条件选择

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。2个固定输出、53次新拟合。

## 假设与实现

主模型109的组pair-logistic算术残差与112的候选uniform-CE线性专家具有不同错误。检验只用置信度8维、或再加26维算术/最终答案差异，能否学习何时采用专家。选择器lambda0.1、阈值0.5固定；答案相同时不切换，两模型均错的分歧题对选择监督中性。scaler只fit当前fit专家分歧题。

outer-fit内重新产生两个完整专家的inner-OOF；主模型的inner残差又使用inner-fit内三折基础OOF margin。外层held标签不参与任何内层拟合，避免直接在同一全OOF上训练门控再声称其拟合分数为无偏评估。最终门控用全训练专家OOF拟合，部署用两个full-train专家。

|模式|嵌套OOF/4755|嵌套切换|训练修复/新增错|三折净变化|验证/798|分歧/355|验证切换|验证修复/新增错|资产KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|confidence8|4387|62|24/29|[-2, -5, 2]|751|308|3|1/1|54.00|2.786|
|evidence34|4389|59|22/25|[-2, -3, 2]|751|308|3|1/1|54.61|3.283|

最佳round119_evidence34：验证751/798，嵌套OOF4389/4755。

两条件均未通过预设的validation>751且嵌套OOF>4392门槛，本批不测试；不事后调阈值。

## 训练、来源与资源

worker40.434秒、4线程CPU、1800秒父进程硬限。新拟合计数：27 innermost基础、9 inner主残差、9 inner CE专家、6 outer选择器、2 full选择器，共53。CE固定40epoch/lr0.003/L2.001/batch128，seed按计划固定；不选验证epoch。原outer专家重放分数与已存OOF1e-10匹配。

源/计划/继承参数/分区SHA及拟合范围核对；数值梯度、收敛、重复样本不变、torch-float64/NumPy导出、零切换严格等于主模型、候选重排分数1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分通过。完整资产含两个专家及全部scaler/config/gate≤16MiB，各fresh官方validation预测+独立评分≤30秒。本机计时不是参考Xeon资格认证。

历史自身及公开测试汇总已知，长期train/validation开发复用披露。本训练/验证不访问test输入/参考/预测/评分，不按测试总分选模。全部旧源/资产、官方数据/parser/scorer和已有冻结版本保留。

复现：code目录train_round119_nested_switch.py，再evaluate_round119_nested_switch.py；已有目录拒绝覆盖。证据：runs/round119-nested-switch/result.json、innermost-partitions.json、inner-progress.json、gate-progress.json、pair-audit；runs/round119-evaluation/frozen-before-validation.json、all-results.json、integrity.json、selection-before-test.json和官方日志。
