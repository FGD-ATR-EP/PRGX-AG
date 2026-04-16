"""Tests for scripts/ci/check_typos.py."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add scripts/ci to import path so the module can be imported directly.
_CI_DIR = Path(__file__).resolve().parents[1] / "scripts" / "ci"
if str(_CI_DIR) not in sys.path:
    sys.path.insert(0, str(_CI_DIR))

import check_typos  # noqa: E402


# ---------------------------------------------------------------------------
# _collect_markdown_text
# ---------------------------------------------------------------------------

def test_collect_markdown_text_line_numbers_start_at_one(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("line one\nline two\n", encoding="utf-8")
    result = check_typos._collect_markdown_text(md)
    assert result[0] == (1, "line one")
    assert result[1] == (2, "line two")


def test_collect_markdown_text_empty_file(tmp_path: Path) -> None:
    md = tmp_path / "empty.md"
    md.write_text("", encoding="utf-8")
    result = check_typos._collect_markdown_text(md)
    assert result == []


def test_collect_markdown_text_preserves_content(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("## Governance\nSome content here.\n", encoding="utf-8")
    result = check_typos._collect_markdown_text(md)
    assert len(result) == 2
    assert result[0] == (1, "## Governance")
    assert result[1] == (2, "Some content here.")


def test_collect_markdown_text_single_line_no_newline(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text("only line", encoding="utf-8")
    result = check_typos._collect_markdown_text(md)
    assert result == [(1, "only line")]


# ---------------------------------------------------------------------------
# _collect_python_annotations
# ---------------------------------------------------------------------------

def test_collect_python_annotations_module_docstring(tmp_path: Path) -> None:
    py = tmp_path / "mod.py"
    py.write_text('"""Module-level docstring."""\n\nx = 1\n', encoding="utf-8")
    result = check_typos._collect_python_annotations(py)
    texts = [text for _, text in result]
    assert any("Module-level docstring" in t for t in texts)


def test_collect_python_annotations_function_docstring(tmp_path: Path) -> None:
    py = tmp_path / "funcs.py"
    py.write_text(
        'def foo():\n    """Function docstring."""\n    pass\n',
        encoding="utf-8",
    )
    result = check_typos._collect_python_annotations(py)
    texts = [text for _, text in result]
    assert any("Function docstring" in t for t in texts)


def test_collect_python_annotations_class_docstring(tmp_path: Path) -> None:
    py = tmp_path / "cls.py"
    py.write_text(
        'class MyClass:\n    """Class docstring text."""\n    pass\n',
        encoding="utf-8",
    )
    result = check_typos._collect_python_annotations(py)
    texts = [text for _, text in result]
    assert any("Class docstring text" in t for t in texts)


def test_collect_python_annotations_async_function_docstring(tmp_path: Path) -> None:
    py = tmp_path / "async_func.py"
    py.write_text(
        'async def bar():\n    """Async function docstring."""\n    pass\n',
        encoding="utf-8",
    )
    result = check_typos._collect_python_annotations(py)
    texts = [text for _, text in result]
    assert any("Async function docstring" in t for t in texts)


def test_collect_python_annotations_syntax_error_returns_empty(tmp_path: Path) -> None:
    py = tmp_path / "broken.py"
    py.write_text("def foo(\n    invalid syntax here\n", encoding="utf-8")
    result = check_typos._collect_python_annotations(py)
    assert result == []


def test_collect_python_annotations_no_docstrings_returns_list(tmp_path: Path) -> None:
    py = tmp_path / "nodoc.py"
    py.write_text("x = 1\ny = 2\n", encoding="utf-8")
    # Should not raise; may return empty or inline triple-quote entries only
    result = check_typos._collect_python_annotations(py)
    assert isinstance(result, list)


def test_collect_python_annotations_entries_are_tuples(tmp_path: Path) -> None:
    py = tmp_path / "mod.py"
    py.write_text('"""Docstring."""\n', encoding="utf-8")
    result = check_typos._collect_python_annotations(py)
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2
        assert isinstance(item[0], int)
        assert isinstance(item[1], str)


# ---------------------------------------------------------------------------
# _find_typos
# ---------------------------------------------------------------------------

def test_find_typos_returns_empty_for_clean_text() -> None:
    entries = [(1, "This is a clean sentence with correct spelling.")]
    result = check_typos._find_typos(entries)
    assert result == []


def test_find_typos_detects_known_typo() -> None:
    entries = [(3, "We need teh configuration.")]
    result = check_typos._find_typos(entries)
    assert len(result) == 1
    line_no, typo, suggestion = result[0]
    assert line_no == 3
    assert typo == "teh"
    assert suggestion == "the"


def test_find_typos_case_insensitive_detection() -> None:
    entries = [(5, "The Goverment policy.")]
    result = check_typos._find_typos(entries)
    assert len(result) == 1
    _, typo, suggestion = result[0]
    assert typo == "goverment"
    assert suggestion == "government"


def test_find_typos_multiple_typos_on_same_line() -> None:
    entries = [(7, "Teh adn the configuration.")]
    result = check_typos._find_typos(entries)
    typos_found = {t for _, t, _ in result}
    assert "teh" in typos_found
    assert "adn" in typos_found


def test_find_typos_multiple_lines() -> None:
    entries = [
        (1, "No issues here."),
        (2, "There is a recieve problem."),
        (3, "And also an occured issue."),
    ]
    result = check_typos._find_typos(entries)
    assert len(result) == 2
    line_numbers = {ln for ln, _, _ in result}
    assert 2 in line_numbers
    assert 3 in line_numbers


def test_find_typos_preserves_line_number() -> None:
    entries = [(42, "This has a vunerability in it.")]
    result = check_typos._find_typos(entries)
    assert result[0][0] == 42


def test_find_typos_word_not_matching_pattern_ignored() -> None:
    # Single character "a" won't match [A-Za-z][A-Za-z']+ (needs at least 2 chars)
    entries = [(1, "a b c")]
    result = check_typos._find_typos(entries)
    assert result == []


def test_find_typos_empty_entries() -> None:
    result = check_typos._find_typos([])
    assert result == []


def test_find_typos_all_known_typos_in_dict() -> None:
    # Verify each entry in COMMON_TYPOS is detected
    for typo_word, correction in check_typos.COMMON_TYPOS.items():
        entries = [(1, f"text {typo_word} more text")]
        result = check_typos._find_typos(entries)
        assert len(result) >= 1, f"Expected typo '{typo_word}' to be detected"
        found_typos = {t for _, t, _ in result}
        assert typo_word in found_typos


def test_find_typos_correct_word_not_flagged() -> None:
    # "the" is correct; "teh" is the typo - ensure correct words are not flagged
    entries = [(1, "the government repository security environment")]
    result = check_typos._find_typos(entries)
    assert result == []


# ---------------------------------------------------------------------------
# main() – integration using temporary files
# ---------------------------------------------------------------------------

def test_main_returns_zero_when_no_typos(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Point ROOT to tmp_path, with empty governance docs and no python paths
    readme = tmp_path / "README.md"
    readme.write_text("# README\nAll good here.\n", encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", ["README.md"])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    result = check_typos.main()
    assert result == 0


def test_main_returns_one_when_typo_found(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("# README\nThe enviroment is configured.\n", encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", ["README.md"])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    result = check_typos.main()
    assert result == 1


def test_main_skips_missing_governance_doc(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # A governance doc that does not exist should be silently skipped
    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", ["MISSING_FILE.md"])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    result = check_typos.main()
    assert result == 0


def test_main_scans_python_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    py_file = src_dir / "module.py"
    py_file.write_text('"""Contains a vunerability check."""\n\nx = 1\n', encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", [])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [src_dir])

    result = check_typos.main()
    assert result == 1


def test_main_prints_pass_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", [])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    check_typos.main()
    captured = capsys.readouterr()
    assert "passed" in captured.out.lower()


def test_main_prints_failure_details(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("The goverment setup.\n", encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", ["README.md"])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    check_typos.main()
    captured = capsys.readouterr()
    assert "goverment" in captured.out
    assert "government" in captured.out


def test_main_clean_python_file_returns_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    py_file = src_dir / "clean.py"
    py_file.write_text('"""A clean module with no typos."""\n\ndef foo():\n    pass\n', encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", [])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [src_dir])

    result = check_typos.main()
    assert result == 0


def test_main_multiple_governance_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc1 = tmp_path / "A.md"
    doc2 = tmp_path / "B.md"
    doc1.write_text("All correct.\n", encoding="utf-8")
    doc2.write_text("Also correct.\n", encoding="utf-8")

    monkeypatch.setattr(check_typos, "ROOT", tmp_path)
    monkeypatch.setattr(check_typos, "GOVERNANCE_DOCS", ["A.md", "B.md"])
    monkeypatch.setattr(check_typos, "PYTHON_PATHS", [])

    result = check_typos.main()
    assert result == 0