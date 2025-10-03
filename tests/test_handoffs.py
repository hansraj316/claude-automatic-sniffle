"""
Tests for agent handoffs and coordination
"""
import pytest
import asyncio
import os
from agents import (
    AgentCoordinator,
    AgentHandoff,
    AgentType,
    HandoffPlan,
    HandoffStrategy
)


@pytest.fixture
def api_key():
    """Get API key from environment"""
    return os.getenv("ANTHROPIC_API_KEY", "test_key")


@pytest.fixture
def coordinator(api_key):
    """Create agent coordinator"""
    return AgentCoordinator(api_key=api_key)


class TestAgentHandoff:
    def test_handoff_creation(self):
        handoff = AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Test task",
            context={"key": "value"},
            priority=1
        )
        assert handoff.agent_type == AgentType.WEB_RESEARCHER
        assert handoff.task == "Test task"
        assert handoff.context == {"key": "value"}
        assert handoff.priority == 1


class TestAgentCoordinator:
    def test_initialization(self, coordinator):
        assert coordinator is not None
        assert len(coordinator.agents) == 5  # All 5 sub-agents

    @pytest.mark.asyncio
    async def test_execute_single_handoff(self, coordinator):
        handoff = AgentHandoff(
            agent_type=AgentType.QA_AGENT,
            task="What is AI?",
            context={"context": "AI is artificial intelligence"}
        )
        response = await coordinator.execute_handoff(handoff)
        assert response.agent_type == AgentType.QA_AGENT
        assert response.success is not None

    @pytest.mark.asyncio
    async def test_sequential_handoffs(self, coordinator):
        handoffs = [
            AgentHandoff(
                agent_type=AgentType.WEB_RESEARCHER,
                task="Research AI",
                context={}
            ),
            AgentHandoff(
                agent_type=AgentType.SUMMARY_GENERATOR,
                task="Summarize research",
                context={"content": "Research findings"}
            )
        ]
        results = await coordinator.execute_sequential_handoffs(handoffs)
        assert len(results) == 2
        assert all(isinstance(r.success, bool) for r in results)

    @pytest.mark.asyncio
    async def test_parallel_handoffs(self, coordinator):
        handoffs = [
            AgentHandoff(
                agent_type=AgentType.WEB_RESEARCHER,
                task="Research topic 1",
                context={}
            ),
            AgentHandoff(
                agent_type=AgentType.WEB_RESEARCHER,
                task="Research topic 2",
                context={}
            )
        ]
        results = await coordinator.execute_parallel_handoffs(handoffs)
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_research_workflow(self, coordinator):
        plan = coordinator.create_research_workflow("AI trends 2025")
        assert plan.strategy == HandoffStrategy.SEQUENTIAL
        assert len(plan.agents) == 3  # web_researcher, document_analyzer, summary_generator

        results = await coordinator.execute_plan(plan)
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_qa_workflow(self, coordinator):
        plan = coordinator.create_qa_workflow(
            question="What is machine learning?",
            context="ML is a subset of AI"
        )
        assert plan.strategy == HandoffStrategy.SEQUENTIAL

        results = await coordinator.execute_plan(plan)
        assert len(results) > 0

    def test_handoff_history(self, coordinator):
        history = coordinator.get_handoff_history()
        assert isinstance(history, list)

    def test_clear_history(self, coordinator):
        coordinator.clear_history()
        history = coordinator.get_handoff_history()
        assert len(history) == 0


class TestHandoffPlan:
    def test_plan_creation(self):
        plan = HandoffPlan(
            strategy=HandoffStrategy.SEQUENTIAL,
            agents=[
                AgentHandoff(
                    agent_type=AgentType.WEB_RESEARCHER,
                    task="Research",
                    context={}
                )
            ],
            merge_results=True,
            timeout=300
        )
        assert plan.strategy == HandoffStrategy.SEQUENTIAL
        assert len(plan.agents) == 1
        assert plan.timeout == 300

    @pytest.mark.asyncio
    async def test_plan_execution(self, coordinator):
        plan = HandoffPlan(
            strategy=HandoffStrategy.SEQUENTIAL,
            agents=[
                AgentHandoff(
                    agent_type=AgentType.SUMMARY_GENERATOR,
                    task="Summarize this text",
                    context={"content": "Sample text to summarize"}
                )
            ],
            timeout=60
        )
        results = await coordinator.execute_plan(plan)
        assert len(results) == 1


class TestWorkflowStrategies:
    @pytest.mark.asyncio
    async def test_chain_handoffs(self, coordinator):
        handoffs = [
            AgentHandoff(
                agent_type=AgentType.WEB_RESEARCHER,
                task="Find information",
                context={}
            ),
            AgentHandoff(
                agent_type=AgentType.DOCUMENT_ANALYZER,
                task="Analyze findings",
                context={}
            )
        ]
        result = await coordinator.execute_chain_handoffs(handoffs)
        assert result.agent_type == AgentType.DOCUMENT_ANALYZER

    @pytest.mark.asyncio
    async def test_conditional_handoffs(self, coordinator):
        def always_continue(response):
            return True

        handoffs = [
            AgentHandoff(
                agent_type=AgentType.QA_AGENT,
                task="Answer question",
                context={"question": "What is AI?"}
            )
        ]
        results = await coordinator.execute_conditional_handoffs(
            handoffs,
            condition_func=always_continue
        )
        assert len(results) > 0
