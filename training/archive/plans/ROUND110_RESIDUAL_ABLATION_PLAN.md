# Round110：格式/算术消融与最终答案证据

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；用户要求继续提升。先写本计划，再训练。第109轮751研究候选、原Round79冻结模型和既有测试记录保留。

## 假设和固定四配置

H1：第109轮增益来自算术核对而非只学到有等号/写得长等格式相关性。相同anchor、offset、划分、lambda下分别重训格式与算术模块。
H2：官方####答案与其后boxed答案的关系可补充局部等式信息；通过训练学习该证据的权重，可能减少已有不一致答案选择。该证据来自我们早期Round11已有机制，不是针对新验证错题新增规则。

|模式|维数|新拟合|
|---|---:|---|
|format|6|11候选特征中的前三项格式量，组内mean/max|
|arithmetic|16|11候选特征中的后八项算术量，组内mean/max|
|full|22|第109轮完整重训对照，要求与原751模型分数/OOF重现|
|final_evidence|26|22项+4项最终答案证据|

所有配置固定增强anchor（第108轮subset，anchor lambda0.01），残差lambda0.1。不扫新正则/融合权重，不在批内增加模式。全部四配置在训练前确定，验证前冻结。

新增4项组证据：组内成员的late-box冲突比例、组内late-box与官方答案一致比例、全体4候选late-box支持该组答案的比例、组外存在####/boxed冲突且late-box支持该组答案的比例。late-box沿用Round11 final_box定义：仅识别最后####之后最后boxed的有效数字。文本最多前24000字符；组答案始终来自未修改的官方parse_answer。没有late-box为缺失证据，相关量为0；不硬编码调转答案，不据验证标签判断是否启用。

## 训练与隔离

复用第109轮经过哈希冻结的inner-anchor模型和分折证明，重算其outer-fit inner-OOF offset；逐个核对inner-fit/inner-held/outer-held互斥和覆盖。部署及outer-held anchor仍来自第108轮同折模型。复用参数只为减少重复训练，所有新残差都重训：3外层折×4模式+4全训练=16次新拟合。

scaler各模式仅拟合当前fit原题的完整组（不是全部训练或增强子集）；pair按每题归一的logistic均值加0.1/2*范数平方，使用折外anchor margin。优化设置沿用109；full模式的22维统计、设计、权重和OOF必须在严格容差下复现109，而非以相近总分替代。

训练阶段不加载validation/test；保存逐折结果、配对OOF、最终权重、梯度、pair审计。父进程硬timeout600秒，四线程。输出新目录runs/round110-residual-ablation，拒绝覆盖。

## 验证与判定

先冻结四个模型、全部源闭包、本计划、训练结果和继承输入的SHA，再读validation。以751作为当前研究比较基准；新模型与751、原749和anchor746均记录净修复。full模式是751重复对照，不能算新提升。只有>751且资源/接口通过才另存新研究候选，否则保留751。

每配置完整fresh官方预测与独立评分≤30秒，四CPU线程；完整解压资产（anchor+scaler+残差+config）≤16MiB。检查缓存/重载、零修正、候选严格分数重排rtol=atol=1e-8、题序、新ID、不同bank大小、空输入、Python整数、同答案同分。

报告格式/算术/full差异和final_evidence相对full的差异，逐折及验证一致性，成功/失败均保留。不把描述性差异当独立因果或显著性证明。四配置完成后停止本批。

## 历史披露与复现

此前自身与公开他人测试汇总已知；本轮不访问/哈希/预测/评分测试。train和validation已长期开发使用，OOF与验证都不宣称全新独立确认。原已测Round79最终模型/成绩保持，研究候选单列。
在code目录使用现有venv依次运行train_round110_residual_ablation.py与evaluate_round110_residual_ablation.py。训练和验证分别保存在runs/round110-residual-ablation与runs/round110-evaluation；最终记录ROUND110_RESULTS.md、ROUND110_LEARNING.md、WORKLOG.md和AI_DISCLOSURE.md。
方法来源延续CaspianW固定anchor/算术残差思想，具体引用和独立实现差异见ROUND109_ARITHMETIC_RESIDUAL_PLAN.md；本轮不获取新外部代码、数据或权重。
