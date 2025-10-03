"""
Agent Coordination System
Handles agent-to-agent communication and handoffs
"""
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json

from .orchestrator import AgentType, AgentHandoff, AgentResponse
from .web_researcher import WebResearcherAgent
from .document_analyzer import DocumentAnalyzerAgent
from .summary_generator import SummaryGeneratorAgent
from .qa_agent import QAAgent
from .citation_manager import CitationManagerAgent


class HandoffStrategy(Enum):
    """Strategies for agent handoffs"""
    SEQUENTIAL = "sequential"  # One after another
    PARALLEL = "parallel"      # Multiple agents simultaneously
    CONDITIONAL = "conditional"  # Based on previous results
    CHAIN = "chain"            # Results flow through agents


@dataclass
class HandoffPlan:
    """Plan for executing agent handoffs"""
    strategy: HandoffStrategy
    agents: List[AgentHandoff]
    merge_results: bool = True
    timeout: int = 300  # seconds


class AgentCoordinator:
    """
    Coordinates communication and handoffs between agents
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._initialize_agents()
        self.handoff_history = []

    def _initialize_agents(self):
        """Initialize all sub-agents"""
        self.agents = {
            AgentType.WEB_RESEARCHER: WebResearcherAgent(api_key=self.api_key),
            AgentType.DOCUMENT_ANALYZER: DocumentAnalyzerAgent(api_key=self.api_key),
            AgentType.SUMMARY_GENERATOR: SummaryGeneratorAgent(api_key=self.api_key),
            AgentType.QA_AGENT: QAAgent(api_key=self.api_key),
            AgentType.CITATION_MANAGER: CitationManagerAgent(api_key=self.api_key)
        }

    async def execute_handoff(self, handoff: AgentHandoff) -> AgentResponse:
        """
        Execute a single agent handoff
        """
        agent = self.agents.get(handoff.agent_type)

        if not agent:
            return AgentResponse(
                agent_type=handoff.agent_type,
                success=False,
                result=None,
                error=f"Agent {handoff.agent_type.value} not found"
            )

        try:
            # Route to appropriate agent method based on agent type
            if handoff.agent_type == AgentType.WEB_RESEARCHER:
                result = agent.research(handoff.task, handoff.context)
            elif handoff.agent_type == AgentType.DOCUMENT_ANALYZER:
                content = handoff.context.get("content", "")
                analysis_type = handoff.context.get("analysis_type", "general")
                result = agent.analyze_document(content, analysis_type, handoff.context)
            elif handoff.agent_type == AgentType.SUMMARY_GENERATOR:
                content = handoff.context.get("content", "")
                summary_type = handoff.context.get("summary_type", "standard")
                length = handoff.context.get("length", "medium")
                result = agent.generate_summary(content, summary_type, length, handoff.context)
            elif handoff.agent_type == AgentType.QA_AGENT:
                context = handoff.context.get("context")
                history = handoff.context.get("conversation_history")
                result = agent.answer_question(handoff.task, context, history)
            elif handoff.agent_type == AgentType.CITATION_MANAGER:
                source_info = handoff.context.get("source_info", {})
                citation_style = handoff.context.get("citation_style", "APA")
                result = agent.create_citation(source_info, citation_style)
            else:
                result = {"error": f"Unknown agent type: {handoff.agent_type}"}

            # Record handoff
            self.handoff_history.append({
                "agent": handoff.agent_type.value,
                "task": handoff.task,
                "timestamp": asyncio.get_event_loop().time(),
                "success": True
            })

            return AgentResponse(
                agent_type=handoff.agent_type,
                success=True,
                result=result
            )

        except Exception as e:
            self.handoff_history.append({
                "agent": handoff.agent_type.value,
                "task": handoff.task,
                "timestamp": asyncio.get_event_loop().time(),
                "success": False,
                "error": str(e)
            })

            return AgentResponse(
                agent_type=handoff.agent_type,
                success=False,
                result=None,
                error=str(e)
            )

    async def execute_sequential_handoffs(self, handoffs: List[AgentHandoff]) -> List[AgentResponse]:
        """
        Execute handoffs sequentially, passing context between them
        """
        results = []
        accumulated_context = {}

        for handoff in handoffs:
            # Merge accumulated context with handoff context
            handoff.context = {**accumulated_context, **handoff.context}

            # Execute handoff
            response = await self.execute_handoff(handoff)
            results.append(response)

            # Update accumulated context if successful
            if response.success:
                accumulated_context[handoff.agent_type.value] = response.result

        return results

    async def execute_parallel_handoffs(self, handoffs: List[AgentHandoff]) -> List[AgentResponse]:
        """
        Execute multiple handoffs in parallel
        """
        tasks = [self.execute_handoff(handoff) for handoff in handoffs]
        results = await asyncio.gather(*tasks)
        return list(results)

    async def execute_conditional_handoffs(
        self,
        handoffs: List[AgentHandoff],
        condition_func: Callable[[AgentResponse], bool]
    ) -> List[AgentResponse]:
        """
        Execute handoffs conditionally based on previous results
        """
        results = []

        for handoff in handoffs:
            # Check condition if we have previous results
            if results and not condition_func(results[-1]):
                break

            response = await self.execute_handoff(handoff)
            results.append(response)

        return results

    async def execute_chain_handoffs(self, handoffs: List[AgentHandoff]) -> AgentResponse:
        """
        Execute handoffs as a chain, where output of one becomes input to next
        """
        if not handoffs:
            return AgentResponse(
                agent_type=AgentType.QA_AGENT,
                success=False,
                result=None,
                error="No handoffs provided"
            )

        current_result = None

        for i, handoff in enumerate(handoffs):
            # If not first handoff, use previous result as context
            if i > 0 and current_result:
                handoff.context["previous_result"] = current_result.result

            current_result = await self.execute_handoff(handoff)

            # If any handoff fails, stop the chain
            if not current_result.success:
                break

        return current_result

    async def execute_plan(self, plan: HandoffPlan) -> List[AgentResponse]:
        """
        Execute a handoff plan based on strategy
        """
        try:
            if plan.strategy == HandoffStrategy.SEQUENTIAL:
                results = await asyncio.wait_for(
                    self.execute_sequential_handoffs(plan.agents),
                    timeout=plan.timeout
                )
            elif plan.strategy == HandoffStrategy.PARALLEL:
                results = await asyncio.wait_for(
                    self.execute_parallel_handoffs(plan.agents),
                    timeout=plan.timeout
                )
            elif plan.strategy == HandoffStrategy.CHAIN:
                result = await asyncio.wait_for(
                    self.execute_chain_handoffs(plan.agents),
                    timeout=plan.timeout
                )
                results = [result]
            else:
                results = await asyncio.wait_for(
                    self.execute_sequential_handoffs(plan.agents),
                    timeout=plan.timeout
                )

            return results

        except asyncio.TimeoutError:
            return [AgentResponse(
                agent_type=AgentType.QA_AGENT,
                success=False,
                result=None,
                error=f"Execution timed out after {plan.timeout} seconds"
            )]

    def create_research_workflow(self, query: str) -> HandoffPlan:
        """
        Create a standard research workflow
        Web Research → Document Analysis → Summary
        """
        return HandoffPlan(
            strategy=HandoffStrategy.SEQUENTIAL,
            agents=[
                AgentHandoff(
                    agent_type=AgentType.WEB_RESEARCHER,
                    task=query,
                    context={},
                    priority=1
                ),
                AgentHandoff(
                    agent_type=AgentType.DOCUMENT_ANALYZER,
                    task=f"Analyze research findings for: {query}",
                    context={"analysis_type": "research"},
                    priority=2
                ),
                AgentHandoff(
                    agent_type=AgentType.SUMMARY_GENERATOR,
                    task=f"Summarize research on: {query}",
                    context={"summary_type": "research_report", "length": "detailed"},
                    priority=3
                )
            ]
        )

    def create_qa_workflow(self, question: str, context: str = None) -> HandoffPlan:
        """
        Create a Q&A workflow
        Document Analysis (if context) → Q&A
        """
        agents = []

        if context:
            agents.append(AgentHandoff(
                agent_type=AgentType.DOCUMENT_ANALYZER,
                task=f"Extract relevant info for question: {question}",
                context={"content": context, "analysis_type": "qa_prep"},
                priority=1
            ))

        agents.append(AgentHandoff(
            agent_type=AgentType.QA_AGENT,
            task=question,
            context={"context": context} if context else {},
            priority=2
        ))

        return HandoffPlan(
            strategy=HandoffStrategy.SEQUENTIAL,
            agents=agents
        )

    def get_handoff_history(self) -> List[Dict[str, Any]]:
        """Get history of all handoffs"""
        return self.handoff_history

    def clear_history(self):
        """Clear handoff history"""
        self.handoff_history = []


# Example usage
async def main():
    coordinator = AgentCoordinator()

    # Create a research workflow
    plan = coordinator.create_research_workflow(
        "Latest developments in AI agents 2025"
    )

    # Execute the plan
    results = await coordinator.execute_plan(plan)

    # Print results
    for result in results:
        print(f"\n{result.agent_type.value}:")
        print(f"Success: {result.success}")
        if result.success:
            print(f"Result: {json.dumps(result.result, indent=2)}")
        else:
            print(f"Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(main())
