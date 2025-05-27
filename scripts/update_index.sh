#!/bin/bash

# Update Index Script
# Simple wrapper for generate_index.py to update the markdown index table

echo "🔄 Updating System Prompt Library Index..."

# Run the Python script
python3 generate_index.py "$@"

# Check if successful
if [ $? -eq 0 ]; then
    echo "✅ Index update completed successfully!"
else
    echo "❌ Index update failed!"
    exit 1
fi
