# Round120：题目词与答案组特征交互

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。12次新拟合、4最终输出全部官方验证。

## 假设与设计

固定完整110父模型，学习题目词与候选证据的显式交互。题目独立加性项在同题候选间会抵消，交互则能为不同题目条件学习不同候选证据权重。题目采用固定128维有符号BLAKE2b unigram/bigram哈希并L2归一；无词表/IDF/外部语料。候选证据为原6维答案数值、原26维格式/算术/最终答案、或两者合并32维。历史已有问题文本及语义尝试，本批不声称首次问题条件化。

scaler只fit当前fit原始组，新增残差按每题平均pair logistic，L2固定0.1。训练偏置来自当前fit父模型的回代margin；这是same-fit offset策略，outer-held完全排除，不假称inner-OOF offset。稀疏训练，NumPy推理。

|模式|系数数|训练OOF/4755|回代/4755|三折净变化|验证/798|分歧/355|单正确/117|修复751错/新增错|资产KiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|---:|---|---:|---:|
|control|0|4398|4514|[]|751|308|78|0/0|27.12|1.997|
|question_numeric|768|4398|4515|[0, 0, 0]|751|308|78|0/0|33.95|2.741|
|question_evidence|3328|4394|4521|[-2, 0, -2]|752|309|79|1/0|54.27|2.836|
|question_both|4096|4396|4523|[-1, 1, -2]|752|309|79|1/0|60.36|2.806|

本批最佳round120_question_both：752/798。

无人满足训练前固定的validation≥751且OOF>4398及全部核验门槛，本批不触发测试。验证持平可以准入，但须有更好的训练折外证据；不事后改变门槛。

## 核验、资源与复现

训练worker15.826秒，4线程、父进程600秒硬限。三个交互各3outer+1full=12次新拟合；原110控制0新拟合。父fold held分数1e-10复现保存OOF；源/计划/旧参数/新资产SHA冻结核对，scaler及每题权重仅当前fit。梯度、重复pair、收敛、零交互严格等于父、导出、候选重排1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分通过。

全部资产包含父模型、scaler、交互权重和config≤16MiB；每个fresh官方validation预测+独立评分≤30秒。本机验证计时不是参考Xeon完整测试认证。本训练/验证未访问test输入/参考/预测/评分；历史测试汇总已知及长期自适应开发如实披露。旧模型、数据和官方parser/scorer均未改。

复现：code目录train_round120_question_interaction.py，再evaluate_round120_question_interaction.py。已有目录拒绝覆盖。证据：runs/round120-question-interaction/result.json、fit-progress.json、pair-audit；runs/round120-evaluation/frozen-before-validation.json、all-results.json、integrity.json、selection-before-test.json及官方日志。


# Round120验证752候选：追加冻结测试结果

2026-10-29。在看到四个官方验证结果后，按最高validation、同分最高训练OOF选择round120_question_both；测试之前写选择记录并冻结全部代码/参数。

- 官方test：**391/467 = 83.725910%**。
- 官方validation：752/798 = 94.235589%；训练OOF4396/4755，低于父110的4398。
- 方法：冻结110父模型+固定128维题目词哈希×32维数值/算术/最终答案证据交互，L2.1，same-fit父margin。
- 全部解压推理资产：61,805字节；4线程本机完整fresh test预测+独立评分2.296909秒。
- 本机CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon资格未验证。来源/资产/选择记录SHA前后核对通过。
- 原自动测试门槛OOF>4398未通过，原记录保持false。本次基于用户已有授权的追加冻结评价是看到验证结果后的开发决定，不称预注册准入成功，也不称稳定泛化提升。
- 未新增训练、改参、读取测试个题或按测试输赢再选模型；其他752/751候选未测。原110/109/79和历史结果保留。
- 官方JSON、完整冻结源/权重、命令、硬件与日志：final_evaluation/round120-test-20261029。研究候选在测试前已按train/validation选定120，测试后只补总分。原79最终提交字段保持，未创建GitHub issue。

历史测试汇总已知及长期自适应train/validation开发如实披露。评价本身不使一题验证增益变成独立统计证据。
