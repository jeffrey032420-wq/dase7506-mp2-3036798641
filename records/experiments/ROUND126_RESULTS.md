# Round126：固定父模型的组级softmax损失

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；16新拟合、4最终输出官方验证。

## 假设与标签核实

训练4755题按数值分组后均只有一个正确组；776题有多个错误组。pair损失将一题的权重平均分给各错误组；组级CE令所有错误组共同竞争。本批固定原123的ancestry/both、λ.1/.01、父120及same-fit offset，仅切换目标。它与112在原始结构上切换uniform/mass不同，不声称首次研究softmax。不引入候选支持度log先验。两种目标显式λ相同，不声称有效曲率等同。

|条件|维度|λ|训练OOF/4755|回代/4755|修复匹配控制/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry_pair|18|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.94|3.718|
|ancestry_group_ce|18|0.1|4405|4521|3/5|[-2, -2, 2]|749|306|78|1/6|61.95|3.641|
|both_pair|24|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.12|3.606|
|both_group_ce|24|0.01|4406|4518|5/3|[1, -1, 2]|751|308|78|0/3|62.13|3.646|

## 开发选择

新组级CE输出均未严格胜过当前(validation754, OOF4404)；保留123，不新增test，不按验证扩展网格。

## 核验与复现

四条件各3outer+1full=16拟合，worker27.046秒、4线程、600秒硬限。pair控制全部fold/full参数和OOF1e-10复现123；官方validation逐分数复现749/754。CE解析梯度、重复题归一、两组时与pair损失等价、组重排通过；每题权重/fit-only scaler/收敛/导出/零残差与候选重排等接口、源/旧新资产/计划SHA通过。全部推理资产≤16MiB，fresh完整validation预测+独立评分≤30秒；参考Xeon未认证。

生成器只创建新126驱动，未改124；首次两次替换次数保护在生成/数据读取前拒绝执行，修正计数并保存失败及源快照，无拟合或验证重试。精确替换和AST检查、模板/生成SHA保留于code/runs/round126-source-preparation.json。复现先prepare_round126_experiment.py，再train_round126_group_loss.py及其--evaluate；原目录拒绝覆盖。

## 解释边界

本实验切换优化目标，不增加输入数学/语义信息。若准确率不增，不能由此证明所有listwise损失无效；若有小增益，也不是独立确认。四条件全部披露，长期train/validation自适应和已知历史test汇总继续披露，不使用test个题或总分训练/选择。

统计解释11/11：同时报告分层/三折防Simpson；限定题库防Ecological；注意候选选择分布Berkson；无Collider因果调整；有分母防base-rate忽略；考虑小变化和regression-to-mean；全报防survivorship；披露look-elsewhere和forking-paths；不作相关即因果或reverse-causality主张。
