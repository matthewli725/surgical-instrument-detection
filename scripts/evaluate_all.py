from pathlib import Path
import subprocess
import sys
import json

from ultralytics import YOLO

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRAIN_SCRIPT = PROJECT_ROOT / "scripts" / "train.py"
RESULTS_JSON = PROJECT_ROOT / "runs" / "benchmark_results.json"

TESTS = [
    ("yolo11n", 640, 16),
    ("yolo11s", 640, 16),
    ("yolo11s", 960, 16),
    ("yolo11m", 640, 16),
    ("yolo11m", 960, 8),
    ("yolo11l", 640, 16),
    ("yolo11l", 960, 6),
    ("rtdetr-l", 640, 8),
    # ("rtdetr-l", 960, 6),
]


def build_run_name(model: str, imgsz: int, batch: int) -> str:
    return f"{model}_imgsz{imgsz}_batch{batch}"


def run_train(model: str, imgsz: int, batch: int) -> int:
    run_name = build_run_name(model, imgsz, batch)

    cmd = [
        sys.executable,
        str(TRAIN_SCRIPT),
        f"model={model}",
        f"trainer.imgsz={imgsz}",
        f"trainer.batch={batch}",
        f"trainer.name={run_name}"
    ]

    if model == "rtdetr-l":
        cmd.append("trainer.lr0=0.003")

    print("\n")
    print("Running:")
    print(" ".join(cmd))
    print("\n")

    process = subprocess.Popen(
        cmd,
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )

    for line in process.stdout:
        print(line, end="")

    process.wait()

    return process.returncode, run_name


def evaluate_model(run_name, imgsz):

    weights = PROJECT_ROOT / "runs" / "detect" / "runs" / run_name / "weights" / "best.pt"
    data_yaml = PROJECT_ROOT / "datasets" / "dataset_obj_detection" / "data.yaml"

    print("\nEvaluating test set:", run_name)

    model = YOLO(str(weights))

    metrics = model.val(
        data=str(data_yaml),
        split="test",
        imgsz=imgsz,
        plots=False,
        verbose=False
    )

    precision = float(metrics.box.mp)
    recall = float(metrics.box.mr)
    map50 = float(metrics.box.map50)
    map50_95 = float(metrics.box.map)

    speed = metrics.speed or {}

    latency = (
        float(speed.get("preprocess", 0))
        + float(speed.get("inference", 0))
        + float(speed.get("postprocess", 0))
    )

    fp_rate_approx = 1 - precision

    return {
        "precision": precision,
        "recall": recall,
        "map50": map50,
        "map50_95": map50_95,
        "latency_ms": latency,
        "fp_rate_approx": fp_rate_approx,
        "weights": str(weights)
    }


def save_results(results):

    RESULTS_JSON.parent.mkdir(exist_ok=True)

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nSaved results to:", RESULTS_JSON)


def main():
    results = []
    for model, imgsz, batch in TESTS:
        entry = {
                "model": model,
                "imgsz": imgsz,
                "batch": batch
        }

        try:
            code, run_name = run_train(model, imgsz, batch)

            if code != 0:
                entry["status"] = "training_failed"
                results.append(entry)
                save_results(results)
                continue

            metrics = evaluate_model(run_name, imgsz)

            entry.update(metrics)
            entry["run_name"] = run_name
            entry["status"] = "completed"

        except Exception as e:
            entry["status"] = "error"
            entry["error"] = str(e)

        results.append(entry)

        save_results(results)

    print("\nFINAL RESULTS")

    for r in results:
        print(r)


if __name__ == "__main__":
    main()