# Round123：数字来源与最终计算链消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。21新拟合，4最终输出官方验证。

## 假设与输入审计

12/14等历史已有正确链/数量覆盖，本轮区分最终祖先中的真假运算并学习软修正。仅按训练信息设计和选择。grounding/ancestry/both对359训练错的差异覆盖300/256/308题；覆盖不是可修复数。最终祖先可见算术错的161候选中149错误，但父错仅1题选到此类候选，剩余简单算术空间很小。放宽来源的完整真链3904候选仍有752错误，因此不以真链证明题意正确。

|特征|λ|训练OOF/4755|修复父错/新增错|三折净变化|选中|
|---|---:|---:|---|---|---|
|grounding|0.1|4396|2/2|[-1, -1, 2]|False|
|grounding|0.01|4397|6/5|[1, -2, 2]|True|
|ancestry|0.1|4407|16/5|[4, 2, 5]|True|
|ancestry|0.01|4407|24/13|[3, 4, 4]|False|
|both|0.1|4403|15/8|[-1, 3, 5]|False|
|both|0.01|4404|26/18|[3, 4, 1]|True|

|最终候选|训练OOF|回代|验证/798|分歧/355|单正确/117|修复752错/新增错|KiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|
|round120_question_both|4396|4523|752|309|79|0/0|60.36|2.860|
|round123_grounding_l0p01|4397|4524|752|309|79|0/0|61.59|3.626|
|round123_ancestry_l0p1|4407|4524|749|306|78|1/4|61.87|3.658|
|round123_both_l0p01|4404|4519|754|311|79|5/3|62.01|3.598|

开发选择：round123_both_l0p01，验证754/798。新候选按计划选出，须一次独立冻结test。

## 核验与局限

18outer+3full=21拟合，worker25.092秒，总4线程，600秒硬限。父held分数1e-10复现，纯输入缓存/梯度/重复pair/每题权重/fit-only scaler/收敛/导出/零修正/重排等接口通过。全部资产≤16MiB；fresh validation预测+独立评分≤30秒，参考Xeon未验证。

首次自检在数据/训练前发现通用常数遮蔽前序运算，已修正优先级，失败及原源码保留，完成审计输出新v2目录。same-fit frozen parent offset并非inner-OOF。数值相同不能确定实体，部分公式/文字未知；完整算术真链不能验证题意。六训练配置和四最终验证输出全部保留，未按验证追加网格。长期自适应train/validation及已知历史测试汇总如实披露，未用新test调参或分析个题。

## 统计解释检查11/11

1 Simpson：分歧/单正确及三折同时报告。2 Ecological：只对该固定题库作描述。3 Berkson：候选集筛选分布限制外推。4 Collider：不以条件子集作因果推断。5 Base rate：信号同时报告正确/错误计数和分母。6 Regression to mean：小变动与开发选择不称稳定收益。7 Survivorship：六训练配置含失败全部保留。8 Look-elsewhere：披露有限搜索和历史多次比较，不报显著。9 Forking paths：计划冻结、参数先按OOF选择。10 Correlation/causation与11 Reverse causality：不作因果方向主张。

复现：code目录audit_round123_grounded_chain.py、train_round123_grounded_chain.py，然后训练脚本--evaluate；原输出拒绝覆盖。证据runs/round123-train-audit（首次失败）、round123-train-audit-v2、round123-grounded-chain、round123-evaluation。


# Round123：验证754候选的冻结测试

2026-10-29。训练前规则已固定，按最高validation、同分OOF/资产选择round123_both_l0p01；新test预测前冻结全部代码、参数和选择。

- 官方validation：754/798 = 94.486216%；相对120修复5/新增3。
- 训练OOF：4404/4755，相对120净增8，三折[+3,+4,+1]。
- 官方test：**390/467 = 83.511777%**。
- 全部解压推理资产：63,495字节；总4线程，本机完整fresh test预测+独立评分2.778695秒。
- CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；参考Xeon资格未验证。源/参数/计划/选择记录SHA前后核对通过。
- 研究候选在test前已按train/validation选定；评分后只补总分，未训练、改参、分析test个题或根据test再选模型。其他123版本未测。原120/110/109及原79保留，未创建提交issue。
- 原训练前选择规则通过，无事后门槛更改；已知历史测试汇总与长期自适应开发继续披露。

官方JSON、冻结源/权重、命令、日志、硬件：final_evaluation/round123-test-20261029。
