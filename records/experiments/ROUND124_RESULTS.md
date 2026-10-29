# Round124：最终公式存在性匹配重训练消融

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。16新拟合、4最终输出官方验证。

## 假设与匹配设计

123测试前train-only置零诊断提示移除显式最终公式存在项可能有收益；本轮真正删除mean/max两列后重训练。固定120父、特征提取、折、scaler定义和same-fit offset；ancestry λ.1、both λ.01不扫参。其他链特征仍可编码存在性，因此只检验删除这两列的干预，不能称消除了该信息。

|条件|维度|λ|训练OOF/4755|回代/4755|修复匹配控制/新增|相对控制三折|验证/798|分歧/355|单正确/117|修复754错/新增|KiB|fresh秒|
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|---:|---:|
|ancestry_control|18|0.1|4407|4524|0/0|[0, 0, 0]|749|306|78|2/7|61.90|3.592|
|ancestry_drop_presence|16|0.1|4408|4525|2/1|[1, -1, 1]|749|306|78|2/7|61.84|3.954|
|both_control|24|0.01|4404|4519|0/0|[0, 0, 0]|754|311|79|0/0|62.09|3.684|
|both_drop_presence|22|0.01|4409|4522|9/4|[2, -1, 4]|751|308|79|1/4|62.03|4.361|

## 开发选择

两个新输出均未严格胜过当前(validation754, OOF4404)；保留123，不新增test，不根据验证扩展条件。

## 核验和局限

四条件各3outer+1full=16拟合；worker26.987秒，总4线程，600秒硬限。两个control全部fold/full mean/scale/weight及OOF按1e-10复现123；官方validation逐分数复现749/754。缓存纯输入、fit-only scaler、每题权重、梯度/重复pair、收敛、导出/零残差与重排等接口通过；官方源码、旧父/新资产、计划SHA核对。全部资产≤16MiB，fresh validation预测+独立评分≤30秒，本机不是参考Xeon资格。

训练前诊断依赖长期开发train，验证也长期适应。训练折外与验证变化需分别报告；不把置零未重训的4409当作本轮性能，不报独立显著或因果结论。已知历史test汇总披露；本批拟合/选择未读test输入、参考、预测或评分，未改官方解析和原始数据。

统计解释11/11：报告分层和三折（Simpson）；只对本题库推断（Ecological）；固定筛选分布（Berkson）；无因果调整（Collider）；报告分母（base rate）；小增益/开发选择不称稳定（regression to mean）；四输出全报（survivorship）；有限搜索及历史多比较披露（look-elsewhere）；计划冻结（forking paths）；不作因果及反向因果主张。

复现：code目录train_round124_presence_ablation.py，再加--evaluate。原证据目录拒绝覆盖。证据runs/round124-presence-ablation、round124-evaluation。
