#!/bin/bash

# System Prompt Library JSON Format Standardization Script
# Main wrapper script for standardizing JSON format

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to scripts directory and run the standardization script
cd "$SCRIPT_DIR/scripts"
python3 standardize_json_format.py "$@"
