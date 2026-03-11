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
