# Round135学习记录：数量标签、人名与明确状态

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation、3个新最终候选统一冻结后各一次官方test。

## 全部结果

|模式|训练OOF/4755|回代/4755|训练修复/新增|三折净变化|验证/798|验证修复/新增|官方test/467|
|---|---:|---:|---|---|---:|---|---:|
|原123控制|4404|4519|0/0|[0,0,0]|754|0/0|390（已有记录）|
|label|4407|4524|4/1|[2, 0, 1]|753|0/1|390|
|role|4404|4522|3/3|[0, 1, -1]|754|0/0|390|
|both|4407|4522|6/3|[2, 2, -1]|752|0/2|389|

## 与旧方案的区别、审计及局限

14年龄关系、40角色审计、58时期换算、66跨题槽位匹配、70数字身份已做。135不产生新答案，而在同一题上区分数字紧邻标签、局部唯一显式人名、唯一状态词的匹配/冲突；按own与foreign提供者分开。官方final由原parser读取，特征正文遮蔽最终字段。相较134的宽词窗，此处要求数量标签直接邻接或label:number形式；人名/状态多义时未知。

训练4755题识别目标数量标签2857题、目标人名844题、状态1180题。未知不等于错误，识别数不等于正确率；数量标签集合仍是词面前缀，没有POS、代词消解、真实实体/时间推断。money/dollar统一不进行金额换算。

|cue|原错：正确组更强|原错：错误首选更强|原正确：首选更强|原正确：其他错误组更强|非零组|
|---|---:|---:|---:|---:|---:|
|label_own_match|20|23|120|138|745|
|label_foreign_match|6|6|27|80|148|
|label_own_mismatch|16|8|78|85|376|
|label_foreign_mismatch|15|7|47|83|180|
|entity_own_match|3|6|30|43|254|
|entity_foreign_match|2|0|5|37|55|
|entity_own_mismatch|0|1|9|12|47|
|entity_foreign_mismatch|3|0|3|22|34|
|state_own_match|14|15|106|89|634|
|state_foreign_match|1|5|10|60|93|
|state_own_mismatch|3|3|17|18|81|
|state_foreign_mismatch|1|1|7|20|38|

不能把match当正票、mismatch当负票：原错label_own_match为20对23，label_own_mismatch为16对8，foreign_mismatch为15对7。词面“不匹配”在正确组反而可能更强，可能来自题目标签截断、中间量、多个对象或不同提供者的描述；本批未按这些计数手选符号或删特征。人名相关原错覆盖很少，state_own_match14对15，也未显现单向可靠纠错。原正确的多错误组存在计数可重叠，不与单个错误首选的计数混作相同比例。

## 已拟合系数（描述性）

|模式|特征|标准化权重|原始特征斜率|
|---|---|---:|---:|
|round135_label|label_own_match|-0.0298435|-0.256982|
|round135_label|label_foreign_match|-0.050786|-0.856776|
|round135_label|label_own_mismatch|-0.00503382|-0.0499449|
|round135_label|label_foreign_mismatch|0.0334764|0.44758|
|round135_role|entity_own_match|-0.0376685|-0.515464|
|round135_role|entity_foreign_match|-0.0307945|-0.871396|
|round135_role|entity_own_mismatch|-0.0146941|-0.348698|
|round135_role|entity_foreign_mismatch|0.0130364|0.404972|
|round135_role|state_own_match|0.0187889|0.162138|
|round135_role|state_foreign_match|-0.0923412|-2.28063|
|round135_role|state_own_mismatch|-0.00107869|-0.033221|
|round135_role|state_foreign_mismatch|-0.0321595|-1.37165|
|round135_both|label_own_match|-0.0271634|-0.233905|
|round135_both|label_foreign_match|-0.0411626|-0.694426|
|round135_both|label_own_mismatch|-0.00413702|-0.041047|
|round135_both|label_foreign_mismatch|0.0410153|0.548376|
|round135_both|entity_own_match|-0.0353751|-0.484081|
|round135_both|entity_foreign_match|-0.032852|-0.929617|
|round135_both|entity_own_mismatch|-0.014808|-0.3514|
|round135_both|entity_foreign_mismatch|0.0099722|0.309784|
|round135_both|state_own_match|0.0202138|0.174434|
|round135_both|state_foreign_match|-0.0918095|-2.2675|
|round135_both|state_own_mismatch|0.00092216|0.0284004|
|round135_both|state_foreign_mismatch|-0.0302147|-1.28871|

系数存在相关性，不能当作独立因果贡献；没有据系数再删列、放大权重、扫正则或导出新版本。OOF修复和新增、全部三折、回代及验证同时保留，不把训练收益代称验证突破。

## 开发选择和测试边界

新输出未严格胜过(754,4404)，保留原123开发身份；先于新test已记录。

本批已观察test最高390/467，旧最高392/467；全部3个预定最终版本均测试，无test逐题分析或按中途成绩调整其余模型。test已反复暴露且长期自适应开发，不能把最高分当独立泛化估计；后续若据test挑提交版本须披露参与选型。

## 每轮给下一轮的依据

零拟合train诊断核对了全部25次OOF改选的逐特征margin贡献。发现具体的词面表示缺陷：目标gallons of gas被抽成(gallon,of,gas)，正文10 gallons只匹配较短(gallon)，被误标mismatch；ounces of fudge与ounces类似。4个label修复里包括利用这种伪冲突的情况：加油题10对8的修复来自mismatch贡献；另一题也用同类贡献把正确14改成错误6。因此训练净+3并非都来自正确数量标签，不能把它称为可靠单位绑定。完整cases和贡献位于runs/round135-train-diagnosis；未使用validation/test个题。

下一轮只对当前题目标签的严格前缀关系作unknown处理：一个完整标签与其短前缀不再计冲突，也不自动当精确match。此修正来自train表示审计，保持其他抽取、父模型、λ、fold、权重与尺度协议，比较修复前后。不同时修改人名词表、扩大窗口或增加单位换算，以区分表示修复和其他变化。

下一步应以本表的训练修复/新增和三折稳定性决定是否继续这个家族。单独label与role分支可区分精确数量标签和稀疏人名/状态是否互补；若组合新增错误抵消修复，不继续堆关键词。若标签有正向训练净收益但验证持平，也只算训练开发证据，需新保留数据确认。任何词法扩展必须先按train中的目标标签抽取失败/中间量混淆分层审计，独立列出旧正确反例，不按test个题修规则。

## 完整性、失败和复现

最大全部递归未压缩资产64728字节，完整fresh validation预测+独立官方评分最多6.648秒、test最多5.099秒；CPU总4线程，满足16MiB/30秒，本机资格不代替参考Xeon。训练600秒硬限，所有parser/原始数据/官方工具/父源资产、父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全train导出/零残差/重排/题序/新ID/变batch/空输入/同答案同分检查完成。旧132/133压缩包SHA通过。

失败记录：首次builder在拟合前因先替换answer_mentions后schema期望字符串过时而触发guard；原builder保存在runs/round135-source-build-repair，仅修正预期中间字符串，没有修改特征、计划、审计或模型。此时0拟合/0验证/0测试。之后12拟合、4验证、3测试完成，每项test一次。

复现：audit_round135_quantity_binding.py → build_round135_experiment.py → train_round135_quantity_binding.py → train_round135_quantity_binding.py --evaluate → run_frozen_tests_round135.py → closeout_round135.py；已有输出目录拒绝覆盖。所有原始聚合分数、拟合/命令/过程监控、冻结源与参数保留；无公开提交或issue。Codex实质参与实现、训练、评估与分析，AI_DISCLOSURE.md同步记录。

统计11项解释边界覆盖分母/分层、选择条件、生态外推、相关/因果/反向因果、混杂、回归均值、多次比较、假设与效应范围；不作独立显著或稳定提升主张，不作Collider调整。
