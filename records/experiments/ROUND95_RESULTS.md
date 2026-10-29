# Round95：精确分解成对Gram中的正确类与错误类协方差

Material Passport: academic-research-suite / experiment-agent；2026-10-27；VERIFIED_LOCAL_VALIDATION。

**全部6个新输出均未超过749/798（93.8596%），保留Round79。** 六配置在本批验证前固定；全部参数仅用所给train拟合，无外部数据或预训练权重。
没有新OOF或持出筛选，全train回代仅作描述；validation复用明确用于自适应开发，不称无偏或独立泛化。

## 先提出假设与精确分解

原等题权成对平方目标的Gram可精确写为`G=Gc+Cov_good+Cov_bad`。
其中Gc是每道信息题正确/错误候选均值差的外积，类内协方差按ddof=0计算，再对同样2513道信息题平均；rhs始终为原等题权均值差。
假设：原目标对同一题内正确解答间、错误解答间的离散度惩罚，可能使共享排序系数过度收缩某些有用方向。
固定六组(a_good,a_bad)：(0,1)、(.5,1)、(1,0)、(1,.5)、(.5,.5)、(0,0)。
解`(Gc+a_good·Cov_good+a_bad·Cov_bad+.3I)w=rhs`，不重新归一化trace、不改变题权或统计量。
全(1,1)控制复现原semantic权重/分数，独立质心系统核对(0,0)；同时记录PSD、精确分解及rhs一致性检查。
这是现有表示和目标矩阵内的消融；不声称首次研究类内离散度或质心分类，具体历史边界见[计划](ROUND95_LABEL_COVARIANCE_PLAN.md)。
每个输出仅替换固定父79的semantic权重及描述配置，numeric α=1、原门与一次格式转移保持，推理仍使用原method_round11.py。
训练锚点固定79，选型对照则是本批冻结的实际Round79/749，两种资产分别核验。

## 全部拟合、诊断和失败

实际六个候选精确解，另有3次控制求解（完整控制、质心正规方程、独立QR）；耗时44.444秒；1CPU线程、600秒硬上限。
以下保留全部六配置聚合训练记录，完整权重范数、分层回代及目标记录保留在result.json。
训练回代参考固定父79的4406/4755，不是OOF、持出或验证结果，不按它筛选输出或扩大本池。

|a_good|a_bad|完整train回代 /4755|回代修复 / 新错|方程残差∞范数|正确类分数方差|错误类分数方差|质心目标margin MSE|
|---|---:|---:|---:|---:|---:|---:|---:|
|0|1|4402|12 / 16|2.22e-16|0.0194889|0.0310802|0.322121|
|0.5|1|4405|6 / 7|1.11e-15|0.0161032|0.0295939|0.325411|
|1|0|4406|13 / 13|1.33e-15|0.01644|0.041135|0.319483|
|1|0.5|4409|6 / 3|5.55e-16|0.0149129|0.0335861|0.323669|
|0.5|0.5|4406|9 / 9|4.44e-16|0.0175581|0.0350515|0.320211|
|0|0|4411|28 / 23|8.88e-16|0.0242485|0.0460064|0.31378|

|分量矩阵|最小特征值|最大特征值|trace|不对称最大误差|
|---|---:|---:|---:|---:|
|centroid|-3.28e-16|45.5075|374.923|0|
|within_correct|-6.47e-17|9.38287|87.1375|0|
|within_incorrect|-1e-16|8.59109|88.9512|0|
|original_pairwise|-5.21e-16|61.9137|551.012|4.44e-16|

允许最小特征值−1e−10的舍入容差，没有裁剪特征值或trace归一化。所有六配置均成功精确求解并进入验证，没有删去训练表现差的方案。
参考标签仅用于训练时矩阵构造；推理只有保存的系数、统计量与原保护管线，不访问参考答案。

分解、PSD与控制聚合记录：

```json
{
  "decomposition": {
    "gram_max_error": 5.5164206536062466e-15,
    "rhs_max_error": 7.66053886991358e-15,
    "informative_question_count": 2513,
    "positive_negative_pairs": 8271,
    "question_pair_weight_sum": 2513.0,
    "population_covariance_ddof": 0
  },
  "control": {
    "weight_max_error": 7.382983113757291e-15,
    "full_train_semantic_score_max_error": 7.134486228656054e-14,
    "full_control_normal_equation_residual": 7.771561172376096e-16,
    "full_control_coefficients": {
      "correct_covariance": 1.0,
      "incorrect_covariance": 1.0
    },
    "decomposition": {
      "gram_max_error": 5.5164206536062466e-15,
      "rhs_max_error": 7.66053886991358e-15,
      "informative_question_count": 2513,
      "positive_negative_pairs": 8271,
      "question_pair_weight_sum": 2513.0,
      "population_covariance_ddof": 0
    },
    "centroid_independent_identity": {
      "weight_max_error": 5.4817261840867104e-15,
      "full_train_semantic_score_max_error": 3.714043104923996e-14,
      "normal_equation_residual": 8.881784197001252e-16,
      "augmented_qr_rank": 1422,
      "independent_solver": "scipy.linalg.lstsq augmented one-delta-per-question, gelsy",
      "selectable_additional_output": false
    }
  },
  "parent_score_variance_components": {
    "mean_correct_score_population_variance": 0.013771727554593957,
    "mean_incorrect_score_population_variance": 0.028459819829928335,
    "mean_centroid_score_margin": 0.573770492873452,
    "centroid_target_margin_mse": 0.32897298153237453,
    "original_pairwise_margin_mse": 0.3712045289168968
  }
}
```

## 冻结后完整验证

|输出|a_good|a_bad|验证 /798|修复 / 新错（对Round79）|改选数|完整资产 MiB|fresh预测＋独立评分秒|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|round95_good0p0_bad1p0|0|1|743|1 / 7|40|1.6007|1.839|
|round95_good0p5_bad1p0|0.5|1|747|0 / 2|13|1.6007|1.878|
|round95_good1p0_bad0p0|1|0|744|1 / 6|55|1.6007|1.914|
|round95_good1p0_bad0p5|1|0.5|748|0 / 1|18|1.6007|1.855|
|round95_good0p5_bad0p5|0.5|0.5|746|1 / 4|28|1.6007|1.847|
|round95_good0p0_bad0p0|0|0|743|3 / 9|67|1.6007|1.892|

最佳新输出Cov_good×1; Cov_bad×0.5; α=.3为748/798，修复0、新增1。六种类内协方差缩减未超过动态对照；减少类内离散度惩罚不保证改善题内排序泛化。 训练回代不是OOF或持出，这些相关自适应开发比较不能识别唯一机制、证明模型上限或独立泛化。

## 资源、选型与材料边界

严格超过动态对照749且全部官方/资源/接口检查通过才晋级；同分保留当前最佳，新赢家同分按更小完整解压资产、再按名称字典序。
全部六行成功与失败保留，不按个别验证错题加规则，不改协方差系数或额外重训。
完整解压资产1,678,437–1,678,437字节，均≤16MiB；fresh完整验证预测＋独立评分1.839–1.914秒，均≤30秒、4总CPU线程。
动态对照另fresh复核749/798，1.900秒；本机完整验证计时不等于参考Xeon8457C完整测试资格认证。
所有拟合已退出后才开始官方计时，完整缓存/直接推理、严格重排、题序、不同bank大小、新ID、空输入和Python整数检查通过。
历史来源/资产（含89–94）、原官方工具/train与validation文件、固定父79、动态对照及新资产哈希通过；未读取或哈希测试文件。
历史ZIP、报告PDF及submission_ready仍为旧快照，不自动同步本轮成果；没有冻结测试、公开上传或实际GitHub issue提交。

证据：[训练](code/runs/round95-label-covariance/result.json)、[冻结](code/runs/round95-evaluation/frozen-selection.json)、
[全部验证](code/runs/round95-evaluation/all-validation.csv)、[官方审计](code/runs/round95-verification/results.json)、[当前最佳](CURRENT_BEST.json)。
