# API Reference

## Agents

### DocumentOrchestrator

Main coordinator for multi-agent workflows.

```python
from agents import DocumentOrchestrator

orchestrator = DocumentOrchestrator(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**process_message(user_message: str) -> str**

Process a user message and coordinate agents automatically.

```python
response = orchestrator.process_message(
    "Research the latest AI developments"
)
```

**get_conversation_history() -> List[Dict[str, str]]**

Get conversation history.

```python
history = orchestrator.get_conversation_history()
```

**clear_history()**

Clear conversation history.

```python
orchestrator.clear_history()
```

---

### WebResearcherAgent

Specialized agent for web research.

```python
from agents import WebResearcherAgent

agent = WebResearcherAgent(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**research(query: str, context: Dict[str, Any] = None) -> Dict[str, Any]**

Conduct web research on a query.

```python
result = agent.research(
    query="AI agents 2025",
    context={"focus": "latest developments"}
)
```

**validate_source(url: str) -> Dict[str, Any]**

Validate credibility of a source.

```python
validation = agent.validate_source("https://example.com/article")
```

**extract_information(content: str, extraction_goals: List[str]) -> Dict[str, Any]**

Extract specific information from content.

```python
extracted = agent.extract_information(
    content=article_text,
    extraction_goals=["key findings", "methodology"]
)
```

---

### DocumentAnalyzerAgent

Analyzes documents and extracts insights.

```python
from agents import DocumentAnalyzerAgent

agent = DocumentAnalyzerAgent(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**analyze_document(content: str, analysis_type: str = "general", context: Dict[str, Any] = None) -> Dict[str, Any]**

Analyze a document.

```python
analysis = agent.analyze_document(
    content=document_text,
    analysis_type="research",
    context={"domain": "AI"}
)
```

**compare_documents(documents: List[Dict[str, str]]) -> Dict[str, Any]**

Compare multiple documents.

```python
comparison = agent.compare_documents([
    {"title": "Doc 1", "content": "..."},
    {"title": "Doc 2", "content": "..."}
])
```

**extract_structured_data(content: str, schema: Dict[str, Any]) -> Dict[str, Any]**

Extract data according to schema.

```python
data = agent.extract_structured_data(
    content=document_text,
    schema={"fields": ["author", "date", "summary"]}
)
```

**identify_relationships(content: str) -> Dict[str, Any]**

Identify concept relationships.

```python
relationships = agent.identify_relationships(document_text)
```

---

### SummaryGeneratorAgent

Creates summaries and reports.

```python
from agents import SummaryGeneratorAgent

agent = SummaryGeneratorAgent(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**generate_summary(content: str, summary_type: str = "standard", length: str = "medium", context: Dict[str, Any] = None) -> Dict[str, Any]**

Generate a summary.

```python
summary = agent.generate_summary(
    content=long_document,
    summary_type="executive",
    length="brief",
    context={"audience": "executives"}
)
```

**generate_multi_level_summary(content: str) -> Dict[str, Any]**

Generate summaries at multiple levels.

```python
summaries = agent.generate_multi_level_summary(content)
# Returns: executive, standard, and detailed summaries
```

**generate_report(research_data: Dict[str, Any], report_type: str = "research_report", target_audience: str = "general") -> Dict[str, Any]**

Generate a comprehensive report.

```python
report = agent.generate_report(
    research_data=findings,
    report_type="research_report",
    target_audience="technical"
)
```

**synthesize_multiple_sources(sources: List[Dict[str, Any]]) -> Dict[str, Any]**

Synthesize information from multiple sources.

```python
synthesis = agent.synthesize_multiple_sources([
    {"title": "Source 1", "content": "..."},
    {"title": "Source 2", "content": "..."}
])
```

---

### QAAgent

Answers questions using context.

```python
from agents import QAAgent

agent = QAAgent(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**answer_question(question: str, context: Optional[str] = None, conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]**

Answer a question.

```python
answer = agent.answer_question(
    question="What are AI agents?",
    context=background_text,
    conversation_history=prev_messages
)
```

**explain_concept(concept: str, depth: str = "standard", audience: str = "general") -> Dict[str, Any]**

Explain a concept.

```python
explanation = agent.explain_concept(
    concept="Multi-agent systems",
    depth="detailed",
    audience="technical"
)
```

**compare_concepts(concept1: str, concept2: str) -> Dict[str, Any]**

Compare two concepts.

```python
comparison = agent.compare_concepts(
    "Reactive agents",
    "Deliberative agents"
)
```

**generate_faq(topic: str, num_questions: int = 5) -> Dict[str, Any]**

Generate FAQ for a topic.

```python
faq = agent.generate_faq(
    topic="Claude Agent SDK",
    num_questions=10
)
```

---

### CitationManagerAgent

Manages citations and references.

```python
from agents import CitationManagerAgent

agent = CitationManagerAgent(
    api_key: Optional[str] = None,
    model: str = "claude-sonnet-4-5-20250929"
)
```

#### Methods

**create_citation(source_info: Dict[str, Any], citation_style: str = "APA", citation_type: str = "full") -> Dict[str, Any]**

Create a citation.

```python
citation = agent.create_citation(
    source_info={
        "author": "Smith, J.",
        "year": "2024",
        "title": "AI Agents",
        "journal": "AI Research"
    },
    citation_style="APA"
)
```

**generate_bibliography(citations: List[Dict[str, Any]], style: str = "APA", organize_by: str = "alphabetical") -> Dict[str, Any]**

Generate bibliography.

```python
bibliography = agent.generate_bibliography(
    citations=citation_list,
    style="MLA",
    organize_by="chronological"
)
```

**extract_citation_info(source_text: str, source_url: Optional[str] = None) -> Dict[str, Any]**

Extract citation info from text.

```python
info = agent.extract_citation_info(
    source_text=article_text,
    source_url="https://example.com"
)
```

**validate_citations(citations: List[str], style: str = "APA") -> Dict[str, Any]**

Validate citations.

```python
validation = agent.validate_citations(
    citations=["Smith (2024)...", "Jones et al. (2023)..."],
    style="APA"
)
```

**convert_citation_style(citation: str, from_style: str, to_style: str) -> Dict[str, Any]**

Convert citation style.

```python
converted = agent.convert_citation_style(
    citation="Smith, J. (2024)...",
    from_style="APA",
    to_style="MLA"
)
```

---

## Agent Coordinator

### AgentCoordinator

Manages agent handoffs and workflows.

```python
from agents import AgentCoordinator

coordinator = AgentCoordinator(api_key: Optional[str] = None)
```

#### Methods

**execute_handoff(handoff: AgentHandoff) -> AgentResponse**

Execute a single handoff.

```python
response = await coordinator.execute_handoff(
    AgentHandoff(
        agent_type=AgentType.WEB_RESEARCHER,
        task="Research AI trends",
        context={},
        priority=1
    )
)
```

**execute_sequential_handoffs(handoffs: List[AgentHandoff]) -> List[AgentResponse]**

Execute handoffs sequentially.

```python
results = await coordinator.execute_sequential_handoffs([
    handoff1, handoff2, handoff3
])
```

**execute_parallel_handoffs(handoffs: List[AgentHandoff]) -> List[AgentResponse]**

Execute handoffs in parallel.

```python
results = await coordinator.execute_parallel_handoffs([
    handoff1, handoff2, handoff3
])
```

**execute_plan(plan: HandoffPlan) -> List[AgentResponse]**

Execute a handoff plan.

```python
plan = HandoffPlan(
    strategy=HandoffStrategy.SEQUENTIAL,
    agents=[handoff1, handoff2],
    timeout=300
)
results = await coordinator.execute_plan(plan)
```

**create_research_workflow(query: str) -> HandoffPlan**

Create a research workflow.

```python
plan = coordinator.create_research_workflow(
    "AI developments 2025"
)
```

**create_qa_workflow(question: str, context: str = None) -> HandoffPlan**

Create a Q&A workflow.

```python
plan = coordinator.create_qa_workflow(
    question="What are agents?",
    context=document_text
)
```

**get_handoff_history() -> List[Dict[str, Any]]**

Get handoff history.

```python
history = coordinator.get_handoff_history()
```

---

## Data Classes

### AgentType (Enum)

```python
class AgentType(Enum):
    WEB_RESEARCHER = "web_researcher"
    DOCUMENT_ANALYZER = "document_analyzer"
    SUMMARY_GENERATOR = "summary_generator"
    QA_AGENT = "qa_agent"
    CITATION_MANAGER = "citation_manager"
```

### AgentHandoff

```python
@dataclass
class AgentHandoff:
    agent_type: AgentType
    task: str
    context: Dict[str, Any]
    priority: int = 0
```

### AgentResponse

```python
@dataclass
class AgentResponse:
    agent_type: AgentType
    success: bool
    result: Any
    error: Optional[str] = None
    next_handoff: Optional[AgentHandoff] = None
```

### HandoffStrategy (Enum)

```python
class HandoffStrategy(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    CHAIN = "chain"
```

### HandoffPlan

```python
@dataclass
class HandoffPlan:
    strategy: HandoffStrategy
    agents: List[AgentHandoff]
    merge_results: bool = True
    timeout: int = 300
```

---

## MCP Servers

All MCP servers follow the Model Context Protocol specification.

### Filesystem MCP Server

**Tools**: `read_file`, `write_file`, `list_files`, `delete_file`

### Web Search MCP Server

**Tools**: `search_web`, `extract_content`, `extract_links`

### Database MCP Server

**Tools**: `store_document`, `search_documents`, `get_document`, `store_citation`, `store_qa`, `get_qa_history`

### GitHub MCP Server

**Tools**: `search_repositories`, `get_repository_info`, `get_file_content`, `list_repository_files`, `search_code`
