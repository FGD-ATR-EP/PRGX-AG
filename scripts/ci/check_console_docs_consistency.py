#!/usr/bin/env python3
"""Ensure the README console description and index dashboard details stay aligned."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
INDEX = ROOT / "index.html"

README_MARKERS = [
    "operator-oriented dashboard",
    "runtime health",
    "task status",
    "kpi cards",
    "24-hour throughput chart",
    "recent alert queue",
    "copy-ready validation commands",
    "loads repository version from `package.json`",
]

INDEX_MARKERS = [
    "Operational dashboard for PRGX-AG runtime health",
    "Operational Dashboard",
    "Task execution state from orchestrator telemetry",
    "Records Processed (24h)",
    "Recent Alerts",
    "Governance Snapshot",
    "quick validation commands",
    'id="repo-version"',
]



def _extract_operational_console_block(readme_text: str) -> str:
    pattern = re.compile(
        r"## Operational Console \(`index\.html`\)\n(.*?)(?:\n## |\Z)",
        flags=re.DOTALL,
    )
    match = pattern.search(readme_text)
    if not match:
        raise RuntimeError("README is missing the 'Operational Console (`index.html`)' section.")
    return match.group(1).lower()



def _missing_markers(text: str, markers: list[str]) -> list[str]:
    lowered = text.lower()
    return [marker for marker in markers if marker.lower() not in lowered]



def main() -> int:
    readme_text = README.read_text(encoding="utf-8")
    index_text = INDEX.read_text(encoding="utf-8")

    console_block = _extract_operational_console_block(readme_text)

    missing_readme = _missing_markers(console_block, README_MARKERS)
    missing_index = _missing_markers(index_text, INDEX_MARKERS)

    if missing_readme or missing_index:
        print("Console documentation consistency check failed.")
        if missing_readme:
            print("README console section is missing:")
            for marker in missing_readme:
                print(f"- {marker}")
        if missing_index:
            print("index.html is missing:")
            for marker in missing_index:
                print(f"- {marker}")
        return 1

    print("Console documentation consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
