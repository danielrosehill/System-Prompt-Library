#!/bin/bash

# Test script for validating the automated library update process
# This simulates what the GitHub Actions workflow will do

set -e

echo "🧪 Testing System Prompt Library Automation"
echo "=========================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."
if [ ! -f "update_library_unified.py" ]; then
    echo "❌ update_library_unified.py not found"
    exit 1
fi

if [ ! -d "system-prompts/json" ]; then
    echo "❌ system-prompts/json directory not found"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Show current status
echo "📊 Current repository status:"
echo "JSON files: $(find system-prompts/json -name '*.json' 2>/dev/null | wc -l)"
echo "Consolidated file exists: $([ -f consolidated_prompts.json ] && echo 'Yes' || echo 'No')"
echo "Index file exists: $([ -f index.md ] && echo 'Yes' || echo 'No')"
echo "README file exists: $([ -f README.md ] && echo 'Yes' || echo 'No')"
echo ""

# Test the update script
echo "🚀 Testing update script..."
echo "Running: python3 update_library_unified.py"
echo ""

python3 update_library_unified.py

echo ""
echo "📈 Post-update status:"

# Check if files were created/updated
if [ -f consolidated_prompts.json ]; then
    echo "✅ consolidated_prompts.json exists"
    PROMPT_COUNT=$(python3 -c "import json; data=json.load(open('consolidated_prompts.json')); print(len(data))" 2>/dev/null || echo "unknown")
    echo "   Prompt count: $PROMPT_COUNT"
else
    echo "❌ consolidated_prompts.json missing"
fi

if [ -f index.md ]; then
    echo "✅ index.md exists"
    INDEX_SIZE=$(wc -l < index.md)
    echo "   Size: $INDEX_SIZE lines"
else
    echo "❌ index.md missing"
fi

if [ -f README.md ]; then
    echo "✅ README.md exists"
    if grep -q "BEGIN_INDEX_CONTENT" README.md; then
        echo "   Contains index markers: Yes"
    else
        echo "   Contains index markers: No"
    fi
else
    echo "❌ README.md missing"
fi

# Check for metadata files
echo ""
echo "📄 Metadata files:"
for file in consolidated_prompts.metadata.json index_metadata.json growth_history.json; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "⚠️  $file missing"
    fi
done

echo ""
echo "🎯 Test completed!"
echo ""
echo "To test the GitHub Actions workflow:"
echo "1. Commit and push these workflow files"
echo "2. Go to GitHub → Actions tab"
echo "3. Run 'Manual Update System Prompt Library' workflow"
echo "4. The automatic workflow will run daily at 3:00 AM UTC"
