# AI Rename Tool

Fast, safe file renamer powered by deterministic suggestions, with a clean plan → apply → undo workflow.
Designed for **functions-first** architecture, **PEP 8/257** compliance, and **Git tag** versioning.

## Features
- **Dry-run plan** (JSON/CSV) with conflict resolution (`_1`, `_2`, …)
- **Apply** and **Undo** using the saved JSON plan
- **Local heuristic provider** (no network). Pluggable AI provider ready.
- **Docs** (MkDocs Material), **CI** (GitHub Actions), **Security** (Bandit, CodeQL), **SBOM** (CycloneDX)

## Install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
pre-commit install
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
