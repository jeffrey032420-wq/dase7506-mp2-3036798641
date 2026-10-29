# Round116学习记录

## Material Passport

academic-research-suite / experiment-agent；2026-10-28；完成固定四条件后的描述性比较。

## 实验学到了什么

- legacy/legacy → aligned/legacy：训练OOF+0题（三折[0, 0, 0]），官方验证+0题（修复0/新增错0）。
- legacy/aligned → aligned/aligned：训练OOF+0题（三折[0, 0, 0]），官方验证+0题（修复0/新增错0）。
- legacy/legacy → legacy/aligned：训练OOF+3题（三折[1, 4, -2]），官方验证-1题（修复0/新增错1）。
- aligned/legacy → aligned/aligned：训练OOF+3题（三折[1, 4, -2]），官方验证-1题（修复0/新增错1）。

这次分离了115合并变化带来的解释混杂。逐折变化可判断收益是否集中一折；若训练OOF提高而验证不提高，应报告这种不一致，不能通过继续围绕验证个别题调规则消除。

## 下一次的改进入口

对解析收益使用训练OOF错误覆盖审计：分别统计因变量边界拒绝、幂支持、最后数值与最终答案不一致产生的变化，再判断是否需要增加新信号。若只靠这些统计无法纠正剩余错误，下一方向应检验题意数量关系或具有互补OOF错误的真正不同专家；不继续密集搜索同一残差正则。所有下一批先立有限假设和训练筛选规则，再固定最终候选官方验证。公开分数不能替代相同输入/标签/资源/代码版本的可复现比较；本批不作工具品牌能力结论。


## 训练OOF错误覆盖补充（两批实验完成后）

```json
{
  "status": "completed_descriptive_train_oof_only",
  "selection_or_fitting_performed": false,
  "old_oof_correct": 4392,
  "aligned_oof_correct": 4395,
  "aligned_fixed_old_errors": 16,
  "aligned_new_errors": 13,
  "old_errors_with_any_group_feature_changed": 284,
  "feature_coverage_on_original_errors": {
    "legacy": {
      "original_oof_errors": 363,
      "invalid_selected_answer": 0,
      "all_groups_identical_full22": 8,
      "all_groups_identical_arithmetic16": 45,
      "all_correct_groups_match_selected_full22": 17,
      "chosen_has_checked_mismatch_and_some_correct_group_has_none": 2,
      "neither_selected_nor_any_correct_group_has_checked_equation": 39
    },
    "aligned": {
      "original_oof_errors": 363,
      "invalid_selected_answer": 0,
      "all_groups_identical_full22": 4,
      "all_groups_identical_arithmetic16": 41,
      "all_correct_groups_match_selected_full22": 10,
      "chosen_has_checked_mismatch_and_some_correct_group_has_none": 16,
      "neither_selected_nor_any_correct_group_has_checked_equation": 46
    }
  },
  "caveat": "Feature equality is a descriptive bound for corrections sharing this representation and a fixed anchor; it does not establish the performance of new semantic signals.",
  "validation_used": false,
  "test_used": false
}
```

这里不拟合/选择模型，也不查看验证个别错误。若正确答案组与已选错组的22维向量相同，仅改变该表示的残差权重无法改变二者基础margin；需要能区分这两个组的新信息。算式缺失是覆盖不足，不能直接标成正确或错误。
