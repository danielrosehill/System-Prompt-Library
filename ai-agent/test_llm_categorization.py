#!/usr/bin/env python3
"""
Test script to demonstrate LLM-based categorization and tagging
"""

import json
import sys
from pathlib import Path
from categorizer import SystemPromptCategorizer

def test_llm_categorization():
    """Test LLM categorization on a few sample files"""
    
    # Initialize categorizer
    categorizer = SystemPromptCategorizer()
    
    # Test files
    test_files = [
        "system-prompts/json/10SoftwareRecs_270525.json",
        "system-prompts/json/AIAgentBuilders_270525.json",
        "system-prompts/json/ADBAssistant_270525.json"
    ]
    
    print("🤖 Testing LLM-based categorization and tagging\n")
    
    for file_path in test_files:
        if not Path(file_path).exists():
            print(f"❌ File not found: {file_path}")
            continue
            
        print(f"📄 Analyzing: {Path(file_path).name}")
        
        try:
            # Load file
            with open(file_path, 'r') as f:
                agent_data = json.load(f)
            
            agent_name = agent_data.get('agentname', 'Unknown')
            description = agent_data.get('description', 'No description')
            
            print(f"   Name: {agent_name}")
            print(f"   Current Description: {description[:100]}...")
            
            # Test LLM categorization
            print("   🧠 LLM Analysis:")
            category = categorizer._categorize_agent(agent_data)
            tags = categorizer._assign_tags(agent_data)
            
            print(f"   📂 Suggested Category: {category}")
            print(f"   🏷️  Suggested Tags: {', '.join(tags) if tags else 'None'}")
            
            # Test description generation if needed
            if not description or len(description.strip()) < 20:
                print("   ✍️  Generating new description...")
                new_desc = categorizer._generate_description(agent_data)
                print(f"   📝 Generated: {new_desc}")
            
            print()
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")

if __name__ == "__main__":
    # Change to repo root if needed
    if Path.cwd().name == "ai-agent":
        import os
        os.chdir("..")
    
    test_llm_categorization()
