"""Replay the frozen-parent Round137 training stage in a new output directory.

Only the official training split is opened. This entry never evaluates validation
or test and never overwrites the submitted checkpoint. See TRAINING_REPRODUCE.md.
"""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[key] = '4'

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FAMILIES = ('mix', 'joint')
PENALTIES = (.01, .1, 1.)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_assets(code):
    manifest = read(HERE / 'provenance/manifest.json')
    for name, expected in manifest['replay_input_sha256'].items():
        assert digest(HERE / name) == expected, 'Changed replay asset: ' + name
    for name, expected in manifest['inference_source_sha256'].items():
        assert digest(code / name) == expected, 'Changed frozen feature source: ' + name
    return manifest


def config_name(family, penalty):
    return 'round137_' + family + '_l' + str(penalty).replace('.', 'p')


def worker(args, code, data_dir, out):
    # Import numerical packages only in the monitored worker.
    sys.path.insert(0, str(HERE / 'source'))
    sys.path.insert(0, str(code))
    import numpy as np
    from threadpoolctl import threadpool_limits
    from common import check_data, load_inputs, parse_answer, read_jsonl
    from method_round137_joint_retrain import (
        input_features, components, score_components, updated_parameters,
        candidate_scores, BLOCKS, DIMENSIONS,
    )
    from replay_utils import fit_residual, metrics, comparison, pair_design, gradient_check, contracts

    def load_npz(path):
        with np.load(path, allow_pickle=False) as bundle:
            return {key: bundle[key].copy() for key in bundle.files}

    tick = time.perf_counter()
    with threadpool_limits(limits=4):
        manifest = verify_assets(code)
        parents = Path(args.parents_dir).resolve()
        expected_data = read(parents / 'train-data-manifest.json')
        assert expected_data == read(HERE / 'parents/train-data-manifest.json')
        if parents != (HERE / 'parents').resolve():
            # Optional rebuilt centers must reproduce the original center arrays;
            # serialized NPZ SHA can differ across platforms or package versions.
            for name in ('full.npz', 'fold0.npz', 'fold1.npz', 'fold2.npz'):
                rebuilt, original = load_npz(parents / name), load_npz(HERE / 'parents' / name)
                assert rebuilt.keys() == original.keys()
                for key in original:
                    np.testing.assert_allclose(rebuilt[key], original[key], rtol=1e-8, atol=1e-8)
        official = check_data(data_dir, ('train',), inputs_only=False)
        assert official['protocol'] == expected_data['protocol']
        for name, expected in expected_data['sha256'].items():
            assert digest(data_dir / name) == expected, 'Unexpected training data: ' + name

        bank, arrays = load_inputs('train', data_dir=data_dir)
        refs = read_jsonl(data_dir / 'gsm8k_train.jsonl')
        assert len(bank) == len(refs) == expected_data['train_n']
        target = []
        for row, ref in zip(bank, refs):
            assert row['id'] == ref['id'] and row['question'] == ref['question']
            gold = parse_answer(ref['answer'])
            target.append([float(gold is not None and parse_answer(c['text']) == gold)
                           for c in row['candidates']])
        y = np.asarray(target)
        data, local, evidence, q, graph = input_features(bank, arrays)
        folds = read(parents / 'folds.json')
        assert folds == read(HERE / 'parents/folds.json')
        assert sorted(row['fold'] for row in folds) == [0, 1, 2]
        held_union = []
        for row in folds:
            fit, held = set(row['fit']), set(row['held'])
            assert not fit & held and fit | held == set(range(len(bank)))
            held_union.extend(row['held'])
        assert sorted(held_union) == list(range(len(bank)))
        ref = np.load(parents / 'parent-oof-scores.npy', allow_pickle=False)
        assert ref.shape == (len(bank), 4) and metrics(bank, y, ref)['correct'] == 4404
        oof = {(f, p): np.zeros_like(ref) for f in FAMILIES for p in PENALTIES}
        records, mathematics, fits = [], {}, 0
        write(out / 'pretraining.json', dict(
            scope='Round137 replay with supplied frozen train-only parent centers',
            families=FAMILIES, penalties=PENALTIES, planned_fits=20,
            validation_used=False, test_used=False, threads_total=4,
            replay_manifest_sha256=digest(HERE / 'provenance/manifest.json'),
            train_data_sha256=expected_data['sha256'],
        ))
        for fold in folds:
            f = fold['fold']
            fitting, held = np.array(fold['fit']), np.array(fold['held'])
            p = load_npz(parents / f'fold{f}.npz')
            c = components(data, local, evidence, q, graph, p)
            base = score_components(data, c)
            np.testing.assert_allclose(base[held], ref[held], rtol=1e-10, atol=1e-10)
            x, offset, importance, pair_audit = pair_design(data, local, evidence, q, graph, p, c, y, fitting)
            np.savez_compressed(out / f'fold{f}-pair-audit.npz', **pair_audit)
            held_features = ([data[i] for i in held], [local[i] for i in held],
                             [evidence[i] for i in held], q[held], [graph[i] for i in held])
            for family in FAMILIES:
                if family not in mathematics:
                    mathematics[family] = gradient_check(x[family], offset, importance)
                for penalty in PENALTIES:
                    delta, fit_report = fit_residual(x[family], offset, importance, penalty)
                    fits += 1
                    parameters = updated_parameters(p, family, delta)
                    scores = score_components(held_features[0], components(*held_features, parameters))
                    oof[family, penalty][held] = scores
                    np.savez(out / f'fold{f}-{family}-{penalty}.npz', delta=delta)
                    row = dict(fold=f, family=family, lambda_value=penalty, fit=fit_report,
                               held=metrics([bank[i] for i in held], y[held], scores),
                               current_held=metrics([bank[i] for i in held], y[held], ref[held]),
                               **comparison(y[held], ref[held], scores))
                    records.append(row)
                    write(out / 'fit-progress.json', records)
                    print('OUTER ' + json.dumps(row), flush=True)
            del x

        searches = []
        for family in FAMILIES:
            for penalty in PENALTIES:
                scores = oof[family, penalty]
                name = config_name(family, penalty)
                np.save(out / (name + '-oof-scores.npy'), scores)
                searches.append(dict(name=name, family=family, lambda_value=penalty,
                    train_oof=metrics(bank, y, scores), current754_comparison=comparison(y, ref, scores),
                    fold_deltas_vs_current=[row['held']['correct'] - row['current_held']['correct']
                        for row in records if row['family'] == family and row['lambda_value'] == penalty]))
        selected = [min((row for row in searches if row['family'] == family), key=lambda row: (
            -row['train_oof']['correct'], row['current754_comparison']['new_parent_errors'],
            row['current754_comparison']['changed_choices'], -row['lambda_value'])) for family in FAMILIES]
        write(out / 'selected-on-train-before-validation.json', dict(
            selected=selected, all_searches=searches, validation_used=False, test_used=False))

        p = load_npz(parents / 'full.npz')
        assert all(np.isfinite(v).all() for v in p.values())
        for block, size, mean_size in zip(BLOCKS, DIMENSIONS, (1034, 26, 32, 24)):
            assert p[block + '_weight'].shape == (size,)
            assert p[block + '_mean'].shape == p[block + '_scale'].shape == (mean_size,)
            assert (p[block + '_scale'] > 0).all()
        c = components(data, local, evidence, q, graph, p)
        assert metrics(bank, y, score_components(data, c))['correct'] == 4519
        x, offset, importance, pair_audit = pair_design(data, local, evidence, q, graph, p, c, y, np.arange(len(bank)))
        np.savez_compressed(out / 'full-pair-audit.npz', **pair_audit)
        models = []
        for selected_row in selected:
            family, penalty = selected_row['family'], selected_row['lambda_value']
            delta, fit_report = fit_residual(x[family], offset, importance, penalty)
            fits += 1
            parameters = updated_parameters(p, family, delta)
            path = out / 'candidates' / selected_row['name']
            path.mkdir(parents=True)
            write(path / 'config.json', dict(schema='joint_four_block123_v1', family=family,
                lambda_value=penalty, fit_split='train', features='same_four_blocks_as123', standalone=True))
            np.savez(path / 'parameters.npz', **parameters)
            np.savez(out / (selected_row['name'] + '-update.npz'), delta=delta)
            expected = score_components(data, components(data, local, evidence, q, graph, parameters))
            np.testing.assert_allclose(candidate_scores(bank, arrays, path), expected, rtol=1e-10, atol=1e-10)
            checks = contracts(bank[:53], {'embeddings': arrays['embeddings'][:53]}, path)
            checks.update(full_train_export_agrees=True, fit_only_fold_center_and_scaler=True,
                          all_parent_held_scores_reproduced=True)
            row = dict(**selected_row, checkpoint='candidates/' + selected_row['name'],
                       method='method_round137_joint_retrain.py', fit=fit_report, checks=checks,
                       train_resubstitution_not_oof=metrics(bank, y, expected),
                       update_l2=float(np.linalg.norm(delta)),
                       module_coefficients=(1 + delta).tolist() if family == 'mix' else None)
            if args.reference_checkpoint and family == 'joint':
                original = load_npz(Path(args.reference_checkpoint).resolve() / 'parameters.npz')
                assert parameters.keys() == original.keys()
                row['frozen_parameter_comparison'] = dict(
                    max_abs_difference=max(float(np.max(np.abs(parameters[k] - original[k]))) for k in parameters),
                    allclose_rtol_1e_8_atol_1e_8=all(np.allclose(parameters[k], original[k], rtol=1e-8, atol=1e-8)
                                                  for k in parameters))
            models.append(row)
            print('EXPORT ' + json.dumps({k: v for k, v in row.items() if k != 'checks'}), flush=True)

        assert fits == 20
        verify_assets(code)
        write(out / 'result.json', dict(status='completed_train_only_frozen_parent_replay',
            models=models, searches=searches, fold_records=records, mathematical_checks=mathematics,
            model_fits=fits, seconds=time.perf_counter() - tick, threads_total=4,
            validation_used=False, test_used=False, historical_parents_refitted=False,
            final_frozen_submission_checkpoint_overwritten=False))
        print('TRAIN_COMPLETE ' + json.dumps(dict(fits=fits, seconds=time.perf_counter() - tick)), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code-dir', default='../code', help='Frozen inference source directory, relative to this script')
    parser.add_argument('--data-dir', required=True, help='Official data directory containing manifest.json and candidates/')
    parser.add_argument('--parents-dir', default='parents', help='Parent center bundle, relative to this script')
    parser.add_argument('--output', default='runs/reproduction/round137', help='New directory within training/runs/reproduction')
    parser.add_argument('--reference-checkpoint', help='Optional read-only comparison with the submitted two-file checkpoint')
    parser.add_argument('--timeout-seconds', type=float, default=600)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    parents = Path(args.parents_dir)
    if not parents.is_absolute():
        parents = HERE / parents
    args.parents_dir = str(parents.resolve())
    code = Path(args.code_dir)
    if not code.is_absolute():
        code = HERE / code
    code = code.resolve()
    data_dir = Path(args.data_dir).resolve()
    out = Path(args.output)
    if not out.is_absolute():
        out = HERE / out
    out = out.resolve()
    safe_root = (HERE / 'runs/reproduction').resolve()
    assert out.is_relative_to(safe_root) and out != safe_root, 'Output must be under training/runs/reproduction/'
    assert 0 < args.timeout_seconds <= 600, 'Keep the original 600-second training limit'
    verify_assets(code)
    if args.worker:
        assert out.is_dir()
        worker(args, code, data_dir, out)
        return
    assert not out.exists(), 'Preserve existing results; choose a new reproduction subdirectory'
    out.mkdir(parents=True)
    tick = time.perf_counter()
    command = [sys.executable, '-X', 'utf8', str(Path(__file__).resolve()),
               '--worker', '--code-dir', str(code), '--data-dir', str(data_dir),
               '--output', str(out), '--parents-dir', args.parents_dir,
               '--timeout-seconds', str(args.timeout_seconds)]
    if args.reference_checkpoint:
        command.extend(['--reference-checkpoint', str(Path(args.reference_checkpoint).resolve())])
    try:
        process = subprocess.run(command, cwd=HERE, timeout=args.timeout_seconds)
        write(out / 'process-monitor.json', dict(exit_code=process.returncode,
            wall_seconds=time.perf_counter() - tick, hard_timeout_seconds=args.timeout_seconds))
        assert process.returncode == 0, 'Replay failed; partial logs were preserved'
    except subprocess.TimeoutExpired:
        write(out / 'process-monitor.json', dict(status='hard_timeout', wall_seconds=time.perf_counter() - tick))
        raise


if __name__ == '__main__':
    main()
