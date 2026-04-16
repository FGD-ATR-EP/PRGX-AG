#!/usr/bin/env python3
"""Lightweight typo checks for governance docs and Python annotations in CI."""

from __future__ import annotations

import ast
import re
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE_DOCS = [
    "README.md",
    "SECURITY.md",
    "BUGFIX_PROPOSAL.md",
    "ATR_MF_AUGMENTED_PERCEPTION_ARCHITECTURE_TH.md",
    "OFFICIAL_SYSTEM_INTEGRATION_REPORT_TH.md",
]

PYTHON_PATHS = [ROOT / "src", ROOT / "tests"]

COMMON_TYPOS: dict[str, str] = {
    "teh": "the",
    "adn": "and",
    "goverment": "government",
    "governence": "governance",
    "enviroment": "environment",
    "securty": "security",
    "vunerability": "vulnerability",
    "vulnerabilty": "vulnerability",
    "recieve": "receive",
    "recieved": "received",
    "occured": "occurred",
    "occurence": "occurrence",
    "seperate": "separate",
    "consistant": "consistent",
    "consitency": "consistency",
    "maintainance": "maintenance",
    "dependancy": "dependency",
    "similiar": "similar",
    "commad": "command",
    "respository": "repository",
    "repostiory": "repository",
    "intergration": "integration",
    "paramter": "parameter",
    "varient": "variant",
    "infromation": "information",
    "contians": "contains",
    "wirte": "write",
    "statment": "statement",
    "langauge": "language",
}

WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z']+")



def _collect_markdown_text(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [(idx + 1, line) for idx, line in enumerate(lines)]



def _collect_python_annotations(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    entries: list[tuple[int, str]] = []

    try:
        tree = ast.parse(text)
    except SyntaxError:
        return entries

    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc and node.body:
                entries.append((node.body[0].lineno, doc))

    for token in tokenize.generate_tokens(iter(text.splitlines(keepends=True)).__next__):
        if token.type == tokenize.COMMENT:
            entries.append((token.start[0], token.string.lstrip("# ")))

    # Fallback: include file-level strings that are not docstrings but explanatory literals.
    for lineno, line in enumerate(lines, start=1):
        if "#" not in line and line.strip().startswith('"""') and line.strip().endswith('"""'):
            entries.append((lineno, line.strip('"')))

    return entries



def _find_typos(text_entries: list[tuple[int, str]]) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    for line_no, content in text_entries:
        for word in WORD_PATTERN.findall(content):
            lower_word = word.lower()
            if lower_word in COMMON_TYPOS:
                findings.append((line_no, lower_word, COMMON_TYPOS[lower_word]))
    return findings



def main() -> int:
    failures: list[str] = []

    for rel_path in GOVERNANCE_DOCS:
        path = ROOT / rel_path
        if not path.exists():
            continue
        findings = _find_typos(_collect_markdown_text(path))
        for line_no, typo, suggestion in findings:
            failures.append(f"{rel_path}:{line_no}: typo '{typo}' -> '{suggestion}'")

    for base in PYTHON_PATHS:
        for py_file in base.rglob("*.py"):
            findings = _find_typos(_collect_python_annotations(py_file))
            rel = py_file.relative_to(ROOT)
            for line_no, typo, suggestion in findings:
                failures.append(f"{rel}:{line_no}: typo '{typo}' -> '{suggestion}'")

    if failures:
        print("Detected potential typos in governance docs/Python annotations:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Typo checks passed for governance docs and Python annotations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
