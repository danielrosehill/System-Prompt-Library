#!/usr/bin/env python3
"""
System Prompt Library JSON Format Standardization Script

This script standardizes all JSON files in the repo-data/json/ directory
to match the latest format (240925_format.json).

Usage:
    python standardize_json_format.py [--dry-run] [--backup]
"""

import json
import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Field mapping from old format to new format
FIELD_MAPPING = {
    # Basic info fields
    "agentname": "agent_name",
    "description": "Description", 
    "systemprompt": "System Prompt",
    "chatgptlink": "ChatGPT Access URL",
    "creation_date": "Creation Date",
    
    # Boolean capability fields (old -> new)
    "is-agent": "Is Agent",
    "is-single-turn": "Single Turn (Workflow Type)",
    "structured-output-generation": "Structured Output (Workflow Type)",
    "image-generation": "Image Generation (Workflow Type)",
    "data-utility": "Data Utility (Category)",
    "personalised-system-prompt": "Personalised",
    
    # Schema fields
    "json-schema": "JSON Schema (Full)",
    "json-example": "JSON Schema (Example Value)",
}

# Complete new format template with all fields
NEW_FORMAT_TEMPLATE = {
    "agent_name": None,
    "Description": None,
    "One Line Summary": None,
    "Creation Date": None,
    "ChatGPT Access URL": None,
    "Utility Estimate": 0,
    "Test Entry": False,
    "JSON Schema (Full)": None,
    "JSON Schema (Example Value)": None,
    "Better As Tool": False,
    "Is Agent": False,
    "Single Turn (Workflow Type)": False,
    "External Tooling (Required)": False,
    "Structured Output (Workflow Type)": False,
    "Image Generation (Workflow Type)": False,
    "System Prompt": None,
    "Character (Type)": False,
    "Roleplay (Behavior)": False,
    "Voice First": False,
    "Writing Assistant": False,
    "Data Utility (Category)": False,
    "N8N Link": None,
    "RAG (Required)": False,
    "Vision (Req)": False,
    "Spech-To-Speech": False,
    "Video Input (Required)": False,
    "Audio (Required)": False,
    "TTS (Required)": False,
    "File Input (Req)": False,
    "Conversational": False,
    "Instructional": False,
    "Autonomous": False,
    "MCPs Used": None,
    "API Notes": None,
    "MCP Notes": None,
    "Local LLM Friendly?": False,
    "Local LLM Notes": None,
    "LLM Selection Notes": None,
    "Deep Research": False,
    "Update/Iteration": False,
    "Iteration Notes": None,
    "Use Case Outline": None,
    "PII Notes": None,
    "Cost Estimates": None,
    "Localtisation Notes": None,
    "Guardrails Notes": None,
    "Gemini URL": None
}

def normalize_boolean_value(value: Any) -> bool:
    """Convert various boolean representations to actual boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    if isinstance(value, (int, float)):
        return bool(value)
    return False

def normalize_date_value(value: Any) -> Optional[str]:
    """Normalize date values to YYYY-MM-DD format."""
    if value is None:
        return None
    
    if isinstance(value, str):
        # Handle various date formats
        if value.strip() == "":
            return None
        
        # If it's already in YYYY-MM-DD format, keep it
        if len(value) == 10 and value.count('-') == 2:
            try:
                datetime.strptime(value, '%Y-%m-%d')
                return value
            except ValueError:
                pass
        
        # Try to parse ISO format with timezone
        if '+' in value or 'T' in value:
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                pass
    
    return str(value) if value else None

def standardize_json_file(file_path: Path, dry_run: bool = False) -> Dict[str, Any]:
    """
    Standardize a single JSON file to the new format.
    
    Args:
        file_path: Path to the JSON file
        dry_run: If True, don't write changes, just return what would be changed
        
    Returns:
        Dictionary with standardization results
    """
    result = {
        "file": str(file_path),
        "success": False,
        "changes_made": [],
        "errors": []
    }
    
    try:
        # Read the existing file
        with open(file_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        # Start with the new format template
        new_data = NEW_FORMAT_TEMPLATE.copy()
        
        # Map old fields to new fields
        for old_field, new_field in FIELD_MAPPING.items():
            if old_field in old_data:
                old_value = old_data[old_field]
                
                # Handle boolean fields
                if new_field in ["Is Agent", "Single Turn (Workflow Type)", 
                               "Structured Output (Workflow Type)", "Image Generation (Workflow Type)",
                               "Data Utility (Category)"]:
                    new_data[new_field] = normalize_boolean_value(old_value)
                    if old_value != new_data[new_field]:
                        result["changes_made"].append(f"Normalized boolean {old_field} -> {new_field}: {old_value} -> {new_data[new_field]}")
                
                # Handle date fields
                elif new_field == "Creation Date":
                    new_data[new_field] = normalize_date_value(old_value)
                    if old_value != new_data[new_field]:
                        result["changes_made"].append(f"Normalized date {old_field} -> {new_field}: {old_value} -> {new_data[new_field]}")
                
                # Handle regular fields
                else:
                    new_data[new_field] = old_value
                    result["changes_made"].append(f"Mapped {old_field} -> {new_field}")
        
        # Handle fields that might already be in new format
        for field in NEW_FORMAT_TEMPLATE.keys():
            if field in old_data and field not in [v for v in FIELD_MAPPING.values()]:
                new_data[field] = old_data[field]
                result["changes_made"].append(f"Preserved existing field: {field}")
        
        # Special handling for fields that might need boolean normalization
        boolean_fields = [
            "Test Entry", "Better As Tool", "Is Agent", "Single Turn (Workflow Type)",
            "External Tooling (Required)", "Structured Output (Workflow Type)",
            "Image Generation (Workflow Type)", "Character (Type)", "Roleplay (Behavior)",
            "Voice First", "Writing Assistant", "Data Utility (Category)",
            "RAG (Required)", "Vision (Req)", "Spech-To-Speech", "Video Input (Required)",
            "Audio (Required)", "TTS (Required)", "File Input (Req)", "Conversational",
            "Instructional", "Autonomous", "Local LLM Friendly?", "Deep Research",
            "Update/Iteration"
        ]
        
        for field in boolean_fields:
            if field in new_data:
                old_value = new_data[field]
                new_data[field] = normalize_boolean_value(old_value)
                if old_value != new_data[field]:
                    result["changes_made"].append(f"Normalized boolean {field}: {old_value} -> {new_data[field]}")
        
        # Check if any changes were made
        if not result["changes_made"]:
            result["changes_made"].append("File already in correct format")
        
        # Write the standardized file
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, indent=2, ensure_ascii=False)
        
        result["success"] = True
        
    except json.JSONDecodeError as e:
        result["errors"].append(f"JSON decode error: {e}")
    except Exception as e:
        result["errors"].append(f"Unexpected error: {e}")
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Standardize System Prompt Library JSON format")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without making changes")
    parser.add_argument("--backup", action="store_true",
                       help="Create backup of original files before standardization")
    parser.add_argument("--json-dir", type=str, 
                       default="../../repo-data/json",
                       help="Directory containing JSON files to standardize")
    
    args = parser.parse_args()
    
    # Get the script directory and construct paths
    script_dir = Path(__file__).parent
    json_dir = script_dir / args.json_dir
    
    if not json_dir.exists():
        print(f"Error: JSON directory not found: {json_dir}")
        sys.exit(1)
    
    # Find all JSON files
    json_files = list(json_dir.glob("*.json"))
    if not json_files:
        print(f"No JSON files found in {json_dir}")
        sys.exit(1)
    
    print(f"Found {len(json_files)} JSON files to process")
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    
    if args.backup and not args.dry_run:
        backup_dir = json_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)
        print(f"Creating backup in: {backup_dir}")
    
    # Process each file
    total_processed = 0
    total_errors = 0
    total_changes = 0
    
    for json_file in sorted(json_files):
        print(f"\nProcessing: {json_file.name}")
        
        # Create backup if requested
        if args.backup and not args.dry_run:
            backup_file = backup_dir / json_file.name
            shutil.copy2(json_file, backup_file)
        
        # Standardize the file
        result = standardize_json_file(json_file, dry_run=args.dry_run)
        
        if result["success"]:
            total_processed += 1
            if len(result["changes_made"]) > 1 or result["changes_made"][0] != "File already in correct format":
                total_changes += 1
                print(f"  ✓ Changes made:")
                for change in result["changes_made"]:
                    print(f"    - {change}")
            else:
                print(f"  ✓ Already in correct format")
        else:
            total_errors += 1
            print(f"  ✗ Errors:")
            for error in result["errors"]:
                print(f"    - {error}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"STANDARDIZATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {total_processed}")
    print(f"Files with changes: {total_changes}")
    print(f"Files with errors: {total_errors}")
    
    if args.dry_run:
        print(f"\nThis was a dry run. To apply changes, run without --dry-run flag.")
    elif args.backup:
        print(f"\nBackups created in: {backup_dir}")
    
    if total_errors > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
