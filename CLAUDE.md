# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Research Hub

A multi-agent knowledge management and research assistant system built with the Claude Agent SDK.

## Development Commands

### Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### Running the Application
```bash
# Frontend
streamlit run frontend/app.py

# Examples
python examples/basic_usage.py
python examples/advanced_workflows.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_agents.py
pytest tests/test_handoffs.py

# With coverage
pytest --cov=agents tests/
```

## Architecture

### Multi-Agent System
- **DocumentOrchestrator**: Main coordinator that analyzes requests and delegates to sub-agents
- **5 Specialized Sub-Agents**: WebResearcher, DocumentAnalyzer, SummaryGenerator, QAAgent, CitationManager
- **AgentCoordinator**: Manages agent handoffs with 4 strategies (sequential, parallel, conditional, chain)

### MCP Servers
4 Model Context Protocol servers provide tools:
- Filesystem MCP (file operations)
- WebSearch MCP (web research)
- Database MCP (SQLite storage)
- GitHub MCP (code/docs access)

### Key Workflows
1. Research: WebResearcher → DocumentAnalyzer → SummaryGenerator
2. Q&A: DocumentAnalyzer → QAAgent
3. Summary: SummaryGenerator (standalone)
4. Comprehensive: All agents in sequence

## Important Files

### Agent Prompts
- `prompts/` - All agent system prompts in separate .txt files
- Load via `from prompts import ORCHESTRATOR_PROMPT`

### Configuration
- `config/agent_configs.yaml` - Agent settings, models, tools
- `config/mcp_config.json` - MCP server configuration
- `config/models.yaml` - Model selection and performance settings

### Core Agents
- `agents/orchestrator.py` - Main coordinator
- `agents/agent_coordinator.py` - Handoff management
- `agents/{agent_name}.py` - Individual agent implementations

## Development Workflow

### Adding New Agents
1. Create agent class in `agents/`
2. Add system prompt to `prompts/{agent_name}_prompt.txt`
3. Update `config/agent_configs.yaml`
4. Register in `AgentCoordinator._initialize_agents()`
5. Add to `AgentType` enum

### Adding New MCP Servers
1. Implement in `mcp_servers/{server_name}_server.py`
2. Follow MCP protocol with `list_tools()` and `call_tool()`
3. Add configuration to `config/mcp_config.json`
4. Update agent tool permissions

### Creating Custom Workflows
1. Define in `config/agent_configs.yaml` workflows section
2. Create method in `AgentCoordinator`
3. Add UI option in `frontend/app.py`

## Code Patterns

### Agent Handoff
```python
handoff = AgentHandoff(
    agent_type=AgentType.WEB_RESEARCHER,
    task="research query",
    context={},
    priority=1
)
response = await coordinator.execute_handoff(handoff)
```

### Workflow Execution
```python
plan = coordinator.create_research_workflow(query)
results = await coordinator.execute_plan(plan)
```

## Testing Guidelines
- All agents have unit tests in `tests/test_agents.py`
- Handoff coordination tested in `tests/test_handoffs.py`
- Use pytest fixtures from `tests/conftest.py`
- Mock API calls for faster tests

## Documentation
- `docs/architecture.md` - System design
- `docs/agent_workflows.md` - Workflow patterns
- `docs/api_reference.md` - API documentation
