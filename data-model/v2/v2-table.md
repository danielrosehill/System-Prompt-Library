# Agent Library Field Reference (v2)

| Field Name | Type | Required | Category | Description |
|------------|------|----------|----------|-------------|
| Agent Name | string |  |  | The display name of the agent/assistant. |
| API Notes | string |  |  | Free-text notes on API usage, dependencies, or quirks. |
| Audio | boolean | ✓ |  | Indicates if audio input is required. |
| Autonomous | boolean |  |  | Marks if the agent operates autonomously without supervision. |
| Better As Tool | boolean |  |  | Marks if this is better suited as a tool rather than a standalone agent. |
| Character | boolean |  | Type | Indicates whether the agent assumes a specific character/persona. |
| ChatGPT Access URL | string |  |  | Direct link to the deployed ChatGPT agent. |
| Conversational | boolean |  |  | Indicates if the agent supports multi-turn conversations. |
| Cost Estimates | string |  |  | Notes or figures on estimated operating costs. |
| Creation Date | string |  |  | Date the agent was created. |
| Data Utility | boolean |  | Category | Marks relevance to data processing/utility use cases. |
| Deep Research | boolean |  |  | Indicates if the agent is designed for deep research tasks. |
| Description | string |  |  | Text description of the agent’s purpose and behavior. |
| External Tooling | boolean | ✓ |  | Marks if external tools are mandatory for function. |
| File Input | boolean | ✓ |  | Indicates if file input support is required. |
| Guardrails Notes | string |  |  | Free-text notes describing safety rules or refusal logic. |
| Image Generation | boolean |  | Type | Marks if image generation is part of the workflow. |
| Instructional | boolean |  |  | Indicates if designed for teaching or step-by-step guidance. |
| Is Agent | boolean |  |  | Marks if this is a true agent (tool-using, stateful). |
| Iteration Notes | string |  |  | Free-text notes about iteration history. |
| JSON Schema | object |  |  | Example JSON payload showing expected structured output. |
| JSON Schema | object |  |  | Full JSON schema definition for structured output. |
| LLM Selection Notes | string |  |  | Notes on which LLMs are most suitable. |
| Local LLM Friendly? | string |  |  | Indicates suitability for running on local LLMs. |
| Local LLM Notes | string |  |  | Notes about performance or quirks on local LLMs. |
| Localtisation Notes | string |  |  | Notes about localization or language support. |
| MCP Notes | string |  |  | Notes related to Model Context Protocol integrations. |
| MCPs Used | string |  |  | List of Model Context Protocol components/tools used. |
| N8N Link | string |  |  | Link to associated n8n automation. |
| PII Notes | string |  |  | Notes on handling personally identifiable information. |
| RAG | boolean | ✓ |  | Marks if retrieval-augmented generation is required. |
| Roleplay | boolean |  | Behavior | Indicates roleplay functionality/behavior. |
| Single Turn | boolean |  | Type | Marks if designed for single-turn interactions. |
| Spech-To-Speech | boolean |  |  | Indicates if speech-to-speech interaction is supported. |
| Structured Output | boolean |  | Type | Marks if structured output is produced. |
| TTS | boolean | ✓ |  | Indicates if text-to-speech output is required. |
| Update/Iteration | boolean |  |  | Marks if an update or iteration cycle occurred. |
| Use Case Outline | string |  |  | Free-text outline of supported use cases. |
| Utility Estimate | string |  |  | Numerical or qualitative estimate of usefulness. |
| Video Input | boolean | ✓ |  | Marks if video input is required. |
| Vision | boolean | ✓ |  | Indicates if vision input is required. |
| Voice First | boolean |  |  | Marks if designed primarily for voice-first use. |
| Writing Assistant | boolean |  |  | Indicates if designed as a writing assistant. |

