# Contributing Guide

Welcome to the AI Rename Tool project! This guide outlines the process for contributing code, documentation, and bug reports.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for details.

## Getting Started

### Prerequisites
- Python 3.14+
- Git
- Familiarity with pathlib and type hints

### Setting Up Development Environment

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-rename-tool.git
   cd ai-rename-tool
   ```

2. **Create Virtual Environment**
   ```bash
   bash scripts/bootstrap-venv.sh
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify Setup**
   ```bash
   pytest -q --cov=ai_rename_tool
   ai-rename-tool --help
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 2. Make Your Changes

**Code Style:**
- Follow PEP 8 and PEP 257
- Use type hints for all function signatures (Python 3.14+ syntax)
- Keep functions pure and stateless where possible
- Prefer dataclasses for data structures

**Example:**
```python
from pathlib import Path
from typing import Sequence

def process_files(files: Sequence[Path], root: Path) -> list[str]:
    """
    Process files and return suggestions.

    Args:
        files: Files to process
        root: Root directory for relative paths

    Returns:
        List of filename suggestions
    """
    return [str(f.relative_to(root)) for f in files]
```

**Documentation:**
- Add docstrings to all public functions
- Include type annotations
- Update relevant docs in `docs/`
- Add examples for new features

**Testing:**
- Add tests for new features in `tests/`
- Ensure all tests pass
- Maintain >80% code coverage

### 3. Write and Run Tests

```bash
# Run all tests
pytest -q

# Run with coverage
pytest -q --cov=ai_rename_tool --cov-report=term-missing

# Run specific test
pytest tests/test_core.py::test_scan_paths -v
```

Example test:
```python
from pathlib import Path
from ai_rename_tool.core import scan_paths

def test_scan_paths_excludes_hidden(tmp_path):
    """Test that hidden files are excluded by default."""
    (tmp_path / "visible.txt").touch()
    (tmp_path / ".hidden.txt").touch()

    files = scan_paths(tmp_path, include_hidden=False)
    names = [f.name for f in files]

    assert "visible.txt" in names
    assert ".hidden.txt" not in names
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Test additions
- `chore:` - Build/dependency updates

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Create a pull request with:

**Title:** Brief description
```
feat: add batch rename capability
```

**Description:**
```markdown
## Summary
- Added batch rename support for multiple directories
- Implemented parallel processing for large file sets

## Testing
- Added unit tests for batch operations
- Tested with 10,000+ files
- All existing tests still pass

## Documentation
- Updated API docs with batch_rename function
- Added usage examples to README

## Checklist
- [x] Code follows PEP 8/257
- [x] All functions have type hints
- [x] Tests added and passing
- [x] Coverage >80%
- [x] Documentation updated
```

## Types of Contributions

### Bug Reports

Report bugs by creating an issue with:

1. **Title:** Concise bug description
2. **Description:**
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Python version and OS
   - Full error traceback

Example:
```markdown
## Title
Plan generation fails with symlinks

## Steps to Reproduce
1. Create directory with symlinks
2. Run: ai-rename-tool . --json plan.json
3. Observe error

## Expected
Should handle symlinks gracefully

## Actual
Raises FileNotFoundError

## Environment
- Python 3.14.0
- Ubuntu 22.04
- ai-rename-tool 1.0.0

## Traceback
[Include full traceback]
```

### Feature Requests

Request features by creating an issue with:

1. **Title:** Feature name
2. **Description:**
   - Why feature is needed
   - Use cases
   - Expected behavior

Example:
```markdown
## Title
Add support for custom provider plugins

## Need
Users want to integrate their own AI providers for suggestions

## Use Cases
- OpenAI GPT-based naming
- Custom ML model integration
- Cloud-based processing

## Expected Behavior
```python
from my_provider import my_ai_provider
plan = build_plan(root, files, provider=my_ai_provider)
```
```

## Code Review Process

### What to Expect

1. **Initial Review:** 1-3 days
2. **Feedback:** May request changes
3. **Re-review:** After updates
4. **Approval:** When ready
5. **Merge:** Into main branch

## Project Structure

```
ai-rename-tool/
├── docs/                    # Documentation (MkDocs)
├── scripts/                 # Development scripts
├── src/
│   └── ai_rename_tool/      # Main package
│       ├── cli.py          # Command-line interface
│       ├── core.py         # Core logic
│       ├── naming.py       # Naming utilities
│       └── provider.py     # Provider interface
├── tests/                   # Pytest suite
├── CHANGELOG.md            # Release history
├── CONTRIBUTING.md         # This file
├── pyproject.toml          # Project metadata
└── README.md              # Project overview
```

## Documentation Standards

### Function Docstrings
```python
def function_name(param: str, count: int = 10) -> list[str]:
    """
    One-line description.

    Longer description if needed.

    Args:
        param: Description of parameter
        count: Description with default (default: 10)

    Returns:
        Description of return value

    Raises:
        ValueError: When param is empty

    Example:
        >>> result = function_name("test", 5)
        >>> len(result)
        5
    """
```

## Versioning

The project uses Semantic Versioning via Git tags:

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Version is managed through Git tags:
```bash
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

## Testing Guidelines

### Test Coverage
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use pytest fixtures for setup

### Test Organization
```
tests/
├── test_core.py           # Core functionality tests
├── test_naming.py         # Naming utilities tests
├── test_provider.py       # Provider tests
└── test_cli.py           # CLI tests
```

## Common Mistakes to Avoid

1. **Missing type hints** - All functions need complete type annotations
2. **Not following PEP 8** - Use consistent style
3. **Hardcoded paths** - Use pathlib.Path and relative paths
4. **Mutable default arguments** - Use None and create in function
5. **Poor test coverage** - Write tests for new code
6. **Breaking changes** - Maintain backward compatibility

## Questions or Need Help?

1. Check [api.md](api.md) for API details
2. Review [architecture.md](architecture.md) for design
3. Check existing issues/PRs
4. Create a new issue

---

Author: Kris Armstrong

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
