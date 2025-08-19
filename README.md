# System Prompt Library

[![Prompts Site](https://img.shields.io/badge/🌐_Visit-prompts.danielrosehill.com-blue?style=for-the-badge)](https://prompts.userwebsite.com) [![Agent Configs](https://img.shields.io/badge/🤖_Visit-agents.danielrosehill.com-green?style=for-the-badge)](https://agents.danielrosehill.com)

[![View Index](https://img.shields.io/badge/📋_View-Index-blue?style=for-the-badge)](index.md) [![View JSON](https://img.shields.io/badge/📄_View-JSON_Index-green?style=for-the-badge)](consolidated_prompts.json)

![alt text](promptlib.webp)

This repository contains a **comprehensive, up-to-date library of system prompts** for AI systems and autonomous agents.

These configurations can be deployed as simple chatbot configurations, agent systems with MCP (Model Context Protocol), and workflows. 

## Overview

The prompts include configurations for autonomous agents, simple chatbots, specialized assistants, and various AI-powered tools. This repository serves as a centralized hub for these prompts, maintained through automated workflows that ensure the latest versions are always available.

The library is periodically updated as new system prompts are recorded and saved from ongoing AI projects and experiments.

## Point In Time Exports

I periodically export lightly cleaned versions of the consolidated system prompt file.

These are listed in `exports.md`. The latest is:

[![Hugging Face Dataset - 2025-03-08](https://img.shields.io/badge/🤗%20Hugging%20Face-2025--03--08-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/datasets/danielrosehill/System-Prompt-Library-030825)

## Formats

These prompts are mostly now populated from an N8N workflow.

**Markdown** versions are funneled to `system-prompts/md` and **JSON** versions to `system-prompts/json`.

## Data Structure

### JSON Data Model (V2 - August 2025)

This updated data structure includes booleans for:

- Classification (characters, workflows)  
- Architecture reqs (RAG, tooling, APIs) 
- Use-cases and capabilities 
- Data retention policies and compliance 
- Notes about LLM selection, MCP, API

```
[
    {
      "agent_name": "Sample Text",
      "Description": "Sample Text",
      "One Line Summary": "Sample Text",
      "Creation Date": "2025-08-19T12:37:15.024Z",
      "ChatGPT Access URL": "https://nocodb.com",
      "Utility Estimate": 1,
      "Test Entry": true,
      "JSON Schema (Full)": "{}",
      "JSON Schema (Example Value)": "{}",
      "Better As Tool": true,
      "Is Agent": true,
      "Single Turn (Workflow Type)": true,
      "External Tooling (Required)": true,
      "Structured Output (Workflow Type)": true,
      "Image Generation (Workflow Type)": true,
      "Character (Type)": true,
      "Roleplay (Behavior)": true,
      "Voice First": true,
      "Writing Assistant": true,
      "Data Utility (Category)": true,
      "N8N Link": "https://nocodb.com",
      "RAG (Required)": true,
      "Vision (Req)": true,
      "Spech-To-Speech": true,
      "Video Input (Required)": true,
      "Audio (Required)": true,
      "TTS (Required)": true,
      "File Input (Req)": true,
      "Conversational": true,
      "Instructional": true,
      "Autonomous": true,
      "MCPs Used": "Sample Long text",
      "API Notes": "Sample Long text",
      "MCP Notes": "Sample Long text",
      "Local LLM Friendly?": true,
      "Local LLM Notes": "Sample Long text",
      "LLM Selection Notes": "Sample Long text",
      "Deep Research": true,
      "Update/Iteration": true,
      "Iteration Notes": "Sample Long text",
      "Use Case Outline": "Sample Long text",
      "PII Notes": "Sample Long text",
      "Cost Estimates": "Sample Long text",
      "Localtisation Notes": "Sample Long text",
      "Guardrails Notes": "Sample Long text"
    }
  ]
 ``` 

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

## JSON Data Dictionary

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

## Authorship

the user









## System Prompt Index

<!-- BEGIN_INDEX_CONTENT -->
# System Prompt Index

📈 ▇█▁

**Total Prompts:** 2 | **Last Updated:** 2025-08-19

*Generated on 2025-08-19 from consolidated system prompts*

---

## Sample Text

No description available

**Features:**
  - ☐ Agent-based interaction
  - ☐ Single-turn conversation
  - ☐ Structured output generation
  - ☐ Image generation
  - ☐ Data utility functions

**Links:**
  - 📄 [JSON File](system-prompts/json/Sample_Text_270525.json)

---

## Sample Text

Sample Text

**Features:**
  - ☐ Agent-based interaction
  - ☐ Single-turn conversation
  - ☐ Structured output generation
  - ☐ Image generation
  - ☐ Data utility functions

**Links:**
  - 📄 [JSON File](system-prompts/json/Sample_Text_270525.json)

---


<!-- END_INDEX_CONTENT -->
