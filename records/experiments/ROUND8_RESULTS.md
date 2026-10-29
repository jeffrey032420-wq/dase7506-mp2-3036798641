# 第八轮：冲突惩罚、复算支持与格式覆盖

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent（当前会话内执行）。
- Origin Mode: 用户授权设计与执行、官方复算、描述性分析。
- Origin Date: 2026-10-15。
- Verification Status: VERIFIED_LOCAL_VALIDATION；无测试集成绩或参考 CPU 资格结论。
- Version Label: round8_results_v1。

## 结论与当前模型

**本轮没有超过 747/798（93.61%），保留第七轮 strict_core 算术门控模型。**
方法 `code/method_round7_gated.py`，checkpoint `code/runs/round7-gated/model_bundle/`。
原权重与第七轮全部代码哈希均核验未变；CURRENT_BEST.json 只更新最近完成轮次为 8。

尝试中最高训练折外成绩为 4319/4755，但来自有已知提取问题的格式第一版，
且是在同一折外集上选 alpha 后的开发指标。修复后为 4314，验证反而下降。
因此不能把 4319 单独拿来宣称最终模型提升，也不能用“覆盖更多等式”替代准确率比较。

## 1. 原计划及选型

运行前保存 [ROUND8_PLAN.md](ROUND8_PLAN.md)。冻结第七轮解析器，比较：
候选算术冲突惩罚、按答案组聚合的惩罚、复算左值支持另一答案、更保守的数值 head 门控，
以及候选惩罚与复算支持的组合。

权重 {0,0.05,0.1,0.2,0.4,0.8}，共 57 个训练折外配置（包含重复零权重对照）。
复用第七轮按题划分的三折分数：种子 20261018，每道题四个候选保持一起，
各折的模型和标准化只在该折训练部分拟合。每族先以训练折外正确数选一个配置，
并列优先较少改变原选择、较小权重，然后才打开验证集比较五个冻结结果与原模型。

| 族 | 训练折外选中配置 | 正确 /4755 | 修复 / 新错（对第七轮） |
|---|---|---:|---:|
| candidate_penalty | `{"name": "candidate_penalty", "penalty": 0.0}` | 4310 | 0 / 0 |
| group_penalty | `{"name": "group_penalty", "penalty": 0.05}` | 4311 | 1 / 0 |
| repair_support | `{"name": "repair_support", "repair": 0.8}` | 4315 | 5 / 0 |
| selective_gate | `{"name": "selective_gate", "gate": "baseline_selected_conflict"}` | 4311 | 1 / 0 |
| penalty_and_repair | `{"name": "penalty_and_repair", "penalty": 0.0, "repair": 0.8}` | 4315 | 5 / 0 |

H1 候选惩罚未获支持：选中权重为零。
H2 答案组惩罚仅有 1 道训练折外净收益，未转化成验证收益。
H3 复算支持有 5 道训练折外净收益、无新增折外错误，但未转化成验证收益。
H4 更保守的切换条件在折外多对 1 题，验证正确数不变。
组合模型选中零惩罚，退化为单纯复算支持，说明本轮两种信号没有显示额外互补收益。

复算证据采用最后成功提取的错误等式：右值与本候选官方解析答案一致，
复算左值精确等于其他候选答案时提供支持。不按 ID 查表，也不读取参考答案进行推理。
此条件仍不保证题意正确，最后提取等式也不保证是真正末步。

## 2. 格式扩展与失败修复

原定五族均未提高验证成绩后，写入 [ROUND8_AMENDMENT.md](ROUND8_AMENDMENT.md)，
加入数字粗体/数学字体、转义百分号、算式内部金额符号的有限归一化。
训练三折比较 alpha={0.3,0.1,1}，冻结一个 alpha 再在全训练集拟合。
比较全量新冲突门控 format_gate，以及仅新增冲突题使用新 head 的 incremental_gate。

第一版 42 个构造用例通过，但训练样本抽查发现三类缺陷：

- 列表 `- $20 × 30 = $600` 的项目符号被合并成负号，出现假冲突。
- Unicode 减号归一化顺序错误，使 `$20 − $6 = $14` 被截成 `6=14`。
- `8/25 × 100 = 32%` 中结果单位有百分数/比例歧义，不能简单按比例归一化后判错。

v2 在金额处理前统一运算符，仅在数值操作数后的算符或等号后去除金额符号，
处理显式格式化的列表标记，将等号右侧百分比单位歧义视为未知。
旧 32 个边界案例连同新增案例共 49 个构造检查通过，再重跑相同网格。
这些检查验证已覆盖边界，不证明所有自然语言算式都可正确提取。
最初连续粗体数字的贪婪匹配也曾导致构造检查失败，已在第一版训练前修正。

第一版选中 alpha=0.1；v2 选中 alpha=1。两版各保存 9 条折内配置评分。
这是依据已完成实验和训练样本进行的适应性补充，不是全轮预注册。
失败的第一版源文件、checkpoint、分数和训练错例均保留。

| 版本 | 验证候选中有可检查等式 /3192 | 冲突题 /798 | 最终答案正确但有冲突标记 | 最终答案错误且有冲突标记 |
|---|---:|---:|---:|---:|
| 第七轮解析器 | 2361 | 49 | 13 | 55 |
| round8-format | 2541 | 80 | 53 | 79 |
| round8-format-v2 | 2554 | 87 | 52 | 77 |

新解析器覆盖更广，但最终答案正确候选中的冲突标记也增加。
这不是严格的解析器误报率：最终答案正确仍可能含错误中间步、单位歧义或提取噪声。
v2 修复了已识别缺陷，仍没有让选择准确率提高；本轮不部署该解析器。

## 3. 全部冻结验证结果

所有修复/新增错误均相对第七轮 747/798；“选择变化”包括在多个正确候选间切换。
训练折外分数参与了参数选择，不能当成独立泛化成绩。

| 方案 | 训练折外 /4755 | 验证 /798 | 修复 / 新错 | 选择变化题数 |
|---|---:|---:|---:|---:|
| round8 / incumbent | 4310 | 747 | 0 / 0 | 0 |
| round8 / candidate_penalty | 4310 | 747 | 0 / 0 | 0 |
| round8 / group_penalty | 4311 | 747 | 0 / 0 | 0 |
| round8 / repair_support | 4315 | 747 | 0 / 0 | 0 |
| round8 / selective_gate | 4311 | 747 | 0 / 0 | 1 |
| round8 / penalty_and_repair | 4315 | 747 | 0 / 0 | 0 |
| round8-format / format_gate | 4319 | 747 | 0 / 0 | 9 |
| round8-format / incremental_gate | 4314 | 747 | 0 / 0 | 6 |
| round8-format-v2 / format_gate | 4314 | 745 | 0 / 2 | 14 |
| round8-format-v2 / incremental_gate | 4307 | 746 | 0 / 1 | 9 |

按照先前规则，验证必须超过 747，且对应训练折外不低于 4310，才能晋级。
没有方案满足，保留原模型。v2 incremental_gate 的折外也低于 4310。

## 4. 为什么没有继续提高验证准确率

当前仍有 51 道验证错题，其中仅 7 道处在旧解析器发现算术冲突的题中，
其余 44 道没有这样的信号。算术门控能影响的错误范围有限。
旧复算支持覆盖 9 道验证题，其中 8 道支持到正确答案，这 8 道原模型已经全部答对；
另外 1 道的证据没有支持到正确答案。因此本轮的正确复算证据缺少新的纠错目标。
这也是没有在观察验证后继续扩大支持权重网格的原因。

更高覆盖改变了一些候选选择，但大量变化发生在同为正确或同为错误的候选间。
格式 v2 全量门控新增 2 个验证错误、没有修复旧错；增量门控新增 1 个、没有修复旧错。
候选答案抽取、题意误读、单位关系等仍是剩余问题，纯算术正确性不足以解决。
这些是开发集上的描述性证据，不构成关于所有模型或其他数据集的普遍结论。

## 5. 资源与完整性

本机 Intel Core i5-11400H，四线程，Python 3.12.14、NumPy 2.5.3；仅标准库与 NumPy。
三阶段训练/选择脚本累计计时 61.57 秒，不含检查、复算、报告及人工分析。
共 57 个规则折外配置、18 条格式模型折内配置评分、10 个冻结验证输出（含对照）。

每个预算测量为新预测进程＋独立官方评分进程，共享 30 秒截止时间。
资产包括保留的第七轮双模型、新 head（如适用）及所有配置；没有按压缩体积折算。

| 输出 | 全部推理资产 MiB | 新进程预测＋评分秒 |
|---|---:|---:|
| round8 / incumbent | 1.600 | 1.711 |
| round8 / candidate_penalty | 1.600 | 2.124 |
| round8 / group_penalty | 1.600 | 2.090 |
| round8 / repair_support | 1.600 | 2.061 |
| round8 / selective_gate | 1.600 | 2.402 |
| round8 / penalty_and_repair | 1.600 | 2.147 |
| round8-format / format_gate | 2.400 | 1.727 |
| round8-format / incremental_gate | 2.400 | 2.664 |
| round8-format-v2 / format_gate | 2.400 | 1.722 |
| round8-format-v2 / incremental_gate | 2.400 | 2.738 |

全部十个输出通过官方评分、合法返回值、新 ID、bank 大小、候选重排、题目逆序、
空输入、16 MiB 和本地 30 秒检查。官方原始文件、训练/验证数据、原模型和旧源代码哈希未变。
**本地完整验证集测量不等于参考 Xeon Platinum 8457C 上完整测试集的资格认证。**
本轮没有读取测试输入或测试标签，没有测试评分，也没有使用外部数据或预训练模型。

## 6. 复现与产物

命令见 [REPRODUCE.md](REPRODUCE.md) 的 Round 8 部分。

- [初始假设与固定网格](ROUND8_PLAN.md)、[补充与修复记录](ROUND8_AMENDMENT.md)。
- [57 组折外规则成绩](code/runs/round8/oof-selection.json)。
- [10 个验证输出汇总](code/runs/round8/validation-summary.csv)。
- [剩余错误覆盖诊断](code/runs/round8/remaining-error-diagnostics.json)。
- [格式第一版结果](code/runs/round8-format/experiments.json)、[v2 结果](code/runs/round8-format-v2/experiments.json)。
- [新增冲突训练样本](code/runs/round8/format-flagged-training-cases.json)。
- [完整性与源文件哈希](code/runs/round8/final-integrity.json)。
- 各 `code/runs/round8*-verification/` 保存官方评分、预算与接口记录。

最终仍推荐 [第七轮模型](ROUND7_RESULTS.md)。失败方案不能在汇总中被当作新的最佳模型。
最终课程报告排版、公开仓库/checkpoint 链接、最终测试评估与提交尚未完成。
