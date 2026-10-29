# Round109计划：固定答案组模型与局部算术残差

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；用户要求“借鉴他们的方法，再次训练”。先保存计划后实现和训练。四配置固定，不追加验证反馈驱动的网格。

## 来源与假设

借鉴[CaspianW训练代码](https://github.com/CaspianW/dase7506-mp2/blob/main/src/train.py)、[局部特征聚合](https://github.com/CaspianW/dase7506-mp2/blob/main/src/quantity_flow_features.py)和[算术特征定义](https://github.com/CaspianW/dase7506-mp2/blob/main/src/arithmetic_features.py)。独立实现“固定答案组anchor，学习小型算术残差”，不下载他人权重/数据、不执行外部代码。不是完整复现：使用我们已有的有界等式解析器，新增嵌套折外offset，保留这些差异。

H1：第108轮只用答案数值表面量，缺少局部等式正确性和最后算式与答案的关系；加入这些信息可能增加净修复。
H2：固定组模型分数、限制修正维度并加强正则，可能比直接替换/固定融合减少新错。是否成立由结果决定。

## 固定四配置

anchor取第108轮lambda=0.01，完整答案组/子集增强两种条件；各自残差lambda=0.01/0.1，合计四个模型。anchor选择与四配置在本轮验证前固定；不根据既知测试成绩选择。上一轮模型已在验证比较过，属于自适应后续研究。

## 特征和目标

每候选11项：等号存在、log等号数、log含等号行数；有可检查等式、log可检查数、log不匹配数、不匹配比例、log最大相对残差；末个检查结果与最终答案可比较、相符、不符。以同数值答案组内mean和max聚合，共22维。组内成员沿用第108轮确定性排序。只读取候选文本前24000字符，最多64个有界检查，不使用eval或执行候选程序；使用numeric_round7_v3.evidence的既有AST白名单。近似比较固定绝对0.005+相对1e-6（借鉴来源），不改官方答案解析器和评分器。

scaler只拟合当前fit题的原始完整答案组；无子集残差增强。有效正负答案组pair各题均分权重，再在有信息题上均分。目标为mean(logaddexp(0, -(OOF_anchor_margin + scaled_difference@v))) + lambda/2*||v||²。固定SciPy L-BFGS-B maxiter1000、ftol1e-12、gtol1e-7、maxls40。所有参数和统计只拟合train。

## 分折与防泄漏

沿用第108轮三折原题划分，确保两个阶段的评估可配对。
每个外层fold：在outer-fit内再分3折（分层正确候选数，seed=20261030+outer_fold），分别拟合两个anchor得到outer-fit的inner-OOF分数；残差只用outer-fit标签和这些OOF分数。outer-held预测使用第108轮相同outer-fit拟合的anchor，再加本轮残差。outer-held题不得出现在任何inner fit中。
全训练残差使用第108轮保存的完整train OOF分数；部署anchor使用第108轮full-train两个checkpoint。既有源代码、fold、OOF和资产先验哈希核对；不得把旧全训练回代当作OOF。共18个新inner-anchor拟合+12个外层残差+4个全训练残差=34次新拟合。

## 执行与判定

训练全程不加载validation/test。先检查残差梯度、零修正等价anchor、缓存/重载一致；检查分数候选重排rtol=atol=1e-8、题序、新ID、变bank、空输入、Python整数、组内同分。父进程硬预算900秒，四线程。
冻结四模型/全部源闭包/本计划/训练结果SHA，再读取验证集。逐一fresh官方预测+独立评分，每模型合计≤30秒，完整解压资产（含anchor、scaler、残差、config）≤16MiB。与anchor和原Round79对照，记录分层、修复/新错及训练三折逐折结果。
只有验证>749且资源/接口通过才记为验证研究提升；即使提升也另存研究候选，保留已测Round79最终模型/测试记录。若不提升，报告全部失败及下一轮依据，四配置结束即停止本批，不追加参数。

## 历史与复现

此前自身及公开他人测试总分已知；此后开发必须披露历史。本轮不访问、哈希、预测或评分测试，不将多轮使用的train/validation称为独立确认。CPU本机验证计时不代表参考Xeon完整测试资格。
从code目录依次运行train_round109_arithmetic_residual.py、evaluate_round109_arithmetic_residual.py；新目录runs/round109-arithmetic-residual与runs/round109-evaluation，不覆盖既有结果。来源、AI辅助、成功/失败和实现差异写入ROUND109_RESULTS.md、WORKLOG.md和AI_DISCLOSURE.md。
