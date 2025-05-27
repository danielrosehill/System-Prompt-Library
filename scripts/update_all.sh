#!/bin/bash

# Update All Indices Script
# Simple wrapper for update_all.py to update both JSON and markdown indices

echo "🚀 Updating System Prompt Library - All Indices..."

# Run the Python script with all arguments passed through
python3 update_all.py "$@"

# Check if successful
if [ $? -eq 0 ]; then
    echo "🎉 All updates completed successfully!"
else
    echo "⚠️  Some updates failed!"
    exit 1
fi
