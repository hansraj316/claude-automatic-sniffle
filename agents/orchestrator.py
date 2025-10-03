"""
Document Orchestrator Agent
Main coordinator for the Research Hub multi-agent system
"""
import os
import json
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import ORCHESTRATOR_PROMPT


class AgentType(Enum):
    """Types of sub-agents"""
    WEB_RESEARCHER = "web_researcher"
    DOCUMENT_ANALYZER = "document_analyzer"
    SUMMARY_GENERATOR = "summary_generator"
    QA_AGENT = "qa_agent"
    CITATION_MANAGER = "citation_manager"


@dataclass
class AgentHandoff:
    """Represents a handoff to a sub-agent"""
    agent_type: AgentType
    task: str
    context: Dict[str, Any]
    priority: int = 0


@dataclass
class AgentResponse:
    """Response from a sub-agent"""
    agent_type: AgentType
    success: bool
    result: Any
    error: Optional[str] = None
    next_handoff: Optional[AgentHandoff] = None


class DocumentOrchestrator:
    """
    Main orchestrator agent that coordinates all sub-agents
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.conversation_history = []
        self.active_agents = {}

        # Load system prompt from file
        self.system_prompt = ORCHESTRATOR_PROMPT

    def process_message(self, user_message: str) -> str:
        """
        Process a user message and coordinate agents
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Analyze the request and determine required agents
        analysis = self._analyze_request(user_message)

        # Execute agent workflow
        results = self._execute_workflow(analysis)

        # Synthesize final response
        response = self._synthesize_response(results)

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response

    def _analyze_request(self, message: str) -> Dict[str, Any]:
        """
        Analyze user request to determine required agents and workflow
        """
        analysis_prompt = f"""Analyze this user request and determine:
1. What type of task is this? (research, Q&A, document analysis, summary generation, citation)
2. Which sub-agents are needed?
3. What is the optimal workflow/handoff sequence?
4. What context is needed for each agent?

User request: {message}

Respond in JSON format:
{{
    "task_type": "...",
    "required_agents": ["agent1", "agent2"],
    "workflow": [
        {{"agent": "agent1", "task": "...", "context": {{}}}},
        {{"agent": "agent2", "task": "...", "context": {{}}}}
    ],
    "expected_outcome": "..."
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        try:
            analysis = json.loads(response.content[0].text)
            return analysis
        except json.JSONDecodeError:
            # Fallback to simple analysis
            return {
                "task_type": "general",
                "required_agents": ["qa_agent"],
                "workflow": [{
                    "agent": "qa_agent",
                    "task": message,
                    "context": {}
                }],
                "expected_outcome": "Answer user question"
            }

    def _execute_workflow(self, analysis: Dict[str, Any]) -> List[AgentResponse]:
        """
        Execute the planned agent workflow
        """
        results = []
        workflow_context = {}

        for step in analysis.get("workflow", []):
            agent_type = step["agent"]
            task = step["task"]
            context = {**step.get("context", {}), **workflow_context}

            # Handoff to sub-agent
            handoff = AgentHandoff(
                agent_type=AgentType(agent_type),
                task=task,
                context=context
            )

            # Execute agent task
            result = self._handoff_to_agent(handoff)
            results.append(result)

            # Update workflow context with results
            if result.success:
                workflow_context[agent_type] = result.result

        return results

    def _handoff_to_agent(self, handoff: AgentHandoff) -> AgentResponse:
        """
        Handoff a task to a specific sub-agent
        """
        # This is a placeholder - actual implementation would import and call sub-agents
        # For now, we'll simulate the handoff

        agent_module = f"agents.{handoff.agent_type.value}"

        try:
            # Simulate agent execution
            result = {
                "agent": handoff.agent_type.value,
                "task_completed": handoff.task,
                "context": handoff.context,
                "status": "simulated"
            }

            return AgentResponse(
                agent_type=handoff.agent_type,
                success=True,
                result=result
            )
        except Exception as e:
            return AgentResponse(
                agent_type=handoff.agent_type,
                success=False,
                result=None,
                error=str(e)
            )

    def _synthesize_response(self, results: List[AgentResponse]) -> str:
        """
        Synthesize results from multiple agents into a coherent response
        """
        synthesis_prompt = f"""Synthesize these agent results into a coherent response for the user:

Agent Results:
{json.dumps([{
    'agent': r.agent_type.value,
    'success': r.success,
    'result': r.result,
    'error': r.error
} for r in results], indent=2)}

Create a natural, informative response that:
1. Addresses the user's original request
2. Incorporates insights from all successful agent executions
3. Provides actionable information
4. Mentions any errors or limitations if they exist
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        return response.content[0].text

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_active_agents(self) -> Dict[str, Any]:
        """Get currently active agents"""
        return self.active_agents


# Example usage
if __name__ == "__main__":
    orchestrator = DocumentOrchestrator()

    # Example interaction
    response = orchestrator.process_message(
        "I need to research AI agents and create a summary of the latest developments"
    )
    print(response)
