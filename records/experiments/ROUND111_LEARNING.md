# Round111学习记录

训练比较、选择和验证顺序见ROUND111_REGULARIZATION_PLAN.md及ROUND111_RESULTS.md。

```json
[
  {
    "mode": "full",
    "lambda": 0.1,
    "fold_deltas_vs_0p1": [
      0,
      0,
      0
    ],
    "train_oof": 4392,
    "validation_correct": 751
  },
  {
    "mode": "final_evidence",
    "lambda": 0.1,
    "fold_deltas_vs_0p1": [
      0,
      0,
      0
    ],
    "train_oof": 4398,
    "validation_correct": 751
  }
]
```

两种表示都选回原0.1配置，验证仅重复复核。full的0.03/0.3/1.0训练OOF分别4390/4390/4385，低于4392；final_evidence对应4397/4394/4391，低于4398。本轮不支持围绕这四点继续盲目扫更密正则。

后续若继续，先在训练OOF错误中统计：没有可检查等式、已经算对但语义关系错误、最终答案与推理结果冲突。按这些覆盖率决定新增信息，而不是仅扩大现有参数网格。

参数改变可能使训练OOF与验证方向不同，应完整报告冲突。未入选配置不能据本轮验证反馈补测。若要研究新特征或参数，另立计划；本批到此结束，保留751与所有失败/持平配置。
