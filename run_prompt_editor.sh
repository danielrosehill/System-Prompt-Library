#!/usr/bin/env bash
set -euo pipefail

# Use uv to manage venv, install deps, and run the prompt editor GUI.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
VENV_DIR="${REPO_ROOT}/.venv"
PYTHON_BIN="${PYTHON:-python3}"

if ! command -v uv >/dev/null 2>&1; then
  echo "[run] Error: 'uv' is not installed or not on PATH." >&2
  echo "[run] Please install uv: https://docs.astral.sh/uv/ and re-run." >&2
  exit 1
fi

echo "[run] Using python: ${PYTHON_BIN}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[run] Creating virtual environment with uv at ${VENV_DIR}"
  uv venv --python "${PYTHON_BIN}" "${VENV_DIR}"
fi

# Activate the environment created by uv
source "${VENV_DIR}/bin/activate"
echo "[run] Virtualenv activated: ${VENV_DIR}"

# Install dependencies using uv
REQ_FILE="${REPO_ROOT}/requirements.txt"
PYPROJECT_FILE="${REPO_ROOT}/pyproject.toml"
if [[ -f "${PYPROJECT_FILE}" ]]; then
  echo "[run] Installing dependencies via 'uv sync' (pyproject.toml)"
  uv sync || echo "[run] uv sync failed/skipped (possibly offline); continuing."
elif [[ -f "${REQ_FILE}" ]]; then
  echo "[run] Installing dependencies from requirements.txt via 'uv pip'"
  uv pip install -r "${REQ_FILE}" || echo "[run] uv pip failed/skipped (possibly offline); continuing."
else
  echo "[run] No dependency file found (pyproject.toml or requirements.txt); skipping install."
fi

echo "[run] Launching GUI..."
exec python "${REPO_ROOT}/scripts/prompt_editor.py" "$@"
