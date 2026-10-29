# Round133：跨候选错误传播复算支持

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；12新拟合、4官方validation。

完整123固定，local/propagated/both分别4/4/8维残差，λ.1，same-fit完整父margin、原折/fit-only尺度/每题pair权重。整链复算差异覆盖8个原错、3个超出local，正确/错误接收支持答案组75/6；候选解析与123全train逐记录一致。跨候选支持不是题意证明，歧义producer/来源冲突拒绝。

|模式|训练OOF/4755|训练修复/新增|三折|验证/798|验证修复/新增|KiB|fresh秒|
|---|---:|---|---|---:|---|---:|---:|
|control|4404|0/0|[0, 0, 0]|754|0/0|62.01|3.681|
|local|4404|0/0|[0, 0, 0]|754|0/0|63.03|4.531|
|propagated|4404|0/0|[0, 0, 0]|754|0/0|63.03|4.625|
|both|4404|0/0|[0, 0, 0]|754|0/0|63.12|4.481|

未严格胜过(754,4404)，保留123。

12拟合worker89.082秒，4总线程，600秒硬限。原父OOF、缓存、梯度/重复pair/每题权重/fit-only尺度、全训练导出/零修正/重排等接口和源/计划/父新资产SHA通过。全部资产≤16MiB、fresh完整validation预测+独立评分≤30秒，参考Xeon未认证。

三个新版本按预先名单全部冻结后测试；本脚本未执行test，test不用于拟合或本批开发选择。长期自适应开发、已知test汇总披露，不作独立显著/稳定泛化/因果主张；11项解释边界沿用前轮，报告全部配置/分母/折与失败。

复现audit_round133_propagated_repair.py、train_round133_propagated_repair.py及--evaluate，再run_frozen_tests_round133.py；旧证据拒绝覆盖。


# Round131：三个复算支持版本的冻结测试

## Material Passport

academic-research-suite / experiment-agent；2026-10-29。三个候选在第一项新test读取前统一冻结，名单与训练方案相同。0新拟合、每项一次fresh完整预测及独立官方评分。

|模型|训练OOF/4755|验证/798|官方test/467|test准确率|相对123|全部KiB|预测+评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|
|原123（已有记录）|4404|754|390|83.5118%|0|—|—|
|round133_local|4404|754|391|83.7259%|+1|63.03|3.334|
|round133_propagated|4404|754|392|83.9400%|+2|63.03|3.378|
|round133_both|4404|754|392|83.9400%|+2|63.12|3.301|

开发选择在test前已确定为保留原123，没有按以上test分数更换；选择记录runs/round133-evaluation/selection-before-test.json。

用户最近要求最终候选都可测试，因此本批全报告，不按前面候选的test分数停止、调参或增加名单。无test逐题分析、训练或规则设计；如后续按test分选型，需要披露测试集参与选择，最高分不是独立最终估计。历史测试汇总已知、长期自适应开发继续披露，不作稳定或显著提升主张。

CPU：11th Gen Intel(R) Core(TM) i5-11400H @ 2.70GHz；总4线程；每项递归未压缩资产≤16MiB，fresh完整test预测+评分≤30秒；参考Xeon未认证。源/全部资产/开发证据前后SHA通过。完整命令/日志/官方JSON/冻结源/参数/硬件见final_evaluation/round133-all-test-20261029，原模型与79主交付保留，未公开提交。
