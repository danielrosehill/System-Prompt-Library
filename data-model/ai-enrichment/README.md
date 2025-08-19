# AI Enrichment Data Model

This directory contains the schema and examples for AI-generated enrichment data that supplements the original system prompt library entries.

## Purpose

The AI enrichment model provides a structured way to store AI-generated analysis, categorization, and enhancement data **separately** from the original schema. This approach:

- **Preserves original data integrity** - Never modifies the existing v2 schema
- **Clearly distinguishes AI-generated content** - All enriched fields have `ai_enriched_` prefix
- **Enables versioning** - Enrichment data includes metadata about the AI model and process used
- **Supports confidence scoring** - Each enrichment includes confidence metrics
- **Allows iterative improvement** - Can re-run enrichment with better models/prompts

## Schema Structure

### Core Components

1. **`ai_enriched_metadata`** - Information about the enrichment process
2. **`ai_enriched_categorization`** - Category assignment with confidence and reasoning
3. **`ai_enriched_tags`** - Tag assignment with confidence scores
4. **`ai_enriched_description`** - Enhanced/generated descriptions
5. **`ai_enriched_analysis`** - Detailed capability and complexity analysis
6. **`ai_enriched_quality_metrics`** - Quality assessment scores

### Usage Pattern

Enriched data is stored alongside the original JSON files:

```
system-prompts/
├── json/
│   └── MyAgent_270525.json              # Original data (v2 schema)
└── enriched/
    └── MyAgent_270525.enriched.json     # AI enrichment data
```

## Benefits

- **Non-destructive** - Original data remains untouched
- **Traceable** - Full audit trail of AI enrichment process
- **Flexible** - Can add new enrichment types without schema changes
- **Comparable** - Confidence scores allow quality comparison
- **Updatable** - Can re-enrich with improved AI models

## Implementation

The AI agent uses this model to:
1. Analyze original system prompt data
2. Generate enrichment using LLM analysis
3. Store results in separate `.enriched.json` files
4. Provide clear attribution and confidence metrics
5. Enable easy rollback or re-processing

This approach ensures the library maintains data integrity while benefiting from AI-powered enhancements.
