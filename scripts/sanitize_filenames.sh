#!/bin/bash

# Shell wrapper for filename sanitization script
# Usage: ./sanitize_filenames.sh [--dry-run] [--verbose]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"

python3 "$SCRIPT_DIR/sanitize_filenames.py" --repo-root "$REPO_ROOT" "$@"
