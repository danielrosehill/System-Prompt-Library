#!/usr/bin/env python3
"""
Generate markdown index table from system prompt JSON files.

This script creates an index.md file at the repository root containing a markdown table
of all system prompts, sorted alphabetically by agent name. It supports incremental
updates by tracking file modification times.
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import hashlib


def load_metadata(metadata_file):
    """Load existing metadata for incremental updates."""
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"file_hashes": {}, "last_generated": None}


def save_metadata(metadata_file, metadata):
    """Save metadata for future incremental updates."""
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, default=str)


def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_json_file(file_path):
    """Load and parse a JSON file, returning None if invalid."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Handle different field naming conventions
            # Map alternative field names to standard names
            if 'agent-name' in data and 'agentname' not in data:
                data['agentname'] = data['agent-name']
                
            if 'agent-description' in data and 'description' not in data:
                data['description'] = data['agent-description']
                
            # Ensure required fields exist (after mapping)
            if ('agentname' in data or 'agent-name' in data) and \
               ('description' in data or 'agent-description' in data):
                return data
            else:
                print(f"Warning: Missing required fields in {file_path}")
                return None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}")
        return None


def generate_index_table(json_dir, force_rebuild=False, output_file=None):
    """Generate markdown index table from JSON files."""
    json_path = Path(json_dir)
    # Use absolute paths based on script location
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    metadata_file = repo_root / "index_metadata.json"
    
    # Load existing metadata
    metadata = load_metadata(metadata_file)
    
    # Get all JSON files
    json_files = list(json_path.glob("*.json"))
    
    # Track changes
    files_processed = 0
    files_added = 0
    files_updated = 0
    files_removed = 0
    
    # Current file hashes
    current_files = {}
    prompts_data = []
    
    print(f"Processing {len(json_files)} JSON files...")
    
    for json_file in json_files:
        file_hash = get_file_hash(json_file)
        relative_path = str(json_file.relative_to(json_path.parent.parent))
        current_files[relative_path] = file_hash
        
        # Check if file needs processing
        if not force_rebuild and relative_path in metadata["file_hashes"]:
            if metadata["file_hashes"][relative_path] == file_hash:
                # File unchanged, skip processing but we still need the data for the table
                pass
            else:
                files_updated += 1
        else:
            files_added += 1
        
        # Load the JSON data
        data = load_json_file(json_file)
        if data:
            # Clean up agent name (remove leading/trailing whitespace)
            agent_name = (data.get('agentname') or '').strip()
            description = (data.get('description') or '').strip()
            
            # Skip entries with empty required fields
            if not agent_name or not description:
                print(f"Warning: Skipping {json_file.name} - missing agent name or description")
                continue
            
            # Create relative link to the JSON file
            relative_link = f"system-prompts/json/{json_file.name}"
            
            # Check if there's a ChatGPT link
            chatgpt_link = None
            if 'chatgptlink' in data and data['chatgptlink']:
                chatgpt_link = data['chatgptlink']
            elif 'chatgpt-url' in data and data['chatgpt-url']:
                chatgpt_link = data['chatgpt-url']
            
            prompts_data.append({
                'agent_name': agent_name,
                'description': description,
                'link': relative_link,
                'chatgpt_link': chatgpt_link
            })
            files_processed += 1
    
    # Check for removed files
    for old_file in metadata["file_hashes"]:
        if old_file not in current_files:
            files_removed += 1
    
    # Sort prompts alphabetically by agent name
    prompts_data.sort(key=lambda x: x['agent_name'].lower())
    
    # Generate markdown table
    current_date = datetime.now().strftime('%Y-%m-%d')
    markdown_content = f"""# System Prompt Library Index

*Generated on {current_date} from {files_processed} system prompts*

| Agent Name | Description | CustomGPT |
|------------|-------------|----------|
"""
    
    for prompt in prompts_data:
        # Escape pipe characters in content to avoid breaking the table
        agent_name = prompt['agent_name'].replace('|', '\\|')
        description = prompt['description'].replace('|', '\\|')
        
        # Truncate description if too long (optional)
        if len(description) > 150:
            description = description[:147] + "..."
        
        # Create agent name with link to JSON file
        agent_name_with_link = f"[{agent_name}]({prompt['link']})"
        
        # Add CustomGPT badge in a separate column if available
        customgpt_column = ""
        if prompt['chatgpt_link']:
            customgpt_column = f"[![CustomGPT](https://img.shields.io/badge/CustomGPT-Available-green)]({prompt['chatgpt_link']})"
        
        markdown_content += f"| {agent_name_with_link} | {description} | {customgpt_column} |\n"
    
    # Write the index file
    index_file = output_file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    # Update metadata
    metadata.update({
        "file_hashes": current_files,
        "last_generated": datetime.now(),
        "total_prompts": files_processed,
        "files_processed": files_processed,
        "files_added": files_added,
        "files_updated": files_updated,
        "files_removed": files_removed,
        "force_rebuild": force_rebuild
    })
    
    save_metadata(metadata_file, metadata)
    
    # Print summary
    print(f"\n✅ Index generated successfully!")
    print(f"📊 Total prompts: {files_processed}")
    print(f"📁 Output file: {index_file}")
    
    if not force_rebuild:
        print(f"🔄 Files added: {files_added}")
        print(f"🔄 Files updated: {files_updated}")
        print(f"🔄 Files removed: {files_removed}")
    
    return index_file


def main():
    """Main function with command line argument parsing."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    parser = argparse.ArgumentParser(
        description="Generate markdown index table from system prompt JSON files"
    )
    parser.add_argument(
        "--json-dir",
        default=str(repo_root / "system-prompts" / "json"),
        help="Directory containing JSON files (default: ../system-prompts/json)"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild of entire index, ignoring incremental updates"
    )
    parser.add_argument(
        "--output",
        default=str(repo_root / "index.md"),
        help="Output file name (default: ../index.md)"
    )
    
    args = parser.parse_args()
    
    # Check if JSON directory exists
    if not os.path.exists(args.json_dir):
        print(f"❌ Error: JSON directory '{args.json_dir}' not found!")
        return 1
    
    try:
        generate_index_table(args.json_dir, args.force_rebuild, args.output)
        return 0
    except Exception as e:
        print(f"❌ Error generating index: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
