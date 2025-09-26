#!/bin/bash

# System Prompt Library Growth Metrics Update Script
# Updates growth history, sparkline, and generates growth chart

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to scripts directory
cd "$SCRIPT_DIR"

# Run the Python script with all passed arguments
python3 update_growth_metrics.py "$@"
