#!/usr/bin/env python3
"""
Generate markdown index table from consolidated prompts JSON file.

This script creates an index.md file from the consolidated_prompts.json file,
ensuring consistency and tracking growth metrics over time.
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import hashlib


def load_growth_history(history_file):
    """Load existing growth history."""
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"entries": []}


def save_growth_history(history_file, history):
    """Save growth history."""
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, default=str)


def update_growth_history(history_file, prompt_count):
    """Update growth history with current count."""
    history = load_growth_history(history_file)
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Check if we already have an entry for today
    today_entry = None
    for entry in history["entries"]:
        if entry["date"] == current_date:
            today_entry = entry
            break
    
    if today_entry:
        # Update today's count
        today_entry["count"] = prompt_count
        today_entry["updated"] = datetime.now().isoformat()
    else:
        # Add new entry
        history["entries"].append({
            "date": current_date,
            "count": prompt_count,
            "updated": datetime.now().isoformat()
        })
    
    # Keep only last 365 days
    history["entries"] = history["entries"][-365:]
    
    save_growth_history(history_file, history)
    return history


def generate_growth_chart(history):
    """Generate a simple text-based growth chart."""
    if len(history["entries"]) < 2:
        return "📈 Growth tracking started - check back soon for trends!"
    
    entries = history["entries"]
    latest = entries[-1]
    previous = entries[-2] if len(entries) > 1 else entries[0]
    
    # Calculate growth
    growth = latest["count"] - previous["count"]
    growth_sign = "📈" if growth > 0 else "📊" if growth == 0 else "📉"
    
    # Get some historical points
    chart_data = []
    if len(entries) >= 30:
        # Show last 30 days
        chart_data = entries[-30:]
        period = "30 days"
    elif len(entries) >= 7:
        # Show last 7 days
        chart_data = entries[-7:]
        period = "7 days"
    else:
        chart_data = entries
        period = f"{len(entries)} days"
    
    # Simple sparkline-style representation
    counts = [entry["count"] for entry in chart_data]
    min_count = min(counts)
    max_count = max(counts)
    
    if max_count == min_count:
        sparkline = "▬" * len(counts)
    else:
        # Normalize to 0-7 range for simple bar chart
        normalized = []
        for count in counts:
            norm = int(((count - min_count) / (max_count - min_count)) * 7)
            normalized.append(norm)
        
        # Convert to simple bar chart
        bars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        sparkline = "".join(bars[n] for n in normalized)
    
    return f"""📊 **Growth Metrics** ({period}): {sparkline}
- Current: **{latest['count']} prompts**
- Change: {growth_sign} **{abs(growth)} prompts** since {previous['date']}
- Range: {min_count} - {max_count} prompts"""


def generate_index_from_consolidated(consolidated_file, output_file=None, growth_history_file=None):
    """Generate markdown index table from consolidated JSON file."""
    
    # Load consolidated prompts
    try:
        with open(consolidated_file, 'r', encoding='utf-8') as f:
            consolidated_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading consolidated file: {e}")
        return None
    
    # Handle different consolidated file structures
    if isinstance(consolidated_data, list):
        # Old format: direct list of prompts
        prompts_data = consolidated_data
    elif isinstance(consolidated_data, dict) and 'prompts' in consolidated_data:
        # New format: object with metadata and prompts
        prompts_data = consolidated_data['prompts']
    else:
        print(f"❌ Error: Unexpected consolidated file structure: {type(consolidated_data)}")
        print(f"Available keys: {list(consolidated_data.keys()) if isinstance(consolidated_data, dict) else 'Not a dict'}")
        return None
    
    if not isinstance(prompts_data, list):
        print(f"❌ Error: Expected list of prompts, got {type(prompts_data)}")
        return None
    
    # Filter valid prompts (those with required fields)
    valid_prompts = []
    for prompt in prompts_data:
        if isinstance(prompt, dict):
            agent_name = (prompt.get('agentname') or prompt.get('agent-name', '')).strip()
            description = (prompt.get('description') or prompt.get('agent-description', '')).strip()
            
            if agent_name and description:
                # Create relative link to JSON file
                filename = prompt.get('_filename', '')
                if filename:
                    relative_link = f"system-prompts/json/{filename}"
                else:
                    # Fallback: try to construct filename from agent name
                    safe_name = agent_name.replace(' ', '').replace('/', '_').replace('\\', '_')
                    relative_link = f"system-prompts/json/{safe_name}.json"
                
                # Get ChatGPT link if available
                chatgpt_link = prompt.get('chatgptlink') or prompt.get('chatgpt-url', '')
                
                valid_prompts.append({
                    'agent_name': agent_name,
                    'description': description,
                    'link': relative_link,
                    'chatgpt_link': chatgpt_link
                })
    
    # Sort prompts alphabetically by agent name
    valid_prompts.sort(key=lambda x: x['agent_name'].lower())
    
    # Update growth history
    if growth_history_file:
        history = update_growth_history(growth_history_file, len(valid_prompts))
        growth_chart = generate_growth_chart(history)
    else:
        growth_chart = f"📊 **{len(valid_prompts)} system prompts** available"
    
    # Generate markdown content
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M UTC')
    
    markdown_content = f"""# System Prompt Library Index

{growth_chart}

*Last updated: {current_date} at {current_time} | Generated from consolidated_prompts.json*

| Agent Name | Description | CustomGPT |
|------------|-------------|----------|
"""
    
    for prompt in valid_prompts:
        # Escape pipe characters in content to avoid breaking the table
        agent_name = prompt['agent_name'].replace('|', '\\|')
        description = prompt['description'].replace('|', '\\|')
        
        # Truncate description if too long
        if len(description) > 150:
            description = description[:147] + "..."
        
        # Create agent name with link to JSON file
        agent_name_with_link = f"[{agent_name}]({prompt['link']})"
        
        # Add CustomGPT badge if available
        customgpt_column = ""
        if prompt['chatgpt_link']:
            customgpt_column = f"[![CustomGPT](https://img.shields.io/badge/CustomGPT-Available-green)]({prompt['chatgpt_link']})"
        
        markdown_content += f"| {agent_name_with_link} | {description} | {customgpt_column} |\n"
    
    # Write the index file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n✅ Index generated successfully from consolidated file!")
    print(f"📊 Total valid prompts: {len(valid_prompts)}")
    print(f"📁 Output file: {output_file}")
    print(f"📈 Growth tracking: {'enabled' if growth_history_file else 'disabled'}")
    
    return output_file


def main():
    """Main function with command line argument parsing."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    parser = argparse.ArgumentParser(
        description="Generate markdown index table from consolidated prompts JSON file"
    )
    parser.add_argument(
        "--consolidated-file",
        default=str(repo_root / "consolidated_prompts.json"),
        help="Consolidated prompts JSON file (default: ../consolidated_prompts.json)"
    )
    parser.add_argument(
        "--output",
        default=str(repo_root / "index.md"),
        help="Output file name (default: ../index.md)"
    )
    parser.add_argument(
        "--growth-history",
        default=str(repo_root / "growth_history.json"),
        help="Growth history file (default: ../growth_history.json)"
    )
    parser.add_argument(
        "--no-growth-tracking",
        action="store_true",
        help="Disable growth tracking"
    )
    
    args = parser.parse_args()
    
    # Check if consolidated file exists
    if not os.path.exists(args.consolidated_file):
        print(f"❌ Error: Consolidated file '{args.consolidated_file}' not found!")
        return 1
    
    growth_file = None if args.no_growth_tracking else args.growth_history
    
    try:
        generate_index_from_consolidated(args.consolidated_file, args.output, growth_file)
        return 0
    except Exception as e:
        print(f"❌ Error generating index: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
