# Round121：题目交互的正则参数消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。48新拟合，4个最终输出全部官方验证。

## 假设与训练诊断

120数值交互在训练OOF一道选择都未改变；证据交互改8题却修2/新增6，说明修正偏小和方向带噪声并存。固定110父模型、原三类特征及哈希，只比较λ=1/.1/.01/.001/.0001。训练OOF选每类一档，平分取较大λ；未选参数不看验证。

|特征|λ|训练OOF/4755|相对110修复/新增|三折净变化|训练选中|
|---|---:|---:|---|---|---|
|question_numeric|1.0|4398|0/0|[0, 0, 0]|是|
|question_numeric|0.1|4398|0/0|[0, 0, 0]|否|
|question_numeric|0.01|4393|2/7|[-2, -3, 0]|否|
|question_numeric|0.001|4383|17/32|[-7, -2, -6]|否|
|question_numeric|0.0001|4356|37/79|[-18, -10, -14]|否|
|question_evidence|1.0|4398|0/0|[0, 0, 0]|是|
|question_evidence|0.1|4394|2/6|[-2, 0, -2]|否|
|question_evidence|0.01|4389|15/24|[-1, -6, -2]|否|
|question_evidence|0.001|4348|49/99|[-19, -15, -16]|否|
|question_evidence|0.0001|4261|80/217|[-53, -40, -44]|否|
|question_both|1.0|4398|0/0|[0, 0, 0]|是|
|question_both|0.1|4396|3/5|[-1, 1, -2]|否|
|question_both|0.01|4380|14/32|[-2, -7, -9]|否|
|question_both|0.001|4344|49/103|[-20, -13, -21]|否|
|question_both|0.0001|4261|78/215|[-57, -43, -37]|否|

## 官方验证

|最终候选|λ|训练OOF|验证/798|分歧/355|单正确/117|相对752修复/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|0.1|4396|752|309|79|0/0|60.36|2.984|
|round121_question_numeric_l1p0|1.0|4398|751|308|78|0/1|33.95|2.818|
|round121_question_evidence_l1p0|1.0|4398|751|308|78|0/1|54.27|2.957|
|round121_question_both_l1p0|1.0|4398|751|308|78|0/1|60.36|2.885|

本轮开发选择：round120_question_both，验证752/798、训练OOF4396/4755。
只根据train/validation排序；新候选未胜出，保留120，不新增test。

## 解释与局限

网格包含比原设置强10倍和弱1000倍的正则；应结合完整表格判断更弱正则是否增加OOF净收益。训练目标下降、权重增大或回代上升均不等于泛化提升。本轮未分离哈希碰撞、语言关系不足及same-fit offset影响；不能把失败解释为题目语义无用。参数已用OOF选择，因此所选OOF是开发指标。长期train/validation适应及历史测试汇总已知如实披露，不做独立显著性或因果主张。

## 资源、核验与复现

45outer+3full=48新拟合，worker21.540秒，总4线程，600秒硬限。三个λ=.1严格复现120折外分数1e-10。fit-only scaler/每题权重/梯度/收敛/导出/零修正/重排/题序/新ID/变batch/空输入/Python整数/同答案同分核验通过。所有父参数和官方输入/解析/评估工具未修改，源/计划/参数SHA核对通过。全部资产≤16MiB，fresh validation预测+独立评分≤30秒；未做参考Xeon完整test认证。

复现：code目录train_round121_regularization.py，再evaluate_round121_regularization.py；存在证据目录则拒绝覆盖。证据位于runs/round121-train-diagnosis、round121-regularization、round121-evaluation。

## 统计解释检查（11/11）

1 Simpson：报告总体、分歧、单正确及三折，不以总体代替全部分组。2 Ecological：只推断本批题目表现。3 Berkson：数据固定且分歧分布不同，不能外推总体。4 Collider：无因果调整主张。5 Base rate：报告分母和容易的一致题占比。6 Regression to mean：小增益及自适应选择不称稳定提升。7 Survivorship：15训练配置含失败表现全部保留，4最终输出全验证。8 Look-elsewhere：有限参数搜索及全部结果披露，不报显著性。9 Forking paths：计划冻结、旧设置复现、未按验证追加。10 Correlation/causation：噪声和强度是当前实现的操作性解释，不推广为唯一因果。11 Reverse causality：无因果方向主张。
