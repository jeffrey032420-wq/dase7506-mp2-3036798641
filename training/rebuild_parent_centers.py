"""Optional compact from-data reconstruction of the fixed A -> L -> I -> G chain.

Authored and statically reviewed after freeze; NOT numerically executed then.
This rebuilds the fixed selected chain, not every historical model search.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[key] = '4'
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from replay_round137 import HERE, read, write, digest, verify_assets


def worker(code, data_dir, out):
    # These archive modules define the original mathematical functions. Their
    # historical main()/worker() functions and hardcoded run paths are not called.
    sys.path.insert(0, str(HERE / 'archive/source'))
    sys.path.insert(0, str(code))
    import numpy as np
    from sklearn.model_selection import StratifiedKFold
    from threadpoolctl import threadpool_limits
    from common import check_data, load_inputs, parse_answer, read_jsonl
    from method_round108_group_subsets import tables, score_tables
    from method_round109_arithmetic_residual import anchored
    from method_round120_question_interaction import add_interaction
    from method_round137_joint_retrain import input_features, components, score_components
    from train_round108_group_subsets import scale_fit, design, fit as fit_anchor
    from train_round109_arithmetic_residual import residual_scale, residual_design, fit_residual
    from train_round120_question_interaction import pair_design, fit_cross, scale_fit as interaction_scale

    tick, count, reports = time.perf_counter(), 0, []
    with threadpool_limits(limits=4):
        manifest = verify_assets(code)
        for name, expected in manifest['historical_source_sha256'].items():
            assert digest(HERE / 'archive/source' / name) == expected
        expected_data = read(HERE / 'parents/train-data-manifest.json')
        check_data(data_dir, ('train',), inputs_only=False)
        for name, expected in expected_data['sha256'].items():
            assert digest(data_dir / name) == expected
        bank, arrays = load_inputs('train', data_dir=data_dir)
        refs = read_jsonl(data_dir / 'gsm8k_train.jsonl')
        target = []
        for row, ref in zip(bank, refs):
            assert row['id'] == ref['id'] and row['question'] == ref['question']
            gold = parse_answer(ref['answer'])
            target.append([float(gold is not None and parse_answer(c['text']) == gold)
                           for c in row['candidates']])
        y = np.asarray(target)
        assert len(bank) == len(refs) == expected_data['train_n']
        # All learned weights/scalers below are fitted from these train inputs.
        data = tables(bank, arrays, include_subsets=True)
        _, local, ev, q, graph = input_features(bank, arrays)
        folds = [dict(fold=f, fit=a.tolist(), held=b.tolist()) for f, (a, b) in enumerate(
            StratifiedKFold(3, shuffle=True, random_state=20261029).split(np.arange(len(bank)), y.sum(1)))]
        assert folds == read(HERE / 'parents/folds.json')
        original_folds = {row['fold']: row for row in folds}
        params, anchor_oof, nested = {}, np.zeros((len(bank), 4)), {}

        def remember(stage, fold, p, report):
            nonlocal count
            count += 1
            reports.append(dict(stage=stage, fold=fold, fit=report))
            write(out / 'fit-progress.json', reports)
            print('REBUILD ' + json.dumps(reports[-1]), flush=True)
            return p

        def anchor_fit(indices, tag):
            mean, scale = scale_fit(data, indices)
            x, importance, _, _ = design(data, y, indices, scale, True)
            weight, report = fit_anchor(x, importance, .01)
            return remember('A_subsets_lambda0.01', tag, dict(mean=mean, scale=scale, weight=weight), report)

        def anchor_scores(p):
            return score_tables(data, p['mean'], p['scale'], p['weight'])

        all_indices = np.arange(len(bank))
        for fold in folds:
            f, fitting, held = fold['fold'], np.asarray(fold['fit']), np.asarray(fold['held'])
            ap = anchor_fit(fitting, f)
            params[f'fold{f}'] = {'A': ap}
            anchor_oof[held] = anchor_scores(ap)[held]
            offsets = np.zeros((len(bank), 4))
            for inner, (a, b) in enumerate(StratifiedKFold(3, shuffle=True, random_state=20261030 + f).split(
                    fitting, y[fitting].sum(1))):
                inner_fit, inner_held = fitting[a], fitting[b]
                assert not set(inner_fit) & set(held)
                ip = anchor_fit(inner_fit, f'{f}/inner{inner}')
                offsets[inner_held] = anchor_scores(ip)[inner_held]
            nested[f] = offsets
        params['full'] = {'A': anchor_fit(all_indices, 'full')}

        for key, blocks in params.items():
            f = None if key == 'full' else int(key[-1])
            fitting = all_indices if f is None else np.asarray(original_folds[f]['fit'])
            base = anchor_scores(blocks['A'])
            # Exact R110 offsets: A OOF for full fit; nested A OOF inside each
            # outer fit. The L scaler uses original full groups in the fit only.
            margin_source = anchor_oof if f is None else nested[f]
            mean, scale = residual_scale(local, fitting)
            x, offset, importance, _ = residual_design(data, local, y, fitting, scale, margin_source)
            weight, report = fit_residual(x, offset, importance, .1)
            blocks['L'] = remember('L_final_evidence_lambda0.1', key, dict(mean=mean, scale=scale, weight=weight), report)
            base = anchored(data, local, base, mean, scale, weight)
            # R120 fits a question/evidence interaction on the corresponding
            # same-fit frozen A+L margin, with fixed lambda .1.
            mean, scale = interaction_scale(ev, fitting, list(range(32)))
            x, offset, importance, _ = pair_design(data, ev, q, y, fitting, list(range(32)), scale, base)
            weight, report = fit_cross(x, offset, importance)
            blocks['I'] = remember('I_question_both_lambda0.1', key, dict(mean=mean, scale=scale, weight=weight), report)
            base = add_interaction(data, ev, q, base, list(range(32)), mean, scale, weight)
            # R123 selected both (24 graph features), lambda .01. This is the
            # fixed chosen chain; no old validation search is repeated here.
            mean, scale = residual_scale(graph, fitting)
            x, offset, importance, _ = residual_design(data, graph, y, fitting, scale, base)
            weight, report = fit_residual(x, offset, importance, .01)
            blocks['G'] = remember('G_both_lambda0.01', key, dict(mean=mean, scale=scale, weight=weight), report)

        assert count == 25
        bundle = out / 'parents'
        bundle.mkdir()
        parent_oof, comparisons = np.zeros((len(bank), 4)), {}
        for key, blocks in params.items():
            flat = {b + '_' + k: np.asarray(v, dtype=float).ravel().copy()
                    for b, values in blocks.items() for k, v in values.items()}
            np.savez(bundle / (key + '.npz'), **flat)
            scores = score_components(data, components(data, local, ev, q, graph, flat))
            if key != 'full':
                held = np.asarray(original_folds[int(key[-1])]['held'])
                parent_oof[held] = scores[held]
            # Read saved centers only after all 25 fits, as a reproduction check.
            with np.load(HERE / 'parents' / (key + '.npz'), allow_pickle=False) as old:
                comparisons[key] = dict(max_abs_difference=max(float(np.max(np.abs(flat[k] - old[k]))) for k in flat),
                    allclose_rtol_1e_8_atol_1e_8=all(np.allclose(flat[k], old[k], rtol=1e-8, atol=1e-8) for k in flat))
        np.save(bundle / 'parent-oof-scores.npy', parent_oof)
        for name in ('folds.json', 'train-data-manifest.json'):
            shutil.copy2(HERE / 'parents' / name, bundle / name)
        original_oof = np.load(HERE / 'parents/parent-oof-scores.npy', allow_pickle=False)
        oof_match = bool(np.allclose(parent_oof, original_oof, rtol=1e-8, atol=1e-8))
        comparisons_passed = all(v['allclose_rtol_1e_8_atol_1e_8'] for v in comparisons.values()) and oof_match
        write(out / 'result.json', dict(status='completed_fixed_chain_from_data_rebuild' if comparisons_passed
            else 'comparison_failed', model_fits=count,
            seconds=time.perf_counter() - tick, threads_total=4, validation_used=False, test_used=False,
            saved_parent_arrays_used_in_fit=False, fixed_selected_hyperparameters=True,
            all_historical_searches_repeated=False, comparisons=comparisons, parent_oof_allclose=oof_match))
        assert comparisons_passed, \
            'Rebuilt parent differs from original; report is saved, do not treat it as a verified replacement'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-dir', default='../code')
    parser.add_argument('--data-dir', required=True)
    parser.add_argument('--output', default='runs/reproduction/rebuilt-parents')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    code = Path(args.code_dir)
    code = (code if code.is_absolute() else HERE / code).resolve()
    data_dir = Path(args.data_dir).resolve()
    out = Path(args.output)
    out = (out if out.is_absolute() else HERE / out).resolve()
    safe_root = (HERE / 'runs/reproduction').resolve()
    assert out.is_relative_to(safe_root) and out != safe_root
    verify_assets(code)
    if args.worker:
        worker(code, data_dir, out)
        return
    assert not out.exists(), 'Preserve existing results; choose a new reproduction subdirectory'
    out.mkdir(parents=True)
    tick = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, '-X', 'utf8', str(Path(__file__).resolve()), '--worker',
                            '--code-dir', str(code), '--data-dir', str(data_dir), '--output', str(out)],
                           cwd=HERE, timeout=600)
        write(out / 'process-monitor.json', dict(exit_code=p.returncode,
            wall_seconds=time.perf_counter() - tick, hard_timeout_seconds=600))
        assert p.returncode == 0, 'Parent rebuild failed; partial evidence is preserved'
    except subprocess.TimeoutExpired:
        write(out / 'process-monitor.json', dict(status='hard_timeout', wall_seconds=time.perf_counter() - tick))
        raise


if __name__ == '__main__':
    main()
