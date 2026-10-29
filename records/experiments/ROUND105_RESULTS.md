# Round105：补齐旧语义系数分量消融

Material Passport: academic-research-suite / experiment-agent；2026-10-28 UTC+8；VERIFIED_LOCAL_VALIDATION。

**两个旧系数组件输出最高747/798，未超过749/798（93.8596%），保留Round79。** 两个输出在构建与本批验证前固定，零次新系数拟合、无新OOF。原交付PDF/ZIP/submission_ready保持历史快照。

## 为什么补齐这个对照

R103同时更新旧semantic1422系数和新增证据系数；R104固定旧权重后，四个新增numeric14单独/残差配置的验证均未净增。
因此补齐旧系数变化单独使用的两个对照，辅助alpha固定.3/3。不追加alpha、混合或门控搜索，不把归因对照包装为新特征。
R103旧系数是在带有numeric14的联合目标中学得，即使本轮推理不使用新增14维，系数仍携带该训练过程的影响。
不能把“仅旧系数”解释为完全没有接触新增训练证据。

## 两个零拟合输出与TRAIN控制

复制完整R79，只用对应R103 numeric donor的old_weight替换semantic权重；原base mean/scale、投影、最终semantic mean/scale逐数组不变。
没有新增numeric14运行时校正；原numeric alpha1算术门不变，raw分数合并后只应用一次原R11格式迁移，推理仍为method_round11.py。
辅助alpha指训练donor的新增块正则，不是当前运行时numeric分支alpha。

|辅助numeric14 alpha|TRAIN回代/4755|修复/新错（对4406父模型）|改变选择数|旧权重变化L2|
|---|---:|---:|---:|---:|
|0.3|4406|10/10|200|0.037741|
|3|4405|6/7|138|0.027320|

这些混合TRAIN结果完整保留：alpha.3为10修复/10新错、总数与父模型持平；alpha3为6/7、净少1题。
它们严格复现冻结的TRAIN104组件审计，没有用回代筛选准入，也不是OOF、持出或独立泛化证据。
记录0次新拟合、2次构建；一CPU线程，构建/控制/接口检查24.924秒，硬预算600秒。
原完整父模型复现≤1e−8，完整TRAIN缓存/重载、gate不变、非semantic资产SHA、semantic统计/投影及53题严格接口控制通过。

## 本批完整验证

|辅助alpha|验证/798|修复/新错|改变选择数|完整解压MiB|fresh预测＋独立评分秒|
|---|---:|---:|---:|---:|---:|
|0.3|746|1/4|35|1.6005|2.043|
|3|747|1/3|24|1.6005|2.030|

最佳旧分量输出辅助alpha=3：验证修复1、新增错误3。该组件消融没有超过当前最佳，不能把组件有修复或训练回代变化称为准确率突破。

## 103–105的12个输出整体串联

|轮次|模式|新增证据族|辅助alpha|TRAIN回代/4755|验证/798|验证修复/新错|
|---|---|---|---:|---:|---:|---:|
|103|joint|numeric|0.3|4408|747|1/3|
|103|joint|numeric|3|4407|748|1/2|
|103|joint|answer_context|3|4386|744|1/6|
|103|joint|answer_context|30|4395|743|0/6|
|103|joint|both|3|4386|743|1/7|
|103|joint|both|30|4399|743|0/6|
|104|joint_new_only|numeric|0.3|4407|748|0/1|
|104|joint_new_only|numeric|3|4408|748|0/1|
|104|anchored|numeric|0.3|4408|748|0/1|
|104|anchored|numeric|3|4408|748|0/1|
|105|old_component_only|numeric|0.3|4406|746|1/4|
|105|old_component_only|numeric|3|4405|747|1/3|

共12个输出：103为6、104为4、105为2；重复父模型控制不计入。完整归因比较集中在numeric14的8项匹配配置；
其余4项answer_context/both输出没有对应的旧分量独立对照，不能把numeric14结论推广到所有证据族。
joint_new_only是固定R103新增系数的组件消融；anchored是另拟合的固定父权重残差，两者不是同一个优化解。

R103联合numeric14产生过修复、而104仅新增分量没有修复，说明在已比较配方中新增运行时项单独并不足以复现联合收益；
旧系数重分配或两分量交互需要区分。105结果提供旧分量单独的数量对照，但本报告只汇总已完成记录，未读验证逐题分数/题目；
相同修复数量不证明修复的是同一道题，也不能证明某种数学证据是唯一原因。未净增不能称为突破；即使存在净增也只是复用validation的开发选型。

## 资源、复现与边界

严格超过冻结的749且全部官方/资源/接口检查通过才晋级；同分保留当前最佳，新赢家同分按更小完整解压资产、再按名称字典序。
两个输出通过fresh官方预测、独立完整验证798题评分，四总CPU线程预测＋评分≤30秒，全部嵌套解压资产≤16MiB。
严格候选重排rtol=atol=1e−8、题序、bank大小、新ID、空输入及Python整数选择均通过。
本机完整验证时间不是参考CPU完整测试资格认证。多轮validation用于自适应开发，会产生选择偏差；不作独立泛化或显著性声明。
没有读取、哈希或运行测试输入/参考/预测/分数，没有公开发布或提交。所有旧来源、原官方文件、父模型、donors及旧交付快照保持。

复现使用独立副本，先从code/runs/round105-evaluation/incumbent-pointer.json还原CURRENT_BEST（latest104），
保留原官方数据、父79、两个R103 numeric donor、冻结104-preflight/audit.py与result.json、103/104完成记录及全部历史来源/交付快照。
副本中的runs/round105-old-component、runs/round105-evaluation、runs/round105-verification生成目录应不存在。
从code工作目录使用固定venv Python依次运行build_round105_old_component.py，全部构建/训练停止后evaluate_round105.py，最后finalize_round105.py。
不需要额外分析步骤；已冻结104预检作为既有依赖保留，不覆盖交付工作区或旧证据。

证据：[TRAIN构建](code/runs/round105-old-component/result.json)、[冻结记录](code/runs/round105-evaluation/frozen-selection.json)、
[两项完整结果](code/runs/round105-evaluation/all-validation.csv)、[12项汇总](code/runs/round105-evaluation/component-chain-summary.json)、
[官方审计](code/runs/round105-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
