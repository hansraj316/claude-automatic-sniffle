# Agent Workflows

This document describes common workflow patterns and how agents collaborate.

## Workflow Types

### 1. Research Workflow

**Purpose**: Conduct comprehensive research on a topic

**Agent Sequence**:
```
Web Research Agent → Document Analyzer → Summary Generator
```

**Steps**:
1. **Web Research Agent**
   - Searches for relevant information
   - Validates sources
   - Extracts key content
   - Returns research findings with citations

2. **Document Analyzer**
   - Analyzes research findings
   - Extracts themes and insights
   - Identifies relationships between concepts
   - Returns structured analysis

3. **Summary Generator**
   - Creates multi-level summary
   - Generates executive summary
   - Produces detailed report
   - Returns formatted output

**Example Usage**:
```python
coordinator = AgentCoordinator()
plan = coordinator.create_research_workflow(
    "Latest developments in AI agents 2025"
)
results = await coordinator.execute_plan(plan)
```

**Output**:
- Comprehensive research report
- Source citations
- Key insights and findings
- Executive summary

---

### 2. Question & Answer Workflow

**Purpose**: Answer questions using available context

**Agent Sequence**:
```
Document Analyzer (optional) → Q&A Agent
```

**Steps**:
1. **Document Analyzer** (if context provided)
   - Analyzes provided context
   - Extracts relevant information
   - Prepares structured data for Q&A

2. **Q&A Agent**
   - Processes question
   - Uses analyzed context
   - Generates comprehensive answer
   - Provides confidence level

**Example Usage**:
```python
coordinator = AgentCoordinator()
plan = coordinator.create_qa_workflow(
    question="What are the key benefits of multi-agent systems?",
    context=research_document
)
results = await coordinator.execute_plan(plan)
```

**Output**:
- Direct answer to question
- Supporting evidence
- Related topics
- Follow-up questions

---

### 3. Summary Workflow

**Purpose**: Create summaries at various levels

**Agent Sequence**:
```
Summary Generator
```

**Steps**:
1. **Summary Generator**
   - Analyzes input content
   - Creates summary at requested level (brief/medium/detailed)
   - Extracts key points
   - Returns formatted summary

**Example Usage**:
```python
handoff = AgentHandoff(
    agent_type=AgentType.SUMMARY_GENERATOR,
    task="Summarize this research paper",
    context={
        "content": paper_text,
        "summary_type": "executive",
        "length": "brief"
    }
)
result = await coordinator.execute_handoff(handoff)
```

**Output**:
- Concise summary
- Key takeaways
- Word count and reading time

---

### 4. Comprehensive Research Workflow

**Purpose**: Full research cycle with citations

**Agent Sequence**:
```
Web Research → Document Analyzer → Summary Generator → Citation Manager
```

**Steps**:
1. **Web Research Agent**: Gathers information
2. **Document Analyzer**: Analyzes findings
3. **Summary Generator**: Creates report
4. **Citation Manager**: Formats citations

**Example Usage**:
```python
plan = HandoffPlan(
    strategy=HandoffStrategy.SEQUENTIAL,
    agents=[
        AgentHandoff(AgentType.WEB_RESEARCHER, ...),
        AgentHandoff(AgentType.DOCUMENT_ANALYZER, ...),
        AgentHandoff(AgentType.SUMMARY_GENERATOR, ...),
        AgentHandoff(AgentType.CITATION_MANAGER, ...)
    ]
)
results = await coordinator.execute_plan(plan)
```

**Output**:
- Complete research report
- Formatted citations
- Bibliography
- Source validation

---

## Workflow Strategies

### Sequential Execution

Agents run one after another, each using previous results.

```python
results = await coordinator.execute_sequential_handoffs([
    handoff1, handoff2, handoff3
])
```

**Use when**:
- Each step depends on previous results
- Order matters
- Building context progressively

---

### Parallel Execution

Multiple agents run simultaneously.

```python
results = await coordinator.execute_parallel_handoffs([
    handoff1, handoff2, handoff3
])
```

**Use when**:
- Tasks are independent
- Speed is priority
- Merging different perspectives

---

### Conditional Execution

Next agent runs based on conditions.

```python
def should_continue(response):
    return response.success and response.result.get("confidence") > 0.8

results = await coordinator.execute_conditional_handoffs(
    handoffs,
    condition_func=should_continue
)
```

**Use when**:
- Quality gates needed
- Early exit on failure
- Adaptive workflows

---

### Chain Execution

Output of one agent becomes input to next.

```python
result = await coordinator.execute_chain_handoffs([
    handoff1, handoff2, handoff3
])
```

**Use when**:
- Transforming data through stages
- Refinement process
- Progressive enhancement

---

## Custom Workflow Examples

### Document Comparison Workflow

```python
async def compare_documents_workflow(doc1, doc2):
    # Analyze both documents in parallel
    analysis_results = await coordinator.execute_parallel_handoffs([
        AgentHandoff(
            AgentType.DOCUMENT_ANALYZER,
            task="Analyze document 1",
            context={"content": doc1}
        ),
        AgentHandoff(
            AgentType.DOCUMENT_ANALYZER,
            task="Analyze document 2",
            context={"content": doc2}
        )
    ])

    # Generate comparison summary
    summary = await coordinator.execute_handoff(
        AgentHandoff(
            AgentType.SUMMARY_GENERATOR,
            task="Compare documents",
            context={
                "doc1_analysis": analysis_results[0].result,
                "doc2_analysis": analysis_results[1].result
            }
        )
    )

    return summary
```

### Multi-Source Research Workflow

```python
async def multi_source_research(topic, sources):
    # Research each source in parallel
    research_results = await coordinator.execute_parallel_handoffs([
        AgentHandoff(
            AgentType.WEB_RESEARCHER,
            task=f"Research {topic} from {source}",
            context={"source": source}
        )
        for source in sources
    ])

    # Synthesize findings
    synthesis = await coordinator.execute_handoff(
        AgentHandoff(
            AgentType.SUMMARY_GENERATOR,
            task="Synthesize multi-source research",
            context={
                "sources": [r.result for r in research_results]
            }
        )
    )

    return synthesis
```

### Iterative Refinement Workflow

```python
async def iterative_refinement(query, max_iterations=3):
    context = {}

    for i in range(max_iterations):
        # Research
        research = await coordinator.execute_handoff(
            AgentHandoff(
                AgentType.WEB_RESEARCHER,
                task=query,
                context=context
            )
        )

        # Analyze
        analysis = await coordinator.execute_handoff(
            AgentHandoff(
                AgentType.DOCUMENT_ANALYZER,
                task="Analyze research quality",
                context={"research": research.result}
            )
        )

        # Check if sufficient
        if analysis.result.get("quality_score", 0) > 0.8:
            break

        # Refine query based on gaps
        context["previous_attempts"] = analysis.result

    return analysis
```

---

## Workflow Best Practices

1. **Start Simple**: Use predefined workflows when possible
2. **Error Handling**: Always check `response.success`
3. **Context Management**: Pass relevant context between agents
4. **Timeout Management**: Set appropriate timeouts for complex workflows
5. **Logging**: Track agent handoffs for debugging
6. **Fallbacks**: Have fallback strategies for failures

---

## Workflow Monitoring

Track workflow execution:

```python
# Get handoff history
history = coordinator.get_handoff_history()

# Check for failures
failures = [h for h in history if not h.get("success")]

# Analyze timing
for handoff in history:
    print(f"{handoff['agent']}: {handoff['timestamp']:.2f}s")
```
