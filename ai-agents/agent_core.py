#!/usr/bin/env python3
"""
True AI Agent for System Prompt Library Categorization
Autonomous agent with decision-making, planning, and workflow orchestration
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import requests
from dataclasses import dataclass, asdict
from enum import Enum
import logging

class AgentState(Enum):
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    REFLECTING = "reflecting"
    COMPLETED = "completed"
    ERROR = "error"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Task:
    id: str
    description: str
    priority: TaskPriority
    dependencies: List[str]
    estimated_effort: int  # minutes
    status: str = "pending"
    result: Optional[Dict] = None
    confidence: float = 0.0

@dataclass
class AgentMemory:
    processed_files: Dict[str, Dict] = None
    learned_patterns: Dict[str, Any] = None
    performance_metrics: Dict[str, float] = None
    error_history: List[Dict] = None
    
    def __post_init__(self):
        if self.processed_files is None:
            self.processed_files = {}
        if self.learned_patterns is None:
            self.learned_patterns = {}
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.error_history is None:
            self.error_history = []

class SystemPromptAgent:
    """Autonomous AI Agent for System Prompt Library Management"""
    
    def __init__(self, config_path: str = "ai-agent/config/agent_config.json"):
        self.state = AgentState.INITIALIZING
        self.config = self._load_config(config_path)
        self.memory = self._load_memory()
        self.task_queue: List[Task] = []
        self.current_task: Optional[Task] = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Setup logging
        self._setup_logging()
        self.logger.info(f"Agent initialized with session ID: {self.session_id}")
        
        # Load taxonomies
        self.categories = self._load_taxonomy("ai-agent/taxonomies/categories.json")
        self.tags = self._load_taxonomy("ai-agent/taxonomies/tags.json")
        
        self.state = AgentState.ANALYZING
    
    def _setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path("ai-agent/logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"agent_{self.session_id}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("SystemPromptAgent")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load agent configuration"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.error(f"Config file not found: {config_path}")
            sys.exit(1)
    
    def _load_memory(self) -> AgentMemory:
        """Load persistent agent memory"""
        memory_path = Path("ai-agent/memory/agent_memory.json")
        memory_path.parent.mkdir(exist_ok=True)
        
        if memory_path.exists():
            try:
                with open(memory_path, 'r') as f:
                    data = json.load(f)
                return AgentMemory(**data)
            except Exception as e:
                self.logger.warning(f"Could not load memory: {e}")
        
        return AgentMemory()
    
    def _save_memory(self):
        """Persist agent memory"""
        memory_path = Path("ai-agent/memory/agent_memory.json")
        memory_path.parent.mkdir(exist_ok=True)
        
        with open(memory_path, 'w') as f:
            json.dump(asdict(self.memory), f, indent=2, default=str)
    
    def _load_taxonomy(self, path: str) -> Dict:
        """Load taxonomy with error handling"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Taxonomy not found: {path}")
            return {}
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """Call LLM with enhanced prompting"""
        full_prompt = f"""You are an autonomous AI agent specializing in system prompt analysis and categorization.

Current Context:
- Session: {self.session_id}
- State: {self.state.value}
- Current Task: {self.current_task.description if self.current_task else 'None'}

{system_prompt if system_prompt else ''}

{prompt}

Provide a thoughtful, analytical response that demonstrates understanding of the context and task."""

        try:
            response = requests.post("http://localhost:11434/api/generate", 
                json={
                    "model": "llama3.2",
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json().get("response", "").strip()
                self.logger.debug(f"LLM response: {result[:100]}...")
                return result
            else:
                self.logger.error(f"LLM API error: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            return None
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Autonomous analysis of the repository state"""
        self.logger.info("Starting autonomous repository analysis...")
        
        json_dir = Path("system-prompts/json")
        if not json_dir.exists():
            self.logger.error("JSON directory not found")
            return {"error": "Repository structure invalid"}
        
        files = list(json_dir.glob("*.json"))
        analysis = {
            "total_files": len(files),
            "files_needing_description": 0,
            "files_with_errors": 0,
            "categories_identified": set(),
            "complexity_distribution": {"simple": 0, "medium": 0, "complex": 0},
            "estimated_work_hours": 0
        }
        
        # Sample analysis of first 10 files to understand patterns
        sample_files = files[:10]
        for file_path in sample_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Check if description needs work
                desc = data.get("description", "")
                if not desc or len(desc.strip()) < 20:
                    analysis["files_needing_description"] += 1
                
                # Analyze complexity
                prompt_length = len(data.get("systemprompt", ""))
                if prompt_length < 500:
                    analysis["complexity_distribution"]["simple"] += 1
                elif prompt_length < 2000:
                    analysis["complexity_distribution"]["medium"] += 1
                else:
                    analysis["complexity_distribution"]["complex"] += 1
                    
            except Exception as e:
                analysis["files_with_errors"] += 1
                self.logger.warning(f"Error analyzing {file_path}: {e}")
        
        # Extrapolate to full dataset
        sample_ratio = len(sample_files) / len(files) if files else 1
        analysis["files_needing_description"] = int(analysis["files_needing_description"] / sample_ratio)
        analysis["estimated_work_hours"] = analysis["files_needing_description"] * 0.5  # 30 seconds per file
        
        self.logger.info(f"Analysis complete: {analysis['files_needing_description']} files need enhancement")
        return analysis
    
    def create_execution_plan(self, analysis: Dict) -> List[Task]:
        """Autonomous planning based on analysis"""
        self.state = AgentState.PLANNING
        self.logger.info("Creating autonomous execution plan...")
        
        tasks = []
        
        # Task 1: Validate repository structure
        tasks.append(Task(
            id="validate_structure",
            description="Validate repository structure and dependencies",
            priority=TaskPriority.CRITICAL,
            dependencies=[],
            estimated_effort=5
        ))
        
        # Task 2: Process high-priority files (missing descriptions)
        if analysis.get("files_needing_description", 0) > 0:
            tasks.append(Task(
                id="enhance_descriptions",
                description=f"Generate descriptions for {analysis['files_needing_description']} files",
                priority=TaskPriority.HIGH,
                dependencies=["validate_structure"],
                estimated_effort=int(analysis.get("estimated_work_hours", 1) * 60)
            ))
        
        # Task 3: Quality assurance
        tasks.append(Task(
            id="quality_check",
            description="Perform quality checks and validation",
            priority=TaskPriority.MEDIUM,
            dependencies=["enhance_descriptions"],
            estimated_effort=10
        ))
        
        # Task 4: Update memory and metrics
        tasks.append(Task(
            id="update_memory",
            description="Update agent memory with learned patterns",
            priority=TaskPriority.LOW,
            dependencies=["quality_check"],
            estimated_effort=5
        ))
        
        self.logger.info(f"Created execution plan with {len(tasks)} tasks")
        return tasks
    
    def execute_task(self, task: Task) -> bool:
        """Execute a specific task autonomously"""
        self.current_task = task
        self.logger.info(f"Executing task: {task.description}")
        
        try:
            if task.id == "validate_structure":
                return self._validate_structure(task)
            elif task.id == "enhance_descriptions":
                return self._enhance_descriptions(task)
            elif task.id == "quality_check":
                return self._quality_check(task)
            elif task.id == "update_memory":
                return self._update_memory(task)
            else:
                self.logger.error(f"Unknown task: {task.id}")
                return False
                
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            task.status = "failed"
            return False
    
    def _validate_structure(self, task: Task) -> bool:
        """Validate repository structure"""
        required_paths = [
            "system-prompts/json",
            "ai-agent/config",
            "ai-agent/taxonomies"
        ]
        
        for path in required_paths:
            if not Path(path).exists():
                self.logger.error(f"Required path missing: {path}")
                task.status = "failed"
                return False
        
        task.status = "completed"
        task.confidence = 1.0
        self.logger.info("Repository structure validation passed")
        return True
    
    def _enhance_descriptions(self, task: Task) -> bool:
        """Autonomously enhance file descriptions"""
        json_dir = Path("system-prompts/json")
        files = list(json_dir.glob("*.json"))
        enhanced_count = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Check if enhancement needed
                desc = data.get("description", "")
                if desc and len(desc.strip()) >= 20:
                    continue
                
                # Generate enhanced description
                prompt = f"""
Analyze this system prompt agent and generate a concise, professional description (max 150 chars):

Agent Name: {data.get('agentname', 'Unknown')}
System Prompt: {data.get('systemprompt', '')[:300]}...

Focus on: primary purpose, key capabilities, target use case.
Return only the description, no additional text.
"""
                
                new_desc = self._call_llm(prompt)
                if new_desc and len(new_desc) <= 200:
                    # Backup original
                    backup_dir = Path("ai-agent/backups")
                    backup_dir.mkdir(exist_ok=True)
                    backup_path = backup_dir / f"{file_path.stem}_{self.session_id}.json"
                    
                    with open(backup_path, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    # Update with new description
                    data["description"] = new_desc
                    with open(file_path, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    enhanced_count += 1
                    self.logger.info(f"Enhanced: {file_path.name}")
                    
                    # Store in memory
                    self.memory.processed_files[str(file_path)] = {
                        "enhanced": True,
                        "timestamp": datetime.now().isoformat(),
                        "session": self.session_id
                    }
                
            except Exception as e:
                self.logger.warning(f"Could not enhance {file_path}: {e}")
        
        task.status = "completed"
        task.result = {"enhanced_count": enhanced_count}
        task.confidence = 0.9
        self.logger.info(f"Enhanced {enhanced_count} descriptions")
        return True
    
    def _quality_check(self, task: Task) -> bool:
        """Perform quality assurance checks"""
        issues = []
        json_dir = Path("system-prompts/json")
        
        for file_path in json_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Check for required fields
                if not data.get("agentname"):
                    issues.append(f"{file_path.name}: Missing agent name")
                
                if not data.get("description"):
                    issues.append(f"{file_path.name}: Missing description")
                
            except json.JSONDecodeError:
                issues.append(f"{file_path.name}: Invalid JSON")
        
        task.status = "completed"
        task.result = {"issues": issues}
        task.confidence = 0.95
        
        if issues:
            self.logger.warning(f"Quality check found {len(issues)} issues")
        else:
            self.logger.info("Quality check passed - no issues found")
        
        return True
    
    def _update_memory(self, task: Task) -> bool:
        """Update agent memory with learned patterns"""
        # Update performance metrics
        self.memory.performance_metrics[self.session_id] = {
            "files_processed": len(self.memory.processed_files),
            "tasks_completed": len([t for t in self.task_queue if t.status == "completed"]),
            "session_duration": time.time(),
            "success_rate": 0.95  # Calculate based on actual results
        }
        
        # Save memory
        self._save_memory()
        
        task.status = "completed"
        task.confidence = 1.0
        self.logger.info("Agent memory updated successfully")
        return True
    
    def reflect_and_learn(self):
        """Autonomous reflection on performance and learning"""
        self.state = AgentState.REFLECTING
        self.logger.info("Starting reflection and learning phase...")
        
        # Analyze session performance
        completed_tasks = [t for t in self.task_queue if t.status == "completed"]
        failed_tasks = [t for t in self.task_queue if t.status == "failed"]
        
        reflection_prompt = f"""
Reflect on this agent session performance:

Completed Tasks: {len(completed_tasks)}
Failed Tasks: {len(failed_tasks)}
Files Processed: {len(self.memory.processed_files)}

What patterns can you identify? What improvements could be made for future sessions?
Provide specific, actionable insights.
"""
        
        insights = self._call_llm(reflection_prompt)
        if insights:
            self.memory.learned_patterns[self.session_id] = {
                "insights": insights,
                "timestamp": datetime.now().isoformat(),
                "performance_summary": {
                    "completed": len(completed_tasks),
                    "failed": len(failed_tasks)
                }
            }
        
        self.logger.info("Reflection complete - insights stored in memory")
    
    def run(self) -> Dict[str, Any]:
        """Main autonomous execution loop"""
        try:
            self.logger.info("Starting autonomous agent execution...")
            
            # Phase 1: Analysis
            analysis = self.analyze_repository()
            if "error" in analysis:
                return analysis
            
            # Phase 2: Planning
            self.task_queue = self.create_execution_plan(analysis)
            
            # Phase 3: Execution
            self.state = AgentState.EXECUTING
            for task in self.task_queue:
                # Check dependencies
                if not all(t.status == "completed" for t in self.task_queue 
                          if t.id in task.dependencies):
                    self.logger.warning(f"Skipping {task.id} - dependencies not met")
                    continue
                
                success = self.execute_task(task)
                if not success and task.priority in [TaskPriority.CRITICAL, TaskPriority.HIGH]:
                    self.logger.error(f"Critical task failed: {task.id}")
                    self.state = AgentState.ERROR
                    return {"error": f"Critical task failed: {task.id}"}
            
            # Phase 4: Reflection
            self.reflect_and_learn()
            
            # Phase 5: Completion
            self.state = AgentState.COMPLETED
            self._save_memory()
            
            result = {
                "status": "success",
                "session_id": self.session_id,
                "tasks_completed": len([t for t in self.task_queue if t.status == "completed"]),
                "files_processed": len(self.memory.processed_files),
                "analysis": analysis
            }
            
            self.logger.info(f"Agent execution completed successfully: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Agent execution failed: {e}")
            self.state = AgentState.ERROR
            return {"error": str(e)}

def main():
    """Main entry point for autonomous agent"""
    agent = SystemPromptAgent()
    result = agent.run()
    
    if "error" in result:
        print(f"❌ Agent execution failed: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ Agent completed successfully!")
        print(f"   Session: {result['session_id']}")
        print(f"   Tasks: {result['tasks_completed']}")
        print(f"   Files: {result['files_processed']}")

if __name__ == "__main__":
    main()
