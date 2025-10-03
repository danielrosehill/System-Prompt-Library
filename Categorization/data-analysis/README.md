# Data & Analysis Cluster

## Overview

This cluster contains system prompts for data processing, organization, analysis, visualization, governance, and data engineering tasks. These agents handle the complete data lifecycle from collection and cleaning to analysis and visualization.

## Core Capabilities

- Data collection and extraction
- Data cleaning and transformation
- Data organization and structuring
- Data analysis and insights
- Data visualization and storytelling
- Data governance and quality
- Context data management
- Database design and management
- Data pipeline development

## Agent Roles in This Cluster

### Data Collection & Extraction Agents

- [DataSourceScout](../../system-prompts/json/DataSourceScout_270525.json)
- [ContextDataExtractionTool](../../system-prompts/json/ContextDataExtractionTool_270525.json)
- [bilateral-trade-data](../../system-prompts/json/bilateral-trade-data_260925.json)
- [greenhouse-gas-emissions-data-finder](../../system-prompts/json/greenhouse-gas-emissions-data-finder_260925.json)

### Data Organization & Structuring Agents

- [DataOrganisationSidekick](../../system-prompts/json/DataOrganisationSidekick_270525.json)
- [ContextDataChunker](../../system-prompts/json/ContextDataChunker_270525.json)
- [context-data-condenser](../../system-prompts/json/context-data-condenser_270925.json)
- [DataDictionaryAssistant](../../system-prompts/json/DataDictionaryAssistant_270525.json)
- [DataFieldsIdeationAssistant](../../system-prompts/json/DataFieldsIdeationAssistant_270525.json)

### Data Quality & Governance Agents

- [DataGovernanceBackgroundChecker](../../system-prompts/json/DataGovernanceBackgroundChecker_270525.json)
- [DuplicateDataDetector](../../system-prompts/json/DuplicateDataDetector_270525.json)
- [DataSafehouse](../../system-prompts/json/DataSafehouse_270525.json)

### Data Analysis Agents

- [DataClusteringAssistant_EntityGrouping](../../system-prompts/json/DataClusteringAssistant_EntityGrouping_270525.json)
- [DataTrendsIdentifier](../../system-prompts/json/DataTrendsIdentifier_270525.json)
- [DataRelationshipUtility](../../system-prompts/json/DataRelationshipUtility_270525.json)
- [evidence-based-analysis](../../system-prompts/json/evidence-based-analysis_270925.json)

### Data Visualization Agents

- [DataVisualizationandStorytelling](../../system-prompts/json/DataVisualizationandStorytelling_270525.json)
- [data-visualisation-storytelling-guide](../../system-prompts/json/data-visualisation-storytelling-guide_260925.json)
- [DataVisualizationIdeator](../../system-prompts/json/DataVisualizationIdeator_270525.json)
- [DataDashboardsInfo](../../system-prompts/json/DataDashboardsInfo_270525.json)

### Context Data Management Agents

- [ContextDataDevelopmentHelper](../../system-prompts/json/ContextDataDevelopmentHelper_270525.json)
- [ContextDataInterviewer](../../system-prompts/json/ContextDataInterviewer_270525.json)
- [ContextDataJSONGenerator](../../system-prompts/json/ContextDataJSONGenerator_270525.json)
- [ContextData_Reformatter_Only](../../system-prompts/json/ContextData_Reformatter_Only_270525.json)
- [DictatedDataFormatter](../../system-prompts/json/DictatedDataFormatter_270525.json)

### Data Pipeline & Engineering Agents

- [DataPipelineTestingAgent](../../system-prompts/json/DataPipelineTestingAgent_270525.json)
- [DataTagGenerator](../../system-prompts/json/DataTagGenerator_270525.json)
- [DataArchivalAndPreservation](../../system-prompts/json/DataArchivalAndPreservation_270525.json)

### Data Tools & Apps Discovery

- [DataAndDatabaseAppsFinder](../../system-prompts/json/DataAndDatabaseAppsFinder_270525.json)
- [ai-for-data-workloads](../../system-prompts/json/ai-for-data-workloads_270925.json)

## Multi-Agent Orchestration Patterns

### Pattern 1: Complete Data Analytics Pipeline

```
DataSourceScout (Discovery)
    ↓
ContextDataExtractionTool (Collection)
    ↓
DuplicateDataDetector (Cleaning)
    ↓
DataOrganisationSidekick (Structuring)
    ↓
DataClusteringAssistant + DataTrendsIdentifier (Analysis)
    ↓
DataVisualizationandStorytelling (Visualization)
```

**Use Case:** End-to-end data analysis from raw data to insights.

**Framework Recommendation:** **CrewAI** - Sequential pipeline with clear stages and role separation.

### Pattern 2: Data Governance & Quality Loop

```
DataGovernanceBackgroundChecker (Policy Check)
    ↓
DuplicateDataDetector (Quality Scan)
    ↓
DataDictionaryAssistant (Documentation)
    ↓
DataSafehouse (Security & Storage)
    ↓
DataArchivalAndPreservation (Long-term Management)
```

**Use Case:** Ensuring data quality, compliance, and governance.

**Framework Recommendation:** **Apache Airflow + LangChain** - Robust data pipeline orchestration with scheduling.

### Pattern 3: Context Data Management Workflow

```
ContextDataInterviewer (Requirements Gathering)
    ↓
ContextDataExtractionTool (Data Collection)
    ↓
context-data-condenser + ContextDataChunker (Processing)
    ↓
ContextDataJSONGenerator (Structuring)
    ↓
ContextData_Reformatter_Only (Final Formatting)
```

**Use Case:** Building context data for RAG applications and AI systems.

**Framework Recommendation:** **LangGraph** - State management for iterative context refinement.

### Pattern 4: Collaborative Data Analysis

```
User Query → DataSourceScout
                ↓
    ┌───────────┴───────────┐
    ↓                       ↓
DataTrendsIdentifier    DataRelationshipUtility
    ↓                       ↓
    └───────────┬───────────┘
                ↓
    evidence-based-analysis (Synthesis)
                ↓
    DataVisualizationIdeator
```

**Use Case:** Multi-perspective data analysis with collaborative insights.

**Framework Recommendation:** **AutoGen** - Collaborative agent discussions for comprehensive analysis.

### Pattern 5: Real-Time Data Dashboard Pipeline

```
Data Stream → DataPipelineTestingAgent (Validation)
                    ↓
            DataTrendsIdentifier (Analysis)
                    ↓
            DataDashboardsInfo (Dashboard Design)
                    ↓
            DataVisualizationandStorytelling (Visualization)
```

**Use Case:** Real-time analytics dashboards and monitoring.

**Framework Recommendation:** **n8n + LangChain** - Event-driven workflows with webhook triggers.

## Recommended Multi-Agent Frameworks

### Primary Recommendations

1. **CrewAI**
   - **Best for:** Sequential data pipelines, structured analysis workflows
   - **Why:** Clear role separation, task dependencies, process management
   - **Use when:** Building traditional ETL/ELT pipelines with AI agents

2. **Apache Airflow + LangChain**
   - **Best for:** Production data pipelines, scheduled workflows
   - **Why:** Industry-standard orchestration, robust scheduling, monitoring
   - **Use when:** Enterprise data engineering with AI-enhanced processing

3. **LangGraph**
   - **Best for:** Iterative data exploration, adaptive analysis
   - **Why:** State management, cyclic workflows, conditional branching
   - **Use when:** Exploratory data analysis requiring adaptive approaches

### Secondary Recommendations

4. **AutoGen**
   - **Best for:** Collaborative data analysis, multi-perspective insights
   - **Why:** Agent conversations, collaborative problem-solving
   - **Use when:** Complex analysis requiring multiple analytical approaches

5. **Prefect**
   - **Best for:** Modern data pipeline orchestration
   - **Why:** Dynamic workflows, easy monitoring, cloud-native
   - **Use when:** Building cloud-based data pipelines with AI agents

6. **n8n**
   - **Best for:** Visual workflow design, rapid prototyping
   - **Why:** Low-code interface, extensive integrations, event triggers
   - **Use when:** Business users building data workflows visually

## Implementation Example

### Data Analysis Pipeline with Visualization

**Agents Involved:**
1. DataSourceScout
2. ContextDataExtractionTool
3. DataOrganisationSidekick
4. DataTrendsIdentifier
5. DataVisualizationandStorytelling

**Orchestration (CrewAI):**

```python
from crewai import Agent, Task, Crew, Process

# Define data agents
data_scout = Agent(
    role="Data Source Scout",
    goal="Identify and locate relevant data sources",
    backstory="Expert in data discovery and source evaluation",
    tools=[web_search, api_connector]
)

data_extractor = Agent(
    role="Data Extractor",
    goal="Extract and collect data from identified sources",
    backstory="Specialist in data extraction and API integration"
)

data_organizer = Agent(
    role="Data Organizer",
    goal="Structure and clean extracted data",
    backstory="Expert in data organization and normalization"
)

data_analyst = Agent(
    role="Trends Analyst",
    goal="Identify patterns and trends in data",
    backstory="Data scientist specializing in trend analysis"
)

visualizer = Agent(
    role="Data Storyteller",
    goal="Create compelling visualizations and narratives",
    backstory="Expert in data visualization and storytelling"
)

# Define tasks
task1 = Task(description="Find data sources for market analysis", agent=data_scout)
task2 = Task(description="Extract data from identified sources", agent=data_extractor)
task3 = Task(description="Clean and organize data", agent=data_organizer)
task4 = Task(description="Analyze trends and patterns", agent=data_analyst)
task5 = Task(description="Create visualizations and insights report", agent=visualizer)

# Create crew
crew = Crew(
    agents=[data_scout, data_extractor, data_organizer, data_analyst, visualizer],
    tasks=[task1, task2, task3, task4, task5],
    process=Process.sequential
)

result = crew.kickoff()
```

## Tool Requirements

Agents in this cluster often require:

- **Database connections** - SQL, NoSQL, graph databases
- **API access** - REST APIs, GraphQL for data sources
- **File I/O** - CSV, JSON, Parquet, Excel reading/writing
- **Data processing libraries** - Pandas, NumPy equivalents via tools
- **Visualization tools** - Chart generation, dashboard creation
- **Statistical analysis** - Mathematical computations
- **Web scraping** - Data extraction from websites
- **Cloud storage** - S3, GCS, Azure Blob integration

## Scaling Considerations

When deploying this cluster in production:

1. **Data Volume** - Handle large datasets with chunking and streaming
2. **Performance** - Optimize query patterns and caching
3. **Security** - Encrypt sensitive data, manage access controls
4. **Compliance** - GDPR, CCPA, industry-specific regulations
5. **Monitoring** - Track pipeline performance and data quality
6. **Error Handling** - Robust retry logic and failure recovery
7. **Cost Management** - Optimize API calls and compute resources
8. **Data Lineage** - Track data transformations and provenance

## Integration with Other Clusters

This cluster naturally integrates with:

- **[Research & Knowledge](../research-knowledge/)** - Deep research on data sources and methodologies
- **[Code & Development](../code-development/)** - Code generation for data processing
- **[Business & Productivity](../business-productivity/)** - Business intelligence and analytics
- **[Automation & Integration](../automation-integration/)** - Automated data pipelines
- **[Technical Infrastructure](../technical-infrastructure/)** - Data infrastructure management

## Getting Started

1. Start with **DataSourceScout** to identify data sources
2. Use **ContextDataExtractionTool** for data collection
3. Clean with **DuplicateDataDetector** and organize with **DataOrganisationSidekick**
4. Analyze with **DataTrendsIdentifier** and **DataClusteringAssistant**
5. Visualize with **DataVisualizationandStorytelling**
6. Document with **DataDictionaryAssistant**
7. Govern with **DataGovernanceBackgroundChecker**

## Best Practices

- **Data Quality First** - Validate and clean early in pipeline
- **Incremental Processing** - Process data in batches for scalability
- **Metadata Management** - Document data lineage and transformations
- **Version Control** - Track data schema and transformation changes
- **Testing** - Use DataPipelineTestingAgent for validation
- **Monitoring** - Real-time alerts for data quality issues
- **Documentation** - Maintain data dictionaries and governance docs

## Additional Resources

- [Data Pipeline Design Patterns](https://www.oreilly.com/library/view/data-pipelines-pocket/9781492087823/)
- [Apache Airflow Documentation](https://airflow.apache.org/)
- [LangChain Data Processing](https://python.langchain.com/docs/use_cases/data_generation)
