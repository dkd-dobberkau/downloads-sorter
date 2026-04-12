"""Tests for downloads_sorter.sorter module."""

import pytest
from pathlib import Path
from downloads_sorter.sorter import (
    get_downloads_dir,
    ensure_dir_exists,
    get_unique_path,
    sort_file,
    sort_downloads,
    get_stats,
)


@pytest.fixture
def tmp_downloads(tmp_path):
    """Create a temporary downloads directory with test files."""
    return tmp_path


def _create_file(directory: Path, name: str, content: str = "test") -> Path:
    """Helper to create a test file."""
    path = directory / name
    path.write_text(content)
    return path


# --- get_downloads_dir ---

def test_get_downloads_dir():
    result = get_downloads_dir()
    assert result == Path.home() / "Downloads"


# --- ensure_dir_exists ---

def test_ensure_dir_exists_creates_new(tmp_path):
    new_dir = tmp_path / "subdir"
    assert not new_dir.exists()
    result = ensure_dir_exists(new_dir)
    assert new_dir.exists()
    assert result == new_dir


def test_ensure_dir_exists_existing(tmp_path):
    result = ensure_dir_exists(tmp_path)
    assert result == tmp_path


def test_ensure_dir_exists_nested(tmp_path):
    nested = tmp_path / "a" / "b" / "c"
    ensure_dir_exists(nested)
    assert nested.exists()


# --- get_unique_path ---

def test_get_unique_path_no_conflict(tmp_path):
    target = tmp_path / "file.txt"
    assert get_unique_path(target) == target


def test_get_unique_path_one_conflict(tmp_path):
    existing = tmp_path / "file.txt"
    existing.write_text("x")
    result = get_unique_path(existing)
    assert result == tmp_path / "file(1).txt"


def test_get_unique_path_multiple_conflicts(tmp_path):
    (tmp_path / "file.txt").write_text("x")
    (tmp_path / "file(1).txt").write_text("x")
    (tmp_path / "file(2).txt").write_text("x")
    result = get_unique_path(tmp_path / "file.txt")
    assert result == tmp_path / "file(3).txt"


# --- sort_file ---

def test_sort_file_by_extension(tmp_downloads):
    pdf = _create_file(tmp_downloads, "document.pdf")
    result = sort_file(pdf, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_pdf"
    assert not pdf.exists()  # original moved


def test_sort_file_by_special_pattern(tmp_downloads):
    invoice = _create_file(tmp_downloads, "Rechnung_2024.pdf")
    result = sort_file(invoice, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_receipts"  # pattern takes priority over .pdf


def test_sort_file_unknown_extension(tmp_downloads):
    unknown = _create_file(tmp_downloads, "data.xyz")
    result = sort_file(unknown, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_misc"


def test_sort_file_hidden_file(tmp_downloads):
    hidden = _create_file(tmp_downloads, ".hidden")
    result = sort_file(hidden, tmp_downloads)
    assert result is None
    assert hidden.exists()  # not moved


def test_sort_file_skip_file(tmp_downloads):
    ds_store = _create_file(tmp_downloads, ".DS_Store")
    result = sort_file(ds_store, tmp_downloads)
    assert result is None


def test_sort_file_dry_run(tmp_downloads):
    pdf = _create_file(tmp_downloads, "document.pdf")
    result = sort_file(pdf, tmp_downloads, dry_run=True)
    assert result is not None
    assert pdf.exists()  # original NOT moved in dry run


def test_sort_file_not_a_file(tmp_downloads):
    subdir = tmp_downloads / "subdir"
    subdir.mkdir()
    result = sort_file(subdir, tmp_downloads)
    assert result is None


def test_sort_file_dmg_goes_to_applications(tmp_downloads):
    dmg = _create_file(tmp_downloads, "installer.dmg")
    result = sort_file(dmg, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_applications"


def test_sort_file_screenshot_pattern(tmp_downloads):
    screenshot = _create_file(tmp_downloads, "Screenshot 2024-01-15.png")
    result = sort_file(screenshot, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_screenshots"


def test_sort_file_case_insensitive_pattern(tmp_downloads):
    invoice = _create_file(tmp_downloads, "INVOICE_123.pdf")
    result = sort_file(invoice, tmp_downloads)
    assert result is not None
    assert result.parent.name == "_receipts"


def test_sort_file_collision_handling(tmp_downloads):
    _create_file(tmp_downloads, "doc.pdf")
    result1 = sort_file(tmp_downloads / "doc.pdf", tmp_downloads)
    # Create another file with same name
    _create_file(tmp_downloads, "doc.pdf")
    result2 = sort_file(tmp_downloads / "doc.pdf", tmp_downloads)
    assert result1.name == "doc.pdf"
    assert result2.name == "doc(1).pdf"


# --- sort_downloads ---

def test_sort_downloads_mixed_files(tmp_downloads):
    _create_file(tmp_downloads, "report.pdf")
    _create_file(tmp_downloads, "photo.jpg")
    _create_file(tmp_downloads, "archive.zip")
    _create_file(tmp_downloads, ".DS_Store")

    result = sort_downloads(tmp_downloads)
    assert result["processed"] == 4
    assert result["moved"] == 3
    assert result["skipped"] == 1
    assert result["errors"] == 0


def test_sort_downloads_empty_directory(tmp_downloads):
    result = sort_downloads(tmp_downloads)
    assert result["processed"] == 0
    assert result["moved"] == 0
    assert result["errors"] == 0


def test_sort_downloads_dry_run(tmp_downloads):
    _create_file(tmp_downloads, "report.pdf")
    _create_file(tmp_downloads, "photo.jpg")

    result = sort_downloads(tmp_downloads, dry_run=True)
    assert result["moved"] == 2
    # Files should still be in place
    assert (tmp_downloads / "report.pdf").exists()
    assert (tmp_downloads / "photo.jpg").exists()


def test_sort_downloads_error_tracking(tmp_downloads, monkeypatch):
    _create_file(tmp_downloads, "report.pdf")

    def mock_sort_file(*args, **kwargs):
        raise PermissionError("Access denied")

    monkeypatch.setattr("downloads_sorter.sorter.sort_file", mock_sort_file)
    result = sort_downloads(tmp_downloads)
    assert result["errors"] == 1
    assert result["moved"] == 0


# --- get_stats ---

def test_get_stats_empty(tmp_downloads):
    stats = get_stats(tmp_downloads)
    assert stats["total_files"] == 0
    assert stats["organized_files"] == 0
    assert stats["unorganized_files"] == 0


def test_get_stats_unorganized_files(tmp_downloads):
    _create_file(tmp_downloads, "loose_file.txt")
    _create_file(tmp_downloads, "another.pdf")

    stats = get_stats(tmp_downloads)
    assert stats["unorganized_files"] == 2
    assert stats["total_files"] == 2
    assert stats["organized_files"] == 0


def test_get_stats_organized_files(tmp_downloads):
    pdf_dir = tmp_downloads / "_pdf"
    pdf_dir.mkdir()
    _create_file(pdf_dir, "doc1.pdf")
    _create_file(pdf_dir, "doc2.pdf")

    stats = get_stats(tmp_downloads)
    assert stats["organized_files"] == 2
    assert stats["folders"]["_pdf"] == 2
    assert stats["file_types"][".pdf"] == 2


def test_get_stats_mixed(tmp_downloads):
    # Organized
    pdf_dir = tmp_downloads / "_pdf"
    pdf_dir.mkdir()
    _create_file(pdf_dir, "doc.pdf")
    # Unorganized
    _create_file(tmp_downloads, "loose.txt")

    stats = get_stats(tmp_downloads)
    assert stats["total_files"] == 2
    assert stats["organized_files"] == 1
    assert stats["unorganized_files"] == 1


def test_get_stats_ignores_hidden(tmp_downloads):
    _create_file(tmp_downloads, ".hidden_file")
    hidden_dir = tmp_downloads / ".hidden_dir"
    hidden_dir.mkdir()
    _create_file(hidden_dir, "secret.txt")

    stats = get_stats(tmp_downloads)
    assert stats["total_files"] == 0
