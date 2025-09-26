#!/usr/bin/env python3
"""
Generate data model documentation in multiple formats from the v2.md specification.
Converts the field definitions into markdown table and JSON schema formats.
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any

def parse_data_model(content: str) -> List[Dict[str, Any]]:
    """Parse the data model from markdown content."""
    fields = []
    
    # Split content into sections by ### headers
    sections = re.split(r'\n### ', content)
    
    for section in sections[1:]:  # Skip the first split (title)
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        # Parse the header line
        header = lines[0]
        description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
        
        # Extract field name and metadata from header
        field_info = parse_field_header(header)
        if field_info:
            field_info['description'] = description
            fields.append(field_info)
    
    return fields

def parse_field_header(header: str) -> Dict[str, Any]:
    """Parse field header to extract name, type, and flags."""
    # Pattern to match: "Field Name (Type) (Flags) (Boolean/JSON/etc)"
    # Examples: "agentname (Text / String)", "Audio (Required) (Boolean)"
    
    field = {
        'name': '',
        'type': 'string',
        'required': False,
        'category': None,
        'workflow_type': False,
        'behavior_type': False
    }
    
    # Extract field name (everything before first parenthesis)
    name_match = re.match(r'^([^(]+)', header)
    if name_match:
        field['name'] = name_match.group(1).strip()
    
    # Extract all parenthetical content
    parentheticals = re.findall(r'\(([^)]+)\)', header)
    
    for paren in parentheticals:
        paren_lower = paren.lower().strip()
        
        # Check for data types
        if 'boolean' in paren_lower:
            field['type'] = 'boolean'
        elif 'json' in paren_lower:
            field['type'] = 'object'
        elif 'text' in paren_lower or 'string' in paren_lower:
            field['type'] = 'string'
        
        # Check for required flag
        if 'required' in paren_lower or 'req' in paren_lower:
            field['required'] = True
        
        # Check for categories/types
        if 'category' in paren_lower:
            field['category'] = 'category'
        elif 'type' in paren_lower:
            field['category'] = 'type'
        elif 'workflow type' in paren_lower:
            field['workflow_type'] = True
        elif 'behavior' in paren_lower:
            field['behavior_type'] = True
    
    return field

def generate_markdown_table(fields: List[Dict[str, Any]]) -> str:
    """Generate markdown table from field definitions."""
    
    table = "# Agent Library Field Reference (v2)\n\n"
    table += "| Field Name | Type | Required | Category | Description |\n"
    table += "|------------|------|----------|----------|-------------|\n"
    
    for field in fields:
        name = field['name']
        field_type = field['type']
        required = "✓" if field['required'] else ""
        
        # Build category info
        category_parts = []
        if field['category']:
            category_parts.append(field['category'].title())
        if field['workflow_type']:
            category_parts.append("Workflow")
        if field['behavior_type']:
            category_parts.append("Behavior")
        
        category = ", ".join(category_parts) if category_parts else ""
        
        # Clean description for table (remove newlines, escape pipes)
        description = field['description'].replace('\n', ' ').replace('|', '\\|').strip()
        
        table += f"| {name} | {field_type} | {required} | {category} | {description} |\n"
    
    return table

def generate_json_schema(fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate JSON schema from field definitions."""
    
    properties = {}
    required_fields = []
    
    for field in fields:
        field_name = field['name'].lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
        
        property_def = {
            "type": field['type'],
            "description": field['description']
        }
        
        # Add format hints for specific types
        if field['type'] == 'string':
            if 'url' in field['name'].lower() or 'link' in field['name'].lower():
                property_def["format"] = "uri"
            elif 'date' in field['name'].lower():
                property_def["format"] = "date"
        
        # Add enum for boolean fields with specific meanings
        if field['type'] == 'boolean':
            property_def["default"] = False
        
        properties[field_name] = property_def
        
        if field['required']:
            required_fields.append(field_name)
    
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "System Prompt Agent",
        "type": "object",
        "description": "Schema for system prompt agent definitions in the library",
        "properties": properties,
        "required": required_fields,
        "additionalProperties": False
    }
    
    return schema

def main():
    parser = argparse.ArgumentParser(description='Generate data model documentation')
    parser.add_argument('--input', '-i', 
                       default='data-model/v2/v2.md',
                       help='Input markdown file (default: data-model/v2/v2.md)')
    parser.add_argument('--output-md', '-m',
                       default='data-model/v2/v2-table.md', 
                       help='Output markdown table file')
    parser.add_argument('--output-json', '-j',
                       default='data-model/v2/v2-schema.json',
                       help='Output JSON schema file')
    parser.add_argument('--update-original', '-u',
                       action='store_true',
                       help='Update the original v2.md file with table format')
    
    args = parser.parse_args()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {input_path} not found")
        return 1
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the data model
    fields = parse_data_model(content)
    print(f"Parsed {len(fields)} fields from data model")
    
    # Generate markdown table
    markdown_table = generate_markdown_table(fields)
    
    # Generate JSON schema
    json_schema = generate_json_schema(fields)
    
    # Write outputs
    if args.update_original:
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write(markdown_table)
        print(f"Updated original file: {input_path}")
    else:
        output_md_path = Path(args.output_md)
        output_md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_table)
        print(f"Generated markdown table: {output_md_path}")
    
    output_json_path = Path(args.output_json)
    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_schema, f, indent=2)
    print(f"Generated JSON schema: {output_json_path}")
    
    return 0

if __name__ == '__main__':
    exit(main())
