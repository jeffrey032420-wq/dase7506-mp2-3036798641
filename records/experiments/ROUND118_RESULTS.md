# Round118：算术解析 × 最终答案证据

## Material Passport

academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。16次新残差拟合、4最终候选全部官方验证。

## 假设与控制

H1：两个已有信号的组合可能具有互补增量；H2：也可能相互抵消。固定原109题目数值分词/子集增强anchor lambda0.01、残差lambda0.1、嵌套OOF margin。四格只切换局部算术legacy/aligned和4维最终答案证据；三旧条件参数/OOF/验证分数均数值重现，不把115的不同正则/题目分词当同配置对照。

|局部算术|最终答案证据|维数|训练OOF/4755|训练回代/4755|官方验证/798|分歧/355|单正确/117|修复751错/新增错|资产KiB|fresh秒|
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
|legacy|False|22|4392|4510|751|308|78|0/0|26.83|2.080|
|legacy|True|26|4398|4514|751|308|78|1/1|26.92|2.102|
|aligned|False|22|4395|4515|750|307|77|0/1|26.83|2.198|
|aligned|True|26|4399|4522|750|307|78|1/2|26.92|2.764|

本批最佳round118_legacy_final：751/798（94.1103%）。

## 固定条件测试准入

计划先于训练规定：官方验证>751、训练OOF>4392、全部资源/接口核验通过，才选唯一候选冻结测试。多候选按验证、OOF、资产、名称依次选择；不用测试总分选。

无人满足全部条件，本批不触发测试。原751模型与冻结测试记录保留，不因训练信号或验证持平而事后放宽门槛。

## 四格条件效应

```json
[
  {
    "from_condition": [
      "legacy",
      false
    ],
    "to_condition": [
      "aligned",
      false
    ],
    "train_oof_delta": 3,
    "fold_deltas": [
      1,
      4,
      -2
    ],
    "validation_delta": -1,
    "validation_fixed": 0,
    "validation_new_errors": 1
  },
  {
    "from_condition": [
      "legacy",
      true
    ],
    "to_condition": [
      "aligned",
      true
    ],
    "train_oof_delta": 1,
    "fold_deltas": [
      -1,
      3,
      -1
    ],
    "validation_delta": -1,
    "validation_fixed": 1,
    "validation_new_errors": 2
  },
  {
    "from_condition": [
      "legacy",
      false
    ],
    "to_condition": [
      "legacy",
      true
    ],
    "train_oof_delta": 6,
    "fold_deltas": [
      3,
      0,
      3
    ],
    "validation_delta": 0,
    "validation_fixed": 1,
    "validation_new_errors": 1
  },
  {
    "from_condition": [
      "aligned",
      false
    ],
    "to_condition": [
      "aligned",
      true
    ],
    "train_oof_delta": 4,
    "fold_deltas": [
      1,
      -1,
      4
    ],
    "validation_delta": 0,
    "validation_fixed": 1,
    "validation_new_errors": 1
  }
]
```

## 资源、来源与复现

16次新残差拟合，0新基础拟合；四线程worker26.451秒，父进程600秒硬上限。继承全训练/outer/inner基础参数、折划分、OOF及旧控制资产逐SHA核对；mean/scale/weight1e-12、OOF/验证分数1e-10重现三个旧条件。逐pair来源/归一权重/anchor margin与旧审计一致；scaler只fit当前fit原始完整组。

梯度/收敛、重复pair、零残差、导出、严格候选重排1e-8、题序/新ID/变batch/空输入/Python整数/同答案同分均通过。每个候选完整解压资产含基础/残差权重和scaler/config≤16MiB，fresh官方validation预测+独立评分≤30秒。这是本机验证资源记录，参考Xeon资格未认证。

历史自身及公开他人测试总分已知；本轮训练/验证未读取测试输入/参考/预测/评分，长期train/validation适应性开发不作独立泛化声明。旧方法/模型/数据/官方parser/scorer均未改；不存在外部训练数据/权重或评估时API调用。

复现：code目录train_round118_evidence_factorial.py，再evaluate_round118_evidence_factorial.py。已有目录拒绝覆盖。证据：runs/round118-evidence-factorial/result.json、nested-partitions.json、pair-audit；runs/round118-evaluation/frozen-before-validation.json、all-results.json、matched-effects.json、integrity.json、selection-before-test.json与官方日志。
