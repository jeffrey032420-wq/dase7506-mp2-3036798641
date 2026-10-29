# 第23–25轮：题目程序、跨候选交互与随机森林

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION；未使用测试。
- Version Label: rounds23_25_results_v1。

**三类新训练方法均未超过748/798，保留Round11。** 本批4＋8＋4=16条训练配置，
三个训练预选最佳输出全部通过官方、预算、接口与完整性审计，但均降低验证准确率。
测试输入、参考、预测、分数均未访问；没有据验证继续调整本批权重。

| 输出 | 训练OOF /4755 | 验证 /798 | 修复 / 新错（对Round11） | 全解压资产 MiB | 预测＋评分秒 |
|---|---:|---:|---:|---:|---:|
| round23_programsearch | 4321 | 747 | 0 / 1 | 1.6988 | 5.651 |
| round24_deepsets | 4344 | 743 | 7 / 12 | 1.7417 | 2.504 |
| round25_extratrees | 4321 | 743 | 0 / 5 | 1.7273 | 4.597 |

## 1. 题目数字短程序：独立信号，仍不能证明正确

候选推理文本仅用于官方终值解析；新特征只使用题目数字到候选终值的2/3叶+-*/程序，
不同于Round18候选推理中的等式图。固定最多6个不同数字、两种括号、无外部常数；
浮点向量化提名后每次命中用Fraction精确复核。超界/零除/未知明确分开，
“此语法不可达”不等于数学错误。四条固定树/融合配置，选7叶100轮、blend0.1，
训练4321，11修复/3新错，三折均正增；验证747，0修复/1新错。

4095题可搜索，15650候选已知、6220可达。正确候选可达率39.17%，错误41.90%，
所以可达本身不是正确性的单调证据。审计发现一些纠错反而是识别浅式偶然可达的错误，
新错则涉及缺60分钟、12个月和英文three。下一轮固定比较词数和题目明确提示的常数，
同时测新正确支持与新偶然匹配；不盲目增加叶子。
详见[程序分支复盘](code/runs/round23-programsearch/FINDINGS.md)。

## 2. 神经比较：交互活跃，但验证新增错误更多

从头学习共享tanh候选编码，以均值、乘积和排除自身的max比较四候选，确保数学结构重排等变。
保留rawlinear支路；width16/32×L2.01/.1×strength.1/.25，共8项，固定40epochs。
每折标准化和context offset仅用拟合题，held标签不进入训练。矩阵L2按元素平均以避免塌缩。
训练最佳width32/.1/.25为4344（74修复/43新错），各折+8/+6/+17。
改变一个候选后其余候选相对分数std.174，交互确实起作用；
但相对历史线性4332的提升同时引入了非线性，不能全归于跨候选比较。
全训练loss约.002也不是泛化证据。验证743，7修复/12新错。
下一轮用同宽pointwise tanh隔离交互，并固定检查较早训练点。

独立只读审计发现原float32推理不满足严格重排容差：全训练3283个分数超限，
原训练检查只指定atol，默认宽松rtol掩盖了问题。先归档原始方法、结果与哈希，
再仅将推理残差计算升float64。全部权重/config与原冻结OOF不变、未重训；
4755题训练选择0变化，严格重排最大差8.88e-16。
中央验证在修复与新哈希冻结后才开始；原OOF没有重算，这一点如实保留。
详见[精度修复](code/runs/round24-deepsets/precision-repair.json)和
[神经训练报告](code/runs/round24-deepsets/TRAIN_ONLY_REPORT.md)。

## 3. 随机阈值森林：更强正则不自动提升

固定compact256结构特征，32棵ExtraTrees，depth4/8，leaf60，maxfeatures.7，
binary候选目标，不把基线分数输入新模型。融合.1/.25共4条OOF；
depth8/.1为4321，20修复/12新错，三折+2/+4/+2。纯森林4188弱于原模型，
提高融合反而4312。验证743，无修复并新增5错，说明不同学习器本身不是足够的新证据。
逐折与最终19020候选导出的NumPy节点预测和sklearn精确一致，推理无需sklearn/pickle。
资产原记录是压缩文件大小，中央已按NPZ展开成员保守计算；全部仍低于16MiB。
下一轮只改变目标为y减本题y均值，保留全正确题与其它参数，隔离目标选择影响。
详见[森林复盘](code/runs/round25-extratrees/LEARNING.md)。

## 4. 审计、复现与下一入口

平台Intel Core i5-11400H，Python3.12.14、NumPy2.5.3、LightGBM4.7.0、
scikit-learn1.9.1。训练各1线程，正式fresh预测＋独立评分在训练停止后依次4总线程；
所有嵌套原模型、权重/词表/统计/配置及NPZ展开尺寸均计入16MiB。
全部通过新ID、1/7/23bank、候选重排、题序、空输入及合法整数检查。
本地完整验证计时不替代参考CPU完整测试资格；官方工具/数据与历史模型源码哈希保留。

全部训练配置见[all-training.csv](code/runs/round23-25/all-training.csv)，
预验证冻结见[frozen-selection.json](code/runs/round23-25/frozen-selection.json)，
官方记录见[results.json](code/runs/round23-25-verification/results.json)。
OOF与验证已多轮复用，均为开发证据，不能将训练高分视作独立可靠性证明。

后续Round26词数/常数、Round27非线性/早期训练点、Round28中心化目标森林已单独计划，
Round29另检验官方不可解析终值的候选资格。各自结果未完成前不宣称提升。
每次事实→机制→下一最小动作见[lessons.json](code/runs/round23-25/lessons.json)。
