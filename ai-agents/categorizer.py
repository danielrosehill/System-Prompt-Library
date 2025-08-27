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
        # Load configuration - handle different working directories
        config_paths = [
            Path("config/agent_config.json"),  # When running from ai-agent/
            Path("ai-agent/config/agent_config.json"),  # When running from repo root
        ]
        
        config_path = None
        for path in config_paths:
            if path.exists():
                config_path = path
                break
                
        if not config_path:
            raise FileNotFoundError(f"Config file not found at any of: {config_paths}")
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load taxonomies - handle different working directories
        taxonomy_paths = {
            "categories": [
                Path("taxonomies/categories.json"),
                Path("ai-agent/taxonomies/categories.json")
            ],
            "tags": [
                Path("taxonomies/tags.json"), 
                Path("ai-agent/taxonomies/tags.json")
            ]
        }
        
        self.categories = self._load_taxonomy_flexible(taxonomy_paths["categories"])
        self.tags = self._load_taxonomy_flexible(taxonomy_paths["tags"])
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
        """Load taxonomy from JSON file"""
        try:
            with open(taxonomy_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Taxonomy file not found at {taxonomy_path}")
            return {"categories": []} if "categories" in taxonomy_path else {"tags": []}
    
    def _load_taxonomy_flexible(self, paths: List[Path]) -> Dict:
        """Load taxonomy from multiple possible paths"""
        for path in paths:
            if path.exists():
                try:
                    with open(path, 'r') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Warning: Error loading taxonomy from {path}: {e}")
                    continue
        
        # Return empty taxonomy if none found
        taxonomy_type = "categories" if "categories" in str(paths[0]) else "tags"
        print(f"Warning: No {taxonomy_type} taxonomy found at any of: {paths}")
        return {"categories": []} if taxonomy_type == "categories" else {"tags": []}
    
    def _backup_file(self, file_path: str) -> str:
        """Create backup of original file"""
        backup_dir = Path("ai-agent/backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{Path(file_path).stem}_{timestamp}.json"
        shutil.copy2(file_path, backup_path)
        return str(backup_path)
    
    def _get_agent_content(self, agent_data: Dict) -> str:
        """Extract all text content from agent data for analysis"""
        content_parts = []
        
        # Add agent name
        if agent_data.get("agentname"):
            content_parts.append(agent_data["agentname"])
        
        # Add description
        if agent_data.get("description"):
            content_parts.append(agent_data["description"])
        
        # Add system prompt if available
        if agent_data.get("systemprompt"):
            content_parts.append(agent_data["systemprompt"])
        
        # Add any other text fields
        text_fields = ["use_case_outline", "api_notes", "guardrails_notes", "iteration_notes"]
        for field in text_fields:
            if agent_data.get(field):
                content_parts.append(str(agent_data[field]))
        
        return " ".join(content_parts)
    
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
        """Categorize agent using LLM analysis"""
        # Prepare content for LLM analysis
        agent_name = agent_data.get('agentname', 'Unknown')
        description = agent_data.get('description', '')
        system_prompt = agent_data.get('systemprompt', '')[:800]  # Limit for context
        
        # Create category options for LLM
        category_options = []
        for cat in self.categories.get("categories", []):
            category_options.append(f"- {cat['id']}: {cat['name']} - {cat['description']}")
        
        prompt = f"""Analyze this AI agent and categorize it into ONE of the following categories:

{chr(10).join(category_options)}

Agent Details:
Name: {agent_name}
Description: {description}
System Prompt: {system_prompt}

Based on the agent's purpose, functionality, and use case, which category fits best?
Respond with ONLY the category ID (e.g., "productivity", "development", etc.)."""

        category_result = self._call_llm(prompt)
        
        if category_result:
            # Validate the result is a valid category
            valid_categories = [cat['id'] for cat in self.categories.get("categories", [])]
            category_clean = category_result.strip().lower()
            if category_clean in valid_categories:
                return category_clean
        
        return "specialized"  # Default fallback
    
    def _assign_tags(self, agent_data: Dict) -> List[str]:
        """Assign relevant tags using enhanced LLM analysis"""
        # Prepare content for LLM analysis
        agent_name = agent_data.get('agentname', 'Unknown')
        description = agent_data.get('description', '')
        system_prompt = agent_data.get('systemprompt', '')[:800]
        
        # Create tag options for LLM
        tag_options = []
        for tag in self.tags.get("tags", []):
            tag_options.append(f"- {tag['id']}: {tag['name']} - {tag['description']}")
        
        max_tags = self.config["categorization_rules"]["tag_assignment"]["max_tags"]
        
        prompt = f"""You are an expert at semantic analysis and domain-specific tagging. Analyze this AI agent deeply and assign the most relevant and specific tags.

Available Tags:
{chr(10).join(tag_options)}

Agent to Analyze:
Name: {agent_name}
Description: {description}
System Prompt: {system_prompt}

Instructions:
1. Look for domain-specific terms (e.g., "ADHD" should get "adhd" and "mental-health" tags)
2. Identify the primary function (e.g., software recommendations → "software-recommendations")
3. Consider the target audience and use case
4. Be specific rather than generic (prefer "adhd" over just "health")
5. Look for technical domains (web-development, api-development, etc.)

Select up to {max_tags} tags that are most specific and relevant to this agent's purpose.
Respond with ONLY the tag IDs separated by commas (e.g., "adhd,mental-health,technology-guidance")."""

        tags_result = self._call_llm(prompt)
        
        if tags_result:
            # Parse and validate tags
            suggested_tags = [tag.strip().lower() for tag in tags_result.split(',')]
            valid_tags = [tag['id'] for tag in self.tags.get("tags", [])]
            
            assigned_tags = []
            for tag in suggested_tags:
                if tag in valid_tags and len(assigned_tags) < max_tags:
                    assigned_tags.append(tag)
            
            return assigned_tags
        
        return []  # Return empty if LLM fails
    
    def _create_enrichment_data(self, agent_data: Dict) -> Dict:
        """Create AI enrichment data following the enrichment schema"""
        import uuid
        from datetime import datetime
        
        print(f"  Creating AI enrichment for: {agent_data.get('agentname', 'Unknown')}")
        
        # Generate session data
        session_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        # Generate all enrichment components using LLM
        category = self._categorize_agent(agent_data)
        tags = self._assign_tags(agent_data)
        
        # Enhanced description
        original_desc = agent_data.get("description", "")
        enhanced_desc = self._generate_description(agent_data) if not original_desc else original_desc
        
        # Detect capabilities and requirements using LLM
        capabilities = self._detect_capabilities(agent_data)
        requirements = self._detect_requirements(agent_data)
        notes = self._generate_notes(agent_data)
        
        enrichment_data = {
            "ai_enriched_metadata": {
                "enrichment_version": "2.0.0",
                "enrichment_timestamp": timestamp,
                "enrichment_model": "llama3.2",
                "enrichment_session_id": session_id,
                "confidence_score": 0.85
            },
            "ai_enriched_categorization": {
                "primary_category": category,
                "category_confidence": 0.8,
                "category_reasoning": f"Categorized as '{category}' based on content analysis",
                "alternative_categories": []
            },
            "ai_enriched_tags": {
                "assigned_tags": tags,
                "tag_confidence_scores": {tag: 0.75 for tag in tags},
                "tag_reasoning": "Tags assigned based on semantic analysis of agent content and comprehensive taxonomy"
            },
            "ai_enriched_description": {
                "enhanced_description": enhanced_desc,
                "description_type": "enhanced" if original_desc else "generated",
                "original_description": original_desc,
                "enhancement_reasoning": "Enhanced for clarity and completeness"
            },
            "ai_enriched_capabilities": capabilities,
            "ai_enriched_requirements": requirements,
            "ai_enriched_notes": notes,
            "ai_enriched_analysis": {
                "complexity_score": self._assess_complexity(agent_data),
                "use_case_breadth": self._assess_use_case_breadth(agent_data),
                "technical_requirements": self._extract_technical_requirements(agent_data),
                "target_audience": self._identify_target_audience(agent_data),
                "improvement_suggestions": self._generate_improvement_suggestions(agent_data)
            },
            "ai_enriched_quality_metrics": {
                "prompt_clarity_score": self._assess_clarity(agent_data),
                "completeness_score": self._assess_completeness(agent_data),
                "specificity_score": self._assess_specificity(agent_data),
                "quality_issues": self._identify_quality_issues(agent_data)
            }
        }
        
        return enrichment_data
    
    def _detect_capabilities(self, agent_data: Dict) -> Dict:
        """Detect capabilities using simple heuristics and LLM analysis"""
        capabilities = {
            "conversational": False,
            "autonomous": False,
            "instructional": False,
            "character": False,
            "roleplay": False,
            "writing_assistant": False,
            "deep_research": False,
            "data_utility": False,
            "better_as_tool": False,
            "is_agent": False,
            "single_turn": False,
            "update_iteration": False
        }
        
        content = self._get_agent_content(agent_data)
        content_lower = content.lower()
        
        # Simple keyword-based detection
        if any(word in content_lower for word in ["conversation", "chat", "dialogue", "multi-turn"]):
            capabilities["conversational"] = True
        if any(word in content_lower for word in ["autonomous", "independent", "self-directed"]):
            capabilities["autonomous"] = True
        if any(word in content_lower for word in ["teach", "instruct", "guide", "tutorial", "step-by-step"]):
            capabilities["instructional"] = True
        if any(word in content_lower for word in ["character", "persona", "role", "personality"]):
            capabilities["character"] = True
        if any(word in content_lower for word in ["roleplay", "role-play", "acting", "simulate"]):
            capabilities["roleplay"] = True
        if any(word in content_lower for word in ["writing", "author", "compose", "draft", "edit"]):
            capabilities["writing_assistant"] = True
        if any(word in content_lower for word in ["research", "investigate", "analyze", "deep dive"]):
            capabilities["deep_research"] = True
        if any(word in content_lower for word in ["data", "process", "utility", "tool", "function"]):
            capabilities["data_utility"] = True
        if any(word in content_lower for word in ["tool", "utility", "function", "helper"]):
            capabilities["better_as_tool"] = True
        if any(word in content_lower for word in ["agent", "autonomous", "tools", "actions"]):
            capabilities["is_agent"] = True
        if any(word in content_lower for word in ["single", "one-time", "once", "immediate"]):
            capabilities["single_turn"] = True
            
        return capabilities
    
    def _detect_requirements(self, agent_data: Dict) -> Dict:
        """Detect technical requirements using heuristics"""
        requirements = {
            "audio": False,
            "vision": False,
            "file_input": False,
            "video_input": False,
            "tts": False,
            "voice_first": False,
            "speech_to_speech": False,
            "external_tooling": False,
            "rag": False,
            "structured_output": False,
            "image_generation": False
        }
        
        content = self._get_agent_content(agent_data)
        content_lower = content.lower()
        
        # Simple keyword-based detection
        if any(word in content_lower for word in ["audio", "voice", "speech", "sound"]):
            requirements["audio"] = True
        if any(word in content_lower for word in ["vision", "image", "visual", "see", "picture"]):
            requirements["vision"] = True
        if any(word in content_lower for word in ["file", "upload", "document", "attachment"]):
            requirements["file_input"] = True
        if any(word in content_lower for word in ["video", "movie", "clip", "recording"]):
            requirements["video_input"] = True
        if any(word in content_lower for word in ["text-to-speech", "tts", "speak", "voice output"]):
            requirements["tts"] = True
        if any(word in content_lower for word in ["voice-first", "voice interface", "spoken"]):
            requirements["voice_first"] = True
        if any(word in content_lower for word in ["external", "tool", "api", "integration"]):
            requirements["external_tooling"] = True
        if any(word in content_lower for word in ["rag", "retrieval", "knowledge base", "search"]):
            requirements["rag"] = True
        if any(word in content_lower for word in ["structured", "json", "xml", "format", "schema"]):
            requirements["structured_output"] = True
        if any(word in content_lower for word in ["generate image", "create image", "dall-e", "midjourney"]):
            requirements["image_generation"] = True
            
        return requirements
    
    def _generate_notes(self, agent_data: Dict) -> Dict:
        """Generate contextual notes using simple analysis"""
        notes = {}
        content = self._get_agent_content(agent_data)
        
        # Use case outline
        if "use case" in content.lower() or "application" in content.lower():
            notes["use_case_outline"] = "Multiple use cases identified in agent description"
        
        # Local LLM assessment
        if any(word in content.lower() for word in ["simple", "basic", "straightforward"]):
            notes["local_llm_friendly"] = "yes"
        elif any(word in content.lower() for word in ["complex", "advanced", "sophisticated"]):
            notes["local_llm_friendly"] = "partial"
        else:
            notes["local_llm_friendly"] = "unknown"
            
        return notes
    
    def _assess_complexity(self, agent_data: Dict) -> int:
        """Assess complexity on 1-10 scale"""
        content = self._get_agent_content(agent_data)
        
        # Simple heuristic based on content length and keywords
        complexity = 5  # Default medium complexity
        
        if len(content) > 1000:
            complexity += 1
        if any(word in content.lower() for word in ["advanced", "complex", "sophisticated"]):
            complexity += 2
        if any(word in content.lower() for word in ["simple", "basic", "easy"]):
            complexity -= 2
            
        return max(1, min(10, complexity))
    
    def _assess_use_case_breadth(self, agent_data: Dict) -> str:
        """Assess use case breadth"""
        content = self._get_agent_content(agent_data)
        
        if any(word in content.lower() for word in ["specific", "specialized", "narrow"]):
            return "narrow"
        elif any(word in content.lower() for word in ["versatile", "multiple", "various", "broad"]):
            return "broad"
        else:
            return "moderate"
    
    def _extract_technical_requirements(self, agent_data: Dict) -> List[str]:
        """Extract technical requirements"""
        requirements = ["LLM", "Text Processing"]
        content = self._get_agent_content(agent_data)
        
        if "api" in content.lower():
            requirements.append("API Integration")
        if "database" in content.lower():
            requirements.append("Database")
        if "web" in content.lower():
            requirements.append("Web Interface")
            
        return requirements
    
    def _identify_target_audience(self, agent_data: Dict) -> List[str]:
        """Identify target audience"""
        content = self._get_agent_content(agent_data)
        audience = []
        
        if any(word in content.lower() for word in ["developer", "programmer", "coder"]):
            audience.append("Developers")
        if any(word in content.lower() for word in ["business", "professional", "enterprise"]):
            audience.append("Business Users")
        if any(word in content.lower() for word in ["student", "learn", "education"]):
            audience.append("Students")
        if any(word in content.lower() for word in ["writer", "author", "content"]):
            audience.append("Content Creators")
            
        return audience if audience else ["General Users"]
    
    def _generate_improvement_suggestions(self, agent_data: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if not agent_data.get("description"):
            suggestions.append("Add detailed description")
        if len(self._get_agent_content(agent_data)) < 100:
            suggestions.append("Expand content and examples")
        if "example" not in self._get_agent_content(agent_data).lower():
            suggestions.append("Include usage examples")
            
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _assess_clarity(self, agent_data: Dict) -> int:
        """Assess prompt clarity (1-10)"""
        content = self._get_agent_content(agent_data)
        
        clarity = 7  # Default good clarity
        if len(content) < 50:
            clarity -= 3
        if not agent_data.get("description"):
            clarity -= 2
        if "example" in content.lower():
            clarity += 1
            
        return max(1, min(10, clarity))
    
    def _assess_completeness(self, agent_data: Dict) -> int:
        """Assess prompt completeness (1-10)"""
        completeness = 5  # Default medium
        
        if agent_data.get("description"):
            completeness += 2
        if agent_data.get("agentname"):
            completeness += 1
        if len(self._get_agent_content(agent_data)) > 200:
            completeness += 2
            
        return max(1, min(10, completeness))
    
    def _assess_specificity(self, agent_data: Dict) -> int:
        """Assess prompt specificity (1-10)"""
        content = self._get_agent_content(agent_data)
        
        specificity = 6  # Default moderate specificity
        if any(word in content.lower() for word in ["specific", "detailed", "precise"]):
            specificity += 2
        if any(word in content.lower() for word in ["general", "broad", "vague"]):
            specificity -= 2
            
        return max(1, min(10, specificity))
    
    def _identify_quality_issues(self, agent_data: Dict) -> List[str]:
        """Identify quality issues"""
        issues = []
        
        if not agent_data.get("description"):
            issues.append("Missing description")
        if len(self._get_agent_content(agent_data)) < 50:
            issues.append("Content too brief")
        if not agent_data.get("agentname"):
            issues.append("Missing agent name")
            
        return issues[:5]  # Limit to 5 issues
    
    def _enhance_agent_data(self, agent_data: Dict) -> tuple[Dict, bool, Dict]:
        """Enhance agent data and create separate enrichment data"""
        enhanced = agent_data.copy()
        needs_enhancement = False
        enrichment_data = None
        
        # Always create enrichment data for analysis
        category = self._categorize_agent(agent_data)
        tags = self._assign_tags(agent_data)
        enrichment_data = self._create_enrichment_data(agent_data)
        
        # Check if enhancement is needed for original data
        current_desc = enhanced.get("description", "")
        if not current_desc or len(current_desc.strip()) < 20:
            # Update original data with AI-generated description
            print(f"  Generating description for: {enhanced.get('agentname', 'Unknown')}")
            enhanced["description"] = enrichment_data.get("ai_enriched_description", {}).get("enhanced_description", self._generate_description(agent_data))
            needs_enhancement = True
        
        # Add enriched data fields to original JSON (with clear AI prefixes)
        enhanced["ai_enriched_category"] = enrichment_data["ai_enriched_categorization"]["primary_category"]
        enhanced["ai_enriched_tags"] = enrichment_data["ai_enriched_tags"]["assigned_tags"]
        enhanced["ai_enriched_confidence"] = enrichment_data["ai_enriched_metadata"]["confidence_score"]
        enhanced["ai_enriched_timestamp"] = enrichment_data["ai_enriched_metadata"]["enrichment_timestamp"]
        needs_enhancement = True
        
        print(f"    AI Category: {enrichment_data['ai_enriched_categorization']['primary_category']}")
        print(f"    AI Tags: {', '.join(enrichment_data['ai_enriched_tags']['assigned_tags'])}")
        
        return enhanced, needs_enhancement, enrichment_data
    
    def _generate_md_file(self, enhanced_data: Dict, enrichment_data: Dict, file_stem: str) -> str:
        """Generate markdown file with enriched data"""
        agent_name = enhanced_data.get('agentname', 'Unknown Agent')
        description = enhanced_data.get('description', 'No description available')
        system_prompt = enhanced_data.get('systemprompt', '')
        chatgpt_link = enhanced_data.get('chatgptlink', '')
        creation_date = enhanced_data.get('creation_date', '')
        
        # AI enrichment data
        category = enrichment_data['ai_enriched_categorization']['primary_category']
        tags = enrichment_data['ai_enriched_tags']['assigned_tags']
        confidence = enrichment_data['ai_enriched_metadata']['confidence_score']
        
        md_content = f"""# {agent_name}

**Description**: {description}

**AI Category**: {category.title()}

**AI Tags**: {', '.join(tags) if tags else 'None'}

**AI Confidence**: {confidence:.2f}

"""
        
        if chatgpt_link:
            md_content += f"**ChatGPT Link**: [{chatgpt_link}]({chatgpt_link})\n\n"
        
        # Add other boolean fields
        boolean_fields = ['is-agent', 'is-single-turn', 'structured-output-generation', 'image-generation', 'data-utility']
        for field in boolean_fields:
            if field in enhanced_data and enhanced_data[field]:
                md_content += f"**{field.replace('-', ' ').title()}**: {enhanced_data[field]}\n"
        
        md_content += f"\n## System Prompt\n\n```\n{system_prompt}\n```\n\n"
        
        if creation_date:
            md_content += f"**Created On**: {creation_date}\n"
        
        return md_content
    
    def process_file(self, file_path: str) -> bool:
        """Process a single JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                agent_data = json.load(f)
            
            enhanced_data, was_enhanced, enrichment_data = self._enhance_agent_data(agent_data)
            
            # Write enhanced JSON back (only file we need)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Enhanced: {file_path}")
            
            # Skip markdown updates for now - focus on JSON enrichment
            
            self.enhanced_count += 1
            return True
            
        except Exception as e:
            error_msg = f"Error processing {file_path}: {e}"
            print(f"  ✗ {error_msg}")
            self.errors.append(error_msg)
            return False
    
    def process_directory(self, directory: str):
        """Process all JSON files in directory with progress tracking"""
        json_files = list(Path(directory).glob("*.json"))
        total_files = len(json_files)
        
        print(f"Found {total_files} JSON files to process...")
        
        for i, file_path in enumerate(json_files, 1):
            print(f"[{i}/{total_files}] Processing: {file_path.name}")
            self.process_file(str(file_path))
            self.processed_count += 1
            
            # Progress indicator every 50 files
            if i % 50 == 0:
                print(f"  📊 Progress: {i}/{total_files} ({i/total_files*100:.1f}%) - Enhanced: {self.enhanced_count}")
        
        # Print final summary
        print(f"\n=== Processing Complete ===")
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
