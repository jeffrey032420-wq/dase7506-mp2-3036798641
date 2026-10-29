# Round114学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成四配置后的描述性比较。

## 每折相对原0.01控制

```json
[
  {
    "fold": 0,
    "anchor_lambda": 0.003,
    "net_vs_0p01": 1
  },
  {
    "fold": 0,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 0,
    "anchor_lambda": 0.03,
    "net_vs_0p01": -1
  },
  {
    "fold": 0,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -13
  },
  {
    "fold": 1,
    "anchor_lambda": 0.003,
    "net_vs_0p01": -4
  },
  {
    "fold": 1,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 1,
    "anchor_lambda": 0.03,
    "net_vs_0p01": -5
  },
  {
    "fold": 1,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -4
  },
  {
    "fold": 2,
    "anchor_lambda": 0.003,
    "net_vs_0p01": -9
  },
  {
    "fold": 2,
    "anchor_lambda": 0.01,
    "net_vs_0p01": 0
  },
  {
    "fold": 2,
    "anchor_lambda": 0.03,
    "net_vs_0p01": 1
  },
  {
    "fold": 2,
    "anchor_lambda": 0.1,
    "net_vs_0p01": -1
  }
]
```

基础正则0.003/0.01/0.03/0.1的完整train OOF分别4380/4392/4387/4374。原0.01仍是这四点的训练OOF最好；不能仅因正则更强、回代差距更小就称泛化更好。

局部残差相对各自基础模型的train OOF增益分别+11/+12/+7/+12。这支持残差在本轮四条件下具有增量，但不意味着总能超过原751。本轮改变基础参数同时重新匹配残差，避免分数尺度与旧残差错配。

若验证和训练OOF排序不一致，完整报告，不能把验证赢家当成稳定泛化证明。本轮结束，不继续插值密集扫lambda；后续应优先训练OOF中尚未覆盖的题意数量关系和末结果/答案联系，先提出可复现的新信息特征，再做小型匹配消融。751与所有失败/持平配置保留，测试未运行。
