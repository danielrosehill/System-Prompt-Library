#!/bin/bash

# System Prompt Library - Main Update Script
# Wrapper that calls the maintenance script in the new location
# Updated for reorganized repository structure

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAINTENANCE_SCRIPT="$REPO_ROOT/maintenance-scripts/update_library.sh"

# Check if the maintenance script exists
if [[ ! -f "$MAINTENANCE_SCRIPT" ]]; then
    echo "❌ Error: Maintenance script not found at $MAINTENANCE_SCRIPT"
    exit 1
fi

echo "🚀 System Prompt Library - Update Process"
echo "📁 Repository root: $REPO_ROOT"
echo "🔧 Calling maintenance script..."
echo ""

# Run the maintenance script with all passed arguments
"$MAINTENANCE_SCRIPT" "$@"

# Pass through the exit code
exit $?
