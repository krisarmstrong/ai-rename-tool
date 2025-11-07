#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

PYTHON_CANDIDATES=(
  "${PYTHON_BIN:-}"
  "python3.14"
  "python3"
)

for candidate in "${PYTHON_CANDIDATES[@]}"; do
  if [ -z "$candidate" ]; then
    continue
  fi
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON_BIN="$candidate"
    break
  fi
done

if [ -z "${PYTHON_BIN:-}" ]; then
  echo "bootstrap-venv: unable to locate python3.14; set PYTHON_BIN to the desired interpreter." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

# shellcheck source=/dev/null
source .venv/bin/activate

python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt
fi

if [ -f pyproject.toml ]; then
  python -m pip install -e .
fi

if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
fi

echo "bootstrap-venv: virtual environment ready at ${ROOT}/.venv using $(python --version)"
