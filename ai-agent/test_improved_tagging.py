#!/usr/bin/env python3
"""
Test improved tagging on specific examples
"""

import json
import sys
from pathlib import Path
from categorizer import SystemPromptCategorizer

def test_adhd_tagging():
    """Test improved tagging on ADHD Tech Advisor"""
    
    # Initialize categorizer with improved taxonomy
    categorizer = SystemPromptCategorizer()
    
    # Test ADHD Tech Advisor specifically
    test_file = "system-prompts/json/ADHDTechAdvisor_270525.json"
    
    if not Path(test_file).exists():
        print(f"❌ File not found: {test_file}")
        return
    
    print("🧠 Testing Improved LLM Tagging")
    print("=" * 50)
    
    try:
        # Load file
        with open(test_file, 'r') as f:
            agent_data = json.load(f)
        
        agent_name = agent_data.get('agentname', 'Unknown')
        description = agent_data.get('description', 'No description')
        
        print(f"📄 Agent: {agent_name}")
        print(f"📝 Description: {description}")
        print()
        
        # Test improved categorization
        print("🎯 LLM Categorization:")
        category = categorizer._categorize_agent(agent_data)
        print(f"   Category: {category}")
        print()
        
        # Test improved tagging
        print("🏷️  LLM Tagging (Improved):")
        tags = categorizer._assign_tags(agent_data)
        print(f"   Tags: {', '.join(tags) if tags else 'None'}")
        print()
        
        # Show what tags should be expected
        print("✅ Expected for ADHD Tech Advisor:")
        print("   Should include: adhd, mental-health, technology-guidance, accessibility")
        print("   Should NOT be: ai-tools, research, specialized (too generic)")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Change to repo root if needed
    if Path.cwd().name == "ai-agent":
        import os
        os.chdir("..")
    
    test_adhd_tagging()
