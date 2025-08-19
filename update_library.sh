#!/bin/bash

# System Prompt Library - Main Update Script
# This script runs the unified update process for the entire library
# Updated on 2025-08-19 to use the new unified script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 System Prompt Library - Unified Update Process"
echo "📁 Working from: $SCRIPT_DIR"
echo ""

# Run the unified update script with all arguments passed through
python3 "$SCRIPT_DIR/update_library_unified.py" "$@"

exit $?
