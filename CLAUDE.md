# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Install in development mode
pip install -e .

# Build and install locally (includes build deps)
bash build_and_install.sh

# Run the CLI
downloads-sorter              # Sort downloads
downloads-sorter --dry-run    # Preview without moving
downloads-sorter --stats      # Show statistics
downloads-sorter -d /path     # Custom directory

# Format code
black downloads_sorter/

# Lint
flake8 downloads_sorter/

# Test (when implemented)
pytest
```

## Architecture

This is a Python CLI tool that organizes files in a downloads folder by moving them into categorized subfolders.

### Core Modules

- **`sorter.py`**: Core sorting logic
  - `FILE_TYPES` dict: Maps file extensions to target folders (e.g., `.pdf` → `_pdf`)
  - `SPECIAL_PATTERNS` dict: Maps filename patterns to semantic folders (e.g., `"invoice"` → `_receipts`)
  - `sort_file()`: Sorts a single file - checks patterns first, then extension, falls back to `_misc`
  - `sort_downloads()`: Iterates top-level files in directory and sorts each
  - `get_stats()`: Returns organization statistics

- **`cli.py`**: argparse CLI with `main()` entry point registered as `downloads-sorter` console script

- **`__init__.py`**: Exposes `sort_downloads` and `get_downloads_dir` for library usage; defines `__version__`

### Sorting Logic Priority

1. Check filename against `SPECIAL_PATTERNS` (pattern-based semantic folders)
2. Check file extension against `FILE_TYPES` (extension-based folders)
3. Fall back to `_misc` folder

All target folders are prefixed with `_` (e.g., `_pdf`, `_receipts`).

## Release Process

```bash
# Release new version (updates pyproject.toml + __init__.py, commits, tags)
./release.sh 0.2.0

# Push to GitHub with tags
git push origin main --tags

# Build and upload to PyPI
python -m build
twine upload dist/*
```

Version is maintained in two files (keep in sync):
- `pyproject.toml` → `version = "X.Y.Z"`
- `downloads_sorter/__init__.py` → `__version__ = 'X.Y.Z'`

## Code Style

- Black formatter (line-length=88)
- isort with black profile
- Type hints on function signatures
- Use `Optional[T]` for nullable values
