# Rounds135–136：数量关联与前缀修正的完整记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；2轮、20新拟合、7次官方validation（含2次父控制）、5个新最终候选统一按批冻结后各一次官方test。

|候选|训练OOF/4755|验证/798|test/467|
|---|---:|---:|---:|
|原123控制|4404|754|390（已有）|
|round135_label|4407|753|390|
|round135_role|4404|754|390|
|round135_both|4407|752|389|
|round136_label|4408|753|389|
|round136_both|4407|752|388|

## 结论与后续决策

**没有新增验证或测试最高分。** 开发身份仍为123，validation754/798；此前132以及133传播/组合的已观察test最高392/467保持。两轮新输出全部保留但不晋级，无公开提交。

135增加精确邻接数量标签、人名与状态，label与both OOF均4407，但validation753/752；role OOF4404、validation754。抽取仍有歧义；不能把match当正票或把mismatch当错误证明。

135纯train逐特征margin诊断定位了具体误标：目标gallons of gas与正文gallons、ounces of fudge与ounces被当冲突。136仅把严格前缀关系记unknown，全量断言其他列不变；121题变化，其中11个原错。label OOF4408、修4/新增0、三折[+2,+1,+1]，validation仍753，test389；both OOF4407、validation752、test388。

相对135，136_label在121个输入变化题上修1/新增1，净0；其余4634题重拟合后的修1/新增0带来净+1。136_both训练选择完全不变。这说明仅看训练总分会把全局拟合波动当成局部表示修复的收益；没有证据把这种修正称准确率突破。

停止继续扩展当前词面数量标签家族，不据test个题、阈值或同义词扩表重试。若开启新路线，需能补充可靠的数量角色/算式关系或提供真正不同的学习信号，先在train对照旧正确反例及fold稳定性；不要把浅词窗升级为“语义推理”声称。规则一致性修复与准确率改进分别报告。

## 资源与完整性

两轮最大完整递归未压缩资产64728字节，fresh完整validation预测+独立评分最多6.648秒、test5.099秒，CPU总4线程，符合16MiB/30秒；参考Xeon未认证。原132/133/135/136包SHA核对，原135/父源资产保持。

拟合与5次实际test均完成，每项test一次。拟合前135builder schema guard、136fixture和builder guard，以及136打包计划文件名错误都保留原源和失败记录；均未据结果改特征/重训或重跑评分。136不完整首次打包目录另存output/round136-prefix-candidates-first-run；修正文档路径后重新打包，0新预测。136包元数据复制的three状态文字已单独纠正为通用文字，实际model_count一直为2，zip与源/资产/分数保持。

test按用户既有授权全报，未用于两批拟合、调参或开发选型；长期自适应开发与已暴露test汇总披露。若最终按test分选交付版本须说明测试参与选择，不称独立最终估计。11项解释边界见逐轮记录。

## 可复核文件

- [135完整学习与失败](ROUND135_LEARNING.md)、[136配对学习与失败](ROUND136_LEARNING.md)。
- [135官方测试](FINAL_TEST_ROUND135_ALL_RESULTS.md)、[136官方测试](FINAL_TEST_ROUND136_ALL_RESULTS.md)。
- [135全部3候选推理包](output/round135-quantity-candidates.zip)、[136全部2候选推理包](output/round136-prefix-candidates.zip)。
- 训练改选逐特征贡献：code/runs/round135-train-diagnosis；135/136计划在项目根目录，原始拟合/冻结/命令/评分/监控在各runs与final_evaluation目录。
