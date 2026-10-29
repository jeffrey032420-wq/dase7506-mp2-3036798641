# Round104：固定语义权重的数值校正

Material Passport: academic-research-suite / experiment-agent；2026-10-28 UTC+8；VERIFIED_LOCAL_VALIDATION。

**四个固定输出最高748/798，未超过749/798（93.8596%），保留Round79。** 四个输出在本批拟合和验证前固定：两项无新拟合的R103组件消融，两项14维残差ridge拟合。没有新OOF、外部数据或预训练权重。

## TRAIN诊断与假设

R103同时改变旧语义系数与新增数值系数。固定父79的TRAIN回代为4406/4755。zero-fit组件预检发现，仅保留新增数值项可减少联合模型的部分误伤，但alpha.3的正确总数反而低于联合模型。因此提出有限假设：固定旧语义系数，可能保留部分数值收益并减少系数重分配的损害。以下均为同一TRAIN回代，不是OOF或独立泛化证据。

|新增alpha|R103联合回代|联合新错|仅新增数值回代|仅新增修复/新错|
|---|---:|---:|---:|---:|
|0.3|4408|13|4407|7/6|
|3|4407|7|4408|4/2|

两个组件均满足修复≥2、比联合版本少新增错误，且至少一个达到父模型并严格胜过对应联合版本。该预检资格用于提出本批固定实验，不宣称已改善泛化；四个输出生成后不再按回代筛选。

## 四项受控输出与公式

`joint_new_only`保留R103对应alpha的新增numeric14系数，舍弃其旧系数增量，不做新拟合。`anchored`固定父semantic1422系数w，拟合成对残差目标1-(x_good-x_bad)w；同一2513个有正负候选的TRAIN题等权，解(Gtt+alpha I)v=bt-Gxt.T w，alpha固定.3/3。

两种模式均保持原父base mean/std、投影、最终semantic mean/std与旧权重完全不变。numeric14新增mean/std与R103 donor逐位精确一致。nongate使用父语义分数加数值校正，gate内原numeric alpha1分数不变，最后只应用一次原R11格式迁移。复用冻结的method_round103_semantic_evidence.py，无新推理编译器。

|模式|alpha|TRAIN回代/4755|回代修复/新错|新系数拟合|残差正规方程误差|
|---|---:|---:|---:|---|---:|
|joint_new_only|0.3|4407|7/6|False|0.02133|
|joint_new_only|3|4408|4/2|False|0.01557|
|anchored|0.3|4408|5/3|True|2.776e-17|
|anchored|3|4408|4/2|True|5.551e-17|

只有anchored是该残差目标的优化解，故仅这两项要求残差正规方程误差≤1e-8；组件消融的该数值仅作描述，不冒充已优化目标。小型显式加权pair残差解对Gram解、旧semantic重建与零新增完整父复现均≤1e-8。记录2次新系数拟合、2项无拟合组件导出及1次旧控制求解；一个CPU线程，训练/导出/控制49.134秒，硬预算600秒。

## 完整验证与解释

|模式|alpha|验证/798|修复/新错|改变选择数|完整解压MiB|fresh预测+独立评分秒|
|---|---:|---:|---:|---:|---:|---:|
|joint_new_only|0.3|748|0/1|22|1.6129|2.096|
|joint_new_only|3|748|0/1|9|1.6129|2.029|
|anchored|0.3|748|0/1|17|1.6129|2.022|
|anchored|3|748|0/1|9|1.6129|2.105|

最佳新输出anchored; numeric14 alpha=0.3; old semantic weight frozen，验证修复0、新增错误1。TRAIN组件消融减少误伤没有在本批配置中转化为验证净增；固定语义权重本身不能保证新的数值校正可靠。 这些结果不证明模型达到上限，也不能从回代组件变化直接推出独立因果或泛化结论。

全部输出通过完整TRAIN缓存/重载、old_weight精确冻结、gate保持、53题26gate/27nongate严格候选重排（rtol=atol=1e-8）、问题顺序、bank大小、新ID、empty与Python int选择控制。全部嵌套推理资产≤16MiB，四线程本机完整验证预测加独立评分≤30秒；这不是参考CPU完整测试时间认证。

验证反复用于自适应开发，选型分数可能乐观，不能当独立泛化或显著性证据。未读取、哈希或运行测试输入/参考/预测/分数，未公开提交。原模型、R103 donors、历史来源及官方文件均保持；旧PDF、ZIP和submission_ready保留历史快照。

## 复现与下一步

独立工作副本还原本批incumbent-pointer.json（latest103），保留官方数据、父79、两份R103 numeric donors、预检源及历史证据。预检result和本批training/evaluation/verification生成目录应不存在。先从code工作目录用runpy执行runs/round104-preflight/audit.py，再train_round104_fixed_semantic.py；所有训练停止后evaluate_round104.py，最后finalize_round104.py。完整预检/候选/失败记录均保留，不覆盖原冻结批次。

后续先根据真实修复与新错判断新增信息是否可迁移；若本批仍无净增，不能只凭回代减少误伤继续扩大同一alpha或融合网格。

证据：code/runs/round104-preflight/result.json、code/runs/round104-fixed-semantic/result.json、code/runs/round104-evaluation/results.json、code/runs/round104-verification/results.json。
