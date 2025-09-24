#!/bin/bash

# System Prompt Library Growth Metrics Update Script
# Main wrapper script for updating growth metrics

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to scripts directory and run the growth metrics update script
cd "$SCRIPT_DIR/scripts"
python3 update_growth_metrics.py "$@"
