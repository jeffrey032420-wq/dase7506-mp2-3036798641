# round33-36：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round33-36_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批41条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round33_clean_margin | 4319 | 743 | 1 / 6 | 2.4009 | 2.319 |
| round34_group | 4333 | 746 | 0 / 2 | 1.6491 | 2.341 |
| round35_target_operation | 4318 | 748 | 0 / 0 | 1.8777 | 3.027 |

## 假设、控制与实际结果

### Round33：完整context最大间隔排序

固定1422维fold内context、correct−wrong及反向样本、逐题总权重1，
LinearSVC L2/squared-hinge、C.001/.01/.1×4融合权重，共12项。
与Round20 pointwise残差不同，这是独立完整表示和最大间隔目标。
最佳C.1/融合.5训练4319（39修复/33新错，折+1/−2/+7），纯头4273更弱。
所有折和最终拟合5–11次迭代收敛无warning；验证743（1修复/6新错）。
最大间隔并未解决泛化或提供更强单头，停止继续扩大C。

工程失败必须说明：助手额度错误后根接手同名文件，助手恢复又写入并启动自身任务，
导致并发写入。根运行的结束源码哈希guard触发AssertionError，未进入验证。
当前旧目录完整归档并标为不可使用；保持最终源码与原12超参，在独占新目录完整重跑。
唯一中央入口由[clean索引](code/runs/round33-clean-replay-launch.json)指定，
前后完整源码、全部资产哈希均一致；干净OOF仍4319，严格重排4.33e-15。
旧目录不用于选型或最终模型；重跑不构成额外独立证据，额外计算与失败档案保留。
根的原始较早版本未能由文件归档重建，只保留在会话工具调用记录；不能声称所有版本均已本地保存。

### Round34：组表示与组级二元目标复核

历史Round3已有组级监督，故本轮不作首次声明。不同之处是2066维Embedding mean/max、
textmean与4组属性；None每候选独立无效组，候选成员数不将未知输出当一致答案。
组binary logistic折内scaler、每题权重1，C.01/.1/1×4融合共12项。
8684组、2513有效训练题；最佳C1/.25为4333（35修复/15新错，三折+8/+2/+10）。
全20净增来自答案分歧题，但验证746，无修复且新增2错。纯组权重1仅4318，
说明表示仅提供局部互补。9折与full均收敛，NumPy导出决策误差0。
下一轮固定2066表示比较组softmax目标，不能将当前收益全归于组监督或max池化。
详见[组模型复盘](code/runs/round34-group/LEARNING.md)。

### Round35：目标问句运算监督有训练收益，验证未增加覆盖

沿用Round16教师/候选运算提取，词表与logistic均fitfold内。
target_only、full_plus_target各6融合/置信配置，加3knownness-only控制，共15项。
运算分类61.14%/61.00%，超过旧full56.46%；选full_plus_target/gate0/strength.1，
4318（5修复/0新错，三折均增），超过旧full4317及knownness4315。
其中3修复的旧/新运算都可提取，控制未修复，支持运算匹配有额外训练信号；
另外2修复仍有knownness混杂。验证748、0修复/0新错。
发现末尾find?会覆盖句首How much的目标截断缺陷，保存原实现，另作边界修复实验；
不据验证提高strength，较大强度训练已新增错误。
详见[目标句复盘](code/runs/round35-target-operation/FINDINGS.md)。

### Round36：嵌套boxed数值结论的覆盖检查

严格balanced-box、精确分数或有限+-*/表达式，匹配另一个现有官方终值后才转移。
不修改官方parser，不将百分数/未知变量/单位强行解释。两模式OOF均4313，
无改选、selected=null，未打开验证。工程上能读取新的结论语法，并不意味着
它触及当前选择错误；停止扩展同族权重或把解析覆盖当准确率提升。

## 下一入口

另行计划Round37非线性成对核偏好、Round38固定组表示的softmax损失、
Round39目标句边界修复。各自固定训练网格，不预报未完成收益。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round33-36/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round33-36/frozen-selection.json)，
官方记录见[审计结果](code/runs/round33-36-verification/results.json)，
下一步见[经验](code/runs/round33-36/lessons.json)及[下一实验](code/runs/round33-36/next-experiment.json)。
