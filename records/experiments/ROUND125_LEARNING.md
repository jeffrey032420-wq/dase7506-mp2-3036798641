# Round125学习记录：嵌套margin不是当前提升的充分条件

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；34新拟合、36个核验复用anchor、4官方验证，未新增test。

|特征|same-fit OOF→nested OOF|相对控制三折|same-fit验证→nested验证|
|---|---|---|---|
|ancestry18 λ.1|4407→4406|-2/+1/0|749→750|
|both24 λ.01|4404→4399|+1/-6/0|754→754|

组合nested与原754在validation上选择完全相同，OOF较低；ancestry虽验证增1仍低于当前754。按预先规则保留原123研究候选，不新增test。

## 对假设的更新

训练margin乐观差距确实存在，但在此固定特征/正则下替换为真正嵌套OOF没有产生更好的最终开发候选。它不是当前平台期已经证实的唯一原因，也不能由此推断所有交叉拟合无用。
inner父模型只训练约2113题，比outer父3170题更少，分数质量、噪声及校准也会变化；本批没有分离这几个因素。不根据验证继续扫描offset混合系数。

## 完整嵌套与核验

每outer-fit内部3个inner分区，inner110残差的基础margin再来自3个innermost anchor；9个inner110与9个inner120均新拟合。链条层四条件12outer+4full=16拟合，共34。
36个已保存anchor逐个核对fit/held索引、当前fit-only scaler、增强pair、λ.01目标与梯度；119的22维残差没有被错误复用到110的26维残差。所有父层排除outer-held。
same-fit控制全部fold/full参数和OOF1e-10复现123，validation逐分数复现749/754。原始数据/parser/scorer及原父参数未改。

## 后续研究要求

下一步先核实组级标签结构及当前pair损失的权重分配，再考虑与组级softmax排序损失匹配比较。每题可能有多个正确候选，但同数值答案分组后可能只有一个正确组，不能把“多正确候选”和“多正确组”混为一谈。此处尚未进行新损失拟合。

## 资源与限制

4线程，worker32.727秒、600秒硬限；官方fresh validation预测+独立评分最慢3.657秒；全部资产最大63,400字节。满足本机30秒/16MiB，参考Xeon未认证。
长期自适应开发、已知历史测试汇总继续披露；本批未读取test输入/参考/预测/评分。原123/120及原79提交字段保留，未创建GitHub issue。统计解释11/11及全部结果见ROUND125_RESULTS.md；不作独立显著或因果结论。
