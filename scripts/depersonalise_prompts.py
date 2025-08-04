#!/usr/bin/env python3
"""
depersonalise_prompts.py - Depersonalises references in System Prompt Library

This script recursively searches through JSON and Markdown files in the repository
and replaces personalised references with generic ones:
- "Daniel Rosehill" -> "the user"
- "Daniel" -> "user"
- "Daniel's" -> "user's"

Usage:
    python depersonalise_prompts.py [--dry-run] [--path /path/to/repo]

Options:
    --dry-run       Show what would be changed without making actual changes
    --path PATH     Specify the repository path (default: current directory)
"""

import os
import json
import re
import argparse
from pathlib import Path
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Replacement patterns
REPLACEMENTS = [
    # Order is important - more specific patterns first
    (r"Daniel Rosehill", "the user"),
    (r"Daniel's", "user's"),
    (r"Daniel", "user"),
]

def depersonalise_text(content):
    """Replace personal references in text with generic ones."""
    original_content = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    return content, content != original_content

def process_json_file(file_path, dry_run=False):
    """Process a JSON file and replace personal references."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON file {file_path}: {e}")
                return False
        
        # Check if this is a prompt file with systemprompt field
        changed = False
        if 'systemprompt' in data:
            original = data['systemprompt']
            data['systemprompt'], systemprompt_changed = depersonalise_text(original)
            changed = changed or systemprompt_changed
        
        # Also check depersonalised-system-prompt field
        if 'depersonalised-system-prompt' in data and data['depersonalised-system-prompt'] is not None:
            original = data['depersonalised-system-prompt']
            data['depersonalised-system-prompt'], depersonalised_changed = depersonalise_text(original)
            changed = changed or depersonalised_changed
            
        if changed:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"{'Would update' if dry_run else 'Updated'} JSON file: {file_path}")
            return True
        
        # Handle consolidated_prompts.json or direct list structure
        elif 'prompts' in data and isinstance(data['prompts'], list):
            changes_made = False
            for prompt in data['prompts']:
                if 'systemprompt' in prompt:
                    original = prompt['systemprompt']
                    prompt['systemprompt'], changed = depersonalise_text(original)
                    if changed:
                        changes_made = True
                
                # Also check depersonalised-system-prompt field
                if 'depersonalised-system-prompt' in prompt and prompt['depersonalised-system-prompt'] is not None:
                    original = prompt['depersonalised-system-prompt']
                    prompt['depersonalised-system-prompt'], changed = depersonalise_text(original)
                    if changed:
                        changes_made = True
            
            if changes_made:
                if not dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                logger.info(f"{'Would update' if dry_run else 'Updated'} consolidated JSON file: {file_path}")
                return True
    
    except Exception as e:
        logger.error(f"Error processing JSON file {file_path}: {e}")
    
    return False

def process_markdown_file(file_path, dry_run=False):
    """Process a Markdown file and replace personal references."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changed = depersonalise_text(content)
        
        if changed:
            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            logger.info(f"{'Would update' if dry_run else 'Updated'} Markdown file: {file_path}")
            return True
    
    except Exception as e:
        logger.error(f"Error processing Markdown file {file_path}: {e}")
    
    return False

def process_repository(repo_path, dry_run=False):
    """Process all relevant files in the repository to depersonalise content."""
    repo_path = Path(repo_path)
    
    # Stats tracking
    stats = {
        'json_files_processed': 0,
        'json_files_updated': 0,
        'md_files_processed': 0,
        'md_files_updated': 0,
    }
    
    # Process system-prompts/json directory
    json_dir = repo_path / 'system-prompts' / 'json'
    if json_dir.exists():
        for json_file in json_dir.glob('*.json'):
            stats['json_files_processed'] += 1
            if process_json_file(json_file, dry_run):
                stats['json_files_updated'] += 1
    
    # Process system-prompts/md directory
    md_dir = repo_path / 'system-prompts' / 'md'
    if md_dir.exists():
        for md_file in md_dir.glob('*.md'):
            stats['md_files_processed'] += 1
            if process_markdown_file(md_file, dry_run):
                stats['md_files_updated'] += 1
    
    # Process consolidated_prompts.json
    consolidated_json = repo_path / 'consolidated_prompts.json'
    if consolidated_json.exists():
        if process_json_file(consolidated_json, dry_run):
            stats['json_files_updated'] += 1
        stats['json_files_processed'] += 1
    
    # Process README.md and other root markdown files
    for md_file in repo_path.glob('*.md'):
        stats['md_files_processed'] += 1
        if process_markdown_file(md_file, dry_run):
            stats['md_files_updated'] += 1
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Depersonalise references in System Prompt Library')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making actual changes')
    parser.add_argument('--path', default=os.getcwd(), help='Path to the repository')
    
    args = parser.parse_args()
    
    logger.info(f"Starting depersonalisation process {'(DRY RUN)' if args.dry_run else ''}")
    logger.info(f"Repository path: {args.path}")
    
    start_time = datetime.now()
    stats = process_repository(args.path, args.dry_run)
    end_time = datetime.now()
    
    logger.info(f"Depersonalisation completed in {(end_time - start_time).total_seconds():.2f} seconds")
    logger.info(f"JSON files processed: {stats['json_files_processed']}, updated: {stats['json_files_updated']}")
    logger.info(f"Markdown files processed: {stats['md_files_processed']}, updated: {stats['md_files_updated']}")
    logger.info(f"Total files processed: {stats['json_files_processed'] + stats['md_files_processed']}")
    logger.info(f"Total files updated: {stats['json_files_updated'] + stats['md_files_updated']}")

if __name__ == "__main__":
    main()
