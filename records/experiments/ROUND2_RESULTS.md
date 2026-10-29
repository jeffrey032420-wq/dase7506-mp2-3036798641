# 第二轮模型改进（2026-10-14）

当前推荐：`code/method_round2.py`，配套 checkpoint 为
`code/runs/round2/model_bundle/`。第一轮代码和 checkpoint 保留用于对照。

## 实验方法与选型

第一轮对每个候选独立回归正确性。第二轮比较两种训练目标：

- centered：在每道题内对特征和标签去均值，学习候选之间的差异。
- pairwise：枚举同一题中正确候选与错误候选的配对，学习令正确候选得分高出 1。
  每题的所有配对共享相同总权重；四个候选都正确的题没有排序信号，跳过。

特征方面，从训练集拟合标准化参数，将原始 1024 维向量通过固定种子的随机矩阵
投影到 96 维。该矩阵自行生成，不来自额外预训练模型。
nonlinear 模式加入 ReLU 与平方特征；context 模式再加入投影向量与同题均值的乘积、
以及与同题均值的平方距离。所有投影矩阵和拟合统计量都保存在 checkpoint 内。

搜索先将训练题按 seed 20261014 划分为 3,804 拟合题和 951 留出题。
在这一划分上为 3 种特征 × 2 种目标分别从 5 个 alpha 中选择参数。
随后在全部训练集上重训 6 个方案，用官方验证集选择方案。数据划分按整道题进行，
同题四个候选不会分到两边。整个流程未读取测试集用于训练、选型或评分。

## 官方验证集结果

| 方法 | alpha | 答对数 / 798 | 准确率 |
|---|---:|---:|---:|
| 第一轮最佳 | 1 | 723 | 90.60% |
| linear + centered | 0.003 | 719 | 90.10% |
| linear + pairwise | 0.03 | 728 | 91.23% |
| nonlinear + centered | 0.3 | 731 | 91.60% |
| nonlinear + pairwise | 0.3 | 736 | 92.23% |
| context + centered | 0.003 | 725 | 90.85% |
| **context + pairwise** | **0.3** | **744** | **93.23%** |

新方案比第一轮净增 21 题，提升 2.63 个百分点：修正 26 题，新增 5 道错误。
在 355 道至少出现两个不同可解析答案的验证题中，从 78.87% 提升至 84.79%。
官方评分文件：`code/runs/round2/validation-score.json`。

同为 alpha=0.3 的 nonlinear 两组对比中，pairwise 比 centered 多答对 5 题。
同为 pairwise、alpha=0.3 的 nonlinear/context 对比中，context 多答对 8 题。
其他跨 alpha 的对比不能单独归因于训练目标或特征。

## 稳定性与误差

固定两轮各自选定的配置，在训练集上另外做三次整题 80/20 划分：

| 划分种子 | 第一轮 / 951 | 第二轮 / 951 | 净增 |
|---|---:|---:|---:|
| 31 | 859 | 867 | 8 |
| 73 | 858 | 867 | 9 |
| 101 | 858 | 868 | 10 |

这些留出集相互重叠，只用于诊断稳定性，不能当作三个独立外部测试。
验证集配对 bootstrap 的差值区间约为 [1.25, 4.01] 个百分点，但未校正模型选择，
不能据此宣称独立测试上的统计显著提升。

验证集中仅有一个正确候选的 117 道题是主要难点：旧模型答对 48 题，新模型答对 70 题。
仍有 47 道此类题答错。54 道全部剩余错题和各候选得分保存在
`code/runs/round2/validation-errors.json`，仅供开发分析，不进入推理代码或模型资产。
例如，配对人数题的错误解答把配对数当作配对人数，算术等式正确但语义错误；
现有特征尚不能稳定识别这种错误。另有题意与参考标签可能存在歧义的例子，
需在报告中区分“符合官方数值标签”和“数学推理有效”，保持评分规则不变。

按最高与次高候选得分差分为四组，准确率并非单调上升。
同答案的多个候选也会影响这种差值，因此它不能直接视作可靠概率。

## 资源与验证

- 初次第二轮搜索及拟合约 17.88 秒；额外三次稳定性实验约 11.11 秒。
- Intel Core i5-11400H，本次新进程验证集预测加独立评分约 0.90 秒，总线程限制 4。
- 推理资产共 838,847 字节，约 0.80 MiB；包含配置、权重、投影和标准化统计量。
- 新 ID、1/7/23 题小批量、题目重排、候选重排、空输入与官方进程输出一致性均通过。
- 这是本机验证集测量，不代替参考 CPU 上完整测试集的 30 秒资格测量。

## 复现

先按 REPRODUCE.md 安装环境，以下命令从 `code/` 运行：

```powershell
$env:OMP_NUM_THREADS = '4'
$env:OPENBLAS_NUM_THREADS = '4'
$env:MKL_NUM_THREADS = '4'
$env:NUMEXPR_NUM_THREADS = '4'
.\.venv\Scripts\python.exe predict.py --method method_round2.py --checkpoint runs/round2/model_bundle --split validation --output runs/round2/validation-predictions.json
.\.venv\Scripts\python.exe score_predictions.py --split validation --predictions runs/round2/validation-predictions.json --output runs/round2/validation-score.json
```

独立重训：

```powershell
.\.venv\Scripts\python.exe train_round2.py --output runs/reproduced-round2
```

分析和接口检查：`python analyze_round2.py`。
三个固定配置的训练集留出实验：`python robustness_round2.py`。
后两条命令默认使用已有 `runs/round2/` 目录。

当前仍为开发版本。继续改进优先研究答案分组、语义错误识别和置信度评估；
报告、最终冻结、正式测试和提交尚未完成。
