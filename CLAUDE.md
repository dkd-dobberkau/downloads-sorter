# CLAUDE.md - Development Guidelines for downloads-sorter

## Build & Installation
```bash
# Build and install locally
bash build_and_install.sh

# Install in development mode
pip install -e .
```

## Code Style
- Format code with Black (line-length=88)
- Sort imports with isort (profile=black)
- Follow PEP 8 naming conventions:
  - snake_case for functions, variables, methods
  - CamelCase for classes
  - UPPER_CASE for constants
- Use docstrings for all functions, classes, and modules

## Typing
- Add type hints to all function signatures
- Use Optional[T] for nullable values

## Error Handling
- Use specific exception types
- Log exceptions through the logger module
- Provide clear error messages to users

## Linting & Testing
```bash
# Run formatter 
black downloads_sorter/

# Run linter
flake8 downloads_sorter/

# Run tests (when implemented)
pytest 
```

## Documentation
- Keep docstrings up to date
- Document CLI changes in README.md