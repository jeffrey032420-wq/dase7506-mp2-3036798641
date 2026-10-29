"""Freeze and validate the four predeclared Round108 models; never access test."""
import os
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile
import numpy as np
from threadpoolctl import threadpool_limits
from common import load_inputs, validate_choices
from train_round1 import labels
from train_round108_group_subsets import closure, digest, write, metrics, contracts, asset_inventory
from method_round108_group_subsets import candidate_scores, predict
from method_round11 import predict as incumbent_predict

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
TRAIN = CODE/'runs/round108-group-subsets'
OUT = CODE/'runs/round108-evaluation'
PLAN = ROOT/'ROUND108_GROUP_SUBSETS_PLAN.md'


def expanded(folder):
    total = 0
    for p in folder.rglob('*'):
        if p.is_file():
            size = p.stat().st_size
            if p.suffix == '.npz':
                with zipfile.ZipFile(p) as z:
                    size = max(size, sum(i.file_size for i in z.infolist()))
            total += size
    return total


def fresh(method, checkpoint, target):
    target.mkdir()
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    commands = [
        [sys.executable, '-X', 'utf8', 'predict.py', '--method', method, '--checkpoint', str(checkpoint),
         '--split', 'validation', '--output', str(target/'validation-predictions.json')],
        [sys.executable, '-X', 'utf8', 'score_predictions.py', '--split', 'validation',
         '--predictions', str(target/'validation-predictions.json'), '--output', str(target/'validation-score.json')],
    ]
    write(target/'commands.json', {'commands': commands, 'cwd': str(CODE), 'threads_total': 4})
    tick, durations = time.perf_counter(), []
    for label, command in zip(('prediction', 'scoring'), commands):
        remaining = 30-(time.perf_counter()-tick)
        assert remaining > 0
        begin = time.perf_counter()
        result = subprocess.run(command, cwd=CODE, env=env, capture_output=True, text=True,
                                encoding='utf-8', timeout=remaining)
        durations.append(time.perf_counter()-begin)
        (target/f'{label}-stdout.txt').write_text(result.stdout, encoding='utf-8')
        (target/f'{label}-stderr.txt').write_text(result.stderr, encoding='utf-8')
        result.check_returncode()
    seconds = time.perf_counter()-tick
    assert seconds <= 30
    return {'official_score': json.loads((target/'validation-score.json').read_text(encoding='utf-8')),
            'prediction_process_seconds': durations[0], 'scoring_process_seconds': durations[1],
            'prediction_plus_scoring_wall_seconds': seconds}


def main():
    assert not OUT.exists(), 'Round108 evaluation already exists; no automatic retry/expansion'
    trained = json.loads((TRAIN/'result.json').read_text(encoding='utf-8'))
    assert trained['status'] == 'completed_train_only' and not trained['validation_used'] and not trained['test_used']
    models = trained['models']
    assert len(models) == 4 and {(r['augmented'], r['lambda']) for r in models} == {
        (a, p) for a in (False, True) for p in (.003, .01)}
    assert all(digest(CODE/n) == sha for n, sha in trained['sources'].items())
    assert digest(PLAN) == trained['plan_sha256']
    pointer_path = ROOT/'CURRENT_BEST.json'
    pointer_bytes = pointer_path.read_bytes()
    pointer = json.loads(pointer_bytes)
    assert pointer['round'] == 79 and pointer['validation_correct'] == 749
    incumbent = ROOT/pointer['checkpoint']
    incumbent_assets = asset_inventory(incumbent)
    for r in models:
        assert asset_inventory(CODE/r['checkpoint']) == r['assets'] and all(r['checks'].values())
        assert expanded(CODE/r['checkpoint']) <= 16*2**20
    manifest = json.loads((CODE/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))['files']
    for n in ('common.py', 'predict.py', 'score_predictions.py', 'check_data.py'):
        assert digest(CODE/n) == manifest['code/'+n]
    sources = closure(['evaluate_round108_group_subsets.py', 'train_round108_group_subsets.py',
                       'method_round108_group_subsets.py', 'method_round11.py'])
    OUT.mkdir()
    (OUT/'incumbent-pointer-before-research.json').write_bytes(pointer_bytes)
    (OUT/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n, OUT/'sources'/n)
    shutil.copy2(PLAN, OUT/'sources/PLAN.md')
    frozen = {'models': models, 'sources': sources, 'training_result_sha256': digest(TRAIN/'result.json'),
              'plan_sha256': trained['plan_sha256'], 'incumbent_assets': incumbent_assets,
              'purpose': 'post-test-disclosure train/validation research', 'test_access_in_this_round': False,
              'final_submission_model_unchanged': True}
    write(OUT/'frozen-before-validation.json', frozen)
    # Freeze every candidate and its provenance before opening validation inputs/references.
    bank, arrays = load_inputs('validation')
    y = labels(bank, 'validation')
    old = np.asarray(incumbent_predict(bank, arrays, incumbent))
    old_right = y[np.arange(len(y)), old].astype(bool)
    assert int(old_right.sum()) == 749
    control = fresh(pointer['method'].removeprefix('code/'), incumbent, OUT/'incumbent-control')
    assert control['official_score']['correct'] == 749
    write(OUT/'incumbent-control.json', control)
    results = []
    for row in models:
        path = CODE/row['checkpoint']
        scores = candidate_scores(bank, arrays, path)
        choices = predict(bank, arrays, path)
        validate_choices(bank, [b['id'] for b in bank], choices)
        local = metrics(bank, y, scores)
        right = y[np.arange(len(y)), choices].astype(bool)
        audit = fresh(row['method'], path, OUT/row['name'])
        official = json.loads((OUT/row['name']/'validation-predictions.json').read_text(encoding='utf-8'))['selected']
        assert official == choices and audit['official_score']['correct'] == local['correct']
        checks = contracts(bank[:53], {'embeddings': arrays['embeddings'][:53]}, path)
        report = {'name': row['name'], 'augmented': row['augmented'], 'lambda': row['lambda'], **local,
                  'fixed_old_errors': int((~old_right & right).sum()), 'new_errors': int((old_right & ~right).sum()),
                  'changed_choices': int((np.asarray(choices) != old).sum()), 'train_oof': row['train_oof'],
                  'train_resubstitution_not_oof': row['train_resubstitution_not_oof'], 'fit': row['fit'],
                  'uncompressed_asset_bytes': expanded(path), 'checks': checks, **audit,
                  'status': 'verified_local_validation', 'reference_cpu_complete_test_verified': False}
        results.append(report)
        write(OUT/'all-results.json', results)
        print(json.dumps(report, ensure_ascii=False), flush=True)
    assert closure(['evaluate_round108_group_subsets.py', 'train_round108_group_subsets.py',
                    'method_round108_group_subsets.py', 'method_round11.py']) == sources
    assert digest(PLAN) == frozen['plan_sha256'] and digest(TRAIN/'result.json') == frozen['training_result_sha256']
    assert pointer_path.read_bytes() == pointer_bytes and asset_inventory(incumbent) == incumbent_assets
    assert all(asset_inventory(CODE/r['checkpoint']) == r['assets'] for r in models)
    write(OUT/'integrity.json', {'status': 'passed', 'all_sources_assets_unchanged': True,
                                'final_test_pointer_unchanged': True, 'test_used': False,
                                'frozen_manifest_sha256': digest(OUT/'frozen-before-validation.json')})
    best = min(results, key=lambda r: (-r['correct'], r['uncompressed_asset_bytes'], r['name']))
    if best['correct'] > 749:
        write(ROOT/'RESEARCH_CANDIDATE_ROUND108.json', {**best,
              'method': 'code/method_round108_group_subsets.py',
              'checkpoint': next('code/'+r['checkpoint'] for r in models if r['name'] == best['name']),
              'final_submission_model_not_changed': True, 'new_test_score': None,
              'selection_split': 'validation', 'prior_test_aggregates_known': True})
    effects = {}
    for label, key in [('validation', None), ('train_oof', 'train_oof')]:
        c = {(r['augmented'], r['lambda']): (r if key is None else r[key])['correct'] for r in results}
        effects[label] = {'augmentation_at_0p003': c[True,.003]-c[False,.003],
                          'augmentation_at_0p01': c[True,.01]-c[False,.01],
                          'stronger_regularization_full': c[False,.01]-c[False,.003],
                          'stronger_regularization_subsets': c[True,.01]-c[True,.003]}
    write(OUT/'factorial-effects.json', effects)
    lines = ['# Round108：答案组子集增强与固定正则', '', '## Material Passport', '',
             'academic-research-suite / experiment-agent；2026-10-28；VERIFIED_LOCAL_VALIDATION。'
             '先写计划，再自行实现；四配置完整报告。本轮未访问测试，既往自身及公开测试总分已知。', '',
             '|组内增强|lambda|训练三折OOF/4755|验证/798|分歧/355|单正确/117|修复/新增错|资产MiB|fresh预测+评分秒|',
             '|---|---:|---:|---:|---:|---:|---|---:|---:|']
    for r in results:
        lines.append(f'|{r["augmented"]}|{r["lambda"]}|{r["train_oof"]["correct"]}|{r["correct"]}|'
                     f'{r["disagreement_correct"]}|{r["single_correct"]}|{r["fixed_old_errors"]}/{r["new_errors"]}|'
                     f'{r["uncompressed_asset_bytes"]/2**20:.5f}|{r["prediction_plus_scoring_wall_seconds"]:.3f}|')
    improved = best['correct'] > 749
    lines += ['', f'本轮最佳{best["name"]}：{best["correct"]}/798（{best["accuracy"]:.4f}%）；'
              + ('超过既有749，另存研究候选。' if improved else '未超过既有749，不宣布突破。')
              + '已完成测试的Round79模型和成绩仍保留。', '', '## 消融解释', '',
              '以下是正确题数差；共享划分、缩放和每题损失权重，只比较本轮固定表示内的条件：', '',
              '```json', json.dumps(effects, ensure_ascii=False, indent=2), '```', '',
              '增强将全训练pair数从3058变为12200，但2114道有正负有效答案组的题目总权重保持一致；'
              '目标采用每题平均logistic损失加lambda/2*范数平方，因此排除了固定C随样本数改变有效正则的混杂。'
              '数值梯度与重复pair保持损失/梯度不变检查通过。', '',
              '三折中每题及其所有子集处于同一侧；缩放只拟合该折原始完整组。OOF与训练回代分别记录，'
              '不把回代准确率作为泛化结果。训练数据和官方验证均已长期用于开发，不能视为全新独立确认。', '',
              f'16次拟合、四线程、worker墙钟{trained["seconds"]:.3f}秒，600秒硬上限；'
              '训练停止后串行计时。全部模型资产按NPZ解压保守计数，包含权重/mean/scale/config。'
              '通过官方fresh预测及独立评分、严格分数重排、题序、新ID、变bank、空输入、Python整数和组内同分检查。'
              '本机验证计时不代表参考Xeon完整测试资格。', '',
              '来源：CaspianW答案组内子集增强与显式正则思想，独立实现，'
              '不是其最终算术残差系统的复现。来源URL/版本见GITHUB_METHOD_SOURCES_2026-10-28.json。', '',
              '复现：在code目录依次运行train_round108_group_subsets.py、evaluate_round108_group_subsets.py。'
              '已有输出目录时拒绝覆盖；完整计划见ROUND108_GROUP_SUBSETS_PLAN.md。', '',
              '证据：code/runs/round108-group-subsets/result.json、folds.json、pair-audit和fold-models；'
              'code/runs/round108-evaluation/frozen-before-validation.json、all-results.json、'
              'factorial-effects.json、integrity.json及五组官方评分/命令/进程日志。', '']
    report = '\n'.join(lines)
    (ROOT/'ROUND108_RESULTS.md').write_text(report, encoding='utf-8')
    with (ROOT/'WORKLOG.md').open('a', encoding='utf-8') as f:
        f.write('\n\n'+report)
    with (ROOT/'AI_DISCLOSURE.md').open('a', encoding='utf-8') as f:
        f.write('\n\n## Round108 — group subsets and invariant L2, 2026-10-28\n\n'
                'At the student\'s request, Codex first saved a finite 2x2 plan, then independently implemented '
                'numeric answer groups, within-group nonempty subsets, and question-normalized logistic loss '
                'with explicit L2. It executed train-only three-fold fitting plus four full-train exports '
                'and all four official validation/resource/interface checks. The idea was attributed to '
                'CaspianW; no peer code, weights or external data were imported. '
                f'Best validation: {best["correct"]}/798. Prior test aggregates were known; no test input, '
                'reference, prediction or scoring was accessed in this round. The frozen final Round79 '
                'model and its historical test result were retained. See ROUND108_RESULTS.md.\n')
    pointer['latest_completed_development_round'] = 108
    pointer['latest_round_result'] = f'Round108 fixed group subsets/L2: max {best["correct"]}/798; frozen final Round79 unchanged. See ROUND108_RESULTS.md.'
    write(pointer_path, pointer)
    write(OUT/'completion.json', {'status': 'completed', 'new_models': 4,
                                 'best_validation_correct': best['correct'], 'research_improvement_over_749': improved,
                                 'final_selected_round': 79, 'test_used_in_round': False})
    print('ROUND108_COMPLETE '+json.dumps({'best_validation_correct': best['correct'], 'improved': improved}), flush=True)


if __name__ == '__main__':
    with threadpool_limits(limits=4):
        main()
