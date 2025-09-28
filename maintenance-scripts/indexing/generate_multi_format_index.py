#!/usr/bin/env python3
"""
Multi-Format Index Generator for System Prompt Library

Generates index files in multiple formats (JSON, CSV, Markdown) from consolidated prompts.
All index files are created in the index/ directory with consistent data.

Usage:
    python generate_multi_format_index.py [options]
    
Options:
    --force-rebuild     Force rebuild of all index formats
    --json-only         Only generate JSON index
    --csv-only          Only generate CSV index  
    --markdown-only     Only generate Markdown index
"""

import json
import csv
import os
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class MultiFormatIndexGenerator:
    """Generates index files in multiple formats from consolidated prompts."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.consolidated_file = repo_root / "repo-data" / "consolidated_prompts.json"
        self.index_dir = repo_root / "index"
        self.growth_history_file = repo_root / "repo-data" / "growth_history.json"
        
        # Index files
        self.json_index_file = self.index_dir / "index.json"
        self.csv_index_file = self.index_dir / "index.csv"
        self.markdown_index_file = self.index_dir / "index.md"
        self.metadata_file = self.index_dir / "index_metadata.json"
        
        # Ensure index directory exists
        self.index_dir.mkdir(exist_ok=True)
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "PROGRESS": "🔄"}
        icon = icons.get(level, "📝")
        print(f"{icon} [{timestamp}] {message}")
    
    def load_consolidated_prompts(self) -> List[Dict]:
        """Load prompts from consolidated JSON file."""
        if not self.consolidated_file.exists():
            self.log("Consolidated JSON file not found", "ERROR")
            return []
        
        try:
            with open(self.consolidated_file, 'r', encoding='utf-8') as f:
                prompts = json.load(f)
            self.log(f"Loaded {len(prompts)} prompts from consolidated file")
            return prompts
        except Exception as e:
            self.log(f"Error loading consolidated prompts: {e}", "ERROR")
            return []
    
    def load_growth_history(self) -> Dict:
        """Load existing growth history."""
        if not self.growth_history_file.exists():
            return {"entries": []}
        
        try:
            with open(self.growth_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Error loading growth history: {e}", "WARNING")
            return {"entries": []}
    
    def generate_sparkline(self, counts: List[int]) -> str:
        """Generate a simple sparkline from count data."""
        if not counts or len(counts) < 2:
            return "▁"
        
        min_val = min(counts)
        max_val = max(counts)
        
        if min_val == max_val:
            return "▁" * len(counts)
        
        # Normalize values to 0-7 range for sparkline characters
        chars = "▁▂▃▄▅▆▇█"
        normalized = []
        
        for count in counts:
            if max_val == min_val:
                normalized.append(0)
            else:
                norm = int(((count - min_val) / (max_val - min_val)) * 7)
                normalized.append(min(norm, 7))
        
        return ''.join(chars[n] for n in normalized)
    
    def prepare_index_data(self, prompts: List[Dict]) -> Tuple[List[Dict], Dict]:
        """Prepare standardized index data from prompts."""
        # Filter valid prompts (those with agent names)
        valid_prompts = [p for p in prompts if p.get('agent_name')]
        
        # Sort alphabetically by agent name
        valid_prompts.sort(key=lambda x: (x.get('agent_name') or '').lower())
        
        # Prepare index entries
        index_entries = []
        
        for prompt in valid_prompts:
            # Extract basic information
            agent_name = prompt.get('agent_name', 'Unnamed')
            description = prompt.get('Description', 'No description available')
            
            # Feature capabilities (standardized boolean handling)
            features = {}
            feature_fields = {
                'Is Agent': 'is_agent',
                'Single Turn (Workflow Type)': 'single_turn',
                'Structured Output (Workflow Type)': 'structured_output',
                'Image Generation (Workflow Type)': 'image_generation',
                'Data Utility (Category)': 'data_utility'
            }
            
            for field, key in feature_fields.items():
                value = prompt.get(field, False)
                if isinstance(value, str):
                    value = value.lower() == 'true'
                features[key] = bool(value)
            
            # Links
            original_filename = prompt.get('_original_filename')
            if original_filename:
                json_link = f"system-prompts/json/{original_filename}"
            else:
                # Fallback to old method if filename not stored
                json_filename = f"{agent_name.replace(' ', '_').replace('/', '_')}_270525.json"
                json_link = f"system-prompts/json/{json_filename}"
            
            chatgpt_link = prompt.get('ChatGPT Access URL', '')
            
            # Create standardized entry
            entry = {
                'agent_name': agent_name,
                'description': description,
                'features': features,
                'json_link': json_link,
                'chatgpt_link': chatgpt_link,
                'original_filename': original_filename or '',
                # Include raw prompt data for JSON export
                '_raw_data': prompt
            }
            
            index_entries.append(entry)
        
        # Generate metadata
        history = self.load_growth_history()
        counts = [entry["count"] for entry in history["entries"]]
        sparkline = self.generate_sparkline(counts)
        
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'total_prompts': len(prompts),
            'valid_prompts': len(valid_prompts),
            'last_updated': datetime.now().strftime('%Y-%m-%d'),
            'sparkline': sparkline,
            'growth_data': {
                'current_count': len(prompts),
                'historical_counts': counts[-10:] if counts else []  # Last 10 entries
            }
        }
        
        return index_entries, metadata
    
    def generate_json_index(self, entries: List[Dict], metadata: Dict) -> bool:
        """Generate JSON format index."""
        self.log("Generating JSON index", "PROGRESS")
        
        try:
            # Create comprehensive JSON structure
            json_data = {
                'metadata': metadata,
                'prompts': []
            }
            
            # Add prompt entries (include full raw data)
            for entry in entries:
                prompt_entry = {
                    'agent_name': entry['agent_name'],
                    'description': entry['description'],
                    'features': entry['features'],
                    'links': {
                        'json_file': entry['json_link'],
                        'chatgpt': entry['chatgpt_link'] if entry['chatgpt_link'] else None
                    },
                    'metadata': {
                        'original_filename': entry['original_filename']
                    },
                    # Include full prompt data for API consumers
                    'full_data': entry['_raw_data']
                }
                json_data['prompts'].append(prompt_entry)
            
            # Save JSON index
            with open(self.json_index_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            self.log(f"Generated JSON index: {self.json_index_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error generating JSON index: {e}", "ERROR")
            return False
    
    def generate_csv_index(self, entries: List[Dict], metadata: Dict) -> bool:
        """Generate CSV format index."""
        self.log("Generating CSV index", "PROGRESS")
        
        try:
            with open(self.csv_index_file, 'w', newline='', encoding='utf-8') as f:
                # Define CSV columns
                fieldnames = [
                    'agent_name',
                    'description', 
                    'is_agent',
                    'single_turn',
                    'structured_output',
                    'image_generation',
                    'data_utility',
                    'json_link',
                    'chatgpt_link',
                    'original_filename'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                # Write entries
                for entry in entries:
                    row = {
                        'agent_name': entry['agent_name'],
                        'description': entry['description'],
                        'is_agent': entry['features']['is_agent'],
                        'single_turn': entry['features']['single_turn'],
                        'structured_output': entry['features']['structured_output'],
                        'image_generation': entry['features']['image_generation'],
                        'data_utility': entry['features']['data_utility'],
                        'json_link': entry['json_link'],
                        'chatgpt_link': entry['chatgpt_link'],
                        'original_filename': entry['original_filename']
                    }
                    writer.writerow(row)
            
            self.log(f"Generated CSV index: {self.csv_index_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error generating CSV index: {e}", "ERROR")
            return False
    
    def generate_markdown_index(self, entries: List[Dict], metadata: Dict) -> bool:
        """Generate Markdown format index."""
        self.log("Generating Markdown index", "PROGRESS")
        
        try:
            # Generate markdown content
            content = f"""# System Prompt Index

📈 {metadata['sparkline']}

**Total Prompts:** {metadata['total_prompts']} ({metadata['valid_prompts']} with names) | **Last Updated:** {metadata['last_updated']}

*Generated on {metadata['last_updated']} from consolidated system prompts*

---

"""
            
            # Add each prompt entry
            for entry in entries:
                agent_name = entry['agent_name']
                description = entry['description']
                features = entry['features']
                
                # Feature capabilities with checkboxes
                feature_lines = []
                feature_labels = {
                    'is_agent': 'Agent-based interaction',
                    'single_turn': 'Single-turn conversation',
                    'structured_output': 'Structured output generation',
                    'image_generation': 'Image generation',
                    'data_utility': 'Data utility functions'
                }
                
                for key, label in feature_labels.items():
                    checkbox = "☑️" if features.get(key, False) else "☐"
                    feature_lines.append(f"  - {checkbox} {label}")
                
                # Links section
                links = [f"  - 📄 [JSON File]({entry['json_link']})"]
                if entry['chatgpt_link']:
                    links.append(f"  - 🤖 [ChatGPT]({entry['chatgpt_link']})")
                
                # Build entry
                content += f"""## {agent_name}

{description}

**Features:**
{chr(10).join(feature_lines)}

**Links:**
{chr(10).join(links)}

---

"""
            
            # Save markdown index
            with open(self.markdown_index_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log(f"Generated Markdown index: {self.markdown_index_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"Error generating Markdown index: {e}", "ERROR")
            return False
    
    def save_metadata(self, metadata: Dict) -> bool:
        """Save index metadata."""
        try:
            # Add generation details
            full_metadata = {
                **metadata,
                'formats_generated': ['json', 'csv', 'markdown'],
                'index_files': {
                    'json': str(self.json_index_file.relative_to(self.repo_root)),
                    'csv': str(self.csv_index_file.relative_to(self.repo_root)),
                    'markdown': str(self.markdown_index_file.relative_to(self.repo_root))
                }
            }
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(full_metadata, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            self.log(f"Error saving metadata: {e}", "ERROR")
            return False
    
    def generate_all_formats(self, force_rebuild: bool = False) -> bool:
        """Generate all index formats."""
        self.log("Starting multi-format index generation", "PROGRESS")
        
        # Load prompts
        prompts = self.load_consolidated_prompts()
        if not prompts:
            return False
        
        # Prepare standardized data
        entries, metadata = self.prepare_index_data(prompts)
        
        # Generate all formats
        success = True
        
        success &= self.generate_json_index(entries, metadata)
        success &= self.generate_csv_index(entries, metadata)  
        success &= self.generate_markdown_index(entries, metadata)
        success &= self.save_metadata(metadata)
        
        if success:
            self.log(f"Generated all index formats with {len(entries)} prompts", "SUCCESS")
        else:
            self.log("Some index formats failed to generate", "WARNING")
        
        return success
    
    def generate_specific_format(self, format_type: str) -> bool:
        """Generate a specific index format."""
        self.log(f"Generating {format_type.upper()} index only", "PROGRESS")
        
        # Load prompts
        prompts = self.load_consolidated_prompts()
        if not prompts:
            return False
        
        # Prepare standardized data
        entries, metadata = self.prepare_index_data(prompts)
        
        # Generate specific format
        if format_type == 'json':
            success = self.generate_json_index(entries, metadata)
        elif format_type == 'csv':
            success = self.generate_csv_index(entries, metadata)
        elif format_type == 'markdown':
            success = self.generate_markdown_index(entries, metadata)
        else:
            self.log(f"Unknown format type: {format_type}", "ERROR")
            return False
        
        # Update metadata
        if success:
            success &= self.save_metadata(metadata)
        
        return success


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Multi-Format Index Generator for System Prompt Library"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild of all index formats"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only generate JSON index"
    )
    parser.add_argument(
        "--csv-only",
        action="store_true",
        help="Only generate CSV index"
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only generate Markdown index"
    )
    
    args = parser.parse_args()
    
    # Get repository root (script is in maintenance-scripts/indexing/)
    repo_root = Path(__file__).parent.parent.parent
    
    # Create generator
    generator = MultiFormatIndexGenerator(repo_root)
    
    try:
        if args.json_only:
            success = generator.generate_specific_format('json')
        elif args.csv_only:
            success = generator.generate_specific_format('csv')
        elif args.markdown_only:
            success = generator.generate_specific_format('markdown')
        else:
            success = generator.generate_all_formats(args.force_rebuild)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        generator.log("Index generation interrupted by user", "WARNING")
        return 1
    except Exception as e:
        generator.log(f"Unexpected error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    exit(main())
