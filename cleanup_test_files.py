#!/usr/bin/env python3
"""
Test File Cleanup Script for System Prompt Library

This script identifies and deletes files containing "Test Entry: True" in both
JSON and markdown formats from the system-prompts directory structure.
"""

import os
import json
import re
import argparse
from pathlib import Path

def find_test_files_json(json_dir):
    """Find JSON files with 'Test Entry': true"""
    test_files = []
    json_path = Path(json_dir)
    
    if not json_path.exists():
        print(f"Warning: JSON directory {json_dir} does not exist")
        return test_files
    
    for json_file in json_path.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check for "Test Entry" field with value True
            if data.get("Test Entry") is True:
                test_files.append(json_file)
                print(f"Found test JSON file: {json_file}")
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not process {json_file}: {e}")
            
    return test_files

def find_test_files_md(md_dir):
    """Find markdown files with '- [x] Test Entry' pattern"""
    test_files = []
    md_path = Path(md_dir)
    
    if not md_path.exists():
        print(f"Warning: Markdown directory {md_dir} does not exist")
        return test_files
    
    # Pattern to match "- [x] Test Entry" in markdown (checkbox format)
    test_pattern = re.compile(r'-\s*\[x\]\s*Test Entry', re.IGNORECASE)
    
    for md_file in md_path.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if test_pattern.search(content):
                test_files.append(md_file)
                print(f"Found test MD file: {md_file}")
                
        except FileNotFoundError as e:
            print(f"Warning: Could not process {md_file}: {e}")
            
    return test_files

def delete_files(files, dry_run=False):
    """Delete the specified files"""
    if not files:
        print("No files to delete.")
        return
    
    print(f"\n{'DRY RUN: Would delete' if dry_run else 'Deleting'} {len(files)} files:")
    
    for file_path in files:
        print(f"  - {file_path}")
        if not dry_run:
            try:
                file_path.unlink()
                print(f"    ✓ Deleted")
            except OSError as e:
                print(f"    ✗ Error deleting: {e}")

def main():
    parser = argparse.ArgumentParser(description="Clean up test files from System Prompt Library")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be deleted without actually deleting")
    parser.add_argument("--json-only", action="store_true",
                       help="Only process JSON files")
    parser.add_argument("--md-only", action="store_true", 
                       help="Only process markdown files")
    
    args = parser.parse_args()
    
    # Get repository root (script location)
    repo_root = Path(__file__).parent
    json_dir = repo_root / "system-prompts" / "json"
    md_dir = repo_root / "system-prompts" / "md"
    
    print("System Prompt Library Test File Cleanup")
    print("=" * 40)
    print(f"Repository root: {repo_root}")
    print(f"JSON directory: {json_dir}")
    print(f"Markdown directory: {md_dir}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be deleted")
    
    print("\nScanning for test files...")
    
    all_test_files = []
    
    # Find test files in JSON directory
    if not args.md_only:
        print(f"\nScanning JSON files in {json_dir}...")
        json_test_files = find_test_files_json(json_dir)
        all_test_files.extend(json_test_files)
    
    # Find test files in markdown directory  
    if not args.json_only:
        print(f"\nScanning markdown files in {md_dir}...")
        md_test_files = find_test_files_md(md_dir)
        all_test_files.extend(md_test_files)
    
    # Delete found files
    if all_test_files:
        print(f"\nFound {len(all_test_files)} test files total")
        
        if not args.dry_run:
            confirm = input("\nProceed with deletion? (y/N): ").lower().strip()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
        
        delete_files(all_test_files, dry_run=args.dry_run)
        
        if not args.dry_run:
            print(f"\n✅ Cleanup complete! Deleted {len(all_test_files)} test files.")
            print("\nRecommendation: Run ./update_library.sh to regenerate indices after cleanup.")
    else:
        print("\n✅ No test files found. Repository is clean!")

if __name__ == "__main__":
    main()
