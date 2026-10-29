# 第20–22轮：集合损失、特征消融与局部近邻

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent。
- Origin Date: 2026-10-21。
- Verification Status: TRAIN_OOF＋ONE_FROZEN_LOCAL_VALIDATION，未使用测试。
- Version Label: rounds20_22_results_v1。

**当前最佳仍为748/798（93.7343%），Round11保留。** 本批24条固定训练配置；
只有Round20预选赢者获准中央验证，得748（修复1／新增1），未获得净提升。
Round21和22按各自预定门槛停止，没有为它们读取验证或测试。

## 1. Round20：减少新错，也减少了修复

假设来自Round17：39个训练新增错误中31个在多正确候选题上。
固定uniform-correct softmax CE和逐题归一的pairwise logistic两种损失，
每种decay0.01/0.1、strength0.1/0.25，40epochs，合计8配置。
折内context offset与标准化保护held标签不进入拟合；原算术gate与格式transfer保留。
两族最好同为4322（20修复/11新错）；按较少改选，选pairwise logistic进入验证。
三折净增+2/+2/+5；单线程32.48秒，包括两族全训练重拟合与导出。

公平对照使用相同strength0.25：原any-correct4332，37修复/18新错；
pairwise4322，20修复/11新错。多正确组新错14→4，但修复37→20，总体下降10。
因此“减少新错”不等于总体更好。按可观察答案一致票数分层也没有支持直接损失切换，
本轮不追加一致性门槛搜索。分析见[训练复盘](code/runs/round20-setloss/TRAIN_ONLY_REPORT.md)。

中央预验证冻结后，官方得748/798，修复1／新错1。
全解压推理资产1692423字节（1.6140MiB），
全新预测进程＋独立评分2.287秒，4总线程。
官方/接口/完整性检查通过；本地完整验证计时不代表参考CPU完整测试资格。

## 2. Round21：哪些结构特征真正贡献了OOF

固定LambdaRank7叶100轮、原其余参数；五表示各3折，仅融合0.1/0.25，10条结果。
删组同时删除该组四套候选间相对变换；full重拟合与Round18相同头逐值完全一致。

| 表示 | 维数 | OOF，融合0.1 | OOF，融合0.25 |
|---|---:|---:|---:|
| full控制 | 636 | 4324 | 4335 |
| 删除答案数值组 | 604 | 4321 | 4326 |
| 删除来源图组 | 588 | 4325 | 4333 |
| 删除原文本组 | 580 | 4323 | 4333 |
| 删除问题词与终运算交互组 | 256 | 4323 | 4335 |

平局按计划保留full，本轮无新验证入口。最高新表示no_question的bundle保存供复现，
但标为不合格，不将平局称为准确率提升。380维交互删除无损，仅支持这组特征在此
固定配置中未显示边际增益。剩余图仍用问题数字/单位，所以这不是完全不使用问题的消融。
答案8维组还包含操作数身份和相对排名，−9不能全归于整数/大小先验。
详见[特征消融复盘](code/runs/round21-ablation/LEARNING.md)。

## 3. Round22：局部Embedding几何没有稳定正确性

每题Embedding减四候选均值，训练折拟合PCA64，再L2归一。
只将训练中有对有错的题目候选放入余弦索引，监督为y减本题y均值。
这是局部top-K残差，不同于Round6的全局RBF/Nyström拟合。
K32/128×强度0.05/0.1/0.25，6配置。原算术路由与格式transfer保持。

最高4314仅一折正增，selected=null。K128/0.05修复1／新错0；
K32/0.25修复5却新增4错。PCA保留86.5–86.7%方差不能证明保留正确性信息；
逐例发现同一道题另一个正确候选仍可获负局部残差。停止继续扩大邻居/权重搜索。
仅训练OOF，没有导出推理模型或声称推理资格。单线程6.28秒，8项构造检查通过。
详见[近邻复盘](code/runs/round22-neighbor/FINDINGS.md)。

## 4. 记录、下一方向与边界

全部24配置及失败见[all-training.csv](code/runs/round20-22/all-training.csv)，
唯一验证选择的预冻结与哈希见[frozen-selection.json](code/runs/round20-22/frozen-selection.json)，
官方记录见[results.json](code/runs/round20-22-verification/results.json)。
训练参考只用于训练监督；官方解析器/工具、训练/验证数据、历史源码与旧模型均保留。
同一OOF与验证多轮复用，这些是开发证据，不能视作无偏泛化结果。

按用户要求继续的独立实验：Round23用题目数字短程序推导候选终值支持；
Round24从头学习候选之间对称交互；Round25用随机阈值森林检验不同学习器。
各自拟合前固定小网格，不根据测试结果调参；未完成结果不预报为成功。
每项事实→机制→下一步见[lessons.json](code/runs/round20-22/lessons.json)。
