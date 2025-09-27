#!/bin/bash

# Multi-Format Index Update Script
# Generates JSON, CSV, and Markdown index files in the index/ directory

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🔄 Updating multi-format index files..."

cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate"
fi

# Run the multi-format index generator
python3 generate_multi_format_index.py "$@"

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "✅ Multi-format index update completed successfully"
    echo "📁 Index files available in: $REPO_ROOT/index/"
    echo "   - index.json (JSON format)"
    echo "   - index.csv (CSV format)" 
    echo "   - index.md (Markdown format)"
    echo "   - index_metadata.json (Metadata)"
else
    echo "❌ Multi-format index update failed"
fi

exit $exit_code
