"""Run two unchanged official processes with a shared 30-second CPU budget.

This convenience entry checks checkpoint integrity and enforces the local budget.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--split", choices=("validation", "test", "audit"), default="test")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    checkpoint = root / "code/checkpoint"
    hashes = {
        "config.json": "041359516d344e57c53629a39aede6c30debb7d9aa97a2fdda690c8299b4fe41",
        "parameters.npz": "61ff97395a049186e4f2887043d9e1b0755414a0fe42e34a81bba1584010e8fa",
    }
    for name, expected in hashes.items():
        actual = hashlib.sha256((checkpoint / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError("Frozen checkpoint hash mismatch: " + name)
    asset_bytes = sum(p.stat().st_size for p in checkpoint.rglob("*") if p.is_file())
    if asset_bytes > 16 * 2**20:
        raise ValueError("Inference asset limit exceeded")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    data = args.data_dir.resolve()
    env = os.environ.copy()
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[key] = "4"
    env["PYTHONUTF8"] = "1"
    prediction = output / "predictions.json"
    score = output / "score.json"
    commands = [
        [sys.executable, "-X", "utf8", str(root / "code/predict.py"),
         "--method", str(root / "code/method_round137_joint_retrain.py"),
         "--checkpoint", str(checkpoint), "--data-dir", str(data),
         "--split", args.split, "--output", str(prediction)],
        [sys.executable, "-X", "utf8", str(root / "code/score_predictions.py"),
         "--data-dir", str(data), "--split", args.split,
         "--predictions", str(prediction), "--output", str(score)],
    ]
    started = time.perf_counter()
    process_seconds = []
    for command in commands:
        remaining = 30 - (time.perf_counter() - started)
        if remaining <= 0:
            raise TimeoutError("Combined prediction and scoring exceeded 30 seconds")
        process_started = time.perf_counter()
        subprocess.run(command, check=True, env=env, timeout=remaining)
        process_seconds.append(time.perf_counter() - process_started)
    elapsed = time.perf_counter() - started
    result = {
        "split": args.split, "official_score": json.loads(score.read_text(encoding="utf-8")),
        "prediction_process_seconds": process_seconds[0],
        "scoring_process_seconds": process_seconds[1],
        "prediction_plus_scoring_wall_seconds": elapsed,
        "inference_assets_uncompressed_bytes": asset_bytes, "numerical_threads_total": 4,
        "reference_xeon_8457c_certified": False,
        "within_local_limits": elapsed <= 30 and asset_bytes <= 16 * 2**20,
    }
    (output / "complete-evaluation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
