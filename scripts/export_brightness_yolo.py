from __future__ import annotations

import sys

from micro_design_project.cli import main


if __name__ == "__main__":
    main(["export-brightness-yolo", *sys.argv[1:]])
