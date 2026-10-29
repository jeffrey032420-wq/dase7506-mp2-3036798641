# Round124学习记录：固定系数诊断与重新拟合的区别

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16拟合、4官方验证，2新候选+2严格控制；未新增test。

## 本轮结果

|方法|原训练OOF→删列后|相对原三折|原验证→删列后|
|---|---|---|---|
|ancestry，λ.1|4407→4408|+1/-1/+1|749→749|
|both，λ.01|4404→4409|+2/-1/+4|754→751|

组合删列版在训练OOF修复9题、增加4错，但官方验证只修复原754的一题、增加4错。原123研究模型754/798保留，两个新版本未通过预先开发排序规则，未新增测试。删除的只是显式final_has_scalar_equation的mean/max，其他特征仍可能包含存在性信息，不称完全移除此信息。

## 学到了什么

1. 123测试前的固定系数置零诊断只能形成待验证假设。真正重训练后ancestry OOF是4408，不能拿之前未重训的4409当作本轮结果；组合重训练恰巧也为4409，属于不同模型。
2. 这项删除在训练划分有净收益，在验证未兑现；训练三折中也有一折下降。不能把该项简单认定为普遍有害，继续按验证删除小特征会增加自适应选择风险。
3. 两个控制fold/full mean/scale/weight、OOF和官方validation分数均严格复现，因而本次差异不是父模型、parser或不同正则的混杂。

## 补充训练诊断：父模型margin的乐观程度

新残差目前用same-fit frozen parent margin训练。以下只看train，没有新拟合、validation或test访问；比较描述当前差距，不证明它造成了验证下降。

|父120分数来源|题数|正确数|准确率%|每题归一pair logloss|平均pair margin|
|---|---:|---:|---:|---:|---:|
|full same-fit|4755|4523|95.1209|0.206198|2.949183|
|saved outer OOF|4755|4396|92.4501|0.302900|2.727199|
|fold0 same_fit|3170|3049|96.1830|0.181025|3.105511|
|fold0 outer_held|1585|1463|92.3028|0.309009|2.726168|
|fold1 same_fit|3170|3049|96.1830|0.179793|3.123739|
|fold1 outer_held|1585|1461|92.1767|0.305993|2.647429|
|fold2 same_fit|3170|3045|96.0568|0.183247|3.045271|
|fold2 outer_held|1585|1472|92.8707|0.293763|2.806761|

## 下一步可检验方向

固定原123保留全部特征的ancestry/both及各自正则，对比same-fit margin和真正inner-OOF父margin。只改变修正训练时看到的父分数，先做匹配训练折外比较，再冻结候选官方验证。这是由训练margin诊断形成的待检验假设，尚未执行，不声称已解决OOF/验证分歧。

**实现约束：**不能直接把全train保存的parent OOF抽出outer-fit行用于该折残差训练，因为其他折parent可能训练过当前outer-held。需要在每个outer-fit内部重新拟合或严格核对可复用的inner父模型及其scaler/训练索引，完整父120的各层也须排除held。最终full fit可使用父120对完整train的既有OOF，但新残差的外层OOF仍需上述嵌套过程。

## 资源与完整性

4线程，16拟合worker26.987秒；fresh官方validation预测+独立评分最慢4.361秒；全部推理资产最大63,577字节（62.09KiB）。满足本机30秒/16MiB约束，参考Xeon未认证。源/计划/父新资产SHA、缓存、每题权重、梯度/重复pair、导出/零修正、重排/题序/新ID/变batch等通过；旧123/120及原79提交字段保留。

长期自适应train/validation及已知历史测试汇总披露；本批没有test输入/预测/评分访问或测试驱动选择。统计解释11/11见ROUND124_RESULTS.md；只作描述，无显著性或唯一因果判断。

完整结果ROUND124_RESULTS.md；机器闭环code/runs/round124-closeout/result.json；训练margin诊断code/runs/round124-margin-gap/result.json。
