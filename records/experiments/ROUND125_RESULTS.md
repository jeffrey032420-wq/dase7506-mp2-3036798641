# Round125：same-fit与真正嵌套OOF父margin

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。34新拟合、4最终输出官方验证；36个旧anchor核验复用。

## 假设与干预

124训练诊断显示父same-fit相对held更乐观；本轮只改变链残差训练margin来源，固定原123特征/正则及部署父120，不删列、不搜参数。same-fit为原配方；nested_parent_oof在每个outer-fit内构造完整120父模型的3-fold OOF，所有父层排除outer-held。

|特征|margin|λ|训练OOF/4755|回代/4755|相对匹配控制修复/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry|same_fit|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.77|3.657|
|ancestry|nested_parent_oof|0.1|4406|4522|5/6|[-2, 1, 0]|750|307|79|1/5|61.78|3.561|
|both|same_fit|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|61.91|3.625|
|both|nested_parent_oof|0.01|4399|4522|9/14|[1, -6, 0]|754|311|79|0/0|61.91|3.609|

## 选择

两个新输出未严格胜过当前(验证754, OOF4404)。保留原123，不新增test，不按验证追加网格。

## 嵌套与复用核验

109的9个inner anchor和119的27个innermost anchor按fit/predicted/outer-held索引核对，并重新计算fit-only scaler、增强pair、λ.01目标及梯度；36组均通过。新fit9个inner110的26维残差（使用innermost anchor OOF），再fit9个inner120交互（使用A-fit110 margin），每次只给inner-held B提供父分数。三份B覆盖当前outer-fit后训练链残差，部署在outer-held仍用原outer120。full链fit仅用原120完整train OOF。未将全局OOF直接切给outer-fit训练。

新增fit计数{'inner110': 9, 'inner120': 9, 'outer_chain': 12, 'full_chain': 4}，合计34；worker32.727秒、总4线程、600秒硬限。控制fold/full参数和OOF1e-10复现123，官方validation逐分数复现749/754。纯输入缓存、每题权重/梯度/重复pair、收敛/导出/零残差与重排等接口、源/计划/旧新资产SHA核对。全部解压推理资产≤16MiB，fresh官方validation预测+独立评分≤30秒；参考Xeon未认证。

## 解释边界

消除same-fit margin不等于性能一定提高：inner模型训练量较小，误差和校准也变化。这是原固定两种正则下的具体配方对比，不能单凭某一结果证明乐观偏差是或不是平台期唯一原因。OOF及validation已长期用于开发，历史test汇总已知继续披露。报告全部四条件，不报独立显著或因果效果；本批训练/选择未读取test输入、参考、预测、评分。

统计解释11/11：分层及三折检查Simpson误读；固定题库范围避免Ecological外推；候选筛选分布限定Berkson；不作Collider因果调整；报告分母防base-rate忽略；小变动与适应开发考虑regression-to-mean；四条件全报防survivorship；有限搜索与历史比较披露look-elsewhere；预先计划防forking-paths隐瞒；不作相关即因果或reverse-causality主张。

复现：code目录train_round125_nested_offsets.py，再evaluate_round125_nested_offsets.py；原证据目录拒绝覆盖。训练、索引证明/参数梯度、官方日志与选择保存在runs/round125-nested-offsets和round125-evaluation。
