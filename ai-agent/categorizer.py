#!/usr/bin/env python3
"""
System Prompt Library Categorizer
Automatically categorizes and enhances system prompt entries without modifying schema
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import requests
from typing import Dict, List, Optional, Any
import argparse

class SystemPromptCategorizer:
    def __init__(self, config_path: str = "ai-agent/config/agent_config.json"):
        self.config = self._load_config(config_path)
        self.categories = self._load_taxonomy("ai-agent/taxonomies/categories.json")
        self.tags = self._load_taxonomy("ai-agent/taxonomies/tags.json")
        self.processed_count = 0
        self.enhanced_count = 0
        self.errors = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load agent configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Config file not found at {config_path}")
            sys.exit(1)
    
    def _load_taxonomy(self, taxonomy_path: str) -> Dict:
        """Load taxonomy definitions"""
        try:
            with open(taxonomy_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Taxonomy file not found at {taxonomy_path}")
            return {}
    
    def _backup_file(self, file_path: str) -> str:
        """Create backup of original file"""
        backup_dir = Path("ai-agent/backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{Path(file_path).stem}_{timestamp}.json"
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    
    def _call_llm(self, prompt: str, use_local: bool = True) -> Optional[str]:
        """Call LLM for categorization and enhancement"""
        if use_local and self.config["llm_options"]["local"]["recommended"]:
            return self._call_ollama(prompt)
        else:
            return self._call_openai(prompt)
    
    def _call_ollama(self, prompt: str) -> Optional[str]:
        """Call local Ollama model"""
        try:
            endpoint = self.config["llm_options"]["local"]["endpoint"]
            model = self.config["llm_options"]["local"]["model"]
            
            response = requests.post(f"{endpoint}/api/generate", 
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=self.config["processing_config"]["timeout_seconds"]
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                print(f"Ollama API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
    
    def _call_openai(self, prompt: str) -> Optional[str]:
        """Call OpenAI API as fallback"""
        # This would require OpenAI API key setup
        print("OpenAI fallback not implemented - please use local Ollama")
        return None
    
    def _generate_description(self, agent_data: Dict) -> str:
        """Generate description using LLM"""
        prompt = f"""
Analyze this system prompt agent and generate a concise, professional description (max 200 characters).

Agent Name: {agent_data.get('agentname', 'Unknown')}
System Prompt: {agent_data.get('systemprompt', '')[:500]}...

Focus on:
- Primary purpose and functionality
- Key capabilities
- Target use case

Return only the description, no additional text.
"""
        
        description = self._call_llm(prompt)
        if description and len(description) > 200:
            description = description[:197] + "..."
        
        return description or "AI assistant for specialized tasks"
    
    def _categorize_agent(self, agent_data: Dict) -> Optional[str]:
        """Categorize agent based on content analysis"""
        content = f"{agent_data.get('agentname', '')} {agent_data.get('description', '')} {agent_data.get('systemprompt', '')[:300]}"
        content = content.lower()
        
        # Simple keyword-based categorization
        for category in self.categories.get("categories", []):
            keywords = category.get("keywords", [])
            if any(keyword in content for keyword in keywords):
                return category["id"]
        
        return "specialized"  # Default category
    
    def _assign_tags(self, agent_data: Dict) -> List[str]:
        """Assign relevant tags based on content"""
        content = f"{agent_data.get('agentname', '')} {agent_data.get('description', '')} {agent_data.get('systemprompt', '')[:300]}"
        content = content.lower()
        
        assigned_tags = []
        max_tags = self.config["categorization_rules"]["tag_assignment"]["max_tags"]
        
        for tag in self.tags.get("tags", []):
            if len(assigned_tags) >= max_tags:
                break
                
            tag_keywords = [tag["id"], tag["name"].lower()]
            if any(keyword in content for keyword in tag_keywords):
                assigned_tags.append(tag["id"])
        
        return assigned_tags[:max_tags]
    
    def _enhance_agent_data(self, agent_data: Dict) -> Dict:
        """Enhance agent data without modifying schema"""
        enhanced = agent_data.copy()
        needs_enhancement = False
        
        # Generate description if missing or too short
        current_desc = enhanced.get("description", "")
        if not current_desc or len(current_desc.strip()) < 20:
            print(f"  Generating description for: {enhanced.get('agentname', 'Unknown')}")
            enhanced["description"] = self._generate_description(agent_data)
            needs_enhancement = True
        
        # Note: We're NOT adding category/tags fields since they don't exist in schema
        # The categorization logic is here for future use when schema is updated
        
        return enhanced, needs_enhancement
    
    def process_file(self, file_path: str) -> bool:
        """Process a single JSON file"""
        try:
            # Load existing data
            with open(file_path, 'r', encoding='utf-8') as f:
                agent_data = json.load(f)
            
            # Create backup
            if self.config["processing_config"]["backup_before_changes"]:
                backup_path = self._backup_file(file_path)
                print(f"  Backup created: {backup_path}")
            
            # Enhance data
            enhanced_data, was_enhanced = self._enhance_agent_data(agent_data)
            
            if was_enhanced:
                # Save enhanced data
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
                
                self.enhanced_count += 1
                print(f"  ✓ Enhanced: {file_path}")
            else:
                print(f"  - No changes needed: {file_path}")
            
            self.processed_count += 1
            return True
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            self.errors.append(error_msg)
            print(f"  ✗ {error_msg}")
            return False
    
    def process_directory(self, directory: str = "system-prompts/json") -> None:
        """Process all JSON files in directory"""
        json_files = list(Path(directory).glob("*.json"))
        total_files = len(json_files)
        
        print(f"Found {total_files} JSON files to process...")
        
        for i, file_path in enumerate(json_files, 1):
            print(f"[{i}/{total_files}] Processing: {file_path.name}")
            self.process_file(str(file_path))
        
        # Print summary
        print(f"\n=== Processing Summary ===")
        print(f"Files processed: {self.processed_count}")
        print(f"Files enhanced: {self.enhanced_count}")
        print(f"Errors: {len(self.errors)}")
        
        if self.errors:
            print("\nErrors encountered:")
            for error in self.errors:
                print(f"  - {error}")

def main():
    parser = argparse.ArgumentParser(description="Categorize and enhance system prompt library")
    parser.add_argument("--directory", "-d", default="system-prompts/json", 
                       help="Directory containing JSON files")
    parser.add_argument("--file", "-f", help="Process single file instead of directory")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    
    args = parser.parse_args()
    
    # Change to repository root if running from ai-agent directory
    if Path.cwd().name == "ai-agent":
        os.chdir("..")
    
    categorizer = SystemPromptCategorizer()
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        categorizer.config["processing_config"]["backup_before_changes"] = False
    
    if args.file:
        print(f"Processing single file: {args.file}")
        categorizer.process_file(args.file)
    else:
        print(f"Processing directory: {args.directory}")
        categorizer.process_directory(args.directory)

if __name__ == "__main__":
    main()
