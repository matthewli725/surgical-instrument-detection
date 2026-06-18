from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Sequence

import uvicorn

from trayguard.web.app import DEFAULT_MODULE, DEFAULT_RUNS_DIR, create_app


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="trayguard train-app",
        description="Launch the TrayGuard training prototype web app.",
    )
    parser.add_argument(
        "--module", type=Path, default=DEFAULT_MODULE, help="Tray module JSON file."
    )
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=DEFAULT_RUNS_DIR,
        help="Directory for learner run exports.",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host.")
    parser.add_argument("--port", type=int, default=8000, help="Bind port.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable Uvicorn reload for local UI development.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.reload:
        os.environ["TRAYGUARD_MODULE_PATH"] = str(args.module)
        os.environ["TRAYGUARD_RUNS_DIR"] = str(args.runs_dir)
        uvicorn.run(
            "trayguard.web.app:create_app",
            host=args.host,
            port=args.port,
            reload=True,
            factory=True,
        )
        return

    app = create_app(args.module, args.runs_dir)
    uvicorn.run(app, host=args.host, port=args.port)
