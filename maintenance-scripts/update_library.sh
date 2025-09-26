#!/bin/bash

# System Prompt Library Master Update Script
# Shell wrapper for the Python master update script
# Updated 2025-09-24 to use new master script with growth metrics

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/update_library.py"

# Check if virtual environment exists and activate it (now in repo root)
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
if [[ -d "$REPO_ROOT/.venv" ]]; then
    echo "🔄 Activating virtual environment..."
    source "$REPO_ROOT/.venv/bin/activate"
fi

# Check if the Python script exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "❌ Error: update_library.py not found at $PYTHON_SCRIPT"
    exit 1
fi

echo "🚀 System Prompt Library - Master Update Process"
echo "📁 Working from: $SCRIPT_DIR"
echo ""

# Run the Python script with all passed arguments
python3 "$PYTHON_SCRIPT" "$@"

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment if it was activated
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi

exit $EXIT_CODE
