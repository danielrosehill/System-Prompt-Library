# Content & Writing Cluster

## Overview

This cluster contains system prompts for content creation, writing assistance, editing, copywriting, and documentation. These agents support the complete content lifecycle from ideation and drafting to editing and formatting.

## Core Capabilities

- Content writing and generation
- Editing and proofreading
- Tone and style adaptation
- Copywriting and headlines
- Blog and article creation
- Email and messaging
- Documentation writing
- Text formatting and conversion
- Content extraction and summarization

## Agent Roles in This Cluster

### Writing Generation Agents

- [BlogOutlineGenerator](../../system-prompts/json/BlogOutlineGenerator_270525.json)
- [FormalWritingGenerator](../../system-prompts/json/FormalWritingGenerator_270525.json)
- [HeadlineCopywriter](../../system-prompts/json/HeadlineCopywriter_270525.json)
- [ArticleBodyTextExtractor](../../system-prompts/json/ArticleBodyTextExtractor_270525.json)
- [SocialToBlogPost](../../system-prompts/json/SocialToBlogPost_270525.json)
- [RepoToBlogPost](../../system-prompts/json/RepoToBlogPost_270525.json)

### Editing & Refinement Agents

- [SimpleTextEditor](../../system-prompts/json/SimpleTextEditor_270525.json)
- [StylisticTextEditor](../../system-prompts/json/StylisticTextEditor_270525.json)
- [stylistic-text-editor](../../system-prompts/json/stylistic-text-editor_280925.json)
- [ChaoticTextEditor](../../system-prompts/json/ChaoticTextEditor_270525.json)
- [InformalTextEditor](../../system-prompts/json/InformalTextEditor_270525.json)
- [NativeEnglishEditor](../../system-prompts/json/NativeEnglishEditor_270525.json)
- [angry-editor-on-call](../../system-prompts/json/angry-editor-on-call_260925.json)

### Tone & Style Adaptation Agents

- [AcademicToneWriter](../../system-prompts/json/AcademicToneWriter_270525.json)
- [RewriteInThirdPerson](../../system-prompts/json/RewriteInThirdPerson_270525.json)
- [ShakespeareanEmailWriter](../../system-prompts/json/ShakespeareanEmailWriter_270525.json)
- [DocumentMyWritingStyle](../../system-prompts/json/DocumentMyWritingStyle_270525.json)
- [professional-narrative-writers](../../system-prompts/json/professional-narrative-writers_250925.json)

### Specialized Content Agents

- [bot-email-writer](../../system-prompts/json/bot-email-writer_260925.json)
- [HebrewMessageWriter](../../system-prompts/json/HebrewMessageWriter_270525.json)
- [MeetingDebriefWriter](../../system-prompts/json/MeetingDebriefWriter_270525.json)
- [ReversePitchWriter](../../system-prompts/json/ReversePitchWriter_270525.json)
- [speechwriter-on-call](../../system-prompts/json/speechwriter-on-call_280925.json)
- [BygoneBusinessEmails](../../system-prompts/json/BygoneBusinessEmails_040625.json)
- [classifieds-listing-writer](../../system-prompts/json/classifieds-listing-writer_260925.json)

### Content Formatting Agents

- [dictated-blog-formatter](../../system-prompts/json/dictated-blog-formatter_260925.json)
- [NewsArticleSummaryGenerator](../../system-prompts/json/NewsArticleSummaryGenerator_270525.json)
- [ArticleTextScraper](../../system-prompts/json/ArticleTextScraper_270525.json)
- [SubtitledContentForLanguageLearners](../../system-prompts/json/SubtitledContentForLanguageLearners_270525.json)

### Creative Writing Agents

- [plot-line-writer](../../system-prompts/json/plot-line-writer_280925.json)
- [ridiculous-ai-lyrics-writer](../../system-prompts/json/ridiculous-ai-lyrics-writer_290925.json)

### Writing Assistant Meta-Agents

- [AssistantIdeator_WritingAndEditing](../../system-prompts/json/AssistantIdeator_WritingAndEditing_270525.json)

## Multi-Agent Orchestration Patterns

### Pattern 1: Blog Content Production Pipeline

```
BlogOutlineGenerator (Planning)
    ↓
Content Research Agent
    ↓
Writing Generation Agent
    ↓
StylisticTextEditor (Refinement)
    ↓
HeadlineCopywriter (Headlines)
    ↓
NativeEnglishEditor (Final Polish)
```

**Use Case:** Professional blog content creation from concept to publication.

**Framework Recommendation:** **CrewAI** - Sequential content production with role-based agents.

### Pattern 2: Multi-Tone Content Adaptation

```
Original Content → DocumentMyWritingStyle (Analysis)
    ↓
┌───────────────┼───────────────┐
↓               ↓               ↓
AcademicToneWriter  FormalWritingGenerator  ShakespeareanEmailWriter
    ↓               ↓               ↓
└───────────────┴───────────────┘
        ↓
Review & Selection
```

**Use Case:** Creating multiple versions of content for different audiences.

**Framework Recommendation:** **AutoGen** - Parallel content generation with collaborative review.

### Pattern 3: Content Repurposing Workflow

```
Source Content
    ↓
┌───────────────┼───────────────┐
↓               ↓               ↓
SocialToBlogPost  RepoToBlogPost  ArticleBodyTextExtractor
    ↓               ↓               ↓
└───────────────┴───────────────┘
        ↓
StylisticTextEditor (Unification)
        ↓
HeadlineCopywriter
```

**Use Case:** Repurposing content across different platforms and formats.

**Framework Recommendation:** **LangGraph** - Flexible branching based on source content type.

### Pattern 4: Editing Gauntlet

```
Draft Content
    ↓
SimpleTextEditor (Basic Cleanup)
    ↓
StylisticTextEditor (Style Enhancement)
    ↓
NativeEnglishEditor (Language Polish)
    ↓
angry-editor-on-call (Critical Review)
    ↓
Final Revision (if needed, loop back)
```

**Use Case:** Multi-pass editing for high-quality content.

**Framework Recommendation:** **LangGraph** - Cyclic workflow with conditional loops based on quality metrics.

### Pattern 5: Specialized Content Creation

```
Requirements Gathering
    ↓
┌───────────────┼───────────────┐
↓               ↓               ↓
speechwriter-on-call  MeetingDebriefWriter  classifieds-listing-writer
    ↓               ↓               ↓
└───────────────┴───────────────┘
        ↓
Appropriate Editor
        ↓
Final Review
```

**Use Case:** Specialized content types requiring domain-specific generation.

**Framework Recommendation:** **CrewAI** - Clear role specialization for different content types.

## Recommended Multi-Agent Frameworks

### Primary Recommendations

1. **CrewAI**
   - **Best for:** Sequential content workflows, editorial pipelines
   - **Why:** Role-based agents, clear task dependencies, process management
   - **Use when:** Building traditional editorial and content production workflows

2. **AutoGen**
   - **Best for:** Collaborative editing, peer review processes
   - **Why:** Multi-agent conversations, iterative refinement
   - **Use when:** Content requires discussion and collaborative improvement

3. **LangGraph**
   - **Best for:** Adaptive content workflows, multi-format repurposing
   - **Why:** Conditional branching, state management, cyclic editing
   - **Use when:** Complex content transformation and adaptation needs

### Secondary Recommendations

4. **n8n + LangChain**
   - **Best for:** Automated content pipelines, scheduled publishing
   - **Why:** Visual workflow design, CMS integrations, webhook triggers
   - **Use when:** Automating content production and distribution

5. **Semantic Kernel**
   - **Best for:** Enterprise content management systems
   - **Why:** Plugin architecture, enterprise integrations
   - **Use when:** Integrating with Microsoft ecosystem (SharePoint, Teams)

## Implementation Example

### Blog Production Pipeline

**Agents Involved:**
1. BlogOutlineGenerator
2. Research Agent (from Research cluster)
3. Writing Agent
4. StylisticTextEditor
5. HeadlineCopywriter
6. NativeEnglishEditor

**Orchestration (CrewAI):**

```python
from crewai import Agent, Task, Crew, Process

# Define content agents
outliner = Agent(
    role="Blog Outliner",
    goal="Create comprehensive blog post outlines",
    backstory="Expert content strategist with years of editorial experience",
    tools=[web_search]
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging and informative blog posts",
    backstory="Professional writer specializing in technical content"
)

style_editor = Agent(
    role="Style Editor",
    goal="Enhance writing style and readability",
    backstory="Editorial expert focused on tone and voice consistency"
)

copywriter = Agent(
    role="Headline Writer",
    goal="Create compelling headlines and subheadings",
    backstory="Copywriting specialist with expertise in attention-grabbing headlines"
)

editor = Agent(
    role="Copy Editor",
    goal="Polish content for native English quality",
    backstory="Professional editor ensuring grammatical perfection"
)

# Define tasks
task1 = Task(description="Create outline for blog post about AI agents", agent=outliner)
task2 = Task(description="Write blog post based on outline", agent=writer)
task3 = Task(description="Refine writing style and tone", agent=style_editor)
task4 = Task(description="Create compelling headline and subheadings", agent=copywriter)
task5 = Task(description="Final editing pass for language quality", agent=editor)

# Create crew
crew = Crew(
    agents=[outliner, writer, style_editor, copywriter, editor],
    tasks=[task1, task2, task3, task4, task5],
    process=Process.sequential
)

result = crew.kickoff()
```

## Tool Requirements

Agents in this cluster often require:

- **Text processing** - String manipulation, formatting
- **Web scraping** - Content extraction from websites
- **File I/O** - Reading/writing documents in various formats
- **Grammar checking** - Integration with tools like Grammarly API
- **Plagiarism detection** - Content originality verification
- **Readability analysis** - Flesch-Kincaid, etc.
- **SEO tools** - Keyword analysis, meta tag generation
- **Translation** - Multi-language support for some agents
- **CMS integration** - WordPress, Ghost, Medium APIs

## Scaling Considerations

When deploying this cluster in production:

1. **Content Quality Gates** - Automated quality checks before publishing
2. **Version Control** - Track content revisions and edits
3. **Brand Guidelines** - Enforce tone, style, and voice consistency
4. **SEO Optimization** - Integrate keyword and meta tag validation
5. **Plagiarism Prevention** - Automated originality checks
6. **Publishing Workflows** - Integration with CMS platforms
7. **Content Calendar** - Scheduled production and publishing
8. **Performance Metrics** - Track engagement and content effectiveness

## Integration with Other Clusters

This cluster naturally integrates with:

- **[Research & Knowledge](../research-knowledge/)** - Research agents for fact-checking and sourcing
- **[Business & Productivity](../business-productivity/)** - Marketing and business content
- **[Creative & Entertainment](../creative-entertainment/)** - Creative writing and ideation
- **[Automation & Integration](../automation-integration/)** - Automated publishing workflows
- **[Data & Analysis](../data-analysis/)** - Content performance analytics

## Getting Started

1. Define your content type (blog, email, article, etc.)
2. Start with **BlogOutlineGenerator** or relevant outlining agent
3. Use specialized writing agents for content generation
4. Apply editing layers: **SimpleTextEditor** → **StylisticTextEditor** → **NativeEnglishEditor**
5. Enhance with **HeadlineCopywriter** for headlines
6. Adapt tone with **AcademicToneWriter**, **FormalWritingGenerator**, etc.
7. Format with specialized formatters as needed

## Best Practices

- **Iterative Editing** - Multiple editing passes improve quality
- **Consistent Voice** - Use **DocumentMyWritingStyle** to maintain brand voice
- **Audience Awareness** - Adapt tone based on target audience
- **SEO Integration** - Incorporate keyword research early
- **Fact-Checking** - Integrate research agents for accuracy
- **Readability** - Target appropriate reading level
- **Version Control** - Track changes and maintain revision history
- **Quality Metrics** - Define and measure content quality standards

## Additional Resources

- [Content Marketing Institute](https://contentmarketinginstitute.com/)
- [Grammarly Blog - Writing Best Practices](https://www.grammarly.com/blog/)
- [HubSpot Content Strategy Guide](https://blog.hubspot.com/marketing/content-marketing)
