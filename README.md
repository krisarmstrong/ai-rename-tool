# AI Rename Tool

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-green) ![Tests](https://img.shields.io/badge/Tests-pytest-passing) ![pip](https://img.shields.io/badge/pip-package-3776AB?logo=pypi&logoColor=white) ![Status](https://img.shields.io/badge/Status-Active-success)


Fast, safe file renamer powered by deterministic suggestions, with a clean plan → apply → undo workflow.
Designed for **functions-first** architecture, **PEP 8/257** compliance, and **Git tag** versioning.
Requires **Python 3.14+**.

## Features
- **Dry-run plan** (JSON/CSV) with conflict resolution (`_1`, `_2`, …)
- **Apply** and **Undo** using the saved JSON plan
- **Local heuristic provider** (no network). Pluggable AI provider ready.
- **Docs** (MkDocs Material), **CI** (GitHub Actions), **Security** (Bandit, CodeQL), **SBOM** (CycloneDX)

## Install
Use the helper script to create a local virtual environment with Python 3.14:

```bash
bash scripts/bootstrap-venv.sh
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## Usage
```bash
ai-rename-tool --help
ai-rename-tool . --categorise --json rename_plan.json --csv rename_plan.csv
ai-rename-tool . --apply
ai-rename-tool --undo rename_plan.json
```

## Versioning
- Semantic Versioning via **Git tags**: `vMAJOR.MINOR.PATCH`
- `setuptools-scm` uses tags as the source of truth

## Development
```bash
pytest -q --cov=ai_rename_tool --cov-report=term-missing
mkdocs serve
```
