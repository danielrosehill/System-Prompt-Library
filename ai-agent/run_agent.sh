#!/bin/bash

# True AI Agent Runner
# Launches the autonomous agent with full decision-making capabilities

set -e

# Change to repository root if needed
if [[ $(basename "$PWD") == "ai-agent" ]]; then
    cd ..
fi

# Check if we're in the right directory
if [[ ! -d "system-prompts/json" ]]; then
    echo "Error: Not in System Prompt Library root directory"
    exit 1
fi

# Ensure Ollama is running
if command -v ollama &> /dev/null; then
    if ! pgrep -f "ollama" > /dev/null; then
        echo "Starting Ollama service..."
        ollama serve &
        sleep 3
    fi
    
    # Ensure llama3.2 model is available
    if ! ollama list | grep -q "llama3.2"; then
        echo "Downloading llama3.2 model..."
        ollama pull llama3.2
    fi
else
    echo "Error: Ollama required for autonomous agent. Install with:"
    echo "curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Create virtual environment if needed
if [[ ! -d "ai-agent/venv" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv ai-agent/venv
fi

# Activate virtual environment
source ai-agent/venv/bin/activate

# Install dependencies
pip install -q requests

# Create necessary directories
mkdir -p ai-agent/logs ai-agent/memory ai-agent/backups

echo "🤖 Launching Autonomous AI Agent..."
echo "   Session ID: $(date +%Y%m%d_%H%M%S)"
echo "   Mode: Fully Autonomous"
echo "   LLM: Ollama/Llama3.2"
echo ""

# Run the autonomous agent
python3 ai-agent/agent_core.py "$@"

echo ""
echo "🎯 Agent execution complete. Check logs in ai-agent/logs/ for details."
