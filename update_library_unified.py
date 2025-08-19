#!/usr/bin/env python3
"""
Unified System Prompt Library Update Script

This single script handles all library maintenance tasks:
1. Consolidates individual JSON files into consolidated_prompts.json
2. Generates index.md from consolidated data with growth tracking
3. Updates README.md with the latest index content
4. Provides comprehensive logging and error handling

Replaces the need for multiple separate scripts and shell wrappers.
"""

import json
import os
import argparse
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class SystemPromptLibraryUpdater:
    """Main class for updating the System Prompt Library."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.json_dir = repo_root / "system-prompts" / "json"
        self.consolidated_file = repo_root / "consolidated_prompts.json"
        self.consolidated_metadata_file = repo_root / "consolidated_prompts.metadata.json"
        self.index_file = repo_root / "index.md"
        self.index_metadata_file = repo_root / "index_metadata.json"
        self.growth_history_file = repo_root / "growth_history.json"
        self.readme_file = repo_root / "README.md"
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "PROGRESS": "🔄"}
        icon = icons.get(level, "📝")
        print(f"{icon} [{timestamp}] {message}")
    
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""
    
    def load_metadata(self, metadata_file: Path) -> Dict:
        """Load metadata from file."""
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"file_hashes": {}, "last_updated": None, "stats": {}}
    
    def save_metadata(self, metadata_file: Path, metadata: Dict):
        """Save metadata to file."""
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
    
    def consolidate_prompts(self, force_rebuild: bool = False) -> Tuple[bool, int, int]:
        """Consolidate individual JSON files into a single file."""
        self.log("Starting JSON consolidation", "PROGRESS")
        
        if not self.json_dir.exists():
            self.log(f"JSON directory not found: {self.json_dir}", "ERROR")
            return False, 0, 0
        
        # Load existing metadata
        metadata = self.load_metadata(self.consolidated_metadata_file)
        existing_hashes = metadata.get("file_hashes", {})
        
        consolidated_prompts = []
        processed_files = 0
        updated_files = 0
        new_hashes = {}
        
        # Get all JSON files
        json_files = list(self.json_dir.glob("*.json"))
        total_files = len(json_files)
        
        self.log(f"Found {total_files} JSON files to process")
        
        for json_file in json_files:
            try:
                # Calculate current hash
                current_hash = self.calculate_file_hash(json_file)
                file_key = json_file.name
                new_hashes[file_key] = current_hash
                
                # Check if file needs processing
                if not force_rebuild and file_key in existing_hashes and existing_hashes[file_key] == current_hash:
                    # File unchanged, skip processing but we still need the content for final output
                    pass
                else:
                    updated_files += 1
                
                # Load and process the JSON file
                with open(json_file, 'r', encoding='utf-8') as f:
                    try:
                        prompt_data = json.load(f)
                        consolidated_prompts.append(prompt_data)
                        processed_files += 1
                    except json.JSONDecodeError as e:
                        self.log(f"Invalid JSON in {json_file.name}: {e}", "WARNING")
                        continue
                        
            except Exception as e:
                self.log(f"Error processing {json_file.name}: {e}", "WARNING")
                continue
        
        # Sort prompts alphabetically by agent name
        consolidated_prompts.sort(key=lambda x: x.get('agentname', '').lower())
        
        # Save consolidated file
        with open(self.consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_prompts, f, indent=2, ensure_ascii=False)
        
        # Update metadata
        metadata.update({
            "file_hashes": new_hashes,
            "last_updated": datetime.now().isoformat(),
            "stats": {
                "total_files": total_files,
                "processed_files": processed_files,
                "updated_files": updated_files,
                "valid_prompts": len(consolidated_prompts)
            }
        })
        
        self.save_metadata(self.consolidated_metadata_file, metadata)
        
        self.log(f"Consolidated {processed_files} valid prompts from {total_files} files", "SUCCESS")
        if not force_rebuild:
            self.log(f"Updated {updated_files} changed files (incremental mode)")
        
        return True, processed_files, len(consolidated_prompts)
    
    def load_growth_history(self) -> Dict:
        """Load growth history."""
        if self.growth_history_file.exists():
            with open(self.growth_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"entries": []}
    
    def update_growth_history(self, prompt_count: int):
        """Update growth history with current count."""
        history = self.load_growth_history()
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Check if we already have an entry for today
        today_entry = None
        for entry in history["entries"]:
            if entry["date"] == current_date:
                today_entry = entry
                break
        
        if today_entry:
            today_entry["count"] = prompt_count
            today_entry["updated"] = datetime.now().isoformat()
        else:
            history["entries"].append({
                "date": current_date,
                "count": prompt_count,
                "created": datetime.now().isoformat()
            })
        
        # Save updated history
        with open(self.growth_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, default=str)
    
    def generate_sparkline(self, counts: List[int], width: int = 20) -> str:
        """Generate a simple ASCII sparkline."""
        if not counts or len(counts) < 2:
            return "📈 " + "▁" * width
        
        min_count = min(counts)
        max_count = max(counts)
        
        if max_count == min_count:
            return "📈 " + "▄" * width
        
        # Normalize values to 0-7 range for block characters
        normalized = []
        for count in counts[-width:]:  # Take last 'width' values
            norm = int(((count - min_count) / (max_count - min_count)) * 7)
            normalized.append(norm)
        
        # Unicode block characters for sparkline
        blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        sparkline = "📈 " + "".join(blocks[n] for n in normalized)
        
        return sparkline
    
    def generate_index(self, force_rebuild: bool = False) -> bool:
        """Generate markdown index from consolidated JSON."""
        self.log("Starting index generation", "PROGRESS")
        
        if not self.consolidated_file.exists():
            self.log("Consolidated JSON file not found", "ERROR")
            return False
        
        # Load consolidated prompts
        with open(self.consolidated_file, 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        valid_prompts = [p for p in prompts if p.get('agentname')]
        prompt_count = len(valid_prompts)
        
        # Update growth history
        self.update_growth_history(prompt_count)
        
        # Load growth history for sparkline
        history = self.load_growth_history()
        counts = [entry["count"] for entry in history["entries"]]
        sparkline = self.generate_sparkline(counts)
        
        # Generate index content
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        index_content = f"""# System Prompt Index

{sparkline}

**Total Prompts:** {prompt_count} | **Last Updated:** {current_date}

*Generated on {current_date} from consolidated system prompts*

---

"""
        
        # Sort prompts alphabetically
        valid_prompts.sort(key=lambda x: x.get('agentname', '').lower())
        
        for prompt in valid_prompts:
            agent_name = prompt.get('agentname', 'Unnamed')
            description = prompt.get('description', 'No description available')
            
            # Feature capabilities with checkboxes
            features = []
            feature_fields = {
                'is-agent': 'Agent-based interaction',
                'is-single-turn': 'Single-turn conversation',
                'structured-output-generation': 'Structured output generation',
                'image-generation': 'Image generation',
                'data-utility': 'Data utility functions'
            }
            
            for field, label in feature_fields.items():
                value = prompt.get(field, False)
                if isinstance(value, str):
                    value = value.lower() == 'true'
                checkbox = "☑️" if value else "☐"
                features.append(f"  - {checkbox} {label}")
            
            # Links section
            json_filename = f"{agent_name.replace(' ', '_').replace('/', '_')}_270525.json"
            links = [f"  - 📄 [JSON File](system-prompts/json/{json_filename})"]
            
            if prompt.get('chatgptlink'):
                links.append(f"  - 🤖 [ChatGPT]({prompt['chatgptlink']})")
            
            # Build entry
            index_content += f"""## {agent_name}

{description}

**Features:**
{chr(10).join(features)}

**Links:**
{chr(10).join(links)}

---

"""
        
        # Save index file
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        # Save metadata
        index_metadata = {
            "generated_at": datetime.now().isoformat(),
            "prompt_count": prompt_count,
            "total_entries": len(prompts),
            "valid_entries": len(valid_prompts)
        }
        
        self.save_metadata(self.index_metadata_file, index_metadata)
        
        self.log(f"Generated index with {prompt_count} prompts", "SUCCESS")
        return True
    
    def update_readme(self) -> bool:
        """Update README.md with index content."""
        self.log("Updating README with index content", "PROGRESS")
        
        if not self.readme_file.exists():
            self.log("README.md not found", "ERROR")
            return False
        
        if not self.index_file.exists():
            self.log("index.md not found", "ERROR")
            return False
        
        # Read files
        with open(self.readme_file, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # Update generation date in index content
        current_date = datetime.now().strftime('%Y-%m-%d')
        index_content = re.sub(
            r'\*Generated on \d{4}-\d{2}-\d{2}',
            f'*Generated on {current_date}',
            index_content
        )
        
        # Define markers
        begin_marker = "<!-- BEGIN_INDEX_CONTENT -->"
        end_marker = "<!-- END_INDEX_CONTENT -->"
        
        if begin_marker not in readme_content or end_marker not in readme_content:
            self.log("Marker comments not found in README.md", "ERROR")
            return False
        
        # Remove any existing index sections
        pattern = f"## System Prompt Index[\\s\\n]*{begin_marker}[\\s\\S]*?{end_marker}"
        updated_readme = re.sub(pattern, "", readme_content, flags=re.DOTALL)
        
        # Add index at the end
        if not updated_readme.endswith('\n'):
            updated_readme += '\n'
        
        updated_readme += f"\n## System Prompt Index\n\n{begin_marker}\n{index_content}\n{end_marker}\n"
        
        # Save updated README
        with open(self.readme_file, 'w', encoding='utf-8') as f:
            f.write(updated_readme)
        
        self.log("README updated successfully", "SUCCESS")
        return True
    
    def run_full_update(self, force_rebuild: bool = False) -> bool:
        """Run the complete update process."""
        self.log("🚀 Starting System Prompt Library Update", "INFO")
        self.log(f"Repository: {self.repo_root}")
        
        success_count = 0
        total_tasks = 3
        
        # Step 1: Consolidate JSON files
        success, processed, valid = self.consolidate_prompts(force_rebuild)
        if success:
            success_count += 1
        else:
            self.log("JSON consolidation failed, aborting", "ERROR")
            return False
        
        # Step 2: Generate index
        if self.generate_index(force_rebuild):
            success_count += 1
        else:
            self.log("Index generation failed, continuing with README update", "WARNING")
        
        # Step 3: Update README
        if self.update_readme():
            success_count += 1
        else:
            self.log("README update failed", "WARNING")
        
        # Summary
        self.log(f"📊 Completed {success_count}/{total_tasks} tasks successfully")
        
        if success_count == total_tasks:
            self.log("🎉 All updates completed successfully!", "SUCCESS")
            return True
        else:
            self.log("⚠️ Some tasks failed, check output above", "WARNING")
            return success_count > 0


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Unified System Prompt Library updater - handles consolidation, indexing, and README updates"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild of all files, ignoring incremental updates"
    )
    parser.add_argument(
        "--consolidate-only",
        action="store_true",
        help="Only run JSON consolidation"
    )
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Only generate index (requires existing consolidated file)"
    )
    parser.add_argument(
        "--readme-only",
        action="store_true",
        help="Only update README (requires existing index file)"
    )
    
    args = parser.parse_args()
    
    # Determine repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent
    
    # Initialize updater
    updater = SystemPromptLibraryUpdater(repo_root)
    
    # Run appropriate tasks
    if args.consolidate_only:
        success, _, _ = updater.consolidate_prompts(args.force_rebuild)
        return 0 if success else 1
    elif args.index_only:
        success = updater.generate_index(args.force_rebuild)
        return 0 if success else 1
    elif args.readme_only:
        success = updater.update_readme()
        return 0 if success else 1
    else:
        # Run full update
        success = updater.run_full_update(args.force_rebuild)
        return 0 if success else 1


if __name__ == "__main__":
    exit(main())
