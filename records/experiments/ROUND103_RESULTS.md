# Round103：语义分支联合使用既有数值与答案组证据

Material Passport: academic-research-suite / experiment-agent；2026-10-28 UTC+8；VERIFIED_LOCAL_VALIDATION。

**六个固定新输出最高748/798，未超过749/798（93.8596%），保留Round79。** 六个配置在拟合和本批验证前固定，全部仅使用给定TRAIN拟合。没有新增OOF、训练回代筛选、外部数据或预训练权重。

## 历史查重与实验假设

R7已研究semantic1422加numeric14/answer_context386，但使用全坐标统一alpha的bare ranker；R85只替换算术门控的numeric头，新增特征不作用nongate。R62使用结构/Embedding树，R89只改原1422内部正则，R97/98/100新增的是其他块。本轮是已有特征在语义分支的未评估组合，不是新特征发明。

假设是固定旧1422维L2=.3，同时单独收缩新增块，可能避免统一正则或仅门控组合的限制。numeric14固定新增L2=.3/3；answer_context386固定3/30；both400固定3/30。保留全部14数值项，以观察checked/true等证据，不把前六项在nongate全部当作常数。

## 拟合前TRAIN覆盖

原79的完整TRAIN回代为4406/4755，nongate回代错题316道。新增块能区分父选择与至少一个正确替代候选的错题数如下；这是拟合机会，不是已学会或泛化证明。每个family超过预定至少10题门槛，未据此扩充参数。

|新增块|新增维度|nongate回代错题有可辨别正确替代项|本批最佳验证/798|
|---|---:|---:|---:|
|numeric|14|267|748|
|answer_context|386|316|744|
|both|400|316|743|

## 联合目标与实现控制

保留原父模型的base mean/std、随机投影和最终semantic mean/std，只有新增块mean/std从所有TRAIN候选拟合；answer_context接收原transform输出，未将最终标准化后的1422再次投影。按2513个有正负候选的题等权拟合成对单位间隔平方目标。

精确Schur补联合解同时更新旧/新权重，非固定父残差拟合。旧块alpha.3重建、零新增权重完整父复现、小型Schur对直接联合解、全部实际正规方程残差≤1e-8均通过。numeric gate复用同一解析器has_false，gate内原numeric alpha1分数保持；合并后只应用一次原R11格式迁移。

|新增块|新增alpha|TRAIN回代/4755|回代修复/新增错|旧权重改变量L2|新增权重L2|
|---|---:|---:|---:|---:|---:|
|numeric|0.3|4408|15/13|0.0377411|0.057169|
|numeric|3|4407|8/7|0.0273201|0.0252886|
|answer_context|3|4386|12/32|0.101146|0.0403212|
|answer_context|30|4395|8/19|0.047128|0.011145|
|both|3|4386|16/36|0.107285|0.0468466|
|both|30|4399|9/16|0.0488905|0.0130275|

TRAIN回代仅作描述，无OOF或独立泛化含义；全部六个输出均进入官方验证。一个CPU线程，六次候选Schur求解和一个旧块控制求解，拟合/导出/控制总计54.507秒，600秒硬子进程预算。所有数据统计、权重、配置和嵌套父资产均显式保存。

## 完整官方验证与资源

|新增块|新增alpha|验证/798|修复/新增错|改变选择数|完整解压MiB|fresh预测+独立评分秒|
|---|---:|---:|---:|---:|---:|---:|
|numeric|0.3|747|1/3|33|1.6128|1.946|
|numeric|3|748|1/2|23|1.6128|1.925|
|answer_context|3|744|1/6|64|1.6213|1.998|
|answer_context|30|743|0/6|38|1.6213|2.080|
|both|3|743|1/7|68|1.6216|2.004|
|both|30|743|0/6|39|1.6216|2.012|

每个输出通过53题26gate/27nongate的严格候选重排（rtol=atol=1e-8）、问题顺序、可变bank、新ID、empty、Python int选择、完整TRAIN缓存/导出一致和父gate保持。完整解压资产均≤16MiB，四线程本机完整验证预测加独立评分均≤30秒。这不认证参考CPU完整测试时间。

最佳新输出为numeric 14D; new alpha=3; old alpha=.3，验证修复1、新增错误2。即使TRAIN中存在可辨别正确替代项，这组特征/正则组合也未产生验证净增；表示覆盖不能替代可迁移排序证据。 这些结果不证明模型达到上限，也不能将变化唯一归因于数值语义；两块联合拟合会同时改变旧系数。

验证集反复用于自适应开发，选出的准确率可能乐观，不能称为独立泛化或显著性结果。未读取、哈希或运行测试输入/参考/预测/分数；没有公开提交。原模型、官方文件与所有历史来源均核验；旧PDF、ZIP、submission_ready作为历史快照保持，不自动更新。

## 复现与下一步

在独立工作副本还原本批incumbent-pointer.json（latest102）；保留官方数据、原79父checkpoint、预检源runs/round103-preflight/audit.py，以及全部历史证据。预检result.json和本批训练/evaluation/verification生成目录应不存在。先用runpy从code工作目录执行预检源，再运行train_round103_semantic_evidence.py；等所有训练停止后运行evaluate_round103.py，最后finalize_round103.py。按预检同样的TRAIN输入与固定六项配置复现，不更换折或依据测试选型。

后续应先区分可迁移的新排序证据与单纯增加训练拟合；保留每个family的修复/新增错误及负结果。若本批没有净增，不能仅凭高覆盖或更好的回代继续扩大正则/融合网格。

证据：code/runs/round103-preflight/result.json、code/runs/round103-semantic-evidence/result.json、code/runs/round103-evaluation/results.json、code/runs/round103-verification/results.json。
