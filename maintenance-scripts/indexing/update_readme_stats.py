#!/usr/bin/env python3
"""
Update README.md with current system prompt count and growth visualization.

This script reads from growth_history.json and index_metadata.json to add
current statistics and a sparkline chart to the README header.
"""

import json
import re
import subprocess
import sys
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


def generate_growth_chart(repo_root: Path) -> bool:
    """Generate growth chart using the maintained chart generator."""
    try:
        chart_script = repo_root / "maintenance-scripts" / "indexing" / "generate_growth_chart.py"
        if not chart_script.exists():
            print("⚠️ Chart script not found at maintenance-scripts/indexing/generate_growth_chart.py")
            return False

        # Prefer system Python; virtualenv is optional
        result = subprocess.run(
            [sys.executable, str(chart_script)],
            cwd=str(repo_root),
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("⚠️ Chart generation stdout:\n" + result.stdout)
            print("⚠️ Chart generation stderr:\n" + result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ Chart generation failed: {e}")
        return False


def load_growth_data(repo_root: Path) -> tuple:
    """Load growth history and current metadata."""
    growth_file = repo_root / "repo-data" / "growth_history.json"
    # Prefer the generated index metadata in index/
    metadata_file = repo_root / "index" / "index_metadata.json"
    
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
        metadata = {"total_prompts": 0}
    
    return growth_data, metadata


def update_readme_with_stats(repo_root: Path):
    """Update README.md with current statistics and growth chart."""
    readme_file = repo_root / "README.md"
    
    if not readme_file.exists():
        print("❌ README.md not found")
        return False
    
    # Load data
    growth_data, metadata = load_growth_data(repo_root)
    
    # Try multiple keys for count/date for robustness
    current_count = (
        metadata.get("total_prompts")
        or metadata.get("prompt_count")
        or metadata.get("growth_data", {}).get("current_count")
        or 0
    )
    last_updated = metadata.get("last_updated") or metadata.get("generated_at", datetime.now().isoformat())
    
    # Parse the date for display
    try:
        update_date = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        formatted_date = update_date.strftime('%Y-%m-%d')
    except:
        formatted_date = datetime.now().strftime('%Y-%m-%d')
    
    # Generate growth chart (or reuse if already available)
    chart_generated = generate_growth_chart(repo_root)
    chart_path = repo_root / "images" / "growth_chart.png"
    
    # Get counts for fallback text
    counts = [entry["count"] for entry in growth_data.get("entries", [])]
    if not counts:
        counts = [current_count]
    
    # Create stats section with proper chart
    if chart_generated or chart_path.exists():
        chart_section = "![Growth Chart](images/growth_chart.png)"
    else:
        # Fallback to sparkline if chart generation fails
        chart_section = generate_sparkline(counts)
    
    # Create stats section
    stats_section = f"""
## Library Statistics

{chart_section}

**Total System Prompts:** {current_count:,} | **Last Updated:** {formatted_date}

*This library has grown from {counts[0] if counts else 0} to {counts[-1] if counts else current_count} prompts since tracking began*

"""
    
    # Read current README
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use markers to only update the statistics section, preserving manual edits
    stats_begin_marker = "<!-- BEGIN_STATS_SECTION -->"
    stats_end_marker = "<!-- END_STATS_SECTION -->"
    
    # Check if markers exist
    if stats_begin_marker in content and stats_end_marker in content:
        # Replace only the content between markers
        pattern = f"{stats_begin_marker}.*?{stats_end_marker}"
        replacement = f"{stats_begin_marker}\n{stats_section.strip()}\n{stats_end_marker}"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print("✅ Updated existing statistics section between markers")
    else:
        # Insert stats section with markers after the badges but before Table of Contents
        # Look for the pattern: badges -> image -> Table of Contents
        toc_pattern = r'(!\[alt text\].*?\n\n)(## Table of Contents)'
        
        if re.search(toc_pattern, content, re.DOTALL):
            stats_with_markers = f"{stats_begin_marker}\n{stats_section.strip()}\n{stats_end_marker}\n\n"
            new_content = re.sub(
                toc_pattern, 
                r'\1' + stats_with_markers + r'\2', 
                content, 
                flags=re.DOTALL
            )
            print("✅ Added new statistics section with markers before Table of Contents")
        else:
            # Fallback: add after the first heading
            lines = content.split('\n')
            insert_pos = 1
            for i, line in enumerate(lines):
                if line.startswith('##') and 'Table of Contents' in line:
                    insert_pos = i
                    break
            
            stats_with_markers = f"{stats_begin_marker}\n{stats_section.strip()}\n{stats_end_marker}"
            lines.insert(insert_pos, stats_with_markers)
            new_content = '\n'.join(lines)
            print("✅ Added new statistics section with markers (fallback method)")
    
    # Write updated content
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"📊 Updated README with {current_count:,} prompts and growth chart")
    return True


def main():
    """Main function."""
    # Script resides in maintenance-scripts/indexing/, so repo root is three levels up
    repo_root = Path(__file__).parent.parent.parent
    
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
