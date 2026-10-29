# 第16–19轮：新监督、残差学习、结构树与固定融合

## Material Passport

- Origin Skill: academic-research-suite / experiment-agent，同任务协作。
- Origin Date: 2026-10-21。
- Verification Status: VERIFIED_LOCAL_VALIDATION，未使用测试。
- Version Label: rounds16_19_results_v1。

## 结论

**没有超过748/798（93.7343%），保留Round11。** 本批确实训练了新模型；
训练OOF最高4359/4755，但该提升没有迁移到验证，不能称为准确率突破。
所有训练配置先冻结，再集中比较7个输出，全部通过官方评分、接口和本地资源审计。
测试输入、参考、预测与分数均未访问。

| 冻结输出 | 训练OOF /4755 | 验证 /798 | 修复 / 新错（相对Round11） |
|---|---:|---:|---:|
| round17_linear | 4342 | 747 | 3 / 4 |
| round17_collapsed_bilinear | 4343 | 747 | 3 / 4 |
| round17_active_bilinear | 4327 | 747 | 2 / 3 |
| round18_binary | 4331 | 744 | 3 / 7 |
| round18_lambdarank | 4356 | 741 | 5 / 12 |
| round16_selected | 4317 | 748 | 0 / 0 |
| round19_selected | 4359 | 748 | 3 / 3 |

## 1. 假设、实际训练与失败

### Round16：从训练参考步骤学习最终运算

4696条训练参考有中间计算标记；严格提取后4387/4755有可用教师终运算，
12037/19020候选有明确、精确成立且产出官方终值的运算。折内TF-IDF和固定四类
logistic训练只读训练参考；推理不访问任何参考或题目ID。12条权重/置信门槛配置
选择gate0、strength0.2，OOF4317，5修复/1新错，三折均正增；验证保持748。
运算分类准确率56.46%，多数类33.21%，是弱预测器。逐例审计发现等价计算程序
可以有不同终运算，部分收益还来自候选运算可提取性，不能全部归于题意理解。
初次导出曾因NumPy整数无法JSON序列化失败；改成Python整数后原网格原样重跑。
下一步先做匹配覆盖的knownness消融，不继续扩大分类器网格。
详见[分支复盘](code/runs/round16-program/FINDINGS.md)。

### Round17：从头训练线性与题目交互残差

三折各自拟合词表、标准化和context offset；残差拟合不把跨折基线OOF用作训练输入，
避免held标签经基线传入训练。原4模型×2强度共8配置；40epochs、固定种子和Adam。
线性4342，原双线性4343。检查发现原双线性投影塌缩，不能把其收益称作条件交互。
先写补充计划，修正初始化和按维度平均的L2，再训练2decay×2强度，活跃交互4327。
三个冻结输出验证均747。线性修复68个训练旧错，却新增39错，其中31个是多正确候选题；
提示需要检验集合监督的鲁棒性，而不是继续增加rank或epochs。
曲线、泄漏保护、塌缩证据与修正版见[训练报告](code/runs/round17-bilinear/TRAIN_ONLY_REPORT.md)。

### Round18：确定性结构特征的非线性排序

636维：文本/一致性、精确算术、终运算、来源图、答案数值、题目线索及候选间相对特征。
不把原始Embedding或基线分数输入新树。binary/LambdaRank×3/7叶×100/300轮，
各3折；5融合权重共40条OOF。基线OOF只在训练后的输出融合使用。
LambdaRank4356（93修复/50新错），binary4331，但验证分别741、744。
全模型纯树弱于原模型，OOF主要收益来自融合，验证却新增更多错。
答案整数性/大小等特征的重要性不等于推理能力的因果证据，下一轮需固定学习器删组消融。
详见[结构树复盘](code/runs/round18-tree/LEARNING.md)。

### Round19：两个冻结家族的互补性

在任何中央验证反馈前固定树权重0.25/0.5/0.75，仅训练OOF选型。
线性独对85、树独对99，但等权仅比树净增3题（45修复/42新错）；
三折相对纯树+10/+2/−9，稳定性不足。对Round11为63修复/17新错、4359。
验证修复3题也新增3错，仍748，未据此再扫融合权重。
所有资产包含两份完整家族和重复的原模型，详见[融合复盘](code/runs/round19-fusion/LEARNING.md)。

## 2. 预算、完整性与证据边界

| 输出 | 全部解压资产 MiB | 新预测进程＋独立评分秒 |
|---|---:|---:|
| round17_linear | 1.6280 | 2.387 |
| round17_collapsed_bilinear | 1.7382 | 2.327 |
| round17_active_bilinear | 1.7382 | 2.376 |
| round18_binary | 1.8806 | 7.566 |
| round18_lambdarank | 1.7050 | 7.487 |
| round16_selected | 1.8727 | 2.977 |
| round19_selected | 3.3330 | 8.945 |

平台Intel Core i5-11400H，Python3.12.14、NumPy2.5.3、SciPy1.18.1、
LightGBM4.7.0、scikit-learn1.9.1。训练任务各1线程；正式预算审计在训练停止后
依次运行、总线程上限4。所有嵌套模型、词表、投影、统计量与配置计入资产；
NPZ按解压成员大小计数，不用压缩文件尺寸规避16MiB。
七输出全部通过官方结果一致、合法Python整数、不同bank大小、新ID、候选重排、
题目逆序、空输入、资产限制及本地共享30秒检查。原官方工具和训练/验证数据，
Round7–15源码、旧模型及本批冻结资产哈希完整性通过。
本地完整验证计时不能证明参考Xeon Platinum8457C完整测试资格。

本批共67条训练配置记录，包含重复控制；同一OOF和验证在多轮被反复使用，
选中最高OOF和本表验证均是开发证据。OOF明显提升而验证下降的原因可能包括
选择偏差、训练规模和样本差异、脆弱特征，不应仅凭这些分数断言某一种原因。
全部配置见[all-training.csv](code/runs/round16-19/all-training.csv)，
预验证冻结与哈希见[frozen-selection.json](code/runs/round16-19/frozen-selection.json)，
官方预算/接口记录见[results.json](code/runs/round16-19-verification/results.json)。

## 3. 下一实验入口

用户要求无提升继续尝试，因此另开三个有边界的训练实验：Round20正确集合损失，
Round21删组消融，Round22候选中心化Embedding的局部近邻学习。
这些方案在各自拟合前写计划，只用训练监督；本报告不预报其收益。
每轮保留错误和成功案例、全表、源码/资产哈希和接受/停止标准。
具体经验与下一入口见[lessons.json](code/runs/round16-19/lessons.json)及
[next-experiment.json](code/runs/round16-19/next-experiment.json)。
最终10页报告、公开代码/checkpoint链接、最终测试和GitHub issue提交仍待完成。
