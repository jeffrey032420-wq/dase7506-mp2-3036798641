# Round113学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；预定四配置完整结果后的描述性分析。

## 匹配差异（正确题数）

```json
{
  "train_oof": {
    "early_minus_fixed_raw": 48,
    "early_minus_fixed_pca": 13,
    "pca_minus_raw_fixed": 8,
    "pca_minus_raw_early": -27
  },
  "validation": {
    "early_minus_fixed_raw": 18,
    "early_minus_fixed_pca": -1,
    "pca_minus_raw_fixed": 13,
    "pca_minus_raw_early": -6
  }
}
```

## 内部选择的epoch

|阶段|输入|选定epoch|实际selector轮数|inner-held最佳正确数|
|---|---|---:|---:|---:|
|0|raw|4|24|575|
|0|pca|22|42|573|
|1|raw|6|26|578|
|1|pca|10|30|569|
|2|raw|28|48|579|
|2|pca|16|36|570|
|全训练|raw|10|30|880|
|全训练|pca|6|26|867|

## 拟合差距

|输入/控制|回代−OOF题数|
|---|---:|
|raw/fixed|458|
|raw/early|206|
|pca/fixed|199|
|pca/early|28|

缩小回代与OOF差距本身不等于准确率提升，必须同时比较OOF与验证。PCA丢弃的方向可能含判别信息；若降维后更差，不应继续盲目压缩。内部选择的epoch不同是合法训练选择，不是从官方验证挑epoch。

下一轮依据：先看以上早停在两种输入中是否方向一致，再决定保留控制；若早停和瓶颈都未改善，不继续扩大同一神经网络网格，应返回已有效的答案组增强与局部残差，以训练折外净修复为依据引入新证据。完整四配置保留，不因结果继续扫epoch/正则。本轮未运行测试，751与原冻结最终模型保留。
