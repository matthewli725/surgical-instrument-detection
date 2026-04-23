from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


LUMEN_START = 800
LUMEN_END = 80
BRIGHTNESS_LEVELS = 11


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replot brightness experiment reports from saved CSV outputs.")
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("reports/brightness_validation"),
        help="Directory containing the saved validation CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports/brightness_validation/lumen_plots"),
        help="Directory where the rewritten plots will be saved.",
    )
    return parser.parse_args(argv)


def brightness_lumens(brightness_rank: int) -> int:
    span = LUMEN_START - LUMEN_END
    return int(round(LUMEN_START - (span * (brightness_rank - 1) / (BRIGHTNESS_LEVELS - 1))))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_plot(path: Path, fig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def make_line_plot(
    rows: list[dict[str, str]],
    *,
    x_field: str,
    y_field: str,
    series_field: str,
    title: str,
    x_label: str,
    output_path: Path,
    invert_x: bool = True,
    y_limit: tuple[float, float] | None = None,
) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row[series_field]].append(row)

    fig, ax = plt.subplots(figsize=(9, 5))
    for series_name, series_rows in sorted(grouped.items()):
        ordered = sorted(series_rows, key=lambda row: int(row[x_field]), reverse=True)
        xs = [int(row[x_field]) for row in ordered]
        ys = [float(row[y_field]) for row in ordered]
        ax.plot(xs, ys, marker="o", label=series_name)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_field.replace("_", " ").title())
    ax.set_xticks(sorted({int(row[x_field]) for row in rows}, reverse=True))
    if y_limit is not None:
        ax.set_ylim(*y_limit)
    if invert_x:
        ax.invert_xaxis()
    ax.grid(alpha=0.25)
    ax.legend()
    write_plot(output_path, fig)


def make_bar_plot(rows: list[dict[str, str]], *, output_path: Path, title: str) -> None:
    test_rows = [row for row in rows if row["split"] == "test"]
    stage_names = [row["stage"] for row in test_rows]
    recalls = [float(row["recall"]) for row in test_rows]
    map50s = [float(row["map50"]) for row in test_rows]
    map95s = [float(row["map50_95"]) for row in test_rows]

    x = list(range(len(stage_names)))
    width = 0.22
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar([value - width for value in x], recalls, width=width, label="Recall")
    ax.bar(x, map50s, width=width, label="mAP50")
    ax.bar([value + width for value in x], map95s, width=width, label="mAP50-95")
    ax.set_title(title)
    ax.set_ylabel("Score")
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(stage_names, rotation=20, ha="right")
    ax.legend()
    write_plot(output_path, fig)


def make_two_panel_plot(
    rows: list[dict[str, str]],
    *,
    output_path: Path,
    title: str,
    y_field: str,
    x_label: str,
    left_stage: str,
    right_stage: str,
    left_title: str,
    right_title: str,
) -> None:
    left_rows = [row for row in rows if row["stage"] == left_stage]
    right_rows = [row for row in rows if row["stage"] == right_stage]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    for ax, stage_rows, panel_title in (
        (axes[0], left_rows, left_title),
        (axes[1], right_rows, right_title),
    ):
        ordered = sorted(stage_rows, key=lambda row: int(row["estimated_lumens"]), reverse=True)
        xs = [int(row["estimated_lumens"]) for row in ordered]
        ys = [float(row[y_field]) for row in ordered]
        ax.plot(xs, ys, marker="o", linewidth=2)
        ax.set_title(panel_title)
        ax.set_xlabel(x_label)
        ax.set_xticks(xs)
        ax.invert_xaxis()
        ax.grid(alpha=0.25)

    axes[0].set_ylabel(y_field.replace("_", " ").title())
    fig.suptitle(title)
    write_plot(output_path, fig)


def add_lumens(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched: list[dict[str, str]] = []
    for row in rows:
        new_row = dict(row)
        if "brightness_rank" in row and row["brightness_rank"]:
            new_row["estimated_lumens"] = str(brightness_lumens(int(row["brightness_rank"])))
        enriched.append(new_row)
    return enriched


def select_brightness_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], bool]:
    preferred = [
        row for row in rows
        if row["stage"] in {"brightest_train_darker_test", "darkest_train_brighter_test"}
        and row["eval_label"] == "test"
    ]
    if preferred:
        return preferred, True

    legacy = [
        row for row in rows
        if row["stage"] in {"bright_train_dim_test", "dim_train_bright_test"}
        and row["eval_label"] == "test"
    ]
    return legacy, False


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    stage_metrics = read_csv(args.reports_dir / "stage_metrics.csv")
    brightness_metrics = add_lumens(read_csv(args.reports_dir / "brightness_map_metrics.csv"))
    grouped_metrics = add_lumens(read_csv(args.reports_dir / "grouped_metrics.csv"))

    make_bar_plot(
        stage_metrics,
        output_path=args.output_dir / "stage_test_overview.png",
        title="Brightness Experiment Stage Overview",
    )

    brightness_rows, using_anchor_stages = select_brightness_rows(brightness_metrics)
    brightness_title = "Brightness Degradation" if using_anchor_stages else "Brightness Transfer"
    left_stage = "darkest_train_brighter_test" if using_anchor_stages else "dim_train_bright_test"
    right_stage = "brightest_train_darker_test" if using_anchor_stages else "bright_train_dim_test"
    left_panel_title = "Train darkest, test brighter" if using_anchor_stages else "Train dim, test bright"
    right_panel_title = "Train brightest, test darker" if using_anchor_stages else "Train bright, test dim"

    make_line_plot(
        brightness_rows,
        x_field="estimated_lumens",
        y_field="map50_95",
        series_field="stage",
        title=f"{brightness_title} mAP50-95 By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "brightness_map50_95.png",
    )

    make_two_panel_plot(
        brightness_metrics,
        output_path=args.output_dir / "brightness_map50_95_panels.png",
        title=f"{brightness_title} mAP50-95",
        y_field="map50_95",
        x_label="Estimated Lumens",
        left_stage=left_stage,
        right_stage=right_stage,
        left_title=left_panel_title,
        right_title=right_panel_title,
    )

    make_line_plot(
        brightness_rows,
        x_field="estimated_lumens",
        y_field="recall",
        series_field="stage",
        title=f"{brightness_title} Recall By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "brightness_test_recall.png",
    )

    make_two_panel_plot(
        brightness_metrics,
        output_path=args.output_dir / "brightness_test_recall_panels.png",
        title=f"{brightness_title} Recall",
        y_field="recall",
        x_label="Estimated Lumens",
        left_stage=left_stage,
        right_stage=right_stage,
        left_title=left_panel_title,
        right_title=right_panel_title,
    )

    make_line_plot(
        [row for row in brightness_metrics if row["stage"] in {"matte_train_reflective_test", "reflective_train_matte_test"} and row["eval_label"] == "test"],
        x_field="estimated_lumens",
        y_field="map50_95",
        series_field="stage",
        title="Background Transfer mAP50-95 By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "background_transfer_map50_95.png",
    )

    make_line_plot(
        [row for row in brightness_metrics if row["stage"] in {"matte_train_reflective_test", "reflective_train_matte_test"} and row["eval_label"] == "test"],
        x_field="estimated_lumens",
        y_field="recall",
        series_field="stage",
        title="Background Transfer Recall By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "background_transfer_recall.png",
    )

    make_line_plot(
        [row for row in brightness_metrics if row["stage"] == "separated_train_overlay_test" and row["eval_label"] in {"test", "separated_baseline"}],
        x_field="estimated_lumens",
        y_field="map50_95",
        series_field="eval_label",
        title="Separated Vs Overlay mAP50-95 By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "overlay_map50_95.png",
    )

    make_line_plot(
        [row for row in grouped_metrics if row["stage"] == "separated_train_overlay_test" and row["eval_label"] in {"test", "separated_baseline"}],
        x_field="estimated_lumens",
        y_field="exact_count_rate",
        series_field="eval_label",
        title="Separated Vs Overlay Exact Count Rate By Estimated Lumens",
        x_label="Estimated Lumens",
        output_path=args.output_dir / "overlay_gap_exact_count.png",
    )

    print(f"Wrote lumen plots to: {args.output_dir}")


if __name__ == "__main__":
    main()
