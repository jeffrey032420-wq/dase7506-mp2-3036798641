# Round115：公开配方核对与四格匹配实验

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。计划保存后先审计训练输入，再冻结训练源码；四候选冻结后全部官方验证。

## 预设假设与固定配置

H1：按公开源码定义对齐题目数值与局部算术解析会改变残差可用信号。H2：残差用same_fit基础分数训练可能与nested_oof不同；两种都只在当前fit训练，outer-held始终排除。本轮固定子集增强、基础lambda0.01、残差lambda0.01。原751使用残差0.1，因此legacy/nested_oof应重现750而非751。

|特征|残差margin|基础OOF/4755|完整OOF/4755|训练回代/4755|官方验证/798|单正确/117|修复751错/新增错|资产MiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|nested_oof|4380|4390|4504|750|77|0/1|0.02591|1.866|
|legacy|same_fit|4380|4390|4507|749|77|0/2|0.02591|1.909|
|aligned|nested_oof|4380|4397|4510|751|78|1/1|0.02592|2.087|
|aligned|same_fit|4380|4392|4516|751|78|1/1|0.02591|2.122|

本批最佳round115_aligned_same_fit：751/798（94.1103%）。未超过751，保留Round109研究候选；尚未测试。
原已测Round79（验证749、历史测试368/467）模型与最终指针不变。当前751研究模型未跑最终测试。

## 训练输入审计

4755题19020候选中，题目数字列表改变45题，局部11维向量改变7673候选；可检查算式候选由13932变为13141，含不一致算式候选由322变为314。这些覆盖差异不自动代表特征更好。人工算式、受限幂、变量边界、分数、Markdown、舍入与百分比拒绝样例通过。审计不用标签/验证/测试。

## 两因子匹配效应

|起点|终点|训练OOF变化|验证修复/新增错|验证净变化|
|---|---|---:|---|---:|
|legacy/nested_oof|aligned/nested_oof|+7|2/1|+1|
|legacy/same_fit|aligned/same_fit|+2|3/1|+2|
|legacy/nested_oof|legacy/same_fit|+0|0/1|-1|
|aligned/nested_oof|aligned/same_fit|-5|0/0|+0|

解析流程包含题目分词与局部算术两部分变化，不能单独归因于幂运算；分数变化只支持本固定配置下的条件效应。验证被长期开发复用，不是新的独立泛化证明。

## 可靠性、限制与复现

29次新拟合（aligned基础13、残差16），worker25.107秒、4线程、父进程600秒硬上限；legacy基础复用108/109 SHA核对资产，legacy/nested_oof的参数1e-12、OOF/验证分数1e-10复现原750。每题权重归一、仅fit完整组scaler、梯度/收敛、零残差、缓存导出、严格候选重排1e-8、题序、新ID、变bank、空输入、Python整数与同答案同分通过。

每个最终候选独立fresh官方validation预测+评分，总计≤30秒；完整解压资产包括嵌套基础权重、scaler及config≤16MiB。本机验证计时不等于参考Xeon完整测试资格。

公开参考静态来源为CaspianW/dase7506-mp2的src/train_surface.py、src/train.py、src/arithmetic_features.py与src/question_operation_features.py，URL/只读txt快照存reference_audit_20261028。独立实现按定义对齐，未执行外部源码、未引入外部权重/数据，也未用对方自报分数选择参数。基础求解器SciPy而非sklearn、保存scaler而非折入权重、并列选择规则仍有差别；不称最终提交方法或公开成绩的完整复现。

历史自身及他人测试汇总已知并披露；本轮未访问/哈希/预测/评分测试。按用户2026-10-28确认，每批最终候选都官方验证；测试留到方法冻结后。这四个配置结束，不按验证输赢追加参数。

复现：code目录依次运行audit_round115_features.py、train_round115_reference_alignment.py、evaluate_round115_reference_alignment.py。已有输出目录拒绝覆盖。证据：runs/round115-feature-audit/audit.json，runs/round115-reference-alignment/result.json、nested-partitions.json、pair-audit，runs/round115-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json和官方进程日志。
