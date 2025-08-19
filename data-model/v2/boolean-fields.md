# Boolean Fields - System Prompt Agent Schema

## Field Reference Table

| Field Name | Required | Category | Description |
|------------|----------|----------|-------------|
| audio | ✓ |  | Indicates if audio input is required |
| autonomous |  |  | Marks if the agent operates autonomously without supervision |
| better_as_tool |  |  | Marks if this is better suited as a tool rather than a standalone agent |
| character |  | Type | Indicates whether the agent assumes a specific character/persona |
| conversational |  |  | Indicates if the agent supports multi-turn conversations |
| data_utility |  | Category | Marks relevance to data processing/utility use cases |
| deep_research |  |  | Indicates if the agent is designed for deep research tasks |
| external_tooling | ✓ |  | Marks if external tools are mandatory for function |
| file_input | ✓ |  | Indicates if file input support is required |
| image_generation |  | Workflow | Marks if image generation is part of the workflow |
| instructional |  |  | Indicates if designed for teaching or step-by-step guidance |
| is_agent |  |  | Marks if this is a true agent (tool-using, stateful) |
| rag | ✓ |  | Marks if retrieval-augmented generation is required |
| roleplay |  | Behavior | Indicates roleplay functionality/behavior |
| single_turn |  | Workflow | Marks if designed for single-turn interactions |
| spech_to_speech |  |  | Indicates if speech-to-speech interaction is supported |
| structured_output |  | Workflow | Marks if structured output is produced |
| tts | ✓ |  | Indicates if text-to-speech output is required |
| update_iteration |  |  | Marks if an update or iteration cycle occurred |
| video_input | ✓ |  | Marks if video input is required |
| vision | ✓ |  | Indicates if vision input is required |
| voice_first |  |  | Marks if designed primarily for voice-first use |
| writing_assistant |  |  | Indicates if designed as a writing assistant |

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "System Prompt Agent - Boolean Fields",
  "type": "object",
  "description": "Boolean field definitions for system prompt agent schema",
  "properties": {
    "audio": {
      "type": "boolean",
      "description": "Indicates if audio input is required.",
      "default": false
    },
    "autonomous": {
      "type": "boolean",
      "description": "Marks if the agent operates autonomously without supervision.",
      "default": false
    },
    "better_as_tool": {
      "type": "boolean",
      "description": "Marks if this is better suited as a tool rather than a standalone agent.",
      "default": false
    },
    "character": {
      "type": "boolean",
      "description": "Indicates whether the agent assumes a specific character/persona.",
      "default": false
    },
    "conversational": {
      "type": "boolean",
      "description": "Indicates if the agent supports multi-turn conversations.",
      "default": false
    },
    "data_utility": {
      "type": "boolean",
      "description": "Marks relevance to data processing/utility use cases.",
      "default": false
    },
    "deep_research": {
      "type": "boolean",
      "description": "Indicates if the agent is designed for deep research tasks.",
      "default": false
    },
    "external_tooling": {
      "type": "boolean",
      "description": "Marks if external tools are mandatory for function.",
      "default": false
    },
    "file_input": {
      "type": "boolean",
      "description": "Indicates if file input support is required.",
      "default": false
    },
    "image_generation": {
      "type": "boolean",
      "description": "Marks if image generation is part of the workflow.",
      "default": false
    },
    "instructional": {
      "type": "boolean",
      "description": "Indicates if designed for teaching or step-by-step guidance.",
      "default": false
    },
    "is_agent": {
      "type": "boolean",
      "description": "Marks if this is a true agent (tool-using, stateful).",
      "default": false
    },
    "rag": {
      "type": "boolean",
      "description": "Marks if retrieval-augmented generation is required.",
      "default": false
    },
    "roleplay": {
      "type": "boolean",
      "description": "Indicates roleplay functionality/behavior.",
      "default": false
    },
    "single_turn": {
      "type": "boolean",
      "description": "Marks if designed for single-turn interactions.",
      "default": false
    },
    "spech_to_speech": {
      "type": "boolean",
      "description": "Indicates if speech-to-speech interaction is supported.",
      "default": false
    },
    "structured_output": {
      "type": "boolean",
      "description": "Marks if structured output is produced.",
      "default": false
    },
    "tts": {
      "type": "boolean",
      "description": "Indicates if text-to-speech output is required.",
      "default": false
    },
    "update_iteration": {
      "type": "boolean",
      "description": "Marks if an update or iteration cycle occurred.",
      "default": false
    },
    "video_input": {
      "type": "boolean",
      "description": "Marks if video input is required.",
      "default": false
    },
    "vision": {
      "type": "boolean",
      "description": "Indicates if vision input is required.",
      "default": false
    },
    "voice_first": {
      "type": "boolean",
      "description": "Marks if designed primarily for voice-first use.",
      "default": false
    },
    "writing_assistant": {
      "type": "boolean",
      "description": "Indicates if designed as a writing assistant.",
      "default": false
    }
  },
  "required": [
    "audio",
    "external_tooling",
    "file_input",
    "rag",
    "tts",
    "video_input",
    "vision"
  ],
  "additionalProperties": false
}
```
