# CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Table of Contents
- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Development Commands](#development-commands)
- [Configuration](#configuration)
- [Core Components](#core-components)
- [Development Workflows](#development-workflows)
- [Code Patterns](#code-patterns)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

**Research Hub** is a production-ready multi-agent knowledge management and research assistant system built with the Claude Agent SDK.

### Key Features
- **6 Specialized Agents**: Orchestrator + 5 sub-agents (WebResearcher, DocumentAnalyzer, SummaryGenerator, QAAgent, CitationManager)
- **4 MCP Servers**: Filesystem, WebSearch, Database (SQLite + ChromaDB), GitHub
- **4 Handoff Strategies**: Sequential, Parallel, Conditional, Chain
- **Streamlit Frontend**: Interactive web UI with chat, workflow selection, and metrics
- **Full Test Coverage**: Unit and integration tests with pytest
- **Comprehensive Documentation**: Architecture, API reference, workflow guides

### Tech Stack
- **Framework**: Claude Agent SDK (≥0.1.0), Anthropic SDK (≥0.40.0)
- **Protocol**: Model Context Protocol (MCP ≥1.0.0)
- **Frontend**: Streamlit (≥1.39.0)
- **Storage**: SQLite + ChromaDB vector database
- **Models**: Claude Sonnet 4.5 (default), Claude Opus 4 (fallback)

---

## Quick Start

### Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run quick start script (recommended)
./run.sh

# OR run components individually:

# 4a. Run demo to verify setup
python demo.py

# 4b. Run Streamlit frontend
streamlit run frontend/app.py

# 4c. Run example scripts
python examples/basic_usage.py
python examples/advanced_workflows.py
```

### Quick Demo
```bash
# demo.py shows 4 usage patterns:
# 1. Orchestrator auto mode
# 2. Research workflow (sequential)
# 3. Q&A workflow
# 4. Parallel execution
python demo.py
```

---

## Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────┐
│      DocumentOrchestrator               │
│   (Main coordinator, analyzes requests) │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│        AgentCoordinator                  │
│  (Manages handoffs & execution strategy) │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         5 Specialized Sub-Agents         │
├──────────────────────────────────────────┤
│ • WebResearcher      (web search)        │
│ • DocumentAnalyzer   (analysis)          │
│ • SummaryGenerator   (synthesis)         │
│ • QAAgent            (Q&A)               │
│ • CitationManager    (citations)         │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│          4 MCP Servers                   │
├──────────────────────────────────────────┤
│ • Filesystem   (file ops)                │
│ • WebSearch    (web research)            │
│ • Database     (SQLite + vector DB)      │
│ • GitHub       (repo/docs access)        │
└──────────────────────────────────────────┘
```

### Key Workflows

1. **Research Workflow**: WebResearcher → DocumentAnalyzer → SummaryGenerator
2. **Q&A Workflow**: DocumentAnalyzer → QAAgent
3. **Summary Workflow**: SummaryGenerator (standalone)
4. **Comprehensive Workflow**: All agents in sequence
5. **Parallel Research**: Multiple topics → parallel execution → synthesis

### Handoff Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **SEQUENTIAL** | Agents execute one after another, output → input | Research pipeline |
| **PARALLEL** | Multiple agents run simultaneously, results merged | Multi-topic research |
| **CONDITIONAL** | Next agent selected based on previous results | Adaptive workflows |
| **CHAIN** | Results flow through pipeline, each agent transforms | Data processing |

---

## Directory Structure

### Complete File Inventory (~2,700 lines of Python)

```
claude-automatic-sniffle/
│
├── agents/                          # Core multi-agent system (8 files, ~1,700 LOC)
│   ├── __init__.py                 # Exports (24 LOC)
│   ├── orchestrator.py             # Main coordinator (245 LOC)
│   ├── agent_coordinator.py        # Handoff manager (325 LOC)
│   ├── web_researcher.py           # Web research (160 LOC)
│   ├── document_analyzer.py        # Document analysis (191 LOC)
│   ├── summary_generator.py        # Summary generation (239 LOC)
│   ├── qa_agent.py                 # Q&A agent (229 LOC)
│   └── citation_manager.py         # Citation formatting (283 LOC)
│
├── mcp_servers/                     # MCP protocol servers (5 files, ~1,000 LOC)
│   ├── __init__.py                 # Module init (13 LOC)
│   ├── filesystem_server.py        # File operations (161 LOC)
│   ├── websearch_server.py         # Web search (183 LOC)
│   ├── database_server.py          # SQLite + ChromaDB (339 LOC)
│   └── github_server.py            # GitHub integration (309 LOC)
│
├── prompts/                         # Agent system prompts (7 files)
│   ├── __init__.py                 # Prompt exports
│   ├── orchestrator_prompt.txt     # Orchestrator instructions
│   ├── web_researcher_prompt.txt   # Web research guidelines
│   ├── document_analyzer_prompt.txt # Analysis instructions
│   ├── summary_generator_prompt.txt # Summary guidelines
│   ├── qa_agent_prompt.txt         # Q&A behavior
│   └── citation_manager_prompt.txt # Citation rules
│
├── config/                          # Configuration files
│   ├── agent_configs.yaml          # Agent settings (2.8 KB)
│   ├── models.yaml                 # Model config (2.6 KB)
│   └── mcp_config.json             # MCP server config (2.7 KB)
│
├── frontend/                        # Streamlit web UI
│   ├── app.py                      # Main app (10.2 KB)
│   └── components/
│       ├── __init__.py             # Component exports
│       └── agent_visualizer.py     # Workflow visualizer (2.9 KB)
│
├── tests/                           # Test suite
│   ├── __init__.py                 # Package marker
│   ├── conftest.py                 # pytest fixtures (1.4 KB)
│   ├── test_agents.py              # Agent unit tests (4.4 KB)
│   └── test_handoffs.py            # Handoff integration tests (5.9 KB)
│
├── docs/                            # Documentation
│   ├── architecture.md             # System design (5.7 KB)
│   ├── agent_workflows.md          # Workflow patterns (8.0 KB)
│   └── api_reference.md            # API docs (10.4 KB)
│
├── examples/                        # Usage examples
│   ├── basic_usage.py              # Simple examples (4.9 KB)
│   └── advanced_workflows.py       # Complex patterns (6.8 KB)
│
├── .env.example                     # Environment template (726 bytes)
├── requirements.txt                 # Dependencies (39 lines)
├── demo.py                          # Quick demo script (4.9 KB)
├── run.sh                           # Quick start script (941 bytes)
├── README.md                        # Project readme (7.7 KB)
├── AGENTS.md                        # Agent details (2.5 KB)
├── TEST_RESULTS.md                  # Test coverage (3.7 KB)
├── CLAUDE.md                        # This file
└── LICENSE                          # Apache 2.0 (11 KB)
```

---

## Development Commands

### Setup & Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Install with development tools
pip install -r requirements.txt pytest pytest-cov pytest-asyncio

# Setup environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY
```

### Running the Application
```bash
# Quick start (checks env, installs deps, runs frontend)
./run.sh

# Run Streamlit frontend
streamlit run frontend/app.py

# Run demo script (4 demo scenarios)
python demo.py

# Run example scripts
python examples/basic_usage.py          # Basic patterns
python examples/advanced_workflows.py   # Advanced patterns
```

### Testing
```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_agents.py          # Agent unit tests
pytest tests/test_handoffs.py        # Handoff integration tests

# Run with coverage report
pytest --cov=agents tests/
pytest --cov=agents --cov=mcp_servers tests/

# Run with verbose output
pytest -v

# Run specific test by name
pytest tests/test_agents.py::test_web_researcher -v
```

### Development
```bash
# Check Python syntax
python -m py_compile agents/*.py

# Format code (if using black/autopep8)
black agents/ mcp_servers/ tests/

# Type checking (if using mypy)
mypy agents/ mcp_servers/

# Linting (if using pylint/flake8)
pylint agents/ mcp_servers/
flake8 agents/ mcp_servers/
```

---

## Configuration

### Environment Variables (.env)

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here        # Claude API key

# Optional
GITHUB_TOKEN=your_github_token_here        # For GitHub MCP server

# Database
DATABASE_PATH=./knowledge_base/research_hub.db

# Frontend
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# MCP Servers
MCP_FILESYSTEM_PATH=./knowledge_base
MCP_LOG_LEVEL=INFO

# Models
DEFAULT_MODEL=claude-sonnet-4-5-20250929   # Primary model
FALLBACK_MODEL=claude-opus-4-20250514      # Fallback model

# Performance
MAX_CONCURRENT_AGENTS=5                    # Max parallel agents
REQUEST_TIMEOUT=300                        # Request timeout (seconds)
RETRY_ATTEMPTS=3                           # Retry failed requests

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/research_hub.log
```

### Agent Configuration (config/agent_configs.yaml)

Each agent has:
- **model**: Claude model to use
- **max_tokens**: Token limit (1024-4096)
- **temperature**: Randomness (0.0-1.0)
- **timeout**: Request timeout in seconds
- **tools**: List of available MCP tools

Example:
```yaml
web_researcher:
  model: claude-sonnet-4-5-20250929
  max_tokens: 2048
  temperature: 0.7
  timeout: 120
  tools:
    - web_search
    - extract_content
    - validate_sources
```

### Model Configuration (config/models.yaml)

```yaml
models:
  primary:
    name: claude-sonnet-4-5-20250929
    max_tokens: 4096
    context_window: 200000
  fallback:
    name: claude-opus-4-20250514
    max_tokens: 4096
    context_window: 200000

performance:
  max_retries: 3
  timeout: 300
  concurrent_limit: 5
```

### MCP Server Configuration (config/mcp_config.json)

Defines tool mappings for each MCP server:
```json
{
  "filesystem": {
    "command": "python",
    "args": ["mcp_servers/filesystem_server.py"],
    "tools": ["read_file", "write_file", "list_files", "search_files"]
  }
}
```

---

## Core Components

### Data Structures

#### AgentType (Enum)
```python
class AgentType(Enum):
    WEB_RESEARCHER = "web_researcher"
    DOCUMENT_ANALYZER = "document_analyzer"
    SUMMARY_GENERATOR = "summary_generator"
    QA_AGENT = "qa_agent"
    CITATION_MANAGER = "citation_manager"
```

#### AgentHandoff (Dataclass)
```python
@dataclass
class AgentHandoff:
    agent_type: AgentType      # Target agent
    task: str                  # Task description
    context: Dict[str, Any]    # Context data
    priority: int = 1          # Priority (1-10)
    metadata: Optional[Dict] = None
```

#### AgentResponse (Dataclass)
```python
@dataclass
class AgentResponse:
    agent_type: AgentType      # Responding agent
    success: bool              # Success flag
    result: Any                # Result data
    error: Optional[str]       # Error message
    metadata: Dict[str, Any]   # Additional metadata
    execution_time: float      # Execution time (seconds)
```

#### HandoffStrategy (Enum)
```python
class HandoffStrategy(Enum):
    SEQUENTIAL = "sequential"   # One after another
    PARALLEL = "parallel"       # Simultaneous execution
    CONDITIONAL = "conditional" # Based on conditions
    CHAIN = "chain"            # Pipeline with transforms
```

### Agent Classes

#### DocumentOrchestrator (agents/orchestrator.py:245)
Main coordinator that analyzes incoming requests and delegates to appropriate agents.

**Key Methods:**
- `process_message(message: str) -> str`: Process user message
- `analyze_request(message: str) -> List[AgentHandoff]`: Determine required agents
- `delegate_to_coordinator(handoffs: List[AgentHandoff]) -> str`: Execute handoffs

#### AgentCoordinator (agents/agent_coordinator.py:325)
Manages agent handoffs and execution strategies.

**Key Methods:**
- `execute_handoff(handoff: AgentHandoff) -> AgentResponse`: Execute single handoff
- `execute_plan(plan: ExecutionPlan) -> List[AgentResponse]`: Execute workflow plan
- `execute_parallel_handoffs(handoffs: List[AgentHandoff]) -> List[AgentResponse]`: Parallel execution
- `create_research_workflow(query: str) -> ExecutionPlan`: Create research plan
- `create_qa_workflow(question: str, context: str) -> ExecutionPlan`: Create Q&A plan
- `create_comprehensive_workflow(query: str) -> ExecutionPlan`: Create full pipeline

#### Specialized Agents

| Agent | File | LOC | Purpose | Tools |
|-------|------|-----|---------|-------|
| **WebResearcher** | web_researcher.py | 160 | Web search, source validation, content extraction | web_search, extract_content, validate_sources |
| **DocumentAnalyzer** | document_analyzer.py | 191 | Document analysis, insight extraction, sentiment analysis | read_file, analyze_content, extract_entities |
| **SummaryGenerator** | summary_generator.py | 239 | Multi-level summaries, executive reports, synthesis | summarize, generate_report, synthesize_data |
| **QAAgent** | qa_agent.py | 229 | Question answering, concept explanation | answer_question, explain_concept, find_evidence |
| **CitationManager** | citation_manager.py | 283 | Citation formatting (APA, MLA, Chicago, IEEE, Harvard) | format_citation, validate_citation, generate_bibliography |

### MCP Servers

#### FilesystemServer (mcp_servers/filesystem_server.py:161)
File operations and knowledge base management.

**Tools:**
- `read_file(path: str)`: Read file contents
- `write_file(path: str, content: str)`: Write file
- `list_files(directory: str)`: List directory contents
- `search_files(pattern: str)`: Search by pattern
- `delete_file(path: str)`: Delete file

#### WebSearchServer (mcp_servers/websearch_server.py:183)
Web search and content extraction.

**Tools:**
- `web_search(query: str, num_results: int)`: Search web
- `extract_content(url: str)`: Extract webpage content
- `validate_source(url: str)`: Validate source credibility

#### DatabaseServer (mcp_servers/database_server.py:339)
SQLite storage with ChromaDB vector database integration.

**Tools:**
- `store_document(doc: Dict)`: Store document
- `query_documents(query: str)`: Full-text search
- `vector_search(embedding: List[float])`: Vector similarity search
- `update_document(id: str, updates: Dict)`: Update document
- `delete_document(id: str)`: Delete document

#### GitHubServer (mcp_servers/github_server.py:309)
GitHub repository access and documentation retrieval.

**Tools:**
- `get_repository(owner: str, repo: str)`: Get repo info
- `search_code(query: str, repo: str)`: Search code
- `get_file_content(path: str, repo: str)`: Get file contents
- `list_repository_files(repo: str)`: List files

---

## Development Workflows

### Adding New Agents

1. **Create agent class** in `agents/{agent_name}.py`:
```python
from typing import Dict, Any
from .orchestrator import AgentResponse, AgentType

class MyNewAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def execute(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        # Implementation
        return AgentResponse(
            agent_type=AgentType.MY_NEW_AGENT,
            success=True,
            result={"data": "..."},
            error=None,
            metadata={},
            execution_time=0.0
        )
```

2. **Add system prompt** to `prompts/{agent_name}_prompt.txt`:
```txt
You are a specialized agent for [purpose].

Your responsibilities:
- Task 1
- Task 2

Guidelines:
- Guideline 1
- Guideline 2
```

3. **Update AgentType enum** in `agents/orchestrator.py`:
```python
class AgentType(Enum):
    # ... existing agents ...
    MY_NEW_AGENT = "my_new_agent"
```

4. **Add configuration** to `config/agent_configs.yaml`:
```yaml
my_new_agent:
  model: claude-sonnet-4-5-20250929
  max_tokens: 2048
  temperature: 0.7
  timeout: 120
  tools:
    - tool1
    - tool2
```

5. **Register in AgentCoordinator** in `agents/agent_coordinator.py`:
```python
def _initialize_agents(self):
    # ... existing agents ...
    self.agents[AgentType.MY_NEW_AGENT] = MyNewAgent(
        self.config['my_new_agent']
    )
```

6. **Export in module** in `agents/__init__.py`:
```python
from .my_new_agent import MyNewAgent
```

7. **Add unit tests** in `tests/test_agents.py`:
```python
async def test_my_new_agent():
    agent = MyNewAgent(config)
    response = await agent.execute("test task", {})
    assert response.success
```

### Adding New MCP Servers

1. **Implement server** in `mcp_servers/{server_name}_server.py`:
```python
from typing import List, Dict, Any

class MyMCPServer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "my_tool",
                "description": "Tool description",
                "parameters": {...}
            }
        ]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if name == "my_tool":
            return self._my_tool(arguments)
        raise ValueError(f"Unknown tool: {name}")

    def _my_tool(self, args: Dict[str, Any]) -> Any:
        # Implementation
        return {"result": "..."}
```

2. **Add configuration** to `config/mcp_config.json`:
```json
{
  "my_mcp_server": {
    "command": "python",
    "args": ["mcp_servers/my_mcp_server.py"],
    "tools": ["my_tool"]
  }
}
```

3. **Update agent tool permissions** in `config/agent_configs.yaml`:
```yaml
web_researcher:
  tools:
    - my_tool  # Add to relevant agents
```

4. **Add tests** in `tests/test_mcp_servers.py` (create if needed):
```python
async def test_my_mcp_server():
    server = MyMCPServer(config)
    result = await server.call_tool("my_tool", {})
    assert result is not None
```

### Creating Custom Workflows

1. **Define workflow method** in `agents/agent_coordinator.py`:
```python
def create_my_workflow(self, input_data: str) -> ExecutionPlan:
    handoffs = [
        AgentHandoff(
            agent_type=AgentType.AGENT_1,
            task=f"Process {input_data}",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.AGENT_2,
            task="Analyze results",
            context={}
        )
    ]

    return ExecutionPlan(
        strategy=HandoffStrategy.SEQUENTIAL,
        agents=handoffs,
        metadata={"workflow": "my_workflow"}
    )
```

2. **Add workflow configuration** to `config/agent_configs.yaml`:
```yaml
workflows:
  my_workflow:
    description: "Custom workflow description"
    agents:
      - web_researcher
      - document_analyzer
    strategy: sequential
```

3. **Add UI option** in `frontend/app.py`:
```python
if workflow_type == "My Custom Workflow":
    plan = coordinator.create_my_workflow(user_input)
    results = await coordinator.execute_plan(plan)
    display_results(results)
```

---

## Code Patterns

### Agent Handoff Pattern
```python
from agents import AgentCoordinator, AgentHandoff, AgentType

# Create coordinator
coordinator = AgentCoordinator()

# Create handoff
handoff = AgentHandoff(
    agent_type=AgentType.WEB_RESEARCHER,
    task="Research latest AI developments",
    context={},
    priority=1
)

# Execute
response = await coordinator.execute_handoff(handoff)

if response.success:
    print(f"Result: {response.result}")
else:
    print(f"Error: {response.error}")
```

### Sequential Workflow Pattern
```python
# Create research workflow (sequential execution)
plan = coordinator.create_research_workflow(
    "What are the benefits of multi-agent systems?"
)

# Execute plan
results = await coordinator.execute_plan(plan)

# Process results
for result in results:
    print(f"{result.agent_type.value}: {result.success}")
```

### Parallel Execution Pattern
```python
# Create multiple handoffs
handoffs = [
    AgentHandoff(AgentType.WEB_RESEARCHER, "Topic 1", {}),
    AgentHandoff(AgentType.WEB_RESEARCHER, "Topic 2", {}),
    AgentHandoff(AgentType.WEB_RESEARCHER, "Topic 3", {})
]

# Execute in parallel
results = await coordinator.execute_parallel_handoffs(handoffs)

# All tasks complete simultaneously
print(f"Completed {len(results)} parallel tasks")
```

### Q&A Workflow Pattern
```python
# Create Q&A workflow
context = """
Multi-agent systems consist of multiple autonomous agents...
"""

plan = coordinator.create_qa_workflow(
    question="How do agents communicate?",
    context=context
)

# Execute
results = await coordinator.execute_plan(plan)

# Extract answer
for result in results:
    if result.agent_type == AgentType.QA_AGENT:
        print(result.result)
```

### Using the Orchestrator (Auto Mode)
```python
from agents import DocumentOrchestrator

# Orchestrator automatically determines workflow
orchestrator = DocumentOrchestrator()

# Process message (auto-delegates to appropriate agents)
response = orchestrator.process_message(
    "Summarize the latest research on AI safety"
)

print(response)
```

### Error Handling Pattern
```python
try:
    response = await coordinator.execute_handoff(handoff)

    if not response.success:
        print(f"Agent failed: {response.error}")
        # Implement fallback logic
        fallback_handoff = AgentHandoff(...)
        response = await coordinator.execute_handoff(fallback_handoff)

except Exception as e:
    print(f"Execution error: {e}")
    # Log error, retry, or notify user
```

---

## Testing

### Test Structure

- **tests/conftest.py**: pytest fixtures (mock configs, agents, coordinators)
- **tests/test_agents.py**: Unit tests for all agent implementations
- **tests/test_handoffs.py**: Integration tests for agent coordination

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_agents.py

# Specific test
pytest tests/test_agents.py::test_web_researcher -v

# With coverage
pytest --cov=agents --cov=mcp_servers tests/

# Coverage report (HTML)
pytest --cov=agents --cov=mcp_servers --cov-report=html tests/
# Open htmlcov/index.html
```

### Writing Tests

#### Agent Unit Test Pattern
```python
import pytest
from agents import WebResearcherAgent

@pytest.mark.asyncio
async def test_web_researcher(mock_config):
    agent = WebResearcherAgent(mock_config)

    response = await agent.execute(
        task="Research AI safety",
        context={}
    )

    assert response.success
    assert response.agent_type == AgentType.WEB_RESEARCHER
    assert "result" in response.result
```

#### Handoff Integration Test Pattern
```python
@pytest.mark.asyncio
async def test_sequential_handoff(coordinator):
    handoffs = [
        AgentHandoff(AgentType.WEB_RESEARCHER, "Task 1", {}),
        AgentHandoff(AgentType.DOCUMENT_ANALYZER, "Task 2", {})
    ]

    plan = ExecutionPlan(
        strategy=HandoffStrategy.SEQUENTIAL,
        agents=handoffs
    )

    results = await coordinator.execute_plan(plan)

    assert len(results) == 2
    assert all(r.success for r in results)
```

### Test Fixtures (conftest.py)

Available fixtures:
- `mock_config`: Mock agent configuration
- `mock_orchestrator`: Mock DocumentOrchestrator
- `mock_coordinator`: Mock AgentCoordinator
- `mock_agent_response`: Mock AgentResponse

### Mocking API Calls

```python
@pytest.mark.asyncio
async def test_with_mock_api(mocker):
    # Mock Anthropic API call
    mock_response = mocker.Mock()
    mock_response.content = "Test response"

    mocker.patch('anthropic.Anthropic.messages.create', return_value=mock_response)

    # Test agent with mocked API
    agent = WebResearcherAgent(config)
    response = await agent.execute("test", {})

    assert response.success
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Set
```
Error: ANTHROPIC_API_KEY not found
```
**Solution:**
```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

#### 2. Module Import Errors
```
ImportError: No module named 'streamlit'
```
**Solution:**
```bash
pip install -r requirements.txt
```

#### 3. Database Connection Issues
```
Error: Could not connect to database
```
**Solution:**
```bash
# Check DATABASE_PATH in .env
mkdir -p knowledge_base
# Verify permissions
chmod 755 knowledge_base
```

#### 4. Streamlit Port Already in Use
```
Error: Port 8501 is already in use
```
**Solution:**
```bash
# Change port in .env
STREAMLIT_SERVER_PORT=8502

# Or kill existing process
lsof -ti:8501 | xargs kill
```

#### 5. Agent Timeout Errors
```
Error: Request timeout after 120s
```
**Solution:**
```bash
# Increase timeout in .env
REQUEST_TIMEOUT=600

# Or in agent_configs.yaml per agent
web_researcher:
  timeout: 300
```

#### 6. Rate Limiting
```
Error: Rate limit exceeded
```
**Solution:**
```bash
# Reduce concurrent agents in .env
MAX_CONCURRENT_AGENTS=2

# Add retry logic in code
RETRY_ATTEMPTS=5
```

### Debugging Tips

1. **Enable Debug Logging**:
```bash
# In .env
LOG_LEVEL=DEBUG
MCP_LOG_LEVEL=DEBUG
```

2. **Check Agent Execution**:
```python
# Add logging to agent execution
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Inspect Handoff Context**:
```python
# Print context before execution
print(f"Handoff context: {handoff.context}")
response = await coordinator.execute_handoff(handoff)
print(f"Response metadata: {response.metadata}")
```

4. **Test Individual Components**:
```bash
# Test agent directly
python -c "from agents import WebResearcherAgent; print('OK')"

# Test MCP server
python mcp_servers/websearch_server.py
```

5. **Validate Configuration**:
```python
# Check config loading
import yaml
with open('config/agent_configs.yaml') as f:
    config = yaml.safe_load(f)
    print(config)
```

### Performance Optimization

1. **Reduce Token Usage**:
   - Lower `max_tokens` in agent configs
   - Use more specific prompts
   - Implement result caching

2. **Parallel Execution**:
   - Use `execute_parallel_handoffs()` for independent tasks
   - Increase `MAX_CONCURRENT_AGENTS` (with caution)

3. **Model Selection**:
   - Use Sonnet for most tasks (faster, cheaper)
   - Reserve Opus for complex reasoning

4. **Caching**:
   - Implement result caching for repeated queries
   - Cache web search results
   - Cache document analysis results

---

## Code Conventions

### Python Style
- **PEP 8** compliant
- **Type hints** for function signatures
- **Docstrings** for classes and public methods
- **Async/await** for I/O operations

### Naming Conventions
- **Classes**: PascalCase (e.g., `DocumentOrchestrator`)
- **Functions/Methods**: snake_case (e.g., `execute_handoff`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `ORCHESTRATOR_PROMPT`)
- **Files**: snake_case (e.g., `web_researcher.py`)

### Import Organization
```python
# 1. Standard library
import os
import asyncio
from typing import Dict, List, Any

# 2. Third-party
import anthropic
from pydantic import BaseModel

# 3. Local
from agents import AgentType, AgentHandoff
from prompts import ORCHESTRATOR_PROMPT
```

### Error Handling
```python
# Always return AgentResponse with success flag
try:
    result = await self._execute_task(task)
    return AgentResponse(
        agent_type=self.agent_type,
        success=True,
        result=result,
        error=None
    )
except Exception as e:
    return AgentResponse(
        agent_type=self.agent_type,
        success=False,
        result=None,
        error=str(e)
    )
```

### Async Patterns
```python
# Use async for I/O operations
async def execute(self, task: str) -> AgentResponse:
    # Async API calls
    response = await self.client.messages.create(...)
    return response

# Use asyncio.gather for parallel operations
results = await asyncio.gather(*[
    self.execute_handoff(h) for h in handoffs
])
```

---

## Additional Resources

### Documentation Files
- **docs/architecture.md** - Detailed system architecture
- **docs/agent_workflows.md** - Comprehensive workflow patterns
- **docs/api_reference.md** - Complete API documentation
- **AGENTS.md** - Agent-specific details
- **TEST_RESULTS.md** - Test coverage reports

### Example Scripts
- **examples/basic_usage.py** - Simple usage patterns
- **examples/advanced_workflows.py** - Complex workflow examples
- **demo.py** - Quick demonstration script

### External Links
- [Claude Agent SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
- [Model Context Protocol (MCP) Spec](https://modelcontextprotocol.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Claude API Reference](https://docs.anthropic.com/)

---

## Summary

This codebase implements a production-ready multi-agent research system with:

- ✅ **Modular Architecture**: 6 specialized agents + 4 MCP servers
- ✅ **Flexible Execution**: 4 handoff strategies for different use cases
- ✅ **Full Test Coverage**: Unit and integration tests with pytest
- ✅ **Interactive UI**: Streamlit frontend with chat and workflows
- ✅ **Comprehensive Config**: YAML/JSON configuration for all components
- ✅ **Complete Documentation**: Architecture, API, and workflow guides

**Quick Reference:**
- 📁 Core agents: `agents/orchestrator.py`, `agents/agent_coordinator.py`
- 🔧 Configuration: `config/agent_configs.yaml`, `config/models.yaml`
- 🧪 Tests: `pytest tests/`
- 🚀 Run: `./run.sh` or `streamlit run frontend/app.py`
- 📖 Docs: `docs/architecture.md`, `docs/api_reference.md`

For questions or issues, refer to the documentation in `docs/` or run the demo script with `python demo.py`.
