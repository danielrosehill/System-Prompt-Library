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
    """Generate markdown index with H2 headers for each system prompt."""
    
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
        # New format: object with metadata and prompts array
        prompts_data = consolidated_data['prompts']
    else:
        print(f"❌ Error: Unrecognized consolidated file format")
        return None
    
    print(f"📊 Processing {len(prompts_data)} prompts from consolidated file...")
    
    valid_prompts = []
    
    for prompt in prompts_data:
        # Get agent name (handle various field names)
        agent_name = (
            prompt.get('agentname') or 
            prompt.get('agent_name') or 
            prompt.get('name', 'Unknown')
        ).strip()
        
        # Get description
        description = (
            prompt.get('description') or 
            prompt.get('desc', 'No description available')
        ).strip()
        
        # Skip if no agent name
        if not agent_name or agent_name == 'Unknown':
            continue
            
        # Create relative link to JSON file
        filename = prompt.get('_filename', '')
        if filename:
            relative_link = f"system-prompts/json/{filename}"
        else:
            # Fallback: try to construct filename from agent name
            safe_name = agent_name.replace(' ', '').replace('/', '-')
            relative_link = f"system-prompts/json/{safe_name}.json"
        
        # Get ChatGPT link if available
        chatgpt_link = prompt.get('chatgptlink') or prompt.get('chatgpt-url', '')
        
        # Get boolean fields for checkboxes (handle both string and boolean values)
        def parse_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() == 'true'
            return False
        
        is_agent = parse_bool(prompt.get('is-agent', False))
        is_single_turn = parse_bool(prompt.get('is-single-turn', 'false'))
        structured_output = parse_bool(prompt.get('structured-output-generation', 'false'))
        image_generation = parse_bool(prompt.get('image-generation', 'false'))
        data_utility = parse_bool(prompt.get('data-utility', 'false'))
        
        valid_prompts.append({
            'agent_name': agent_name,
            'description': description,
            'link': relative_link,
            'chatgpt_link': chatgpt_link,
            'is_agent': is_agent,
            'is_single_turn': is_single_turn,
            'structured_output': structured_output,
            'image_generation': image_generation,
            'data_utility': data_utility
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

---

"""
    
    # Helper function to create checkbox
    def checkbox(value):
        return "☑️" if value else "☐"
    
    for prompt in valid_prompts:
        agent_name = prompt['agent_name']
        description = prompt['description']
        
        # Start with H2 header
        markdown_content += f"## {agent_name}\n\n"
        
        # Add description
        markdown_content += f"{description}\n\n"
        
        # Add capabilities/features with checkboxes
        markdown_content += "**Features:**\n\n"
        markdown_content += f"- {checkbox(prompt['is_agent'])} Agent-based interaction\n"
        markdown_content += f"- {checkbox(prompt['is_single_turn'])} Single-turn conversation\n"
        markdown_content += f"- {checkbox(prompt['structured_output'])} Structured output generation\n"
        markdown_content += f"- {checkbox(prompt['image_generation'])} Image generation\n"
        markdown_content += f"- {checkbox(prompt['data_utility'])} Data utility functions\n\n"
        
        # Add links
        markdown_content += "**Links:**\n\n"
        markdown_content += f"- 📄 [View JSON]({prompt['link']})\n"
        
        if prompt['chatgpt_link']:
            markdown_content += f"- 🤖 [Try in ChatGPT]({prompt['chatgpt_link']})\n"
        
        markdown_content += "\n---\n\n"
    
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
