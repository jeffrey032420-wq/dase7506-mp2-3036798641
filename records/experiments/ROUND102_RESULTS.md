# Round102：严格最终算式与评分字面值核对

## Material Passport

academic-research-suite / experiment-agent；2026-10-27 UTC+8；VERIFIED_LOCAL_VALIDATION。

**验证最高749/798；当前最优749/798。未晋级，保留原模型。** 没有新增拟合；两个固定格式处理版本均完整导出和验证，无OOF。

## 假设和控制

官方解析器读取####后的第一个数值；原R11只处理稍后boxed字面值证据。本轮比较完整且真等式链，以及额外允许完整算术表达式的两个版本，使用原有有界Fraction计算器；百分号、未知文字、变量、不安全操作和不成立等式均不推断。新证据合并到原规则，只执行一次winner transfer，不改官方解析器或标签。

|模式|TRAIN识别候选|TRAIN识别题目|TRAIN回代/4755|
|---|---:|---:|---:|
|equation|0|0|4406|
|expression|0|0|4406|

识别覆盖为零时，该模式在训练分布中没有可作用的证据；不能把数学控制通过称作有效模型改进。按冻结计划仍保留两个预定输出及其验证结果，没有增加规则、扩展网格或按验证错例修改解析器。原规则复现、完整训练缓存/导出、未受影响题输出、53题严格接口均通过。

|模式|验证/798|修复/新增错|本机fresh预测+独立评分秒|
|---|---:|---:|---:|
|equation|749|0/0|2.502|
|expression|749|0/0|2.518|

完整解压资产均≤16MiB，四线程本机完整验证组合均≤30秒。这不认证参考CPU完整测试计时。验证反复用于自适应开发，不能当独立泛化或显著性证据；未读、哈希或运行任何测试输入/参考/预测/分数。旧模型/来源、官方train/validation、PDF/ZIP/submission_ready历史快照全部保持。

## 复现与下一步

在独立工作副本还原本批incumbent-pointer.json（latest101），保留官方train/validation数据与原79父checkpoint；新batch输出目录应不存在。依次从code目录运行build_round102_final_expression.py，待进程结束后evaluate_round102.py，再运行finalize_round102.py。历史失败、完整结果和资产哈希不覆盖。

下一步先在TRAIN确认新机制的实际覆盖，再投入实现与拟合；没有干预覆盖的格式特例缺少继续扩展依据。继续研究需要能改变现有错题排序的可迁移监督。

证据：code/runs/round102-final-expression/result.json、code/runs/round102-evaluation/results.json及code/runs/round102-verification/results.json。
