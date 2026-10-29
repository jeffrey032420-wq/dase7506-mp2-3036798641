# Round89–91：语义分块惩罚、保留原目标的损失与题内差异度量

Material Passport: academic-research-suite / experiment-agent；2026-10-27；VERIFIED_LOCAL_VALIDATION。

**全部14个新输出均未超过749/798（93.8596%），保留Round79。** 用户明确要求继续训练，未冻结为最终提交，也未运行测试。
本批预先限定14配置（6+4+4），Round90固定收敛要求排除0个，实际14个输出在读取本批验证前冻结。
全部权重/统计量来自所给train；没有外部数据或预训练权重。复用validation仅作自适应开发选型，不是无偏或显著性证据。

## 先提出假设与核对历史

1. **Round89**：1024维Embedding、14维文本、384维context可能需要不同收缩。semantic总体α=.3，逐个特征块改变惩罚：Embedding×{.5,2}、文本×{.25,4}、context×{.5,2}，其余为1，共6配置。原特征、训练均值/尺度和投影保持，解`(G+diag(.3·p))w=b`。Round10曾有缺失特征期望的对角惩罚，Round60改变另一套稀疏匹配表示的行范数，Round82改变numeric末6维惩罚；历史审计未找到本轮完整保护语义1024/14/384分块比较，不声称首次研究正则。
2. **Round90**：保留已有效的成对二次目标和α=.3锚点，分别加均匀正确候选CE或成对logistic损失，β∈{.1,.3}，共4配置。此前纯CE/logistic/其他集合目标已有尝试；本轮区别是加到原目标，而不是替代它。固定L-BFGS-B及梯度/收敛要求，失败不修改参数重试、不进入验证。
3. **Round91**：仅减候选均值在成对差分中会抵消，先验证此代数控制；真正干预是使用全部train候选的无标签题内差异方差v，`d=(1−ρ)+ρ·max(v,1e−4)`，解`(G+diag(.3·d))w=b`，ρ∈{.25,.5,.75,1}，共4配置。Round10的diag(G)是有标签成对目标对角量；本轮v来自包含全正确题在内的全部训练题，不把两者视为相同对象。

三路线只改semantic系数及配置记录，numeric α=1、原算术门和一次R11格式转移保持。推理使用原method_round11.py。
没有新OOF或持出筛选；以下回代只说明拟合现象，不用于挑选准入或扩大候选池。

## 实际拟合与控制

- Round89：1个成对目标系统、7次ridge解（含全1控制），44.502秒。
- Round90：4次完整train优化、1次β=0控制，32.873秒；四个有限差分梯度检查通过。
- Round91：2个Gram系统（含纯中心化控制）、6次解，31.248秒；无标签方差与有标签diag(G)的相关系数仅作描述，为0.987311，不等于两者相同。

各路线1CPU线程、600秒硬上限，全部训练退出后才开始4总线程的fresh官方审计。
三条原模型复现控制均≤1e−8；完整train缓存与直接checkpoint、53题且含门内/门外的严格重排、题序、不同bank大小、新ID、空输入及Python整数检查保留。

|轮次|输出|完整train回代 /4755|回代修复 / 新错（对当前）|
|---|---|---:|---:|
|89|round89_embedding_factor0p5|4434|30 / 2|
|89|round89_embedding_factor2p0|4379|3 / 30|
|89|round89_text_factor0p25|4395|3 / 14|
|89|round89_text_factor4p0|4435|46 / 17|
|89|round89_context_factor0p5|4409|7 / 4|
|89|round89_context_factor2p0|4401|3 / 8|
|90|round90_uniform_correct_ce_b0p1|4409|5 / 2|
|90|round90_uniform_correct_ce_b0p3|4418|15 / 3|
|90|round90_pairwise_logistic_b0p1|4406|0 / 0|
|90|round90_pairwise_logistic_b0p3|4406|1 / 1|
|91|round91_rho0p25|4410|8 / 4|
|91|round91_rho0p5|4423|22 / 5|
|91|round91_rho0p75|4438|40 / 8|
|91|round91_rho1p0|4496|106 / 16|

回代的父模型为4406/4755；这些不是验证、OOF、持出或独立泛化结果。

|Round90增加的损失|β|允许导出|优化迭代|最终梯度∞范数|优化器状态|
|---|---:|---|---:|---:|---|
|uniform_correct_ce|0.1|True|52|4.77e-07|CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH|
|uniform_correct_ce|0.3|True|61|5.97e-07|CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH|
|pairwise_logistic|0.1|True|50|3.18e-06|CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH|
|pairwise_logistic|0.3|True|59|1.63e-06|CONVERGENCE: RELATIVE REDUCTION OF F <= FACTR*EPSMCH|

## 冻结后完整验证

|轮次|输出|参数|验证 /798|修复 / 新错（对Round79）|完整资产 MiB|fresh预测＋独立评分秒|
|---|---|---|---:|---:|---:|---:|
|89|round89_embedding_factor0p5|semantic α=.3; embedding penalty ×0.5|746|0 / 3|1.6005|1.896|
|89|round89_embedding_factor2p0|semantic α=.3; embedding penalty ×2|744|0 / 5|1.6005|1.955|
|89|round89_text_factor0p25|semantic α=.3; text penalty ×0.25|744|0 / 5|1.6005|1.983|
|89|round89_text_factor4p0|semantic α=.3; text penalty ×4|740|4 / 13|1.6005|1.882|
|89|round89_context_factor0p5|semantic α=.3; context penalty ×0.5|746|0 / 3|1.6005|1.905|
|89|round89_context_factor2p0|semantic α=.3; context penalty ×2|746|0 / 3|1.6005|1.927|
|90|round90_uniform_correct_ce_b0p1|quadratic + 0.1·uniform_correct_ce|749|0 / 0|1.6006|1.904|
|90|round90_uniform_correct_ce_b0p3|quadratic + 0.3·uniform_correct_ce|747|0 / 2|1.6006|1.962|
|90|round90_pairwise_logistic_b0p1|quadratic + 0.1·pairwise_logistic|749|0 / 0|1.6006|1.919|
|90|round90_pairwise_logistic_b0p3|quadratic + 0.3·pairwise_logistic|749|0 / 0|1.6006|1.937|
|91|round91_rho0p25|within-query variance metric ρ=0.25; floor=1e−4|748|0 / 1|1.6005|1.902|
|91|round91_rho0p5|within-query variance metric ρ=0.5; floor=1e−4|746|0 / 3|1.6005|1.928|
|91|round91_rho0p75|within-query variance metric ρ=0.75; floor=1e−4|743|0 / 6|1.6005|1.877|
|91|round91_rho1p0|within-query variance metric ρ=1; floor=1e−4|739|4 / 14|1.6005|1.975|

Round89（语义分块惩罚）最佳746/798：修复0、新增3，参数semantic α=.3; context penalty ×0.5。 Round90（原二次目标加凸损失）最佳749/798：修复0、新增0，参数quadratic + 0.1·pairwise_logistic。 Round91（题内差异方差惩罚）最佳748/798：修复0、新增1，参数within-query variance metric ρ=0.25; floor=1e−4。

本批三类有限改动未取得验证净增。改变特征收缩、保留原目标后增加损失以及按题内差异调整惩罚，都可能修复部分旧错，同时破坏其他旧正确选择；应比较修复和新增错误，而不能用训练回代改善推断泛化提高。 这是相关的自适应开发比较，不能识别唯一因果机制、证明模型上限或独立测试泛化。

## 资源、选型和材料边界

严格超过749且全部官方/资源/接口检查通过才晋级；同当前分数保留当前模型，新赢家同分按更小完整解压资产、再按名称字典序。
全部14行与所有训练失败均保存，不根据个别验证错题加规则或扩展本批。
完整解压资产1,678,249–1,678,350字节，均≤16MiB；fresh完整验证预测＋独立评分1.877–1.983秒，均≤30秒。
当前Round79另fresh复核749/798，1.908秒。本机完整验证计时不等于参考Xeon8457C完整测试资格认证。
历史来源哈希（含Round88）、官方工具/train与validation文件、原R11/当前R79/全部新嵌套资产均通过；未读取或哈希测试输入、参考、预测或分数。
此前MP2_REVIEW_PACKAGE.zip、REPORT_DRAFT.pdf及已有submission_ready保持原历史快照；它们并非本轮新成果的自动同步版本。
本轮继续开发，没有执行冻结测试、公开上传或实际GitHub issue提交。

证据：[训练89](code/runs/round89-semantic-blocks/result.json)、[训练90](code/runs/round90-anchored-objective/result.json)、[训练91](code/runs/round91-query-metric/result.json)、
[冻结](code/runs/round89-91/frozen-selection.json)、[完整结果](code/runs/round89-91/all-validation.csv)、[官方审计](code/runs/round89-91-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
