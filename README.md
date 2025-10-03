# 🔬 Research Hub

A sophisticated multi-agent knowledge management and research assistant system built with the Claude Agent SDK.

## Features

✅ **Multi-Agent Architecture** - 6 specialized agents working in harmony
✅ **MCP Server Integration** - 4 Model Context Protocol servers for enhanced capabilities
✅ **Latest Claude Models** - Powered by Claude Sonnet 4.5 and Opus 4
✅ **Advanced Workflows** - Sequential, parallel, conditional, and chain execution
✅ **Agent Handoffs** - Seamless context passing between specialized agents
✅ **Streamlit Frontend** - Beautiful, interactive chat interface
✅ **Comprehensive Documentation** - Full API reference and workflow guides
✅ **Extensive Testing** - Test suite for agents and handoffs

## Architecture

### Agents

1. **Document Orchestrator** - Main coordinator that delegates to sub-agents
2. **Web Research Agent** - Searches web, validates sources, extracts information
3. **Document Analyzer** - Analyzes documents, extracts insights, processes data
4. **Summary Generator** - Creates multi-level summaries and reports
5. **Q&A Agent** - Answers questions using context
6. **Citation Manager** - Manages citations in multiple formats (APA, MLA, Chicago, IEEE, Harvard)

### MCP Servers

- **Filesystem MCP** - File operations and document storage
- **Web Search MCP** - Web search and content extraction
- **Database MCP** - SQLite storage with full-text search
- **GitHub MCP** - Repository and code access

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd claude-automatic-sniffle

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Quick Start

### 1. Using the Streamlit Frontend

```bash
streamlit run frontend/app.py
```

Then open your browser to `http://localhost:8501`

### 2. Using the Python API

```python
from agents import DocumentOrchestrator

# Initialize orchestrator
orchestrator = DocumentOrchestrator()

# Ask a question
response = orchestrator.process_message(
    "Research the latest developments in AI agents"
)

print(response)
```

### 3. Using Custom Workflows

```python
import asyncio
from agents import AgentCoordinator

async def main():
    coordinator = AgentCoordinator()

    # Create research workflow
    plan = coordinator.create_research_workflow(
        "AI agent frameworks 2025"
    )

    # Execute
    results = await coordinator.execute_plan(plan)

    for result in results:
        print(f"{result.agent_type.value}: {result.success}")

asyncio.run(main())
```

## Workflow Examples

### Research Workflow
```
Web Research → Document Analysis → Summary Generation
```

### Q&A Workflow
```
Document Analysis → Q&A
```

### Comprehensive Research
```
Web Research → Analysis → Summary → Citations
```

### Parallel Research
```
┌─ Research Topic 1 ─┐
├─ Research Topic 2 ─┤ → Synthesis
└─ Research Topic 3 ─┘
```

## Configuration

### Agent Configuration (`config/agent_configs.yaml`)

```yaml
orchestrator:
  model: "claude-sonnet-4-5-20250929"
  max_tokens: 4000
  temperature: 0.7

web_researcher:
  model: "claude-sonnet-4-5-20250929"
  tools:
    - search_web
    - extract_content
```

### MCP Configuration (`config/mcp_config.json`)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "python",
      "args": ["mcp_servers/filesystem_server.py"],
      "tools": ["read_file", "write_file", "list_files"]
    }
  }
}
```

### Model Configuration (`config/models.yaml`)

```yaml
models:
  claude-sonnet-4-5:
    id: "claude-sonnet-4-5-20250929"
    max_tokens: 8192
    context_window: 200000
```

## Project Structure

```
research-hub/
├── agents/                    # Agent implementations
│   ├── orchestrator.py       # Main coordinator
│   ├── web_researcher.py     # Web research agent
│   ├── document_analyzer.py  # Document analysis
│   ├── summary_generator.py  # Summary creation
│   ├── qa_agent.py          # Q&A agent
│   ├── citation_manager.py  # Citation management
│   └── agent_coordinator.py # Handoff coordination
├── mcp_servers/              # MCP server implementations
│   ├── filesystem_server.py
│   ├── websearch_server.py
│   ├── database_server.py
│   └── github_server.py
├── frontend/                 # Streamlit frontend
│   ├── app.py
│   └── components/
├── prompts/                  # Agent system prompts
│   ├── orchestrator_prompt.txt
│   ├── web_researcher_prompt.txt
│   └── ...
├── config/                   # Configuration files
│   ├── agent_configs.yaml
│   ├── mcp_config.json
│   └── models.yaml
├── docs/                     # Documentation
│   ├── architecture.md
│   ├── agent_workflows.md
│   └── api_reference.md
├── tests/                    # Test suite
│   ├── test_agents.py
│   └── test_handoffs.py
├── examples/                 # Usage examples
│   ├── basic_usage.py
│   └── advanced_workflows.py
└── knowledge_base/           # Document storage
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=agents tests/
```

## Examples

See the `examples/` directory for:

- **basic_usage.py** - Simple examples for getting started
- **advanced_workflows.py** - Complex multi-agent patterns

Run examples:

```bash
python examples/basic_usage.py
python examples/advanced_workflows.py
```

## Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Agent Workflows](docs/agent_workflows.md) - Workflow patterns and strategies
- [API Reference](docs/api_reference.md) - Complete API documentation

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
GITHUB_TOKEN=your_github_token  # For GitHub MCP
DEFAULT_MODEL=claude-sonnet-4-5-20250929
LOG_LEVEL=INFO
```

## Key Features

### 1. Agent Handoffs

Agents can seamlessly hand off tasks to each other:

```python
# Sequential handoff
Web Research → Document Analysis → Summary

# Parallel handoff
Research 1 ┐
Research 2 ├→ Merge Results
Research 3 ┘
```

### 2. Multiple Workflow Strategies

- **Sequential**: Execute agents one by one
- **Parallel**: Run multiple agents simultaneously
- **Conditional**: Execute based on previous results
- **Chain**: Results flow through agents

### 3. Configurable Prompts

All agent prompts are in separate files (`prompts/`) for easy customization.

### 4. MCP Integration

Full Model Context Protocol support with 4 specialized servers.

### 5. Frontend Interface

Beautiful Streamlit UI with:
- Real-time chat
- Agent visualization
- Workflow selection
- Performance metrics

## Performance

- Supports up to 200K token context windows
- Concurrent agent execution
- Async/await for optimal performance
- Automatic context management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

Apache License 2.0 - see LICENSE file

## Support

- Documentation: [docs/](docs/)
- Examples: [examples/](examples/)
- Issues: GitHub Issues

## Powered By

- [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic Claude](https://www.anthropic.com/claude)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Streamlit](https://streamlit.io)

---

Built with ❤️ using Claude Sonnet 4.5 and the multi-agent framework
