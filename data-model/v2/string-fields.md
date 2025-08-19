# String Fields - System Prompt Agent Schema

## Field Reference Table

| Field Name | Required | Format | Description |
|------------|----------|--------|-------------|
| agentname |  |  | The display name of the agent/assistant |
| api_notes |  |  | Free-text notes on API usage, dependencies, or quirks |
| chatgpt_access_url |  | URI | Direct link to the deployed ChatGPT agent |
| cost_estimates |  |  | Notes or figures on estimated operating costs |
| creation_date |  | Date | Date the agent was created |
| description |  |  | Text description of the agent's purpose and behavior |
| guardrails_notes |  |  | Free-text notes describing safety rules or refusal logic |
| iteration_notes |  |  | Free-text notes about iteration history |
| llm_selection_notes |  |  | Notes on which LLMs are most suitable |
| local_llm_friendly |  |  | Indicates suitability for running on local LLMs |
| local_llm_notes |  |  | Notes about performance or quirks on local LLMs |
| localtisation_notes |  |  | Notes about localization or language support |
| mcp_notes |  |  | Notes related to Model Context Protocol integrations |
| mcps_used |  |  | List of Model Context Protocol components/tools used |
| n8n_link |  | URI | Link to associated n8n automation |
| pii_notes |  |  | Notes on handling personally identifiable information |
| use_case_outline |  |  | Free-text outline of supported use cases |
| utility_estimate |  |  | Numerical or qualitative estimate of usefulness |

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "System Prompt Agent - String Fields",
  "type": "object",
  "description": "String field definitions for system prompt agent schema",
  "properties": {
    "agentname": {
      "type": "string",
      "description": "The display name of the agent/assistant."
    },
    "api_notes": {
      "type": "string",
      "description": "Free-text notes on API usage, dependencies, or quirks."
    },
    "chatgpt_access_url": {
      "type": "string",
      "description": "Direct link to the deployed ChatGPT agent.",
      "format": "uri"
    },
    "cost_estimates": {
      "type": "string",
      "description": "Notes or figures on estimated operating costs."
    },
    "creation_date": {
      "type": "string",
      "description": "Date the agent was created.",
      "format": "date"
    },
    "description": {
      "type": "string",
      "description": "Text description of the agent's purpose and behavior."
    },
    "guardrails_notes": {
      "type": "string",
      "description": "Free-text notes describing safety rules or refusal logic."
    },
    "iteration_notes": {
      "type": "string",
      "description": "Free-text notes about iteration history."
    },
    "llm_selection_notes": {
      "type": "string",
      "description": "Notes on which LLMs are most suitable."
    },
    "local_llm_friendly": {
      "type": "string",
      "description": "Indicates suitability for running on local LLMs."
    },
    "local_llm_notes": {
      "type": "string",
      "description": "Notes about performance or quirks on local LLMs."
    },
    "localtisation_notes": {
      "type": "string",
      "description": "Notes about localization or language support."
    },
    "mcp_notes": {
      "type": "string",
      "description": "Notes related to Model Context Protocol integrations."
    },
    "mcps_used": {
      "type": "string",
      "description": "List of Model Context Protocol components/tools used."
    },
    "n8n_link": {
      "type": "string",
      "description": "Link to associated n8n automation.",
      "format": "uri"
    },
    "pii_notes": {
      "type": "string",
      "description": "Notes on handling personally identifiable information."
    },
    "use_case_outline": {
      "type": "string",
      "description": "Free-text outline of supported use cases."
    },
    "utility_estimate": {
      "type": "string",
      "description": "Numerical or qualitative estimate of usefulness."
    }
  },
  "required": [],
  "additionalProperties": false
}
```
