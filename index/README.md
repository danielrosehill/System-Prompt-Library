# System Prompt Library Index

This directory contains the System Prompt Library index in multiple formats, automatically generated from the consolidated prompt data.

## Available Formats

### 📄 [index.md](index.md)
**Human-readable Markdown format**
- Organized with H2 headers for each system prompt
- Feature capabilities shown with checkbox indicators (☑️/☐)
- Direct links to JSON files and ChatGPT custom GPTs
- Growth sparkline chart and statistics
- Perfect for browsing and reading

### 📊 [index.json](index.json)
**Comprehensive JSON format for API consumers**
- Complete metadata including generation timestamps
- Full prompt data embedded for each entry
- Structured feature flags and capabilities
- Growth tracking data included
- Ideal for programmatic access and integrations

### 📈 [index.csv](index.csv)
**Tabular CSV format for data analysis**
- Spreadsheet-compatible format
- Boolean columns for feature capabilities
- Agent names, descriptions, and links
- Perfect for filtering, sorting, and analysis in Excel/Google Sheets

### ⚙️ [index_metadata.json](index_metadata.json)
**Index generation metadata**
- Generation timestamps and statistics
- Growth data and historical counts
- Format information and file paths
- Processing metrics

## Automatic Generation

All index formats are automatically regenerated when the library is updated using:

```bash
# Generate all formats
./maintenance-scripts/indexing/update_multi_format_index.sh

# Or generate specific formats
./maintenance-scripts/indexing/update_multi_format_index.sh --json-only
./maintenance-scripts/indexing/update_multi_format_index.sh --csv-only
./maintenance-scripts/indexing/update_multi_format_index.sh --markdown-only
```

## Data Consistency

All formats contain the same core data:
- **Agent Name**: The name/title of the system prompt
- **Description**: Detailed description of the prompt's purpose
- **Feature Capabilities**: Boolean flags for various capabilities
- **Links**: References to JSON files and ChatGPT custom GPTs
- **Metadata**: Original filenames and processing information

The formats differ only in their presentation and level of detail, ensuring consistency across all access methods.

## Usage Examples

### For Browsing
Use `index.md` for human-readable browsing with rich formatting.

### For API Integration
Use `index.json` for programmatic access with full metadata.

### For Data Analysis
Use `index.csv` for importing into spreadsheet applications or data analysis tools.

### For Automation
Use `index_metadata.json` to check generation status and statistics.
