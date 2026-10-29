# Round127：计算链来源别名消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4最终输出官方验证。

## 假设与审计

按明确百分比p→p/100、同时存在美元语境的cent p→p/100增加原题来源的别名，不增加来源数或覆盖分母、不推断涨跌倍率。历史已有单位/百分比尝试，本批只修改当前123图的来源归一化。原始字面值匹配优先，未知保持未知。train新特征差异区分当前351错中percent31/cents1/both32题；新严格完整链仍含89/3/92错误候选，不能当硬证明。固定120父、24维图残差、λ.01、same-fit margin、三折、fit-only scaler和每题权重。

|模式|训练OOF/4755|回代/4755|修复754父错/新增（OOF）|相对父三折|验证/798|分歧/355|单正确/117|验证修复/新增|KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|legacy|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.94|3.796|
|percent|4399|4520|6/11|[-1, -2, -2]|754|311|79|0/0|61.94|3.821|
|cents|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.94|3.899|
|both|4400|4520|6/10|[0, -2, -2]|754|311|79|0/0|61.94|3.923|

## 开发选择

新输出未严格胜过当前(754,4404)；保留123，不新增test。

## 资源、核验及局限

4模式各3outer+1full=16拟合，worker28.076秒，4线程、600秒硬限。legacy全部fold/full参数、OOF和验证逐分数复现原123；无有效别名题原始特征全量严格不变，但全局重训练仍可改变这些题分数。源/计划/父新资产、缓存、梯度/重复pair/每题权重、导出/零修正及重排/题序/ID/变batch等核验通过；全部资产≤16MiB，fresh完整validation预测+独立评分≤30秒；参考Xeon未认证。

首次构造检查因float与Fraction精确比较失败，数据/拟合前已修复容差，原源/失败保留，新完成审计v2。来源仍按数值去重，不能证明实体/单位/题意；正确终值标签也不保证完整推理正确。训练错例查看驱动本批方向，属于自适应开发。未读取test输入/参考/预测/评分用于训练或选择；已知历史测试汇总继续披露，原123/120及79保留。

统计解释11/11：报告分层/三折防Simpson；限定题库防Ecological；注意筛选分布Berkson；无Collider因果调整；报告分母；考虑regression-to-mean；四模式全报防survivorship；披露look-elsewhere和forking-paths；不作相关即因果或reverse-causality主张。

复现：audit_round127_source_aliases.py，train_round127_source_aliases.py，再训练脚本--evaluate。证据runs/round127-train-audit（首次失败）、round127-train-audit-v2、round127-source-aliases、round127-evaluation；原输出拒绝覆盖。
