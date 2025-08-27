#!/usr/bin/env python3
"""
Generate a proper time-series chart showing System Prompt Library growth over time.

Creates a line chart with:
- X-axis: Time (dates)
- Y-axis: Number of system prompts
- Saves as PNG image for embedding in README
"""

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pathlib import Path
import pandas as pd


def generate_growth_chart(repo_root: Path, output_file: str = "images/growth_chart.png"):
    """Generate and save a growth chart from growth_history.json."""
    
    growth_file = repo_root / "growth_history.json"
    output_path = repo_root / output_file
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not growth_file.exists():
        print("❌ growth_history.json not found")
        return False
    
    # Load growth data
    with open(growth_file, 'r') as f:
        growth_data = json.load(f)
    
    entries = growth_data.get("entries", [])
    if len(entries) < 2:
        print("❌ Need at least 2 data points to create a meaningful chart")
        return False
    
    # Extract dates and counts
    dates = []
    counts = []
    
    for entry in entries:
        # Try different date field names
        date_str = entry.get("date") or entry.get("updated") or entry.get("created")
        if date_str:
            # Parse date (handle both date-only and ISO timestamp formats)
            try:
                if 'T' in date_str:
                    # ISO timestamp format
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    # Date-only format
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                
                dates.append(date_obj)
                counts.append(entry["count"])
            except ValueError as e:
                print(f"⚠️ Skipping invalid date: {date_str} - {e}")
                continue
    
    if len(dates) < 2:
        print("❌ Not enough valid date entries found")
        return False
    
    # Create the chart
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the line chart
    ax.plot(dates, counts, marker='o', linewidth=2.5, markersize=6, 
            color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='white', markeredgewidth=1.5)
    
    # Customize the chart
    ax.set_title('System Prompt Library Growth Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of System Prompts', fontsize=12, fontweight='bold')
    
    # Format dates on x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//6)))  # Show ~6 date labels
    plt.xticks(rotation=45)
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Set y-axis to start from a reasonable minimum
    min_count = min(counts)
    max_count = max(counts)
    padding = (max_count - min_count) * 0.1
    ax.set_ylim(min_count - padding, max_count + padding)
    
    # Add value labels on data points
    for date, count in zip(dates, counts):
        ax.annotate(f'{count}', (date, count), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=9, fontweight='bold')
    
    # Improve layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Growth chart saved to {output_file}")
    print(f"📊 Chart shows {len(dates)} data points from {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")
    print(f"📈 Growth: {min_count} → {max_count} prompts ({max_count - min_count:+d})")
    
    return True


def main():
    """Main function."""
    repo_root = Path(__file__).parent.parent
    
    print("📊 Generating System Prompt Library growth chart...")
    
    # Check if matplotlib is available
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("❌ matplotlib is required. Install with: pip install matplotlib")
        return 1
    
    success = generate_growth_chart(repo_root)
    
    if success:
        print("✅ Growth chart generation completed successfully")
    else:
        print("❌ Failed to generate growth chart")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
