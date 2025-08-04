#!/bin/bash
# depersonalise_library.sh - Shell wrapper for depersonalise_prompts.py
# 
# This script runs the depersonalisation process on the System Prompt Library
# to replace personalised references with generic ones.
#
# Usage:
#   ./depersonalise_library.sh [--dry-run]
#
# Options:
#   --dry-run    Show what would be changed without making actual changes

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get the repository root directory (parent of scripts directory)
REPO_DIR="$(dirname "$SCRIPT_DIR")"
# Make the Python script executable if it's not already
chmod +x "$SCRIPT_DIR/depersonalise_prompts.py"

# Run the depersonalisation script with the provided arguments
python3 "$SCRIPT_DIR/depersonalise_prompts.py" --path "$REPO_DIR" "$@"

# If not a dry run and changes were made, suggest running the update script
if [[ "$*" != *"--dry-run"* ]]; then
    echo ""
    echo "If changes were made, you may want to run ./update_library.sh to rebuild the consolidated JSON and index"
fi
