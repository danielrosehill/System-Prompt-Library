#!/bin/bash

# System Prompt Library - Main Update Script
# This script provides an easy way to run the update scripts from the repository root

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_PATH="$SCRIPT_DIR/scripts"

# Check if scripts directory exists
if [ ! -d "$SCRIPTS_PATH" ]; then
    echo "❌ Error: scripts directory not found at $SCRIPTS_PATH"
    exit 1
fi

# Change to scripts directory and run update_all.py
cd "$SCRIPTS_PATH"

echo "🚀 System Prompt Library - Update All Indices"
echo "📁 Working from: $(pwd)"
echo ""

# Run the update script with all arguments passed through
python3 update_all.py "$@"

# Return to original directory
cd "$SCRIPT_DIR"

exit $?
