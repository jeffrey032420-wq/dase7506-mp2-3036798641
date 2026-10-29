# Round110：格式/算术消融与最终答案证据

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定四配置，训练不读取validation/test；四配置冻结后官方验证。

|模式|维数|训练三折OOF/4755|相对4392|验证/798|相对751|修复751错/新增错|单正确/117|资产MiB|fresh秒|
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
|format|6|4386|-6|746|-5|0/5|74|0.02575|1.948|
|arithmetic|16|4389|-3|749|-2|0/2|77|0.02599|1.980|
|full|22|4392|+0|751|+0|0/0|78|0.02612|2.001|
|final_evidence|26|4398|+6|751|+0|1/1|78|0.02622|1.961|

本轮最佳round110_full：751/798（94.1103%）。未超过751，保留第109轮研究候选；full重复对照不计为新提升。原已测Round79最终模型及历史测试记录保持。

训练条件：固定增强组anchor lambda0.01，残差lambda0.1。仅格式6维、仅算术16维、完整22维和新增最终答案证据26维，均重训。最终答案证据沿用早期Round11解析定义，权重由训练学习，无人工指定答案转移。所有scaler只拟合各fit完整组。

16次新残差拟合，四线程，worker 19.838秒，父进程600秒硬上限。复用第109轮嵌套anchor，重新计算inner-OOF offset并逐pair验证与原审计一致；full模式统计/权重1e-12和OOF/验证分数1e-10重现原751控制。数值梯度、重复pair、缓存导出、零残差和严格重排/题序/新ID/变bank/空输入/Python整数/同组同分通过。

完整资产包含anchor、mean/scale、残差和config，按NPZ解压保守计数≤16MiB；训练停止后，fresh官方预测与独立评分合计≤30秒。以上本机验证计时不是参考Xeon完整测试资格。

历史自身及公开他人测试总分已知；本轮不访问/哈希/预测/评分测试，不把长期开发使用的train或validation视为全新独立确认。

来源延续CaspianW固定anchor与局部算术残差思想（见第109轮计划的源码链接），本轮为自行实现的匹配消融与旧最终答案特征重用，没有引入外部代码/权重/数据。

复现：code目录train_round110_residual_ablation.py，然后evaluate_round110_residual_ablation.py；已有输出目录拒绝覆盖。证据：runs/round110-residual-ablation/result.json、fit-progress.json、nested-offset-proofs.json、pair-audit；runs/round110-evaluation/frozen-before-validation.json、all-results.json、integrity.json和所有官方评分/进程日志。
