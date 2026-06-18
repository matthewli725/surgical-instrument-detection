from __future__ import annotations

import json
import os

from trayguard.web.app import create_app


def write_module(tmp_path, payload):
    path = tmp_path / "module.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_create_app_reads_env_paths(monkeypatch, tmp_path, tiny_module_payload):
    module_path = write_module(tmp_path, tiny_module_payload)
    runs_dir = tmp_path / "runs"
    monkeypatch.setenv("TRAYGUARD_MODULE_PATH", str(module_path))
    monkeypatch.setenv("TRAYGUARD_RUNS_DIR", str(runs_dir))

    app = create_app()

    assert app.state.module.module_id == "tiny_module"
    assert os.fspath(app.state.store.root) == os.fspath(runs_dir)
