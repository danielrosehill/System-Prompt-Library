#!/usr/bin/env python3
"""
Remove the 'depersonalised-system-prompt' field from all JSON files in the system-prompts/json directory.
"""

import json
import os
from pathlib import Path

def remove_depersonalised_field():
    """Remove depersonalised-system-prompt field from all JSON files."""
    
    # Path to JSON files directory
    json_dir = Path(__file__).parent.parent / "system-prompts" / "json"
    
    if not json_dir.exists():
        print(f"Error: Directory {json_dir} does not exist")
        return
    
    files_processed = 0
    files_modified = 0
    errors = 0
    
    # Process all JSON files
    for json_file in json_dir.glob("*.json"):
        try:
            files_processed += 1
            
            # Read the JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if the field exists and remove it
            if 'depersonalised-system-prompt' in data:
                del data['depersonalised-system-prompt']
                files_modified += 1
                
                # Write back the modified JSON
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Removed field from: {json_file.name}")
            
        except json.JSONDecodeError as e:
            print(f"✗ JSON decode error in {json_file.name}: {e}")
            errors += 1
        except Exception as e:
            print(f"✗ Error processing {json_file.name}: {e}")
            errors += 1
    
    print(f"\n--- Summary ---")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")
    print(f"Errors: {errors}")
    
    if files_modified > 0:
        print(f"\nSuccessfully removed 'depersonalised-system-prompt' field from {files_modified} files.")
        print("Consider running ./update_library.sh to regenerate consolidated files.")
    else:
        print("\nNo files contained the 'depersonalised-system-prompt' field.")

if __name__ == "__main__":
    remove_depersonalised_field()
