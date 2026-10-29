# 截至2026-10-28的完整实验记录：Round1–105

## 1. 完成数量与口径

- **已完成105个编号实验轮次**；编号轮次包括训练、规则、诊断、旧模型补评和零拟合消融。不能将其写成105次训练或105个独立算法。

- **73轮产生了官方验证输出，32轮止于训练筛选/内部留出/诊断**。这里计的是轮次；一轮可含多个配置。

- 初始模型为723/798；建立基线后提高历史最佳的是**第2、7、11、79轮**。当前最佳是**第79轮，749/798=93.8596%**。

- 第80–105轮共26轮没有再次晋级。最新12个输出属于第103–105轮，其中8次新增系数拟合、4个零拟合组件消融。

- 本次只整理已有证据，没有启动新实验、改选模型或执行测试评分。

## 2. 如何阅读

- **官方验证**：该轮至少有一个固定输出经官方预测及评分比较，分母798。表内数字是本轮方案成绩，不把保留模型的历史分数冒充本轮新结果；第6轮特别注明搜索选中旧配置。

- **训练OOF**：训练题按题划分得到折外预测，通常分母4755；它不同于官方验证。规则叠加在已有OOF上不等于重新训练了模型。

- **训练内部留出/嵌套评估**：单独注明951、475等分母，不与4755题OOF或798题验证混用。

- **训练回代**：模型在参与拟合的训练数据上评分。近期多轮报告中的回代成绩不能当作OOF或泛化证明。

- 各轮的“修复/新增错”使用该轮注明的父模型，早期多对Round11，后期对Round79；不能跨轮直接相加。

## 3. 真正改变历史最佳的节点

|阶段|验证正确数/798|准确率|相对上一节点|
|---|---:|---:|---:|
|多数投票对照|688|86.22%|—|
|第1轮文本+Embedding基线|723|90.60%|比多数投票多35题|
|第2轮context+pairwise|744|93.23%|+21题|
|第7轮算术冲突门控|747|93.61%|+3题|
|第11轮显式结论转交|748|93.73%|+1题|
|第79轮分支独立正则|749|93.86%|+1题|


从第1轮到目前净增26题，约3.26个百分点。以下逐轮覆盖1–105，无省略编号。


### 第1–15轮：初始模型与稀疏规则

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|1|初始基线：首候选、多数投票、文本、Embedding及两者组合|官方验证|组合模型723；多数投票688，建立初始基线|[WORKLOG.md](<WORKLOG.md>)|
|2|逐候选回归与题内中心化、成对排序；线性/非线性/context表示|官方验证|context+pairwise达到744，比第1轮净增21题|[ROUND2_RESULTS.md](<experiments/ROUND2_RESULTS.md>)|
|3|候选/答案组softmax与logistic、更宽投影、多模型平均、小型神经排序|官方验证|新方案最高738；未超过744|[ROUND3_RESULTS.md](<experiments/ROUND3_RESULTS.md>)|
|4|算术关系、词法、PCA二次项、LambdaRank及融合|官方验证|新方案最高740；算术解析初版修复后重跑|[ROUND4_RESULTS.md](<experiments/ROUND4_RESULTS.md>)|
|5|困难题加权、平方hinge、RBF核、稀疏文本、候选重采样、白化|官方验证|新方案最高742；训练OOF提升未迁移|[ROUND5_RESULTS.md](<experiments/ROUND5_RESULTS.md>)|
|6|直接成对树、完整二次交互、语义×一致性、Nyström及有限融合/容量搜索|官方验证|新增模型表最高742；有限搜索最高744，选中仍为原配置|[ROUND6_RESULTS.md](<experiments/ROUND6_RESULTS.md>)|
|7|成对上下文、Embedding、数值14/核心6维、答案分组消融及算术冲突门控|官方验证|744→747；明确算术冲突题启用数值头，净增3题|[ROUND7_RESULTS.md](<experiments/ROUND7_RESULTS.md>)|
|8|候选/答案组冲突惩罚、复算支持、选择性门控、格式覆盖扩展|官方验证|最高747；格式扩大增加误伤，未晋级|[ROUND8_RESULTS.md](<experiments/ROUND8_RESULTS.md>)|
|9|题目—候选数字/单位/关系词对齐、题目条件Embedding及模型共识|官方验证|新输出最高746；未超过747|[ROUND9_RESULTS.md](<experiments/ROUND9_RESULTS.md>)|
|10|角度/竞争者表示、dropout惩罚、集合损失、严格嵌套堆叠、百分比取值域|官方验证|最高747（百分比规则）；其他新输出最高742|[ROUND10_RESULTS.md](<experiments/ROUND10_RESULTS.md>)|
|11|最终boxed结论与官方解析值错位：转交、惩罚、投票消融|官方验证|747→748；选择可被官方解析为明确结论的现有候选，净增1题|[ROUND11_RESULTS.md](<experiments/ROUND11_RESULTS.md>)|
|12|最终格式扩展、单变量代数、明确折扣关系、数值依赖覆盖|官方验证|代数/折扣及组合均748；部分分支未达准入|[ROUND12_RESULTS.md](<experiments/ROUND12_RESULTS.md>)|
|13|换算来源修复、单位感知依赖图、显式换算矛盾|训练OOF规则筛选|最高4313/4755；恢复误伤但无新纠错，未进入官方验证|[ROUND13_RESULTS.md](<experiments/ROUND13_RESULTS.md>)|
|14|依赖提取充分性门控、年龄共同偏移、连等式依赖修复|训练OOF规则筛选|最高4314/4755，仅1个修复，未达验证门槛|[ROUND14_RESULTS.md](<experiments/ROUND14_RESULTS.md>)|
|15|百分比等价表示、明确债务义务、累计规则与去图消融|官方验证|累计训练OOF4319；验证仍748，无净增|[ROUND15_RESULTS.md](<experiments/ROUND15_RESULTS.md>)|


### 第16–30轮：新监督、结构树、神经与程序搜索

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|16|用参考中间步骤监督题目的最终运算类别|官方验证|训练OOF4317；验证748，未增加纠错覆盖|[ROUND16_19_RESULTS.md](<experiments/ROUND16_19_RESULTS.md>)|
|17|原表示线性残差与题目条件双线性残差；修复交互塌缩|官方验证|3个冻结输出均747；活跃交互未改善验证|[ROUND16_19_RESULTS.md](<experiments/ROUND16_19_RESULTS.md>)|
|18|636维结构/数值/来源图特征的binary树与LambdaRank|官方验证|binary744、LambdaRank741；OOF最高4356未迁移|[ROUND16_19_RESULTS.md](<experiments/ROUND16_19_RESULTS.md>)|
|19|线性语义残差与结构树的固定融合|官方验证|OOF4359；验证748，修复3/新增3|[ROUND16_19_RESULTS.md](<experiments/ROUND16_19_RESULTS.md>)|
|20|uniform-correct CE与逐题归一pairwise logistic，照顾多正确候选|官方验证|选中方案748，修复1/新增1；减少误伤也减少纠错|[ROUND20_22_RESULTS.md](<experiments/ROUND20_22_RESULTS.md>)|
|21|固定结构树，分别删除答案数值、来源图、文本、问题×运算组|训练OOF消融|最高4335/4755，与full控制持平；未进入官方验证|[ROUND20_22_RESULTS.md](<experiments/ROUND20_22_RESULTS.md>)|
|22|题内相对Embedding的PCA64/余弦top-K近邻残差|训练OOF筛选|最高4314/4755，折间收益不足；未导出验证模型|[ROUND20_22_RESULTS.md](<experiments/ROUND20_22_RESULTS.md>)|
|23|题目数字的2/3叶有限四则程序搜索，支持候选终值|官方验证|747，修复0/新增1；算术可达不等于题意正确|[ROUND23_25_RESULTS.md](<experiments/ROUND23_25_RESULTS.md>)|
|24|从头学习对称跨候选DeepSets竞争网络|官方验证|OOF4344；验证743，修复7/新增12|[ROUND23_25_RESULTS.md](<experiments/ROUND23_25_RESULTS.md>)|
|25|compact结构特征上的ExtraTrees及融合|官方验证|743；独立学习器未带来净收益|[ROUND23_25_RESULTS.md](<experiments/ROUND23_25_RESULTS.md>)|
|26|程序搜索增加英文数字词、题目明确提示的常数及两者组合|训练OOF消融|旧控制4321优于扩展4314–4316；未进入官方验证|[ROUND26_29_RESULTS.md](<experiments/ROUND26_29_RESULTS.md>)|
|27|同宽pointwise非线性对照，以及交互网络5/10/20轮早停点|官方验证|pointwise742；早期交互未胜40轮控制，未另验证|[ROUND26_29_RESULTS.md](<experiments/ROUND26_29_RESULTS.md>)|
|28|固定随机森林，把binary标签改为题内中心化标签|官方验证|742；监督目标变化未优于旧模型|[ROUND26_29_RESULTS.md](<experiments/ROUND26_29_RESULTS.md>)|
|29|存在可解析答案时，排除官方终值不可解析候选|官方验证|训练修复2题；验证748，无新增覆盖|[ROUND26_29_RESULTS.md](<experiments/ROUND26_29_RESULTS.md>)|
|30|训练参考AST程序提取、题目槽位检索与新题数值代入|训练OOF筛选|提取2314个程序；全部配置4313、零改选，未验证|[ROUND30_32_RESULTS.md](<experiments/ROUND30_32_RESULTS.md>)|


### 第31–45轮：量级、答案组、目标关系与训练目标

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|31|从题目预测signed-log答案量级：L2/分位数回归对常量控制|训练OOF筛选|回归误差下降，但选择最高4315低于常量4316；未验证|[ROUND30_32_RESULTS.md](<experiments/ROUND30_32_RESULTS.md>)|
|32|数字遮蔽后的候选末段字符TF-IDF样式分类|官方验证|744；学到部分格式/措辞证据，未提升选择|[ROUND30_32_RESULTS.md](<experiments/ROUND30_32_RESULTS.md>)|
|33|完整1422维context的最大间隔排序|官方验证|743；源码并发冲突版本隔离，使用干净重放结果|[ROUND33_36_RESULTS.md](<experiments/ROUND33_36_RESULTS.md>)|
|34|按答案分组，Embedding均值/max与组属性的binary监督|官方验证|OOF4333；验证746，无净提升|[ROUND33_36_RESULTS.md](<experiments/ROUND33_36_RESULTS.md>)|
|35|目标问句单独编码/全文加目标编码的终运算监督|官方验证|OOF4318；验证748，目标分类改善未增加验证纠错|[ROUND33_36_RESULTS.md](<experiments/ROUND33_36_RESULTS.md>)|
|36|嵌套boxed分数/表达式的严格结论解析与转交|训练OOF规则筛选|4313、零改选；未进入官方验证|[ROUND33_36_RESULTS.md](<experiments/ROUND33_36_RESULTS.md>)|
|37|PCA相对表示上的反对称RBF SVC成对偏好|官方验证|OOF4326；验证743，新增5错|[ROUND37_40_RESULTS.md](<experiments/ROUND37_40_RESULTS.md>)|
|38|保持答案组表示，改用正确组softmax损失|官方验证|OOF4350；验证746，修复6/新增8|[ROUND37_40_RESULTS.md](<experiments/ROUND37_40_RESULTS.md>)|
|39|修复目标问句边界：保留完整How much/find等目标片段|训练OOF匹配消融|81题目标改变，但各方案argmax与旧控制一致；未验证|[ROUND37_40_RESULTS.md](<experiments/ROUND37_40_RESULTS.md>)|
|40|时间、百分比、金额错误的真实交集与封闭关系审计|训练集只读诊断|审计523题、50个当前错误；提出预算/利润关系，无模型验证|[ROUND37_40_RESULTS.md](<experiments/ROUND37_40_RESULTS.md>)|
|41|预算余额反推未知商品价的精确角色关系|官方验证|748；只覆盖少量训练纠错，验证无改选收益|[ROUND41_43_RESULTS.md](<experiments/ROUND41_43_RESULTS.md>)|
|42|统一数量单位的单商品净利润关系|官方验证|748；训练有修复，验证无新增覆盖|[ROUND41_43_RESULTS.md](<experiments/ROUND41_43_RESULTS.md>)|
|43|严格嵌套OOF基线offset的残差训练|官方验证|743，修复5/新增10；修正过度自信训练输入未形成净增|[ROUND41_43_RESULTS.md](<experiments/ROUND41_43_RESULTS.md>)|
|44|固定投影的8成员题目Poisson重采样平均，对匹配强正则控制|训练OOF消融|bag8与alpha=.6均4321；未胜控制，未进入官方验证|[ROUND44_47_RESULTS.md](<experiments/ROUND44_47_RESULTS.md>)|
|45|固定表示和正则，比较平方损失与Huber鲁棒损失|官方验证|746；训练OOF4320未迁移|[ROUND44_47_RESULTS.md](<experiments/ROUND44_47_RESULTS.md>)|


### 第46–60轮：共识、数量角色、单位及局部证据

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|46|近邻监督由中心化标签改binary，并比较全训练/信息题索引库|官方验证|748；二值监督未增加验证纠错|[ROUND44_47_RESULTS.md](<experiments/ROUND44_47_RESULTS.md>)|
|47|bootstrap成员7/8、8/8答案共识作为改选条件|官方验证|748；高共识仍可能共同遗漏条件|[ROUND44_47_RESULTS.md](<experiments/ROUND44_47_RESULTS.md>)|
|48|全部训练OOF错题、参考中间量、重复数值和缺因子机制审计|训练集只读诊断|442错中365题仅1个正确候选；定位角色混淆，无新验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|49|保留同值不同数量角色的Counter依赖、祖先与跨候选特征|训练OOF消融|最高4339但折间不稳定、未修复关键缺因子锚点；未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|50|数量、单价、each/for-each的封闭量纲链与唯一目标求解|官方验证|748；TRAIN仅接受5题，验证无新增覆盖|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|51|恢复带单位注释的纯数值算式，比较数学块/完整行提取|训练OOF规则筛选|两模式4311、0修复/2新错；去单位造成换算假冲突，未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|52|安全算式恢复后重做数量依赖特征；修复严格候选重排问题|官方验证|有效重放OOF4341；验证745，新增3错|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|53|从题目学习是否应采用所有正数角色乘积，固定高置信门控|训练OOF筛选|最高概率不足门槛，OOF4313、零改选；未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|54|乘积教师仅在候选确实含该乘积的题上训练|训练OOF匹配消融|低门槛4303；高门槛4313且零变化，未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|55|固定同一棵结构树，只把原/恢复数学特征的局部分差加入基线|训练OOF局部消融|4314，仅修复1题，未达准入、未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|56|把极小数值残差固定置零，检验树零阈值稳定性|训练OOF稳定性消融|OOF4341与父方法相同；稳定性修复无准确率增益，未验证|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|57|对数学注释依赖专家固定较低信任权重.05/.1/.15|官方验证|3个输出均747，均0修复/1新错|[ROUND48_57_RESULTS.md](<experiments/ROUND48_57_RESULTS.md>)|
|58|题目明确目标周期与候选终端计算依赖是否一致|训练OOF规则筛选|识别17题但0可改选，4313；未验证|[ROUND58_60_RESULTS.md](<experiments/ROUND58_60_RESULTS.md>)|
|59|题目短语×候选末步短语的稀疏交互，对无交互词频控制|训练OOF消融|最高4316，与匹配控制持平；未验证|[ROUND58_60_RESULTS.md](<experiments/ROUND58_60_RESULTS.md>)|
|60|稀疏短语匹配各特征块等尺度归一化|训练OOF消融|最高4319，与控制持平；未验证|[ROUND58_60_RESULTS.md](<experiments/ROUND58_60_RESULTS.md>)|


### 第61–78轮：分歧片段、角色监督、多路线与校准

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|61|终端Markdown/周期排版与单位保护规则消融|训练OOF规则筛选|最高4314，仅1修复；保护单位消除旧误伤，未验证|[ROUND61_RESULTS.md](<experiments/ROUND61_RESULTS.md>)|
|62|数学结构与原Embedding/题内相对Embedding联合LambdaRank|官方验证|OOF4346；验证747，修复1/新增2|[ROUND62_RESULTS.md](<experiments/ROUND62_RESULTS.md>)|
|63|从原联合排序网格补评较保守、低误伤的输出|官方验证|748，修复0/新增0；无净提升|[ROUND63_RESULTS.md](<experiments/ROUND63_RESULTS.md>)|
|64|先抽取不同答案候选之间最有分歧的数量句，再学习交互|训练OOF消融|最高4324，与无交互控制一致；未验证|[ROUND64_65_RESULTS.md](<experiments/ROUND64_65_RESULTS.md>)|
|65|分歧片段与原末段词法表示的独立训练内部留出比较|训练内部留出|951题上864，对照末段866；未胜控制，未验证|[ROUND64_65_RESULTS.md](<experiments/ROUND64_65_RESULTS.md>)|
|66|题目数量角色对齐后迁移完整程序，对位置槽控制|训练OOF消融|4配置均4313、零改选；未验证|[ROUND66_67_RESULTS.md](<experiments/ROUND66_67_RESULTS.md>)|
|67|题目直接监督分类完整可执行公式|训练OOF筛选|soft4312、hard4313；高置信有效覆盖不足，未验证|[ROUND66_67_RESULTS.md](<experiments/ROUND66_67_RESULTS.md>)|
|68|参考计算树的数量对/LCA运算关系监督及上下文匹配|训练OOF消融|最高4317；未胜同权重控制及预定门槛，未验证|[ROUND68_69_RESULTS.md](<experiments/ROUND68_69_RESULTS.md>)|
|69|不同答案候选的双向token对齐与有方向局部编辑|官方验证|OOF4324；验证743，修复1/新增6|[ROUND68_69_RESULTS.md](<experiments/ROUND68_69_RESULTS.md>)|
|70|局部编辑恢复题目数字角色、操作数身份与候选数值秩|官方验证|OOF4325；验证744，0修复/4新错|[ROUND70_RESULTS.md](<experiments/ROUND70_RESULTS.md>)|
|71|补评旧成对编辑网格中更稳定的简单词频控制|官方验证|744；零新拟合，自适应补验仍无净增|[ROUND71_RESULTS.md](<experiments/ROUND71_RESULTS.md>)|
|72|从头训练原始文本序列CNN，对匹配词袋控制|训练内部留出|CNN398/401/398（各475题）胜词袋，但低于fresh R2的422；未验证|[ROUND72_75_RESULTS.md](<experiments/ROUND72_75_RESULTS.md>)|
|73|相对Embedding的LDA/QDA，比较全正确题监督与信息题监督|训练内部留出|4配置三个seed均低于fresh R2；未验证|[ROUND72_75_RESULTS.md](<experiments/ROUND72_75_RESULTS.md>)|
|74|训练参考全文作为正确解答扩增，对候选文本单独训练|训练内部留出|参考扩增358/363/362，低于候选控制379/370/373（各475）；未验证|[ROUND72_75_RESULTS.md](<experiments/ROUND72_75_RESULTS.md>)|
|75|词序CNN与固定语义Embedding的联合模型，对dense-only|训练内部留出|联合413–415/475；dense-only420–424，未达到准入；未验证|[ROUND72_75_RESULTS.md](<experiments/ROUND72_75_RESULTS.md>)|
|76|使用验证集补评旧答案组softmax的3个固定融合设置|官方验证|747/745/745；零新训练，明确自适应选型|[ROUND76_RESULTS.md](<experiments/ROUND76_RESULTS.md>)|
|77|严格嵌套拟合的低维二选一专家接受门控|训练嵌套评估|未胜简单截距控制或未达净增门槛；无导出、无官方验证|[ROUND77_78_RESULTS.md](<experiments/ROUND77_78_RESULTS.md>)|
|78|保留raw组置信信息的两个非负系数答案组校准|官方验证|746，修复8/新增10；置信信息修复未带来净增|[ROUND77_78_RESULTS.md](<experiments/ROUND77_78_RESULTS.md>)|


### 第79–92轮：分支正则、训练总体、容量与低秩交互

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|79|完整算术门控+格式保护下，语义/数值分支分别选择正则|官方验证|17个新组合；748→749，语义alpha=.3、数值alpha=1，净增1题|[ROUND79_80_RESULTS.md](<experiments/ROUND79_80_RESULTS.md>)|
|80|原随机投影基的局部正负扰动及幅度对照|官方验证|8个输出最高746；未超过当时748或当前749|[ROUND79_80_RESULTS.md](<experiments/ROUND79_80_RESULTS.md>)|
|81|固定语义alpha=.3，数值分支整体正则7值|官方验证|7个输出最高749；另做三折诊断，无验证净增|[ROUND81_82_RESULTS.md](<experiments/ROUND81_82_RESULTS.md>)|
|82|数值头算术6维子块独立惩罚|官方验证|4个输出最高749；部分OOF提高，验证持平|[ROUND81_82_RESULTS.md](<experiments/ROUND81_82_RESULTS.md>)|
|83|降低非算术门题在数值头训练中的权重|官方验证|4个输出最高749；r=.1修复1/新增1|[ROUND83_RESULTS.md](<experiments/ROUND83_RESULTS.md>)|
|84|当前数值头与条件数值头的固定系数平均|官方验证|4个零新拟合输出最高749|[ROUND84_RESULTS.md](<experiments/ROUND84_RESULTS.md>)|
|85|门内数值头使用完整数值14维/答案组交互，正则1/3|官方验证|4个输出最高749；新增特征仅作用算术门内|[ROUND85_RESULTS.md](<experiments/ROUND85_RESULTS.md>)|
|86|完整保护下改变语义context宽度、线性/非线性容量|官方验证|6个输出最高744；扩大容量未净增|[ROUND86_87_RESULTS.md](<experiments/ROUND86_87_RESULTS.md>)|
|87|语义训练排除/降低门内题权重，或加权单正确候选题|官方验证|4个输出最高749；单正确题加权为746|[ROUND86_87_RESULTS.md](<experiments/ROUND86_87_RESULTS.md>)|
|88|当前语义头与题目重加权语义头的系数平均|官方验证|4个零新拟合输出最高749|[ROUND88_RESULTS.md](<experiments/ROUND88_RESULTS.md>)|
|89|原1422维Embedding/文本/context三块分别设惩罚|官方验证|6个输出最高746；分块收缩未净增|[ROUND89_91_RESULTS.md](<experiments/ROUND89_91_RESULTS.md>)|
|90|保留原成对平方目标，加入正确候选CE或pairwise logistic|官方验证|4个输出最高749；更换损失组合未净增|[ROUND89_91_RESULTS.md](<experiments/ROUND89_91_RESULTS.md>)|
|91|题内方差加权的特征几何/度量|官方验证|4个输出最高748；训练拟合改善未迁移|[ROUND89_91_RESULTS.md](<experiments/ROUND89_91_RESULTS.md>)|
|92|原1024维Embedding的可学习低秩二次残差，rank8/16|官方验证|4个输出最高728；回代4683–4716但验证709–728，明显未迁移|[ROUND92_RESULTS.md](<experiments/ROUND92_RESULTS.md>)|


### 第93–105轮：全候选监督、表示、过程监督与组件归因

|轮次|验证了什么|评估方式|实际结果|原始证据|
|---:|---|---|---|---|
|93|原排序目标加入全部候选BCE与自由截距，利用全正确题|官方验证|4个输出最高745；全正确监督未改善验证|[ROUND93_RESULTS.md](<experiments/ROUND93_RESULTS.md>)|
|94|全部4个低秩残差来源各缩小到.1/.25强度|官方验证|8个零新拟合输出最高745|[ROUND94_RESULTS.md](<experiments/ROUND94_RESULTS.md>)|
|95|精确分解并缩减成对目标中正确/错误类内协方差|官方验证|6个输出最高748；改变类内约束未净增|[ROUND95_RESULTS.md](<experiments/ROUND95_RESULTS.md>)|
|96|仅用TRAIN参考的错误答案数值距离重加权近错/远错|官方验证|4个输出最高749；推理不访问参考，无净增|[ROUND96_RESULTS.md](<experiments/ROUND96_RESULTS.md>)|
|97|同题余弦几何、同/不同答案组条件余弦几何|官方验证|4个联合输出最高749|[ROUND97_98_RESULTS.md](<experiments/ROUND97_98_RESULTS.md>)|
|98|原Embedding坐标平方、与题均值乘积及两者的联合特征|官方验证|6个分块正则输出最高749；回代提高未迁移|[ROUND97_98_RESULTS.md](<experiments/ROUND97_98_RESULTS.md>)|
|99|局部参考步骤的自然语言→运算根监督，对最后/全部步骤|官方验证|4个输出最高748；未修复验证旧错|[ROUND99_101_RESULTS.md](<experiments/ROUND99_101_RESULTS.md>)|
|100|正确/错误候选二阶矩差的监督16维基，对随机基|官方验证|4个输出最高746；监督基未胜随机强正则控制|[ROUND99_101_RESULTS.md](<experiments/ROUND99_101_RESULTS.md>)|
|101|问题条件下的候选分歧跨度成对比较，对旧成对表示；线性/树|官方验证|4个输出最高749（旧线性）；问题条件线性748|[ROUND99_101_RESULTS.md](<experiments/ROUND99_101_RESULTS.md>)|
|102|####后的完整真等式/算术表达式，与评分字面值核对|官方验证|2个零拟合输出均749；TRAIN新证据覆盖0|[ROUND102_RESULTS.md](<experiments/ROUND102_RESULTS.md>)|
|103|nongate语义分支联合追加数值14/答案组386/两者，新增块独立正则|官方验证|6个输出最高748；数值方案修复1/新增2，未净增|[ROUND103_RESULTS.md](<experiments/ROUND103_RESULTS.md>)|
|104|固定旧语义权重：仅保留新增数值分数或拟合数值残差|官方验证|2次新拟合+2个组件消融，4个输出均748（0修复/1新错）|[ROUND104_RESULTS.md](<experiments/ROUND104_RESULTS.md>)|
|105|仅保留Round103的旧语义系数变化，去掉新增数值分数|官方验证|2个零拟合输出746/747；均修复1但新增4/3|[ROUND105_RESULTS.md](<experiments/ROUND105_RESULTS.md>)|


## 4. 已完成但不另计编号的工作

- 依赖安装、官方数据完整性/对齐检查、环境记录。初始官方数据检查涉及数据文件校验；它不是测试集预测、评分或调参。

- 历史错误审计、策略重置、学习曲线诊断、可靠性分层分析；其中未单独编号的工作不再虚增轮数。

- 已选模型训练复现、推理接口/候选排列/ID/批量规模检查、资产哈希与完整解压尺寸审计。

- 本地提交材料草案、复现说明、AI披露、4页报告PDF和历史审阅包。它们是历史快照，不代表已公开提交或已同步全部后续实验。

## 5. 失败与修复也保留在记录中

- 第4轮算术提取原型修复后完整重跑；第7轮数值解析v1/v2/v3及其误伤均有记录。

- 第17轮双线性交互塌缩修复、第24轮推理精度修复、第33轮源码冲突后的干净重放，均不能另算性能提升。

- 第52轮首次重排不稳定版本作废，正式结果使用replay-invariant。第99轮JSONL读取失败及修复前快照保留。

- 第103轮归档脚本的schema兼容修复前版本及差异保留；没有改变候选池、晋级规则或模型。

## 6. 当前模型与评估边界

- 推理入口：`code/method_round11.py`；完整checkpoint：`code/runs/round79-regularization/candidates/round79_s0p3_n1p0`。

- 完整推理资产1,678,154字节（约1.6004MiB）；选型时本机fresh完整验证预测+独立评分约1.782秒。

- 本机完整验证资源检查不能认证参考Xeon上的完整测试资格。

- 没有测试集预测、测试评分或测试调参；当前749是验证成绩，不能当排行榜/测试分数。

- OOF和验证已经多轮用于开发，结果不是独立、无偏或显著性结论。

- 没有把单个解析/工程控制通过、训练回代提高、修复若干旧错但新增更多错，记为模型晋级。


本记录依据各轮RESULTS、WORKLOG及CURRENT_BEST整理；相邻JSON保存105条结构化记录、来源报告SHA256及当前模型指针。
