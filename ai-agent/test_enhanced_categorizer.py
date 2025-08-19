#!/usr/bin/env python3
"""
Test the enhanced categorizer with comprehensive tagging and enrichment
"""

import json
import sys
from pathlib import Path

# Add the ai-agent directory to the path
sys.path.append(str(Path(__file__).parent))

from categorizer import SystemPromptCategorizer

def test_enhanced_categorizer():
    """Test the enhanced categorizer on a sample file"""
    
    # Initialize categorizer
    categorizer = SystemPromptCategorizer()
    
    # Test with ADHD Tech Advisor (should get rich domain-specific tags)
    test_file = Path("../system-prompts/json/ADHDTechAdvisor_270525.json")
    
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return
    
    print("🧪 Testing Enhanced Categorizer with Comprehensive Tagging")
    print("=" * 60)
    
    # Load test data
    with open(test_file, 'r') as f:
        agent_data = json.load(f)
    
    print(f"📄 Testing with: {agent_data.get('agentname', 'Unknown')}")
    print(f"📝 Description: {agent_data.get('description', 'No description')[:100]}...")
    print()
    
    # Test categorization
    print("🏷️ Testing Categorization:")
    category = categorizer._categorize_agent(agent_data)
    print(f"   Category: {category}")
    print()
    
    # Test tagging with comprehensive taxonomy
    print("🏷️ Testing Comprehensive Tagging:")
    tags = categorizer._assign_tags(agent_data)
    print(f"   Tags ({len(tags)}): {', '.join(tags)}")
    print()
    
    # Test capability detection
    print("⚙️ Testing Capability Detection:")
    capabilities = categorizer._detect_capabilities(agent_data)
    detected_caps = [k for k, v in capabilities.items() if v]
    print(f"   Capabilities ({len(detected_caps)}): {', '.join(detected_caps)}")
    print()
    
    # Test requirement detection
    print("🔧 Testing Requirement Detection:")
    requirements = categorizer._detect_requirements(agent_data)
    detected_reqs = [k for k, v in requirements.items() if v]
    print(f"   Requirements ({len(detected_reqs)}): {', '.join(detected_reqs)}")
    print()
    
    # Test full enrichment creation
    print("🚀 Testing Full Enrichment Creation:")
    enrichment_data = categorizer._create_enrichment_data(agent_data)
    
    # Display key enrichment metrics
    analysis = enrichment_data.get("ai_enriched_analysis", {})
    quality = enrichment_data.get("ai_enriched_quality_metrics", {})
    
    print(f"   Complexity Score: {analysis.get('complexity_score', 'N/A')}/10")
    print(f"   Use Case Breadth: {analysis.get('use_case_breadth', 'N/A')}")
    print(f"   Clarity Score: {quality.get('prompt_clarity_score', 'N/A')}/10")
    print(f"   Completeness Score: {quality.get('completeness_score', 'N/A')}/10")
    print(f"   Target Audience: {', '.join(analysis.get('target_audience', []))}")
    print()
    
    # Show improvement suggestions
    suggestions = analysis.get('improvement_suggestions', [])
    if suggestions:
        print("💡 Improvement Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
        print()
    
    # Show quality issues
    issues = quality.get('quality_issues', [])
    if issues:
        print("⚠️ Quality Issues:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
    
    print("✅ Enhanced categorizer test completed!")
    print(f"📊 Total enrichment fields: {len(enrichment_data)}")
    
    # Save sample enrichment for inspection
    output_file = Path("sample_enhanced_enrichment.json")
    with open(output_file, 'w') as f:
        json.dump(enrichment_data, f, indent=2)
    print(f"💾 Sample enrichment saved to: {output_file}")

if __name__ == "__main__":
    test_enhanced_categorizer()
