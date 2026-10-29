"""Validate the supplied experiment exports and build the browser's results data."""
import csv
import json
import math
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "VisionAI-Hub/frontend"
FOOD = ROOT / "FoodVision-AI/results"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def history(path):
    rows = read_csv(path)
    result = []
    for index, row in enumerate(rows):
        assert int(row["epoch"]) == index, f"Discontinuous epochs: {path}"
        record = {key: float(row[key]) for key in ("accuracy", "val_accuracy", "loss", "val_loss")}
        assert all(math.isfinite(v) and v >= 0 for v in record.values())
        assert record["accuracy"] <= 1 and record["val_accuracy"] <= 1
        result.append({"epoch": index + 1, **record})
    assert result, f"Empty history: {path}"
    return result


def extract_mask_results():
    # Read and validate the exported results from the executed training notebook.
    folder = ROOT / "MaskVision-AI/results"
    required = ["evaluation_metrics.json", "classification_report.csv",
                "classification_report.txt", "evaluation_output.txt", "confusion_matrix.png",
                "dataset_split.csv", "training_curves.png"]
    for name in required:
        if not (folder / name).is_file():
            raise FileNotFoundError(f"Missing exported result: {folder / name}")
    metrics = json.loads((folder / "evaluation_metrics.json").read_text(encoding="utf-8-sig"))
    return folder, metrics



def build():
    metrics = json.loads((FOOD / "evaluation_metrics.json").read_text(encoding="utf-8-sig"))
    names = json.loads((ROOT / "FoodVision-AI/model/class_names.json").read_text())
    report = {row[""]: row for row in read_csv(FOOD / "classification_report.csv")}
    classes = [{"name": name, **{key: float(report[name][key]) for key in ("precision", "recall", "f1-score")},
                "support": int(float(report[name]["support"]))} for name in names]
    assert sum(row["support"] for row in classes) == metrics["images"]
    assert abs(float(report["accuracy"]["precision"]) - metrics["accuracy"]) < 1e-6
    assert abs(float(report["macro avg"]["f1-score"]) - metrics["macro_f1"]) < 1e-6
    for row in classes:
        assert all(0 <= row[key] <= 1 for key in ("precision", "recall", "f1-score"))
    models = [
        {"name": "Baseline CNN", "history": history(FOOD / "foodvision11_baseline_history.csv")},
        {"name": "Improved CNN", "history": history(FOOD / "foodvision11_improved_history.csv")},
    ]
    comparison = []
    for row in read_csv(FOOD / "validation_comparison.csv"):
        checkpoint = min(next(model for model in models if model["name"] == row["Model"])["history"], key=lambda r: r["val_loss"])
        assert abs(checkpoint["val_accuracy"] - float(row["Validation Accuracy"])) < 1e-6
        assert abs(checkpoint["val_loss"] - float(row["Validation Loss"])) < 1e-6
        comparison.append({"name": row["Model"], "accuracy": float(row["Validation Accuracy"]), "loss": float(row["Validation Loss"])})
    assert max(comparison, key=lambda row: (row["accuracy"], -row["loss"]))["name"] == metrics["selected_model"]
    downloads = ["evaluation_metrics.json", "classification_report.csv", "validation_comparison.csv",
                 "foodvision11_improved_history.csv", "foodvision11_baseline_history.csv", "confusion_matrix.png"]
    target = FRONTEND / "results-files"
    target.mkdir(exist_ok=True)
    for name in downloads:
        shutil.copy2(FOOD / name, target / name)
    mask_path = ROOT / "MaskVision-AI/model/maskvision_baseline_history.csv"
    shutil.copy2(mask_path, target / mask_path.name)
    mask_folder, mask_metrics = extract_mask_results()
    mask_names = json.loads((ROOT / "MaskVision-AI/model/class_names.json").read_text())
    assert mask_names == ["with_mask", "without_mask"], "Expected the two-class MaskVision export"
    mask_report = {row[""]: row for row in read_csv(mask_folder / "classification_report.csv")}
    mask_classes = [{"name": name, **{key: float(mask_report[name][key]) for key in ("precision", "recall", "f1-score")},
                     "support": int(float(mask_report[name]["support"]))} for name in mask_names]
    assert sum(row["support"] for row in mask_classes) == mask_metrics["images"]
    assert abs(float(mask_report["accuracy"]["precision"]) - mask_metrics["accuracy"]) < 1e-6
    assert abs(float(mask_report["macro avg"]["f1-score"]) - mask_metrics["macro_f1"]) < 1e-6
    splits = read_csv(mask_folder / "dataset_split.csv")
    assert len(splits) == 6 and {(r["Dataset"], r["Class"]) for r in splits} == {
        (split, name) for split in ("training", "validation", "evaluation") for name in mask_names
    }
    for row in mask_classes:
        assert all(0 <= row[key] <= 1 for key in ("precision", "recall", "f1-score"))
        assert row["support"] == sum(int(r["Images"]) for r in splits
                                     if r["Dataset"] == "evaluation" and r["Class"] == row["name"])
    mask_history = history(mask_path)
    best_epoch = min(mask_history, key=lambda r: r["val_loss"])
    with Image.open(mask_folder / "confusion_matrix.png") as picture:
        matrix_width, matrix_height = picture.size
    with Image.open(FOOD / "confusion_matrix.png") as picture:
        food_width, food_height = picture.size
    mask_target = target / "mask"
    mask_target.mkdir(exist_ok=True)
    mask_downloads = ["evaluation_metrics.json", "classification_report.csv", "classification_report.txt",
                      "evaluation_output.txt", "confusion_matrix.png", "dataset_split.csv", "training_curves.png"]
    for name in mask_downloads:
        shutil.copy2(mask_folder / name, mask_target / name)
    data = {
        "food": {"evaluation": metrics, "models": models, "comparison": comparison, "classes": classes,
                 "matrix": "/hub-static/results-files/confusion_matrix.png", "downloads": downloads,
                 "matrix_width": food_width, "matrix_height": food_height},
        "mask": {"evaluation": mask_metrics, "models": [{"name": "Baseline CNN", "history": mask_history}],
                 "comparison": [], "classes": mask_classes, "matrix": "/hub-static/results-files/mask/confusion_matrix.png",
                 "matrix_width": matrix_width, "matrix_height": matrix_height,
                 "split": splits, "best_checkpoint": best_epoch,
                 "downloads": [mask_path.name] + ["mask/" + name for name in mask_downloads]},
    }
    (FRONTEND / "results-data.json").write_text(json.dumps(data, indent=2, allow_nan=False), encoding="utf-8")
    print(f"Verified metrics, class supports, checkpoint comparisons and {sum(len(m['history']) for p in data.values() for m in p['models'])} history rows.")


if __name__ == "__main__":
    build()
