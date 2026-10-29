# Round137：模块校准与联合更新

## Material Passport

academic-research-suite / experiment-agent；20次拟合、6个训练配置、2个train选λ最终候选、3次官方validation。计划和首次审计开始日期2026-10-29；精确过程时间见命令/冻结记录。

|配置|OOF/4755|修复/新增|三折净变化|选为最终输出|
|---|---:|---|---|---|
|round137_mix_l0p01|4401|11/14|[-1, -2, 0]|False|
|round137_mix_l0p1|4405|9/8|[-2, 0, 3]|False|
|round137_mix_l1p0|4406|4/2|[-1, 1, 2]|True|
|round137_joint_l0p01|4383|31/52|[-4, -17, 0]|False|
|round137_joint_l0p1|4398|17/23|[0, -8, 2]|False|
|round137_joint_l1p0|4406|9/7|[-1, 0, 3]|True|

|最终版本|OOF/4755|回代/4755|validation/798|验证修复/新增|KiB|fresh秒|
|---|---:|---:|---:|---|---:|---:|
|round123_both_l0p01|4404|4519|754|0/0|62.01|3.768|
|round137_mix_l1p0|4406|4517|753|0/1|60.98|3.041|
|round137_joint_l1p0|4406|4519|752|0/2|60.99|3.121|

开发选择：保留123，先于新test。两候选会统一冻结后各一次test；本评价未运行test。

四块输入与123保持，mix训练4个系数偏移，joint同时更新5180个已有权重；λ均只在train OOF选，两种正则几何不同，不将差异全部归因于参数数量。旧fit-only中心/尺度逐fold重建held1e-10，零更新和独立导出检查通过。长期自适应train/validation和已知test汇总披露，OOF选λ后分数是开发指标。

全部原始源/父资产/官方工具/数据保持，候选完整接口及所有资产<=16MiB、完整fresh预测+独立评分<=30秒本机检查通过，4总线程；参考Xeon未认证。训练600秒硬限，验证全部输出而不按中途结果改名单/参数。复现audit_round137_joint_retrain.py → train_round137_joint_retrain.py → evaluate_round137_joint_retrain.py；原输出拒绝覆盖。


# Round137：两个最终版本的冻结测试

## Material Passport

两个版本在第一项新test前统一冻结，各一次完整fresh预测与独立官方评分，无新拟合、test个题分析或按test选型。

|版本|训练OOF/4755|验证/798|test/467|test准确率|完整KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---:|
|round137_mix_l1p0|4406|753|392|83.9400%|60.98|2.237|
|round137_joint_l1p0|4406|752|395|84.5824%|60.99|2.331|

test前开发选择：保留123；不按上述test分数更换。测试已经多次暴露，不能作独立最终估计。test只用于冻结评价，不用于训练、调参、选型或规则。

完整冻结源/资产/命令/日志/官方JSON见final_evaluation/round137-all-test-20261030。4总CPU线程、全部递归资产<=16MiB、完整预测+评分<=30秒，本机不代替参考Xeon认证；无公开提交/issue。
