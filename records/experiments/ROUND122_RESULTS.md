# Round122：答案组Embedding子集稳定性

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。10新拟合，2最终输出官方验证。

## 假设与设计

在完整120父模型上，学习相同答案组的非空子集Embedding评分稳定性。支持度/支持比例/答案组数固定为完整组，保留Embedding均值与离散度变化。六维为delta min/max/mean/std、singleton std及删一成员std。单例组全零。不是重做108训练增强。train覆盖：父359错中247题有多成员组，112题全单例，后者新增特征不能改变排序。只按train OOF从三档λ选一档，随后官方验证。

|λ|训练OOF/4755|修复父错/新增错|三折净变化|选中|
|---|---:|---|---|---|
|0.1|4392|2/6|[0, -3, -1]|False|
|0.01|4393|3/6|[0, -2, -1]|True|
|0.001|4393|4/7|[1, -2, -2]|False|

|最终候选|训练OOF|回代|验证/798|分歧/355|单正确/117|修复752错/新增错|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|4396|4523|752|309|79|0/0|60.36|2.757|
|round122_stability_l0p01|4393|4527|752|309|79|0/0|61.47|3.213|

开发选择：round120_question_both，验证752/798。保留原120，未新增test。

## 核验与局限

9outer+1full=10拟合，worker24.157秒，总4线程，600秒硬限。父held分数严格复现，梯度/重复pair/每题权重/fit-only scaler/收敛/导出/零修正/单例不改排序/重排等接口通过。全部资产≤16MiB；fresh validation预测+独立评分≤30秒，参考Xeon未验证。

same-fit frozen parent offset并非inner-OOF offset。子集信息只覆盖多成员组，且与旧离散度相关；覆盖不等于能够识别正确答案。全部3训练配置与2验证输出保留，不按验证追加网格。长期自适应开发、历史测试汇总已知如实披露，新测试不用于训练/选择。统计解释11/11检查：分层及三折防Simpson误读；不做生态/筛选/碰撞因果推断；报告分母；小增益与回归均值谨慎；全部失败保留；披露多重搜索与路径；不声称因果或反向因果。只作描述，不报独立显著性。

复现：code目录train_round122_subset_robustness.py，然后同脚本--evaluate；存在输出目录则拒绝覆盖。证据runs/round122-coverage、round122-subset-robustness、round122-evaluation。
