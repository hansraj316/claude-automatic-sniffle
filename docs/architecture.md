# Research Hub Architecture

## System Overview

Research Hub is a multi-agent knowledge management and research assistant system built on the Claude Agent SDK. It uses specialized AI agents that work together to perform complex research, analysis, and documentation tasks.

## Core Components

### 1. Agent Layer

#### Document Orchestrator
- **Role**: Main coordinator for all agent activities
- **Responsibilities**:
  - Parse user requests
  - Break down complex tasks into sub-tasks
  - Delegate to appropriate sub-agents
  - Synthesize results from multiple agents
  - Manage conversation state

#### Sub-Agents

**Web Research Agent**
- Searches the web for information
- Validates source credibility
- Extracts and summarizes content
- Provides source citations

**Document Analyzer Agent**
- Analyzes documents for themes and insights
- Performs sentiment analysis
- Extracts entities and relationships
- Compares multiple documents

**Summary Generator Agent**
- Creates multi-level summaries
- Generates executive reports
- Synthesizes information from multiple sources
- Produces structured outputs

**Q&A Agent**
- Answers questions using context
- Explains complex concepts
- Compares and contrasts ideas
- Generates FAQs

**Citation Manager Agent**
- Creates citations in multiple formats (APA, MLA, Chicago, IEEE, Harvard)
- Manages bibliographies
- Validates citation accuracy
- Converts between citation styles

### 2. Agent Coordination System

The `AgentCoordinator` manages agent-to-agent communication and handoffs.

#### Handoff Strategies

**Sequential**: Execute agents one after another
```
Web Research → Document Analysis → Summary
```

**Parallel**: Execute multiple agents simultaneously
```
┌─ Agent 1 ─┐
├─ Agent 2 ─┤ → Merge Results
└─ Agent 3 ─┘
```

**Conditional**: Execute based on previous results
```
Agent 1 → [Check] → Agent 2 (if condition met)
```

**Chain**: Results flow through agents
```
A → B → C (output of A feeds B, output of B feeds C)
```

### 3. MCP Server Layer

Model Context Protocol servers provide tools and capabilities to agents.

#### Filesystem MCP Server
- File operations (read, write, list, delete)
- Document storage in knowledge base
- Access control and validation

#### Web Search MCP Server
- Web search via DuckDuckGo
- Content extraction from URLs
- Link extraction and analysis

#### Database MCP Server
- SQLite storage for documents
- Citation management
- Q&A history tracking
- Full-text search capabilities

#### GitHub MCP Server
- Repository search
- Code and documentation retrieval
- File content access
- Code search across GitHub

### 4. Frontend Layer

Streamlit-based web interface providing:
- Real-time chat interaction
- Workflow mode selection (auto, research, Q&A, summary)
- Agent status visualization
- Conversation history
- Configuration management

## Data Flow

### Research Workflow
```
User Query
    ↓
Orchestrator (analyzes request)
    ↓
Web Research Agent (MCP: web search)
    ↓
Document Analyzer Agent (MCP: database)
    ↓
Summary Generator Agent (MCP: filesystem)
    ↓
User Response
```

### Q&A Workflow
```
User Question
    ↓
Orchestrator
    ↓
Document Analyzer (if context provided)
    ↓
Q&A Agent (MCP: database for history)
    ↓
User Answer
```

## Agent Communication

### Handoff Structure
```python
@dataclass
class AgentHandoff:
    agent_type: AgentType
    task: str
    context: Dict[str, Any]
    priority: int = 0
```

### Response Structure
```python
@dataclass
class AgentResponse:
    agent_type: AgentType
    success: bool
    result: Any
    error: Optional[str] = None
    next_handoff: Optional[AgentHandoff] = None
```

## Configuration Architecture

### Agent Configs (`agent_configs.yaml`)
- Model selection per agent
- Temperature and token limits
- Tool permissions
- Workflow presets

### MCP Configs (`mcp_config.json`)
- Server definitions
- Tool mappings
- Environment variables
- Security settings

### Model Configs (`models.yaml`)
- Available models
- Pricing information
- Task-based selection
- Performance settings

## Security Considerations

1. **MCP Sandbox Mode**: Isolates MCP servers
2. **Tool Permissions**: Fine-grained control over agent capabilities
3. **Input Validation**: Sanitizes all user inputs
4. **Rate Limiting**: Controls API usage
5. **Error Handling**: Graceful degradation

## Scalability

### Horizontal Scaling
- Multiple agent instances can run concurrently
- MCP servers are stateless and can be distributed
- Database supports concurrent access

### Vertical Scaling
- Configurable context windows (up to 200K tokens)
- Batch processing capabilities
- Async/await for concurrent operations

## Extensibility

### Adding New Agents
1. Create agent class inheriting from base pattern
2. Define system prompt in `prompts/`
3. Add configuration to `agent_configs.yaml`
4. Register in `AgentCoordinator`

### Adding New MCP Servers
1. Implement MCP server interface
2. Define tools and capabilities
3. Add to `mcp_config.json`
4. Update agent tool permissions

### Adding New Workflows
1. Define in `agent_configs.yaml`
2. Create workflow method in `AgentCoordinator`
3. Add UI option in frontend

## Performance Optimization

1. **Prompt Management**: Separate prompt files for easy iteration
2. **Caching**: LRU cache for repeated queries
3. **Streaming**: Real-time response streaming
4. **Context Compaction**: Automatic context summarization
5. **Parallel Execution**: Concurrent agent handoffs when possible

## Monitoring and Logging

- Request/response logging
- Agent performance metrics
- Error tracking
- Usage analytics
- Handoff timeline visualization
