# Round113：训练内部早停与embedding瓶颈

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。预先固定2×2四配置，训练不访问验证或测试，全部epoch/模型/源冻结后验证。

|输入|训练控制|全训练epoch|训练回代/4755|训练OOF/4755|验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|raw|fixed|40|4725|4267|722|62|9/38|0.0937|1.991|
|raw|early|10|4521|4315|740|70|6/17|0.0937|1.935|
|pca|fixed|40|4474|4275|735|73|13/29|0.5376|1.975|
|pca|early|6|4316|4288|734|63|8/25|0.5376|1.953|

最佳round113_raw_early：740/798（92.7318%）。未超过751，保留第109轮研究候选。原已测Round79最终模型和历史测试记录保持。

## 训练选择与实现

小型attention宽8/4头，correct_set_mass，显式L2=0.01。每个outer-fit再分80/20；selector最多60epoch，每2epoch按inner-held正确数选择、同分取最早，连续10次未提高停止。选好epoch后，重新在整个outer-fit拟合统计/PCA并从头训练，再预测outer-held。全训练也有独立内部选择后重训。selector的模型不是部署模型，所有原题划分、曲线和epoch见partition-proofs.json、selector-progress.json。

PCA64只在当前fit的标准化embedding拟合，投影后均值/缩放也只fit；保留29其他输入量，所有PCA/统计/网络参数写入部署包。raw与pca在本轮条件下匹配比较；相对112宽度和正则也变了，不把跨轮变化单独归因于早停。

24次新拟合、四CPU线程，worker 50.178秒、900秒硬上限。PyTorch只训练，NumPy/标准库推理；训练前损失梯度、小网络导出和重排预检留档。float64原生/NumPy前向<1e-9；训练float32误差另记；缓存重载与正式严格分数重排、题序、新ID、变bank、空输入、Python整数、同组同分通过。

完整解压资产含PCA/统计/网络≤16MiB，fresh官方预测+独立评分≤30秒；训练停止后串行计时。本机验证不代表参考Xeon完整测试资格。历史自身及公开他人测试总分已知，本轮未访问/哈希/预测/评分测试；反复开发的train/validation不是独立确认。

复现：code目录train_round113_earlystop.py，再evaluate_round113_earlystop.py；已有输出拒绝覆盖。证据：runs/round113-earlystop/result.json、preflight.json、partition-proofs.json、selector-progress.json、fit-progress.json；runs/round113-evaluation/frozen-before-validation.json、all-results.json、integrity.json和各官方评分/进程日志。
