from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONSISTENCY_SCRIPT = ROOT / "scripts" / "ci" / "check_console_docs_consistency.py"
TYPO_SCRIPT = ROOT / "scripts" / "ci" / "check_typos.py"


def test_console_consistency_script_has_single_main_definition() -> None:
    tree = ast.parse(CONSISTENCY_SCRIPT.read_text(encoding="utf-8"))
    main_defs = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "main"
    ]
    assert len(main_defs) == 1


def test_console_consistency_script_executes_successfully() -> None:
    completed = subprocess.run(
        [sys.executable, str(CONSISTENCY_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_typo_script_executes_successfully() -> None:
    completed = subprocess.run(
        [sys.executable, str(TYPO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
