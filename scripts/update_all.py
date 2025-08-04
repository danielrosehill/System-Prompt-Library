#!/usr/bin/env python3
"""
Master script to update both JSON consolidation and markdown index.

This script runs consolidate_prompts.py, generate_index_from_consolidated.py, and update_readme.py in sequence,
providing a single command to update all library indices and embed the index in the README.
The index is now generated from the consolidated JSON file for consistency and includes growth tracking.
"""

import subprocess
import sys
import argparse
from datetime import datetime


def run_command(command, description):
    """Run a command and handle its output."""
    print(f"🔄 {description}...")
    print(f"   Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Print stdout if there's any
        if result.stdout.strip():
            print(result.stdout)
        
        print(f"✅ {description} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Update both JSON consolidation and markdown index"
    )
    parser.add_argument(
        "--force-rebuild",
        action="store_true",
        help="Force rebuild of both indices, ignoring incremental updates"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only update JSON consolidation"
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only update markdown index and README"
    )
    parser.add_argument(
        "--json-output",
        help="Custom output path for consolidated JSON file"
    )
    parser.add_argument(
        "--markdown-output",
        help="Custom output path for markdown index file"
    )
    
    args = parser.parse_args()
    
    print("🚀 System Prompt Library - Update All Indices")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    success_count = 0
    total_tasks = 0
    
    # Update JSON consolidation
    if not args.markdown_only:
        total_tasks += 1
        json_command = ["python3", "consolidate_prompts.py"]
        
        if args.force_rebuild:
            json_command.append("--force-rebuild")
        
        if args.json_output:
            json_command.extend(["--output", args.json_output])
        
        if run_command(json_command, "JSON Consolidation"):
            success_count += 1
        else:
            print("⚠️  JSON consolidation failed, but continuing with markdown update...")
    
    print()  # Add spacing between tasks
    
    # Update markdown index
    if not args.json_only:
        total_tasks += 1
        markdown_command = ["python3", "generate_index_from_consolidated.py"]
        
        if args.force_rebuild:
            markdown_command.append("--force-rebuild")
        
        if args.markdown_output:
            markdown_command.extend(["--output", args.markdown_output])
        
        if run_command(markdown_command, "Markdown Index Generation"):
            success_count += 1
            
            # Update README with index content
            total_tasks += 1
            readme_command = ["python3", "update_readme.py"]
            
            if run_command(readme_command, "README Index Update"):
                success_count += 1
            else:
                print("⚠️  README update failed, but continuing...")
    
    print("=" * 60)
    print(f"📊 Summary: {success_count}/{total_tasks} tasks completed successfully")
    print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_tasks:
        print("🎉 All updates completed successfully!")
        return 0
    else:
        print("⚠️  Some updates failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())
