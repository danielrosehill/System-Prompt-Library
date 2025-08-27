# System Prompt Library AI Categorizer

Automated AI agent for categorizing and enhancing system prompt library entries while preserving the existing schema structure.

## Features

- **Schema Preservation**: Only populates existing fields, never modifies the JSON schema
- **Local LLM Support**: Uses Ollama with Llama 3.2 for cost-effective processing
- **Automatic Backups**: Creates timestamped backups before making changes
- **Batch Processing**: Handles large numbers of files efficiently
- **Description Generation**: Fills in missing descriptions using AI analysis

## Quick Start

```bash
# Run from repository root
./ai-agent/run_categorizer.sh

# Or with specific options
./ai-agent/run_categorizer.sh --dry-run
./ai-agent/run_categorizer.sh --file system-prompts/json/specific-file.json
```

## What It Does

The categorizer analyzes each JSON file and:

1. **Generates descriptions** for entries missing them or with very short descriptions
2. **Preserves all existing data** - never overwrites existing content
3. **Creates backups** before making any changes
4. **Uses local AI** (Ollama/Llama 3.2) to keep costs minimal

## Current Schema Fields

The agent works with your existing schema fields:
- `agentname` - Agent display name
- `description` - Purpose and functionality description  
- `systemprompt` - The actual system prompt text
- `chatgptlink` - Link to ChatGPT deployment
- Plus all boolean capability flags

**Note**: Category and tag taxonomies are prepared for future schema updates but not currently applied to preserve your existing structure.

## Configuration

### LLM Options
- **Primary**: Local Ollama with Llama 3.2 (free, private)
- **Fallback**: GPT-4o-mini (requires API key setup)

### Processing Settings
- Batch size: 10 files at a time
- Timeout: 30 seconds per LLM call
- Max retries: 3 attempts
- Automatic backups enabled

## Directory Structure

```
ai-agent/
├── config/
│   └── agent_config.json     # Main configuration
├── taxonomies/
│   ├── categories.json       # Category definitions (for future use)
│   └── tags.json            # Tag definitions (for future use)
├── backups/                 # Automatic backups
├── categorizer.py           # Main Python script
├── run_categorizer.sh       # Wrapper script
└── README.md               # This file
```

## Usage Examples

```bash
# Process all files with automatic backups
./ai-agent/run_categorizer.sh

# Dry run to see what would be changed
./ai-agent/run_categorizer.sh --dry-run

# Process single file
./ai-agent/run_categorizer.sh --file system-prompts/json/MyAgent.json

# Process specific directory
./ai-agent/run_categorizer.sh --directory custom-prompts/
```

## Prerequisites

- Python 3.7+
- Ollama installed and running
- Llama 3.2 model downloaded (`ollama pull llama3.2`)

The wrapper script will handle most setup automatically.

## Safety Features

- **Automatic backups** with timestamps
- **Dry run mode** to preview changes
- **Schema validation** to prevent corruption
- **Error handling** with detailed logging
- **Preserves existing data** - only fills gaps

## Future Enhancements

When you're ready to extend the schema:
- Category field population using prepared taxonomy
- Tag assignment with semantic analysis
- Advanced content analysis and recommendations

## Troubleshooting

**Ollama not found**: Install with `curl -fsSL https://ollama.ai/install.sh | sh`

**Model not available**: Run `ollama pull llama3.2`

**Permission errors**: Ensure script is executable: `chmod +x ai-agent/run_categorizer.sh`

**JSON errors**: Check backup files in `ai-agent/backups/` to restore if needed
