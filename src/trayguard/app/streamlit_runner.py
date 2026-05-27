from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence


APP_PATH = Path(__file__).with_name("streamlit_app.py")


def main(argv: Sequence[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    command = [sys.executable, "-m", "streamlit", "run", str(APP_PATH), *args]
    raise SystemExit(subprocess.run(command, check=False).returncode)
