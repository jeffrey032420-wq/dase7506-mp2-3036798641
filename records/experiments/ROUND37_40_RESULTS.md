# round37-40：训练、消融与冻结验证

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；测试未访问。
- Version Label: round37-40_v1。

**本批没有超过748/798（93.7343%），保留Round11。** 所有配置先用训练OOF选型、冻结，再集中比较合格输出。
本批30条训练配置记录，包含控制；未合格分支保留，不为其另开验证。

| 输出 | OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 新预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round37_pair_kernel | 4326 | 743 | 0 / 5 | 8.9122 | 4.316 |
| round38_group_softmax | 4350 | 746 | 6 / 8 | 1.6493 | 2.426 |

## 训练假设、对照与失败归因

### Round37：非线性成对偏好仍未迁移

1038维输入折内标准化、题内中心化、PCA64白化后，对correct−wrong与反向差训练RBF SVC。
与Round6点式RBF回归不同，新模型学习成对偏好，显式反对称后对其余3候选求和。
固定C.1/1、gamma1/64×融合.1/.25/.5，共6项；每题双向pair总权重1。
最佳C1/.1训练4326，19修复/6新错，各折+4/+3/+6；提高融合反而新增更多错误。
完整支持向量、dual、PCA/scaler与原模型共9,345,107字节。最终13683SV、10820迭代，
全部折及full收敛；NumPy导出误差8.97e-14，严格重排7.11e-15。
fit子进程由remaining-budget强制timeout，scoring逐batch检查同一600s上限，总90.65s。
验证743，无修复且新增5错。三折正增不能保证验证可靠，停止C/权重扩展。
详见[核偏好复盘](code/runs/round37-pair-kernel/TRAIN_ONLY_REPORT.md)。

### Round38：固定组表示时softmax提高OOF，验证仍下降

保持Round34全部2066维表示、分组与scaler逐值不变，仅改为题内正确组softmax平均logloss，
L2 alpha.001/.01/.1×4融合，共12项。最佳alpha.01/.5训练4350，
78修复/41新错，各折+13/+10/+14，超过原binary最佳4333。
同融合.5对照是4325→4350；验证746，修复6却新增8，净−2。
全部OOF净增在答案分歧子集，说明目标更适合开发排序，但不证明独立泛化提升。
9折/full优化均达到SciPy终止条件；full按objective相对下降终止，最大梯度1.63e-4，
不能声称达到梯度1e-6。梯度检查误差1.34e-11，严格重排3.97e-15。
有效C/alpha正则并非完全匹配，仍不能将所有差异单独归因loss。
详见[组损失复盘](code/runs/round38-group-softmax/LEARNING.md)。

### Round39：目标句边界修正没有选择收益

固定新边界规则，6项新配置与6项旧控制匹配。81题目标改变，分类61.00%→61.14%，
但受影响73个已知教师题准确数41→41；全局+6来自未变输入题的重新拟合，
不能归因局部修复。所有6项argmax逐题与旧控制完全一致，best4318，selected=null。
3472的find?截断修正成功，却把Mr./Mrs./Ms.当句末，引入Smith pay?等3个新分类错误；
另3个受影响题改善，局部净0。失败边界保留，不因总分类微升继续部署。
详见[边界复盘](code/runs/round39-target-boundary/FINDINGS.md)。

### Round40：明确区分人工交集与自动解析覆盖

仅训练数据只读审计：时间135题/10当前错、百分比59题/7错、money331题/34错；
合并523题、50个当前错，每个均有官方正确替代。保存所有题目/候选/参考全文。
没有拟合、没有OOF选择改变、没有模型/验证输出。人工提出最多两个封闭关系：
预算余额反推未知商品价（1095/1884）与统一数量单位的单商品净利润（4132/4300）。
每项列出正确对照与必须拒绝的多未知、目标不符、部分出售、分段售价等。
人工能纠正两题不等于实现后的parser能识别两题；下一轮先固定语法与拒绝条件再审计全训练。
时间/百分比族未发现足够小可靠的统一schema，停止扩展。
详见[审计](code/runs/round40-typed-audit/FINDINGS.md)。

## 下一入口

另作预算/利润角色解析实验，以及严格嵌套OOF baseline offset的残差训练。
后者检验旧合法in-sample offset是否导致训练分数过自信；是未验证假设，不能预报成功。


## 完整性、复现与证据边界

全部输出通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、题序、空输入、
16MiB完整解压资产和本地fresh预测＋独立评分共享30秒检查。原工具/数据和历史模型源码哈希保留。
训练各1线程；正式审计在其它训练停止后顺序运行，总线程4。Intel Core i5-11400H，
Python3.12.14、NumPy2.5.3；各分支额外依赖见复盘/REPRODUCE.md。
本地完整验证计时不证明参考Xeon Platinum8457C完整测试资格。
所有OOF和多轮复用验证均为开发证据，不能声称无偏泛化或统计显著。
测试输入、标签、预测与成绩均未用于开发。

全部配置见[训练表](code/runs/round37-40/all-training.csv)，
预验证选择/哈希见[冻结记录](code/runs/round37-40/frozen-selection.json)，
官方记录见[审计结果](code/runs/round37-40-verification/results.json)，
下一步见[经验](code/runs/round37-40/lessons.json)及[下一实验](code/runs/round37-40/next-experiment.json)。
