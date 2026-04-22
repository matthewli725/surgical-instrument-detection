# GitLab Epic Map

This document summarizes the project workstreams and milestone checkpoints.

## Epics

| Epic | Goal | Typical Labels |
| --- | --- | --- |
| Sensing And Capture | Build the physical and data-collection layer: camera setup, lighting setup, tray framing, capture workflow, and dataset inputs. | `epic::sensing-capture`, `category::hardware`, `category::capture`, `category::lighting` |
| Perception | Build and evaluate the detector layer: training, metrics, confidence behavior, similar-class confusion, and robustness experiments. | `epic::perception`, `category::similar`, `category::lighting`, `category::ml` |
| Tray Logic And Decision Support | Define what the system means by present, missing, extra, and review-needed, and connect detections to tray-level results. | `epic::tray-logic`, `category::scope`, `category::workflow` |
| Technician UI And Workflow | Make the live prototype usable as a technician-facing assistant with understandable workflow, correction paths, and review prompts. | `epic::technician-ui`, `category::ui`, `category::workflow`, `category::demo` |
| Traceability And Reporting | Add saved records, reports, and workflow evidence so TrayGuard can support a quality and audit story. | `epic::traceability-reporting`, `category::logging`, `category::reporting`, `category::workflow` |

## Milestones

### Sensing And Capture

- `Sensing / Physical Capture Setup Ready`
- `Sensing / Collection Pipeline Ready`
- `Sensing / Material And Lighting Assumptions Ready`
- `Sensing / Lighting Dataset Ready`

### Perception

- `Perception / Experiment Questions Locked`
- `Perception / Lighting Results Ready`
- `Perception / Similar Baseline Ready`
- `Perception / Demo Model Ready`

### Tray Logic And Decision Support

- `Tray Logic / Result Semantics Defined`
- `Tray Logic / Decision Support Implemented`

### Technician UI And Workflow

- `UI / Baseline Workflow Defined`
- `UI / Workflow Gap Review Complete`
- `UI / Tray Review Flow Improved`
- `UI / Walkthrough Evidence Ready`
- `UI / Demo Flow Ready`

### Traceability And Reporting

- `Traceability / Record Schema Ready`
- `Traceability / Logging Implemented`
- `Traceability / Reporting Ready`
