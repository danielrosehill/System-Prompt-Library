#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to create/activate a virtualenv and launch the prompt editor GUI.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
VENV_DIR="${REPO_ROOT}/.venv"
PYTHON_BIN="${PYTHON:-python3}"

echo "[run] Using python: ${PYTHON_BIN}"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "[run] Creating virtual environment at ${VENV_DIR}"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
echo "[run] Virtualenv activated: ${VENV_DIR}"

# If a requirements file exists, install it (best-effort). Skip if offline.
REQ_FILE="${REPO_ROOT}/requirements.txt"
if [[ -f "${REQ_FILE}" ]]; then
  echo "[run] Installing dependencies from requirements.txt (if network available)"
  pip install -r "${REQ_FILE}" || echo "[run] pip install skipped/failed (likely offline). Continuing."
fi

echo "[run] Launching GUI..."
exec python "${REPO_ROOT}/scripts/prompt_editor.py" "$@"

