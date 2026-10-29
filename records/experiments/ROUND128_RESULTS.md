# Round128：冻结754父模型的别名差值残差

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；8新拟合、3官方验证输出（含原123控制）。

固定完整123；仅用percent/both别名图24维与原图的差值训练独立残差，λ.01，same-fit parent margin，原fold/每题归一权重/fit-only尺度。delta不减均值，未变化题的分数严格不动。127组件诊断发现完整重训在未变化题新增5–6错，但固定旧系数换新特征也净减1；本批检验减少无关误伤是否足够。

|模式|训练OOF|回代|训练修复/新增|三折|验证/798|分歧/355|单正确/117|验证修复/新增|delta零验证题|KiB|fresh秒|
|---|---:|---:|---|---|---:|---:|---:|---|---:|---:|---:|
|control|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|798|62.01|4.244|
|percent|4404|4523|6/6|[0, 2, -2]|754|311|79|0/0|728|63.16|5.553|
|both|4404|4522|6/6|[0, 2, -2]|754|311|79|0/0|726|63.15|5.601|

无人严格胜过当前(754,4404)，保留原123，不新增test。

8新拟合worker29.959秒、4线程、600秒硬限。父outer-held严格复现4404 OOF，delta零题的原分数在全train OOF、full回代与完整validation均逐值复现；零残差也严格复现父。梯度/重复pair/每题权重、缓存/fit-only尺度、导出/重排等接口、源/计划/父新资产SHA通过。全部资产≤16MiB，fresh完整官方validation预测+独立评分≤30秒，参考Xeon未认证。

训练仍包含全部有信息题的归一权重，没有active-only归一或新正则搜索。未变化题不动是设计约束，只有总体修复超过新增才是准确率提升。新来源仍不能证明题意/实体/单位；长期自适应开发与已知历史测试汇总如实披露，测试不用于训练/选择。

统计解释11/11：分层/三折（Simpson）；限定题库（Ecological）；候选分布（Berkson）；不作Collider调整；报告分母；小变化考虑regression-to-mean；全部输出保留（survivorship）；披露look-elsewhere/forking-paths；不作相关即因果或reverse-causality判断。

复现train_round128_alias_delta.py及--evaluate；证据runs/round128-alias-delta、round128-evaluation，旧证据拒绝覆盖。
