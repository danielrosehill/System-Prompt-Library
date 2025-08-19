#!/usr/bin/env python3
"""
File Name Sanitization Script for System Prompt Library

This script sanitizes filenames in both the JSON and Markdown folders to ensure
machine readability by:
- Removing or replacing special characters with underscores
- Converting spaces to underscores
- Handling parentheses, ampersands, and other problematic characters
- Ensuring consistent naming across both JSON and MD folders
- Preserving the date suffix pattern (_DDMMYY)

Usage:
    python sanitize_filenames.py [--dry-run] [--verbose]
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
import argparse
import shutil

class FilenameSanitizer:
    def __init__(self, repo_root: str, dry_run: bool = False, verbose: bool = False):
        self.repo_root = Path(repo_root)
        self.json_dir = self.repo_root / "system-prompts" / "json"
        self.md_dir = self.repo_root / "system-prompts" / "md"
        self.dry_run = dry_run
        self.verbose = verbose
        self.changes = []
        
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename by applying the following rules:
        1. Replace spaces with underscores
        2. Replace problematic characters with underscores
        3. Remove multiple consecutive underscores
        4. Preserve date suffix pattern (_DDMMYY)
        5. Keep file extension
        """
        # Split filename and extension
        name, ext = os.path.splitext(filename)
        
        # Define problematic characters to replace with underscores
        # This includes: &, (, ), ?, !, ', ", :, ;, -, +, =, [, ], {, }, |, \, /, <, >, *, %
        problematic_chars = r'[&()?!\'"":;+\=\[\]{}|\\/<>*%]'
        
        # Replace spaces with underscores
        sanitized = name.replace(' ', '_')
        
        # Replace problematic characters with underscores
        sanitized = re.sub(problematic_chars, '_', sanitized)
        
        # Replace hyphens with underscores (except in date patterns)
        # First, protect date patterns like _270525, _010825, etc.
        date_pattern = r'(_\d{6})$'
        date_match = re.search(date_pattern, sanitized)
        date_suffix = date_match.group(1) if date_match else ''
        
        if date_suffix:
            # Remove date suffix temporarily
            sanitized = sanitized[:-len(date_suffix)]
        
        # Replace remaining hyphens with underscores
        sanitized = sanitized.replace('-', '_')
        
        # Add back date suffix
        sanitized += date_suffix
        
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        return sanitized + ext
    
    def find_problematic_files(self) -> Dict[str, List[Tuple[str, str]]]:
        """Find files that need sanitization in both directories."""
        problematic = {"json": [], "md": []}
        
        for folder_type, folder_path in [("json", self.json_dir), ("md", self.md_dir)]:
            if not folder_path.exists():
                continue
                
            for file_path in folder_path.iterdir():
                if file_path.is_file():
                    original_name = file_path.name
                    sanitized_name = self.sanitize_filename(original_name)
                    
                    if original_name != sanitized_name:
                        problematic[folder_type].append((original_name, sanitized_name))
        
        return problematic
    
    def check_for_conflicts(self, problematic_files: Dict[str, List[Tuple[str, str]]]) -> Set[str]:
        """Check if any sanitized names would create conflicts."""
        conflicts = set()
        
        for folder_type in ["json", "md"]:
            sanitized_names = [new_name for _, new_name in problematic_files[folder_type]]
            folder_path = self.json_dir if folder_type == "json" else self.md_dir
            
            # Check for duplicates in sanitized names
            seen = set()
            for name in sanitized_names:
                if name in seen:
                    conflicts.add(f"Duplicate sanitized name: {name}")
                seen.add(name)
            
            # Check if sanitized names conflict with existing files
            for _, new_name in problematic_files[folder_type]:
                target_path = folder_path / new_name
                if target_path.exists():
                    conflicts.add(f"Target file already exists: {target_path}")
        
        return conflicts
    
    def rename_files(self, problematic_files: Dict[str, List[Tuple[str, str]]]):
        """Rename files in both directories."""
        total_renames = 0
        
        for folder_type, folder_path in [("json", self.json_dir), ("md", self.md_dir)]:
            files_to_rename = problematic_files[folder_type]
            
            if not files_to_rename:
                continue
                
            print(f"\n{folder_type.upper()} folder:")
            
            for original_name, sanitized_name in files_to_rename:
                original_path = folder_path / original_name
                target_path = folder_path / sanitized_name
                
                if self.dry_run:
                    print(f"  WOULD RENAME: {original_name} -> {sanitized_name}")
                else:
                    try:
                        shutil.move(str(original_path), str(target_path))
                        print(f"  RENAMED: {original_name} -> {sanitized_name}")
                        self.changes.append({
                            "folder": folder_type,
                            "original": original_name,
                            "sanitized": sanitized_name
                        })
                        total_renames += 1
                    except Exception as e:
                        print(f"  ERROR renaming {original_name}: {e}")
        
        return total_renames
    
    def update_json_content(self, problematic_files: Dict[str, List[Tuple[str, str]]]):
        """Update JSON file content if the filename field exists and matches the old filename."""
        if self.dry_run:
            return
            
        json_renames = {old: new for old, new in problematic_files["json"]}
        
        for original_name, sanitized_name in problematic_files["json"]:
            json_path = self.json_dir / sanitized_name
            
            if not json_path.exists():
                continue
                
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check if there's a filename field that needs updating
                updated = False
                if 'filename' in data and data['filename'] == original_name:
                    data['filename'] = sanitized_name
                    updated = True
                
                # Update any other fields that might reference the old filename
                for key, value in data.items():
                    if isinstance(value, str) and original_name in value:
                        data[key] = value.replace(original_name, sanitized_name)
                        updated = True
                
                if updated:
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    
                    if self.verbose:
                        print(f"  Updated JSON content: {sanitized_name}")
                        
            except Exception as e:
                print(f"  WARNING: Could not update JSON content for {sanitized_name}: {e}")
    
    def generate_summary_report(self, problematic_files: Dict[str, List[Tuple[str, str]]]):
        """Generate a summary report of changes."""
        total_files = len(problematic_files["json"]) + len(problematic_files["md"])
        
        print(f"\n{'='*60}")
        print("FILENAME SANITIZATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total files needing sanitization: {total_files}")
        print(f"JSON files: {len(problematic_files['json'])}")
        print(f"Markdown files: {len(problematic_files['md'])}")
        
        if self.dry_run:
            print("\n[DRY RUN MODE - No files were actually renamed]")
        else:
            print(f"\nFiles successfully renamed: {len(self.changes)}")
        
        # Show some examples of changes
        if total_files > 0:
            print(f"\nExample changes:")
            examples = []
            for folder_type in ["json", "md"]:
                examples.extend(problematic_files[folder_type][:3])
            
            for original, sanitized in examples[:5]:
                print(f"  {original}")
                print(f"  -> {sanitized}")
                print()
    
    def run(self):
        """Main execution method."""
        print("System Prompt Library - Filename Sanitizer")
        print("=" * 50)
        
        # Check if directories exist
        if not self.json_dir.exists() or not self.md_dir.exists():
            print("ERROR: system-prompts directories not found!")
            return False
        
        # Find problematic files
        print("Scanning for files with problematic names...")
        problematic_files = self.find_problematic_files()
        
        total_files = len(problematic_files["json"]) + len(problematic_files["md"])
        
        if total_files == 0:
            print("✅ All filenames are already properly sanitized!")
            return True
        
        print(f"Found {total_files} files that need sanitization.")
        
        # Check for conflicts
        conflicts = self.check_for_conflicts(problematic_files)
        if conflicts:
            print("\n❌ CONFLICTS DETECTED:")
            for conflict in conflicts:
                print(f"  - {conflict}")
            print("\nPlease resolve conflicts before running the sanitizer.")
            return False
        
        # Show what will be changed
        if self.verbose or self.dry_run:
            for folder_type in ["json", "md"]:
                if problematic_files[folder_type]:
                    print(f"\n{folder_type.upper()} files to rename:")
                    for original, sanitized in problematic_files[folder_type]:
                        print(f"  {original} -> {sanitized}")
        
        # Perform renames
        if not self.dry_run:
            print(f"\nProceeding with file renames...")
        
        total_renames = self.rename_files(problematic_files)
        
        # Update JSON content if needed
        if not self.dry_run and problematic_files["json"]:
            print("\nUpdating JSON file content...")
            self.update_json_content(problematic_files)
        
        # Generate summary
        self.generate_summary_report(problematic_files)
        
        if not self.dry_run and total_renames > 0:
            print(f"\n✅ Successfully sanitized {total_renames} filenames!")
            print("\nRecommendation: Run the library update script to regenerate indices:")
            print("  ./update_library.sh --force-rebuild")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Sanitize filenames in System Prompt Library")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without making changes")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show detailed output")
    parser.add_argument("--repo-root", default=".",
                       help="Path to repository root (default: current directory)")
    
    args = parser.parse_args()
    
    # Find repository root
    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / "system-prompts").exists():
        print("ERROR: Could not find system-prompts directory!")
        print(f"Current path: {repo_root}")
        print("Please run from repository root or specify --repo-root")
        return 1
    
    sanitizer = FilenameSanitizer(
        repo_root=str(repo_root),
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    
    success = sanitizer.run()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
