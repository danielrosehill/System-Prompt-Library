# My AI System Prompt Library

[![View Index](https://img.shields.io/badge/📋_View-Index-blue?style=for-the-badge)](index.md) [![View JSON](https://img.shields.io/badge/📄_View-JSON_Index-green?style=for-the-badge)](consolidated_prompts.json)

![alt text](promptlib.webp)

This repository contains a **comprehensive, up-to-date library of system prompts** for AI systems and autonomous agents, started on May 27th, 2025.

## Overview

This collection houses **923 system prompts** covering a diverse range of AI applications. The prompts include configurations for autonomous agents, simple chatbots, specialized assistants, and various AI-powered tools. This repository serves as a centralized hub for these prompts, maintained through automated workflows that ensure the latest versions are always available.

The library is periodically updated as new system prompts are recorded and saved from ongoing AI projects and experiments.

## Repository Contents

### Prompt Types
- **Autonomous Agents**: Complex multi-step reasoning and task execution
- **Chatbots**: Conversational AI with specific personalities or expertise
- **Specialized Assistants**: Domain-specific helpers (technical, creative, analytical)
- **Tool Integrations**: Prompts designed for specific AI platforms and services

### Storage Formats
System prompts are organized into two main formats:
- **JSON Format**: Structured data with metadata (`system-prompts/json/` - 923 files)
- **Markdown Format**: Human-readable documentation (`system-prompts/md/` - 851 files)

## Repository Structure

```
├── index.md                     # Main searchable index (markdown table)
├── consolidated_prompts.json    # All prompts in single JSON file
├── system-prompts/             # Individual prompt files
│   ├── json/                   # JSON format prompts
│   └── md/                    # Markdown format prompts
├── scripts/                    # Maintenance scripts
│   ├── consolidate_prompts.py  # JSON consolidation
│   ├── generate_index.py       # Markdown index generation
│   ├── update_all.py          # Master update script
│   └── *.sh                   # Shell wrappers
└── update_library.sh          # Main update script (run from root)
```

## How It Works

* Prompts are entered into a structured database with detailed metadata
* Tagged entries marked for export are automatically processed and added to this repository
* Changes are pushed via automation, ensuring the collection stays current with new developments
* Both individual files and consolidated formats are maintained for different use cases

## JSON Data Dictionary

Each system prompt is stored as a JSON file with the following standardized fields:

### Core Fields
| Field | Type | Description |
|-------|------|-------------|
| `agentname` | String | Display name of the AI agent or assistant |
| `description` | String | Brief description of the agent's purpose and capabilities |
| `systemprompt` | String | The complete system prompt text used to configure the AI |
| `creation_date` | String | ISO timestamp of when the prompt was created |

### Integration & Links
| Field | Type | Description |
|-------|------|-------------|
| `chatgptlink` | String/null | URL to ChatGPT custom GPT implementation (if available) |

### Capability Flags
| Field | Type | Description |
|-------|------|-------------|
| `is-agent` | Boolean | Whether this is a complex autonomous agent (vs simple assistant) |
| `is-single-turn` | String | "true"/"false" - Whether designed for single interactions only |
| `structured-output-generation` | String | "true"/"false" - Can generate structured data formats |
| `image-generation` | String | "true"/"false" - Includes image generation capabilities |
| `data-utility` | String | "true"/"false" - Designed for data processing/analysis tasks |
| `personalised-system-prompt` | String | "true"/"false" - Contains user-specific personalization |

### Advanced Configuration
| Field | Type | Description |
|-------|------|-------------|
| `json-schema` | Object/null | JSON schema definition for structured outputs (if applicable) |
| `json-example` | String/null | Example JSON output format (if applicable) |
| `depersonalised-system-prompt` | String/null | Generic version without personal references |
| `chatgpt-privacy` | String/null | Privacy settings for ChatGPT implementations |

### Notes
- Boolean values are stored as strings ("true"/"false") for consistency
- `null` values indicate the field is not applicable to that particular prompt
- All prompts include the core fields; advanced fields are optional based on functionality

## Accessing Prompts

- **Browse**: Use `index.md` for a searchable table of all prompts
- **Bulk access**: Use `consolidated_prompts.json` for programmatic access
- **Individual files**: Browse `system-prompts/json/` for specific prompts

## Purpose

This collection is intended for:

* Reuse across AI projects and experiments
* Open source distribution and community sharing
* Benchmarking and prompt engineering research
* Reference library for AI system development

## Status

This repository is **autogenerated** and updated periodically. The collection represents an evolving library of proven system prompts from real-world AI applications.

## Authorship

All system prmopt by me (Daniel Rosehill) with some drafting assistance with AI.