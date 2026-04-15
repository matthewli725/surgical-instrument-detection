# TrayGuard


## Automated Surgical Tray Inspection Using Computer Vision

## Overview

TrayGuard is a computer vision system designed to automatically detect and analyze surgical instruments on preparation trays. The goal of the system is to help reduce surgical errors by verifying the presence, identity, and condition of surgical tools before procedures begin.

TrayGuard uses a two-stage computer vision architecture that separates instrument detection from fine-grained classification. This modular approach improves robustness when instruments overlap, appear in varying tray configurations, or have visually similar shapes.

***

## System Architecture

TrayGuard uses a segment–then–classify pipeline.

The system operates in two primary stages:

* Instrument Detection and Segmentation
* Fine-Grained Instrument Classification

Separating these tasks allows the system to handle overlapping instruments and visually similar tool types more effectively.

***

## Getting Started

### Step 1: Learn `uv`

We use **`uv`** exclusively for dependency management.

Please do **not** use `conda`, `pip`, or `setup.py` workflows for development.

- [Install `uv`](https://docs.astral.sh/uv/)
- [Recommended `uv` tutorial](https://youtu.be/AMdG7IjgSPM?si=35yro7e7aX2WCrTN)

### Step 2: Clone this repo

```bash
# HTTPS
git clone https://git.capstone.uclalemur.com/2026/building/micro-design-project.git

# SSH
git clone ssh://git@git.capstone.uclalemur.com:5522/2026/building/micro-design-project.git
```

### Step 3: Installation

```bash
uv sync
```

## Usage

### Command Line

Run demos

```bash
uv run scripts/demo.py
```

Collect webcam training data

```bash
uv run trayguard collect
```

The collection tool uses setup sessions for lighting variation. Press `SPACE` or `c` to capture a reference image, draw boxes around the fixed objects, then press `s` to lock that setup. After that, vary the lighting and press `SPACE` or `c` to save each additional image with the same labels. Press `e` to edit the setup boxes, `n` to start a new setup, or `q` to quit.

When labeling a box, type the class name or class number directly in the popup and press `ENTER`. Press `TAB` to autocomplete matching classes, `ESC` to discard the pending box, or `u` to undo the last saved box. Unknown class names require a second `ENTER` before they are added.

By default, session data is saved to `data/collected/sessions`, and class names are saved to `data/collected/classes.txt`.

Export collected sessions to YOLO format

```bash
uv run trayguard export-yolo --overwrite
```

The exporter writes a train/val/test YOLO dataset to `data/collected_yolo`, splitting by setup session so lighting variants from the same object placement stay in the same split.

Train one model

```bash
uv run trayguard train
```

Training uses Hydra configs in `config`. Override model or trainer settings at the command line:

```bash
uv run trayguard train model=yolo11m trainer.imgsz=960 trainer.batch=8 trainer.name=yolo11m_custom
```

Compare model variants

```bash
uv run trayguard benchmark
```

The benchmark command trains the standard YOLO/RT-DETR variants listed in `src/micro_design_project/training/benchmark.py`, evaluates each run on the YOLO test split, and writes results to `runs/benchmark_results.json`.

## Project Layout

Reusable project code lives under `src/micro_design_project`. The main CLI entrypoint is `uv run trayguard ...`; files in `scripts` are kept as small convenience wrappers for direct execution.

Current data collection modules:

- `src/micro_design_project/cli.py`: top-level `trayguard` command dispatcher
- `src/micro_design_project/data_collection/collect.py`: data collection orchestration
- `src/micro_design_project/data_collection/annotation_ui.py`: popup box drawing, class entry, and autocomplete
- `src/micro_design_project/data_collection/camera.py`: webcam capture loops
- `src/micro_design_project/data_collection/session_io.py`: session folders, shared YOLO labels, and metadata
- `src/micro_design_project/data_collection/models.py`: `Box` and `CollectionSession`
- `src/micro_design_project/data_collection/classes.py`: default classes and `classes.txt` handling
- `src/micro_design_project/data_collection/drawing.py`: OpenCV overlay drawing helpers
- `src/micro_design_project/dataset_tools/export_collected_yolo.py`: export collected sessions into a YOLO train/val/test dataset
- `src/micro_design_project/training/train.py`: train one configured object detection model
- `src/micro_design_project/training/benchmark.py`: train and evaluate multiple model variants
- `scripts/collect_data.py`: command wrapper for data collection
- `scripts/export_collected_yolo.py`: command wrapper for YOLO export
- `scripts/train.py`: command wrapper for single-model training
- `scripts/evaluate_all.py`: command wrapper for variant benchmarking
