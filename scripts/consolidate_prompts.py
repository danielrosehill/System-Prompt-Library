#!/usr/bin/env python3
"""
System Prompt Consolidation Script

This script consolidates all individual JSON files from the system-prompts/json/ 
directory into a single JSON array. It supports incremental updates, meaning 
subsequent runs will only update changed files or add new ones rather than 
overwriting the entire consolidated file.

Usage:
    python consolidate_prompts.py [--output OUTPUT_FILE] [--force-rebuild]

Options:
    --output: Specify output file (default: consolidated_prompts.json)
    --force-rebuild: Force complete rebuild instead of incremental update
"""

import json
import os
import argparse
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class PromptConsolidator:
    def __init__(self, json_dir: str, output_file: str):
        self.json_dir = Path(json_dir)
        self.output_file = Path(output_file)
        self.metadata_file = self.output_file.with_suffix('.metadata.json')
        
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file for change detection."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def load_metadata(self) -> Dict[str, Any]:
        """Load metadata about previously processed files."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {
            "file_hashes": {},
            "last_update": None,
            "total_files": 0
        }
    
    def save_metadata(self, metadata: Dict[str, Any]):
        """Save metadata about processed files."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def load_existing_consolidated(self) -> List[Dict[str, Any]]:
        """Load existing consolidated file if it exists."""
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'prompts' in data:
                        return data['prompts']
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return []
    
    def get_json_files(self) -> List[Path]:
        """Get all JSON files from the source directory."""
        return list(self.json_dir.glob("*.json"))
    
    def load_prompt_file(self, file_path: Path) -> Dict[str, Any]:
        """Load and validate a single prompt JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add metadata
            data['_filename'] = file_path.name
            data['_file_modified'] = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()
            
            # Ensure consistent naming
            if 'agentname' not in data and 'name' not in data:
                # Extract name from filename
                name = file_path.stem.replace('_270525', '').replace('_', ' ')
                data['name'] = name
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    def consolidate(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """Main consolidation logic with incremental updates."""
        print(f"Starting consolidation of prompts from {self.json_dir}")
        
        # Load metadata and existing data
        metadata = self.load_metadata()
        existing_prompts = [] if force_rebuild else self.load_existing_consolidated()
        
        # Create lookup for existing prompts by filename
        existing_by_filename = {
            prompt.get('_filename', ''): prompt 
            for prompt in existing_prompts
        }
        
        # Get all JSON files
        json_files = self.get_json_files()
        updated_prompts = []
        files_processed = 0
        files_updated = 0
        files_added = 0
        
        print(f"Found {len(json_files)} JSON files to process")
        
        for file_path in json_files:
            filename = file_path.name
            current_hash = self.calculate_file_hash(file_path)
            previous_hash = metadata["file_hashes"].get(filename)
            
            # Check if file needs processing
            if not force_rebuild and current_hash == previous_hash and filename in existing_by_filename:
                # File unchanged, use existing data
                updated_prompts.append(existing_by_filename[filename])
                files_processed += 1
                continue
            
            # Load and process the file
            prompt_data = self.load_prompt_file(file_path)
            if prompt_data:
                updated_prompts.append(prompt_data)
                metadata["file_hashes"][filename] = current_hash
                
                if filename in existing_by_filename:
                    files_updated += 1
                    print(f"Updated: {filename}")
                else:
                    files_added += 1
                    print(f"Added: {filename}")
                    
                files_processed += 1
        
        # Remove files that no longer exist
        current_filenames = {f.name for f in json_files}
        files_removed = 0
        for filename in list(metadata["file_hashes"].keys()):
            if filename not in current_filenames:
                del metadata["file_hashes"][filename]
                files_removed += 1
                print(f"Removed: {filename}")
        
        # Update metadata
        metadata["last_update"] = datetime.now().isoformat()
        metadata["total_files"] = len(updated_prompts)
        
        # Create final structure
        consolidated_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_prompts": len(updated_prompts),
                "source_directory": str(self.json_dir),
                "files_processed": files_processed,
                "files_added": files_added,
                "files_updated": files_updated,
                "files_removed": files_removed,
                "force_rebuild": force_rebuild
            },
            "prompts": sorted(updated_prompts, key=lambda x: x.get('agentname', x.get('name', x.get('_filename', ''))))
        }
        
        # Save consolidated file
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
        
        # Save metadata
        self.save_metadata(metadata)
        
        print(f"\nConsolidation complete!")
        print(f"Output file: {self.output_file}")
        print(f"Total prompts: {len(updated_prompts)}")
        print(f"Files processed: {files_processed}")
        print(f"Files added: {files_added}")
        print(f"Files updated: {files_updated}")
        print(f"Files removed: {files_removed}")
        
        return consolidated_data


def main():
    parser = argparse.ArgumentParser(description="Consolidate system prompt JSON files")
    parser.add_argument(
        '--output', 
        default='../consolidated_prompts.json',
        help='Output file path (default: ../consolidated_prompts.json)'
    )
    parser.add_argument(
        '--force-rebuild',
        action='store_true',
        help='Force complete rebuild instead of incremental update'
    )
    parser.add_argument(
        '--json-dir',
        default='../system-prompts/json',
        help='Directory containing JSON files (default: ../system-prompts/json)'
    )
    
    args = parser.parse_args()
    
    # Validate input directory
    json_dir = Path(args.json_dir)
    if not json_dir.exists():
        print(f"Error: Directory {json_dir} does not exist")
        return 1
    
    if not json_dir.is_dir():
        print(f"Error: {json_dir} is not a directory")
        return 1
    
    # Run consolidation
    consolidator = PromptConsolidator(json_dir, args.output)
    try:
        consolidator.consolidate(force_rebuild=args.force_rebuild)
        return 0
    except Exception as e:
        print(f"Error during consolidation: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
