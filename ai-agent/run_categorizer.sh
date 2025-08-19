#!/bin/bash

# System Prompt Library Categorizer Runner
# Wrapper script for easy execution

set -e

# Change to repository root if needed
if [[ $(basename "$PWD") == "ai-agent" ]]; then
    cd ..
fi

# Check if we're in the right directory
if [[ ! -d "system-prompts/json" ]]; then
    echo "Error: Not in System Prompt Library root directory"
    echo "Please run from the repository root or ai-agent/ subdirectory"
    exit 1
fi

# Check if Ollama is running (for local LLM)
if command -v ollama &> /dev/null; then
    if ! pgrep -f "ollama" > /dev/null; then
        echo "Starting Ollama service..."
        ollama serve &
        sleep 3
    fi
    
    # Check if llama3.2 model is available
    if ! ollama list | grep -q "llama3.2"; then
        echo "Downloading llama3.2 model (this may take a while)..."
        ollama pull llama3.2
    fi
else
    echo "Warning: Ollama not found. Install with: curl -fsSL https://ollama.ai/install.sh | sh"
fi

# Create virtual environment if it doesn't exist
if [[ ! -d "ai-agent/venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv ai-agent/venv
fi

# Activate virtual environment
source ai-agent/venv/bin/activate

# Install dependencies
pip install -q requests

# Run the categorizer
echo "Starting System Prompt Categorizer..."
python3 ai-agent/categorizer.py "$@"

echo "Categorization complete!"
