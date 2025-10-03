#!/usr/bin/env python3
"""
Growth Metrics Update Script for System Prompt Library

This script updates the growth_history.json file, regenerates the index
with the latest sparkline chart, AND generates the growth chart image
to reflect current library metrics.

Usage:
    python update_growth_metrics.py [--force-new-entry]
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle


class GrowthMetricsUpdater:
    """Updates growth metrics, sparkline, and generates growth chart."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.json_dir = repo_root / "system-prompts" / "json"
        self.consolidated_file = repo_root / "repo-data" / "consolidated_prompts.json"
        self.growth_history_file = repo_root / "repo-data" / "growth_history.json"
        # Correct path to markdown index
        self.index_file = repo_root / "index" / "index.md"
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
    
    def count_valid_prompts(self) -> int:
        """Count valid prompts from consolidated JSON or individual files."""
        # First try consolidated file
        if self.consolidated_file.exists():
            try:
                with open(self.consolidated_file, 'r', encoding='utf-8') as f:
                    prompts = json.load(f)
                total_count = len(prompts)
                self.log(f"Counted {total_count} prompts from consolidated file")
                return total_count
            except Exception as e:
                self.log(f"Error reading consolidated file: {e}", "WARNING")
        
        # Fallback to counting individual files
        if not self.json_dir.exists():
            self.log("JSON directory not found", "ERROR")
            return 0
            
        json_files = list(self.json_dir.glob("*.json"))
        total_count = 0
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
                    total_count += 1
            except Exception:
                continue
        
        self.log(f"Counted {total_count} prompts from {len(json_files)} individual files")
        return total_count
    
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
    
    def update_growth_history(self, current_count: int, force_new_entry: bool = False) -> bool:
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
            if force_new_entry or today_entry["count"] != current_count:
                # Update existing entry
                today_entry["count"] = current_count
                today_entry["updated"] = now
                self.log(f"Updated today's entry: {current_count} prompts")
            else:
                self.log(f"Today's entry already current: {current_count} prompts")
                return False
        else:
            # Add new entry
            new_entry = {
                "date": today,
                "count": current_count,
                "created": now
            }
            history["entries"].append(new_entry)
            self.log(f"Added new entry: {current_count} prompts for {today}")
        
        # Save updated history
        try:
            with open(self.growth_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.log(f"Error saving growth history: {e}", "ERROR")
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
            
            # Add milestone annotations for significant increases
            if len(counts) > 1:
                for i in range(1, len(counts)):
                    increase = counts[i] - counts[i-1]
                    if increase > 50:  # Significant increase
                        ax.annotate(f'+{increase}', (dates[i], counts[i]), 
                                   textcoords="offset points", xytext=(15,-15), 
                                   ha='center', fontsize=9, color='green', fontweight='bold',
                                   arrowprops=dict(arrowstyle='->', color='green', alpha=0.7))
            
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
    
    def update_index_sparkline(self, current_count: int) -> bool:
        """Update the index.md file with new sparkline and count."""
        if not self.index_file.exists():
            self.log("Index file not found", "ERROR")
            return False
        
        # Load growth history for sparkline
        history = self.load_growth_history()
        counts = [entry["count"] for entry in history["entries"]]
        sparkline = self.generate_sparkline(counts)
        
        try:
            # Read current index
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update sparkline and count
            lines = content.split('\n')
            updated_lines = []
            
            for line in lines:
                if line.startswith('📈 '):
                    # Update sparkline
                    updated_lines.append(f'📈 {sparkline}')
                elif line.startswith('**Total Prompts:**'):
                    # Update count and date
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    updated_lines.append(f'**Total Prompts:** {current_count} | **Last Updated:** {current_date}')
                elif '*Generated on' in line and 'from consolidated system prompts*' in line:
                    # Update generation date
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    updated_lines.append(f'*Generated on {current_date} from consolidated system prompts*')
                else:
                    updated_lines.append(line)
            
            # Write updated content
            with open(self.index_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(updated_lines))
            
            self.log(f"Updated index with sparkline: {sparkline} and count: {current_count}")
            return True
            
        except Exception as e:
            self.log(f"Error updating index: {e}", "ERROR")
            return False
    
    def run(self, force_new_entry: bool = False) -> bool:
        """Run the complete growth metrics update."""
        self.log("Starting growth metrics update", "PROGRESS")
        
        # Count current valid prompts
        current_count = self.count_valid_prompts()
        if current_count == 0:
            self.log("No valid prompts found", "ERROR")
            return False
        
        # Update growth history
        history_updated = self.update_growth_history(current_count, force_new_entry)
        
        # Generate growth chart
        chart_generated = self.generate_growth_chart()
        
        # Update index sparkline
        index_updated = self.update_index_sparkline(current_count)
        
        if history_updated or chart_generated or index_updated:
            self.log(f"Growth metrics update completed: {current_count} prompts", "SUCCESS")
            if chart_generated:
                self.log(f"Growth chart saved to: {self.chart_file}", "SUCCESS")
            return True
        else:
            self.log("No updates needed", "INFO")
            return True


def main():
    """Main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Update System Prompt Library growth metrics, sparkline, and chart"
    )
    parser.add_argument(
        "--force-new-entry",
        action="store_true",
        help="Force creation of new entry even if count hasn't changed"
    )
    
    args = parser.parse_args()
    
    # Get repository root (script is now in maintenance-scripts/indexing/)
    repo_root = Path(__file__).parent.parent.parent
    
    # Create updater and run
    updater = GrowthMetricsUpdater(repo_root)
    success = updater.run(args.force_new_entry)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
