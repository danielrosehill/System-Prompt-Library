# Code & Development Cluster

## Overview

This cluster contains system prompts for software development, code generation, debugging, documentation, code review, and technical implementation tasks. These agents assist with the complete software development lifecycle from initial code generation to debugging and maintenance.

## Core Capabilities

- Code generation and scaffolding
- Code review and quality assurance
- Debugging and troubleshooting
- Code documentation and commenting
- Repository management
- Code refactoring and optimization
- Technical architecture guidance
- Development workflow automation

## Agent Roles in This Cluster

### Code Generation Agents

- [CodeEditor_General](../../system-prompts/json/CodeEditor_General_270525.json)
- [code-generation-prompt-formatter](../../system-prompts/json/code-generation-prompt-formatter_260925.json)
- [dummy-csv-data-generator](../../system-prompts/json/dummy-csv-data-generator_260925.json)

### Code Analysis & Review Agents

- [code-repo-finder](../../system-prompts/json/code-repo-finder_260925.json)
- [code-to-human-matchmaker](../../system-prompts/json/code-to-human-matchmaker_260925.json)

### Documentation Agents

- [DocumentMyWritingStyle](../../system-prompts/json/DocumentMyWritingStyle_270525.json)
- [writing-agent-config-helper](../../system-prompts/json/writing-agent-config-helper_170925.json)

### Database Development Agents

- [DatabaseMatchmaker](../../system-prompts/json/DatabaseMatchmaker_270525.json)
- [database-schema-genie-postgres](../../system-prompts/json/database-schema-genie-postgres_260925.json)
- [graph-database-stack-assistant](../../system-prompts/json/graph-database-stack-assistant_260925.json)

### Development Tools & Utilities

- [BrowserAutomationGuide](../../system-prompts/json/BrowserAutomationGuide_270525.json)
- [BrowserUseAgents](../../system-prompts/json/BrowserUseAgents_270525.json)
- [ComputerUseAgents](../../system-prompts/json/ComputerUseAgents_270525.json)

## Multi-Agent Orchestration Patterns

### Pattern 1: Full-Stack Development Pipeline

```
Requirements Analysis Agent
    ↓
Database Schema Design (database-schema-genie-postgres)
    ↓
Code Generation (CodeEditor_General)
    ↓
Code Review Agent
    ↓
Documentation Agent (DocumentMyWritingStyle)
    ↓
Testing & QA Agent
```

**Use Case:** Building complete applications from requirements to deployment.

**Framework Recommendation:** **MetaGPT** - Specifically designed for software development with role-based agents (architect, engineer, tester).

### Pattern 2: Code Improvement Cycle

```
Code Repository → code-repo-finder → Code Analysis
                                         ↓
                Code Review ← code-to-human-matchmaker
                     ↓
            Refactoring Suggestions
                     ↓
            CodeEditor_General (Implementation)
                     ↓
                Testing → (loop back if issues)
```

**Use Case:** Continuous code quality improvement.

**Framework Recommendation:** **LangGraph** - Supports cyclic workflows with state management for iterative improvements.

### Pattern 3: Database Development Workflow

```
DatabaseMatchmaker (Requirements) → database-schema-genie-postgres
                                            ↓
                                    Schema Generation
                                            ↓
                            graph-database-stack-assistant (if graph DB)
                                            ↓
                                    Code Generation
                                            ↓
                                    Migration Scripts
```

**Use Case:** Database-centric application development.

**Framework Recommendation:** **CrewAI** - Sequential tasks with clear role separation.

### Pattern 4: Browser Automation Development

```
Requirement Specification
    ↓
BrowserAutomationGuide (Strategy)
    ↓
BrowserUseAgents (Implementation)
    ↓
Code Generation
    ↓
Testing & Debugging
```

**Use Case:** Building browser automation scripts and tools.

**Framework Recommendation:** **AutoGen** - Collaborative agents for iterative automation script development.

## Recommended Multi-Agent Frameworks

### Primary Recommendations

1. **MetaGPT**
   - **Best for:** Complete software development lifecycles
   - **Why:** Purpose-built for software engineering with SOP (Standard Operating Procedure) patterns
   - **Use when:** Building applications end-to-end with multiple engineering roles

2. **CrewAI**
   - **Best for:** Structured development workflows, code review processes
   - **Why:** Clear role definitions, sequential/hierarchical processes
   - **Use when:** Well-defined development pipelines with specialized roles

3. **LangGraph**
   - **Best for:** Iterative development, debugging loops, complex state management
   - **Why:** Graph-based workflows, cycle support, state tracking
   - **Use when:** Development involves iterative refinement and debugging

### Secondary Recommendations

4. **AutoGen**
   - **Best for:** Pair programming, collaborative debugging
   - **Why:** Multi-agent conversations, code execution capabilities
   - **Use when:** Agents need to discuss and iterate on solutions

5. **Flowise + LangChain**
   - **Best for:** Rapid prototyping of development workflows
   - **Why:** Visual interface, easy integration with code execution tools
   - **Use when:** Experimenting with development agent combinations

## Implementation Example

### Code Review and Documentation Pipeline

**Agents Involved:**
1. code-repo-finder
2. Code Review Agent (custom)
3. DocumentMyWritingStyle
4. CodeEditor_General

**Orchestration (MetaGPT):**

```python
from metagpt.team import Team
from metagpt.roles import Role
from metagpt.actions import Action

class CodeReviewer(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use code review system prompt

class DocumentationWriter(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use DocumentMyWritingStyle system prompt

class CodeRefactorer(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use CodeEditor_General system prompt

# Create team
team = Team()
team.hire([
    CodeReviewer(),
    DocumentationWriter(),
    CodeRefactorer()
])

# Run development workflow
await team.run(project="Review and document codebase X")
```

## Tool Requirements

Agents in this cluster often require:

- **Code execution** - Running and testing generated code
- **File system access** - Reading/writing code files
- **Git integration** - Repository operations
- **Database connections** - Schema management and queries
- **Web browser control** - For browser automation agents
- **Terminal/shell access** - Running build commands and scripts
- **IDE integration** - Enhanced development workflows

## Scaling Considerations

When deploying this cluster in production:

1. **Code Security** - Sandbox code execution environments
2. **Version Control** - Integrate with Git workflows
3. **CI/CD Integration** - Connect to existing pipelines
4. **Code Quality Gates** - Automated linting and testing
5. **Resource Limits** - Constrain compute for code execution
6. **Dependency Management** - Handle package installations securely
7. **Documentation Generation** - Automated doc updates on code changes

## Integration with Other Clusters

This cluster naturally integrates with:

- **[Agent Development & Orchestration](../agent-development-orchestration/)** - Meta-agents that build these development agents
- **[Data & Analysis](../data-analysis/)** - Data processing code generation
- **[Automation & Integration](../automation-integration/)** - Deployment and CI/CD automation
- **[Technical Infrastructure](../technical-infrastructure/)** - DevOps and infrastructure code

## Getting Started

1. Identify your development task (code gen, review, documentation, etc.)
2. Start with **code-repo-finder** if working with existing codebases
3. Use **DatabaseMatchmaker** + **database-schema-genie-postgres** for database work
4. Employ **CodeEditor_General** for code generation tasks
5. Add **DocumentMyWritingStyle** for documentation
6. Implement testing and QA agents as needed

## Best Practices

- **Separation of Concerns** - Use specialized agents for distinct tasks (review vs. generation)
- **Iterative Refinement** - Build feedback loops for code quality
- **Documentation First** - Generate docs alongside code
- **Test-Driven** - Include testing agents in workflows
- **Security Scanning** - Add security review agents
- **Code Style** - Maintain consistent formatting across agent outputs

## Additional Resources

- [MetaGPT Documentation](https://docs.deepwisdom.ai/main/en/)
- [Software Development with LLMs Best Practices](https://github.com/langchain-ai/langchain)
- [Code Generation Prompt Engineering](https://www.promptingguide.ai/)
