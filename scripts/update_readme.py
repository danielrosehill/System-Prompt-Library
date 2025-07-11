#!/usr/bin/env python3
"""
Update README.md with content from index.md.

This script inserts the content from index.md into README.md between
special marker comments, allowing the index to be embedded in the README.
It also updates the generation date in the index content to the current date.
"""

import os
import re
from pathlib import Path
from datetime import datetime


def update_readme_with_index():
    """Update README.md with content from index.md."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    readme_path = repo_root / "README.md"
    index_path = repo_root / "index.md"
    
    # Check if both files exist
    if not readme_path.exists():
        print(f"❌ Error: README.md not found at {readme_path}")
        return False
        
    if not index_path.exists():
        print(f"❌ Error: index.md not found at {index_path}")
        return False
    
    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Read the index content
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
        
    # Update the generation date to the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    index_content = re.sub(
        r'\*Generated on \d{4}-\d{2}-\d{2}',
        f'*Generated on {current_date}',
        index_content
    )
    
    # Define the markers
    begin_marker = "<!-- BEGIN_INDEX_CONTENT -->"
    end_marker = "<!-- END_INDEX_CONTENT -->"
    
    # Check if markers exist in README
    if begin_marker not in readme_content or end_marker not in readme_content:
        print("❌ Error: Marker comments not found in README.md")
        print(f"Make sure {begin_marker} and {end_marker} exist in README.md")
        return False
    
    # Replace content between markers with index content
    pattern = f"{begin_marker}.*?{end_marker}"
    replacement = f"{begin_marker}\n{index_content}\n{end_marker}"
    
    # Use re.DOTALL to match across multiple lines
    updated_readme = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_readme)
    
    print(f"✅ Successfully updated {readme_path} with content from {index_path}")
    return True


def main():
    """Main function."""
    print("🔄 Updating README.md with index content...")
    
    success = update_readme_with_index()
    
    if success:
        print("🎉 README update completed successfully!")
        return 0
    else:
        print("⚠️ README update failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())
