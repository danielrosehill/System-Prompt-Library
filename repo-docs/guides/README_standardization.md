# JSON Format Standardization Script

This script standardizes all JSON files in the System Prompt Library to match the latest format specification (240925_format.json).

## Features

- **Field Mapping**: Automatically maps old field names to new field names
- **Boolean Normalization**: Converts string boolean values ("true"/"false") to actual booleans
- **Date Normalization**: Standardizes date formats to YYYY-MM-DD
- **Complete Schema**: Ensures all files have all required fields with proper null values
- **Backup Support**: Creates backups before making changes
- **Dry Run Mode**: Preview changes without modifying files

## Usage

### From Repository Root
```bash
# Dry run to see what would change
./standardize_json_format.sh --dry-run

# Run with backup
./standardize_json_format.sh --backup

# Run without backup (not recommended)
./standardize_json_format.sh
```

### From Scripts Directory
```bash
cd scripts/

# Dry run to see what would change
python3 standardize_json_format.py --dry-run

# Run with backup
python3 standardize_json_format.py --backup

# Run without backup
python3 standardize_json_format.py
```

## Field Mappings

The script maps old format fields to new format fields:

| Old Field | New Field |
|-----------|-----------|
| `agentname` | `agent_name` |
| `description` | `Description` |
| `systemprompt` | `System Prompt` |
| `chatgptlink` | `ChatGPT Access URL` |
| `creation_date` | `Creation Date` |
| `is-agent` | `Is Agent` |
| `is-single-turn` | `Single Turn (Workflow Type)` |
| `structured-output-generation` | `Structured Output (Workflow Type)` |
| `image-generation` | `Image Generation (Workflow Type)` |
| `data-utility` | `Data Utility (Category)` |
| `json-schema` | `JSON Schema (Full)` |
| `json-example` | `JSON Schema (Example Value)` |

## New Fields Added

The script adds these new fields with null/false default values:

- `One Line Summary`
- `Utility Estimate` (defaults to 0)
- `Test Entry` (defaults to false)
- `Better As Tool`
- `External Tooling (Required)`
- `Character (Type)`
- `Roleplay (Behavior)`
- `Voice First`
- `Writing Assistant`
- `N8N Link`
- `RAG (Required)`
- `Vision (Req)`
- `Spech-To-Speech`
- `Video Input (Required)`
- `Audio (Required)`
- `TTS (Required)`
- `File Input (Req)`
- `Conversational`
- `Instructional`
- `Autonomous`
- `MCPs Used`
- `API Notes`
- `MCP Notes`
- `Local LLM Friendly?`
- `Local LLM Notes`
- `LLM Selection Notes`
- `Deep Research`
- `Update/Iteration`
- `Iteration Notes`
- `Use Case Outline`
- `PII Notes`
- `Cost Estimates`
- `Localtisation Notes`
- `Guardrails Notes`
- `Gemini URL`

## Command Line Options

- `--dry-run`: Show what would be changed without making changes
- `--backup`: Create backup directory before making changes
- `--json-dir PATH`: Specify custom JSON directory (default: ../system-prompts/json)

## Backup Location

When using `--backup`, backups are created in:
`system-prompts/json/backup_YYYYMMDD_HHMMSS/`

## Results

The script processes all JSON files and provides a summary:
- Total files processed
- Files with changes made
- Files with errors (if any)

All 956 JSON files in the library have been successfully standardized to the new format.

## Prompt Editor Compatibility

The System Prompt Library GUI editor (`scripts/prompt_editor.py`) has been updated to support the new standardized format:

- **Field Mapping**: Updated to use new field names (`agent_name`, `Description`, `System Prompt`, etc.)
- **Boolean Handling**: Now saves boolean values as actual booleans instead of strings
- **Full Compatibility**: Works seamlessly with all standardized JSON files

To launch the editor:
```bash
# From repository root
./run_prompt_editor.sh

# Or directly
cd scripts && python3 prompt_editor.py
```

The editor provides a modern Qt-based interface for editing all system prompt metadata and content.
