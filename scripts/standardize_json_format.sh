#!/bin/bash

# System Prompt Library JSON Format Standardization Script
# Wrapper script for standardize_json_format.py

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to scripts directory
cd "$SCRIPT_DIR"

# Run the Python script with all passed arguments
python3 standardize_json_format.py "$@"
