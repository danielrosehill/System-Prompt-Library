#!/usr/bin/env python3
"""
Update README.md with current system prompt count and growth visualization.

This script reads from growth_history.json and index_metadata.json to add
current statistics and a sparkline chart to the README header.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def generate_sparkline(counts: List[int]) -> str:
    """Generate a sparkline chart from count data."""
    if len(counts) < 2:
        return "📈 ▁"
    
    min_val = min(counts)
    max_val = max(counts)
    
    if min_val == max_val:
        return "📈 " + "▄" * len(counts)
    
    # Normalize to 0-7 range for Unicode blocks
    normalized = []
    for count in counts:
        norm = int(7 * (count - min_val) / (max_val - min_val))
        normalized.append(norm)
    
    # Unicode block characters for sparkline
    blocks = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
    sparkline = "📈 " + "".join(blocks[n] for n in normalized)
    
    return sparkline


def load_growth_data(repo_root: Path) -> tuple:
    """Load growth history and current metadata."""
    growth_file = repo_root / "growth_history.json"
    metadata_file = repo_root / "index_metadata.json"
    
    # Load growth history
    if growth_file.exists():
        with open(growth_file, 'r') as f:
            growth_data = json.load(f)
    else:
        growth_data = {"entries": []}
    
    # Load current metadata
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {"prompt_count": 0}
    
    return growth_data, metadata


def update_readme_with_stats(repo_root: Path):
    """Update README.md with current statistics and growth chart."""
    readme_file = repo_root / "README.md"
    
    if not readme_file.exists():
        print("❌ README.md not found")
        return False
    
    # Load data
    growth_data, metadata = load_growth_data(repo_root)
    
    current_count = metadata.get("prompt_count", 0)
    last_updated = metadata.get("generated_at", datetime.now().isoformat())
    
    # Parse the date for display
    try:
        update_date = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        formatted_date = update_date.strftime('%Y-%m-%d')
    except:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate sparkline from growth history
    counts = [entry["count"] for entry in growth_data.get("entries", [])]
    if not counts:
        counts = [current_count]
    
    sparkline = generate_sparkline(counts)
    
    # Create stats section
    stats_section = f"""
## 📊 Library Statistics

{sparkline}

**Total System Prompts:** {current_count:,} | **Last Updated:** {formatted_date}

*This library has grown from {counts[0] if counts else 0} to {current_count} prompts since tracking began*

"""
    
    # Read current README
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if stats section already exists
    stats_pattern = r'## 📊 Library Statistics.*?(?=##|\Z)'
    
    if re.search(stats_pattern, content, re.DOTALL):
        # Replace existing stats section
        new_content = re.sub(stats_pattern, stats_section.strip() + '\n\n', content, flags=re.DOTALL)
        print("✅ Updated existing statistics section")
    else:
        # Insert stats section after the badges but before Table of Contents
        # Look for the pattern: badges -> image -> Table of Contents
        toc_pattern = r'(!\[alt text\].*?\n\n)(## Table of Contents)'
        
        if re.search(toc_pattern, content, re.DOTALL):
            new_content = re.sub(
                toc_pattern, 
                r'\1' + stats_section + r'\2', 
                content, 
                flags=re.DOTALL
            )
            print("✅ Added new statistics section before Table of Contents")
        else:
            # Fallback: add after the first heading
            lines = content.split('\n')
            insert_pos = 1
            for i, line in enumerate(lines):
                if line.startswith('##') and 'Table of Contents' in line:
                    insert_pos = i
                    break
            
            lines.insert(insert_pos, stats_section.strip())
            new_content = '\n'.join(lines)
            print("✅ Added new statistics section (fallback method)")
    
    # Write updated content
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"📊 Updated README with {current_count:,} prompts and growth chart")
    return True


def main():
    """Main function."""
    repo_root = Path(__file__).parent.parent
    
    print("🚀 Updating README with library statistics...")
    success = update_readme_with_stats(repo_root)
    
    if success:
        print("✅ README statistics update completed successfully")
    else:
        print("❌ Failed to update README statistics")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
