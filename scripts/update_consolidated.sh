#!/bin/bash
# Simple script to update the consolidated prompts file
# Can be run periodically via cron or manually

cd "$(dirname "$0")"

echo "Updating consolidated system prompts..."
echo "Started at: $(date)"

python3 consolidate_prompts.py

if [ $? -eq 0 ]; then
    echo "Successfully updated consolidated prompts at: $(date)"
    echo "File size: $(du -h ../consolidated_prompts.json | cut -f1)"
else
    echo "Error occurred during consolidation at: $(date)"
    exit 1
fi
