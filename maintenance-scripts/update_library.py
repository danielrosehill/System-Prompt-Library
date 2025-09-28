#!/usr/bin/env python3
"""
System Prompt Library Master Update Script

This single script handles all library maintenance tasks in the correct order:
1. Consolidates individual JSON files into consolidated_prompts.json
2. Generates index.md from consolidated data with growth tracking
3. Updates growth_history.json and generates growth chart
4. Updates README.md with the latest index content
5. Provides comprehensive logging and error handling

Usage:
    python update_library.py [options]
    
Options:
    --force-rebuild     Force rebuild of all components
    --consolidate-only  Only run consolidation step
    --index-only        Only run index generation
    --growth-only       Only run growth metrics update
    --readme-only       Only run README update
"""

import json
import os
import argparse
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
# Optional matplotlib imports (graceful degradation if not installed)
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except Exception:  # ImportError or other backend issues
    plt = None
    mdates = None


class SystemPromptLibraryUpdater:
    """Master updater for the System Prompt Library."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        # Source of truth for individual prompt JSONs
        self.json_dir = repo_root / "system-prompts" / "json"
        self.consolidated_file = repo_root / "repo-data" / "consolidated_prompts.json"
        self.consolidated_metadata_file = repo_root / "repo-data" / "consolidated_prompts.metadata.json"
        self.index_file = repo_root / "index" / "index.md"
        self.index_metadata_file = repo_root / "repo-data" / "index_metadata.json"
        self.growth_history_file = repo_root / "repo-data" / "growth_history.json"
        self.readme_file = repo_root / "README.md"
        self.images_dir = repo_root / "images"
        self.chart_file = self.images_dir / "growth_chart.png"
        
        # Ensure images directory exists
        self.images_dir.mkdir(exist_ok=True)
        
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
    
    def consolidate_prompts(self, force_rebuild: bool = False) -> Tuple[bool, int, int]:
        """Consolidate individual JSON files into a single consolidated file."""
        self.log("Starting JSON consolidation", "PROGRESS")
        
        if not self.json_dir.exists():
            self.log("JSON directory not found", "ERROR")
            return False, 0, 0
        
        json_files = [
            p for p in self.json_dir.glob("*.json")
            if not p.name.startswith("consolidated_prompts")
        ]
        self.log(f"Found {len(json_files)} JSON files to process")
        
        # Load existing metadata
        metadata = {"file_hashes": {}, "last_updated": "", "stats": {}}
        if self.consolidated_metadata_file.exists() and not force_rebuild:
            try:
                with open(self.consolidated_metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            except Exception:
                pass
        
        consolidated_prompts = []
        processed_files = 0
        new_hashes = {}
        
        # Always load all prompt JSONs so consolidated file is complete
        for json_file in json_files:
            try:
                current_hash = self.calculate_file_hash(json_file)
                new_hashes[json_file.name] = current_hash
                # Process the file
                with open(json_file, 'r', encoding='utf-8') as f:
                    try:
                        prompt_data = json.load(f)
                        # Store original filename for reference
                        prompt_data['_original_filename'] = json_file.name
                        consolidated_prompts.append(prompt_data)
                        processed_files += 1
                    except json.JSONDecodeError as e:
                        self.log(f"Invalid JSON in {json_file.name}: {e}", "WARNING")
                        continue
                        
            except Exception as e:
                self.log(f"Error processing {json_file.name}: {e}", "WARNING")
                continue
        
        # We no longer rely on incremental merge; always write full set
        
        # Sort prompts alphabetically by agent name
        consolidated_prompts.sort(key=lambda x: (x.get('agent_name') or '').lower())
        
        # Save consolidated file
        with open(self.consolidated_file, 'w', encoding='utf-8') as f:
            json.dump(consolidated_prompts, f, indent=2, ensure_ascii=False)
        
        # Update metadata
        metadata.update({
            "file_hashes": new_hashes,
            "last_updated": datetime.now().isoformat(),
            "stats": {
                "total_files": len(json_files),
                "valid_prompts": len(consolidated_prompts),
                "processed_files": processed_files
            }
        })
        
        with open(self.consolidated_metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Also mirror consolidated outputs to system-prompts/json for convenience
        try:
            mirror_dir = self.repo_root / "system-prompts" / "json"
            mirror_dir.mkdir(parents=True, exist_ok=True)
            mirror_consolidated = mirror_dir / "consolidated_prompts.json"
            mirror_metadata = mirror_dir / "consolidated_prompts.metadata.json"
            with open(mirror_consolidated, 'w', encoding='utf-8') as f:
                json.dump(consolidated_prompts, f, indent=2, ensure_ascii=False)
            with open(mirror_metadata, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            self.log("Mirrored consolidated files to system-prompts/json", "INFO")
        except Exception as e:
            self.log(f"Could not mirror consolidated files: {e}", "WARNING")
        
        self.log(f"Consolidated {len(consolidated_prompts)} prompts from {len(json_files)} files", "SUCCESS")
        
        return True, len(consolidated_prompts), processed_files
    
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
    
    def update_growth_history(self, current_count: int) -> bool:
        """Update growth history with current count."""
        history = self.load_growth_history()
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().isoformat()
        
        # Check if we already have an entry for today
        today_entry = None
        for entry in history["entries"]:
            if entry["date"] == today:
                today_entry = entry
                break
        
        if today_entry:
            if today_entry["count"] != current_count:
                # Update existing entry
                today_entry["count"] = current_count
                today_entry["updated"] = now
                self.log(f"Updated today's growth entry: {current_count} prompts")
                updated = True
            else:
                updated = False
        else:
            # Add new entry
            new_entry = {
                "date": today,
                "count": current_count,
                "created": now
            }
            history["entries"].append(new_entry)
            self.log(f"Added new growth entry: {current_count} prompts for {today}")
            updated = True
        
        if updated:
            # Save updated history
            try:
                with open(self.growth_history_file, 'w', encoding='utf-8') as f:
                    json.dump(history, f, indent=2, ensure_ascii=False)
                return True
            except Exception as e:
                self.log(f"Error saving growth history: {e}", "ERROR")
                return False
        
        return False
    
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
    
    def generate_growth_chart(self) -> bool:
        """Generate the growth chart image."""
        # If matplotlib not available, skip gracefully
        if plt is None or mdates is None:
            self.log("matplotlib not available; skipping growth chart", "WARNING")
            return False
        history = self.load_growth_history()
        
        if not history["entries"]:
            self.log("No growth history data available", "WARNING")
            return False
        
        try:
            # Prepare data
            dates = []
            counts = []
            
            for entry in history["entries"]:
                date_obj = datetime.strptime(entry["date"], '%Y-%m-%d')
                dates.append(date_obj)
                counts.append(entry["count"])
            
            # Create the plot
            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot the main line
            ax.plot(dates, counts, 'o-', linewidth=3, markersize=8, 
                   color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=2)
            
            # Fill area under the curve
            ax.fill_between(dates, counts, alpha=0.3, color='#2E86AB')
            
            # Customize the plot
            ax.set_title('System Prompt Library Growth', fontsize=20, fontweight='bold', pad=20)
            ax.set_xlabel('Date', fontsize=14, fontweight='bold')
            ax.set_ylabel('Number of Prompts', fontsize=14, fontweight='bold')
            
            # Format x-axis - show only months and years
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.xticks(rotation=0)
            
            # Add grid
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Add value labels on points
            for i, (date, count) in enumerate(zip(dates, counts)):
                ax.annotate(f'{count}', (date, count), 
                           textcoords="offset points", xytext=(0,15), 
                           ha='center', fontsize=10, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
            
            # Style improvements
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CCCCCC')
            ax.spines['bottom'].set_color('#CCCCCC')
            
            # Set y-axis to start from a reasonable minimum
            y_min = max(0, min(counts) - 50)
            y_max = max(counts) + 50
            ax.set_ylim(y_min, y_max)
            
            # Add summary box
            total_growth = counts[-1] - counts[0] if len(counts) > 1 else 0
            days_tracked = len(counts)
            avg_per_day = total_growth / max(1, days_tracked - 1) if days_tracked > 1 else 0
            
            summary_text = f"Total Growth: +{total_growth}\nDays Tracked: {days_tracked}\nAvg/Day: {avg_per_day:.1f}"
            ax.text(0.02, 0.98, summary_text, transform=ax.transAxes, 
                   verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", 
                   facecolor='lightblue', alpha=0.8), fontsize=10)
            
            # Tight layout and save
            plt.tight_layout()
            plt.savefig(self.chart_file, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            plt.close()
            
            self.log(f"Generated growth chart: {self.chart_file}")
            return True
            
        except Exception as e:
            self.log(f"Error generating growth chart: {e}", "ERROR")
            return False
    
    def generate_index(self) -> bool:
        """Generate multi-format index files using the new index generator."""
        self.log("Starting multi-format index generation", "PROGRESS")
        
        # Import and use the new multi-format index generator
        import sys
        indexing_dir = self.repo_root / "maintenance-scripts" / "indexing"
        sys.path.insert(0, str(indexing_dir))
        
        try:
            from generate_multi_format_index import MultiFormatIndexGenerator
            
            # Create generator and run it
            generator = MultiFormatIndexGenerator(self.repo_root)
            success = generator.generate_all_formats()
            
            if success:
                # Update growth history using the total prompt count
                if self.consolidated_file.exists():
                    with open(self.consolidated_file, 'r', encoding='utf-8') as f:
                        prompts = json.load(f)
                    prompt_count = len(prompts)
                    self.update_growth_history(prompt_count)
                    
                    # Generate growth chart
                    self.generate_growth_chart()
                    
                    self.log(f"Generated multi-format index with {prompt_count} prompts", "SUCCESS")
                else:
                    self.log("Consolidated file not found for growth tracking", "WARNING")
                
                return True
            else:
                self.log("Multi-format index generation failed", "ERROR")
                return False
                
        except ImportError as e:
            self.log(f"Could not import multi-format index generator: {e}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error in multi-format index generation: {e}", "ERROR")
            return False
        finally:
            # Clean up sys.path
            if str(indexing_dir) in sys.path:
                sys.path.remove(str(indexing_dir))
    
    def update_readme(self) -> bool:
        """Update README.md with latest index content."""
        self.log("Starting README update", "PROGRESS")
        
        if not self.index_file.exists():
            self.log("Index file not found", "ERROR")
            return False
        
        if not self.readme_file.exists():
            self.log("README file not found", "ERROR")
            return False
        
        try:
            # Read current README and index
            with open(self.readme_file, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            with open(self.index_file, 'r', encoding='utf-8') as f:
                index_content = f.read()
            
            # Find the table of contents section and replace everything after it
            toc_pattern = r'(### Table of Contents.*?\n)'
            match = re.search(toc_pattern, readme_content, re.DOTALL)
            
            if match:
                # Keep everything up to and including the TOC
                readme_before_toc = readme_content[:match.end()]
                
                # Add the index content (skip the first line "# System Prompt Index")
                index_lines = index_content.split('\n')[1:]  # Skip first line
                updated_readme = readme_before_toc + '\n'.join(index_lines)
                
                # Write updated README
                with open(self.readme_file, 'w', encoding='utf-8') as f:
                    f.write(updated_readme)
                
                self.log("Updated README with latest index content", "SUCCESS")
                return True
            else:
                self.log("Could not find Table of Contents section in README", "WARNING")
                return False
                
        except Exception as e:
            self.log(f"Error updating README: {e}", "ERROR")
            return False
    
    def run_all(self, force_rebuild: bool = False) -> bool:
        """Run all update steps in the correct order."""
        self.log("Starting complete library update", "PROGRESS")
        
        # Step 1: Consolidate prompts
        success, total_prompts, processed = self.consolidate_prompts(force_rebuild)
        if not success:
            return False
        
        # Step 2: Generate index (includes growth tracking and chart)
        success = self.generate_index()
        if not success:
            return False
        
        # Step 3: Update README
        success = self.update_readme()
        if not success:
            self.log("README update failed, but continuing", "WARNING")
        
        self.log(f"Complete library update finished: {total_prompts} prompts", "SUCCESS")
        return True


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="System Prompt Library Master Update Script"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild of all components"
    )
    parser.add_argument(
        "--consolidate-only",
        action="store_true",
        help="Only run consolidation step"
    )
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Only run index generation"
    )
    parser.add_argument(
        "--growth-only",
        action="store_true",
        help="Only run growth metrics update"
    )
    parser.add_argument(
        "--readme-only",
        action="store_true",
        help="Only run README update"
    )
    
    args = parser.parse_args()
    
    # Get repository root (script is now in maintenance-scripts/)
    repo_root = Path(__file__).parent.parent
    
    # Create updater
    updater = SystemPromptLibraryUpdater(repo_root)
    
    try:
        if args.consolidate_only:
            success, _, _ = updater.consolidate_prompts(args.force_rebuild)
        elif args.index_only:
            success = updater.generate_index()
        elif args.growth_only:
            # Load consolidated file to get current count
            if updater.consolidated_file.exists():
                with open(updater.consolidated_file, 'r') as f:
                    prompts = json.load(f)
                current_count = len([p for p in prompts if p.get('agent_name')])
                updater.update_growth_history(current_count)
                success = updater.generate_growth_chart()
            else:
                updater.log("Consolidated file not found for growth update", "ERROR")
                success = False
        elif args.readme_only:
            success = updater.update_readme()
        else:
            success = updater.run_all(args.force_rebuild)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        updater.log("Update interrupted by user", "WARNING")
        return 1
    except Exception as e:
        updater.log(f"Unexpected error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    exit(main())
