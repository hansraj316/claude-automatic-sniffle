#!/usr/bin/env python3
"""
Quick Demo of Research Hub Multi-Agent System
"""
import os
import asyncio
from agents import (
    DocumentOrchestrator,
    AgentCoordinator,
    AgentHandoff,
    AgentType
)

def demo_orchestrator():
    """Demo 1: Using the orchestrator (auto mode)"""
    print("\n" + "="*60)
    print("DEMO 1: Document Orchestrator (Auto Mode)")
    print("="*60)

    orchestrator = DocumentOrchestrator()

    response = orchestrator.process_message(
        "What are the key benefits of multi-agent AI systems?"
    )

    print("\nQuestion: What are the key benefits of multi-agent AI systems?")
    print("\nResponse:")
    print(response[:500] + "..." if len(response) > 500 else response)


async def demo_research_workflow():
    """Demo 2: Research workflow"""
    print("\n" + "="*60)
    print("DEMO 2: Research Workflow")
    print("="*60)

    coordinator = AgentCoordinator()

    # Create research workflow
    plan = coordinator.create_research_workflow(
        "Latest developments in Claude AI"
    )

    print(f"\nWorkflow Strategy: {plan.strategy.value}")
    print(f"Number of agents: {len(plan.agents)}")
    print("\nAgent sequence:")
    for i, agent in enumerate(plan.agents, 1):
        print(f"  {i}. {agent.agent_type.value}")

    # Execute workflow
    print("\nExecuting workflow...")
    results = await coordinator.execute_plan(plan)

    print("\nResults:")
    for i, result in enumerate(results, 1):
        status = "✅ Success" if result.success else "❌ Failed"
        print(f"  {i}. {result.agent_type.value}: {status}")


async def demo_qa_workflow():
    """Demo 3: Q&A workflow"""
    print("\n" + "="*60)
    print("DEMO 3: Question & Answer Workflow")
    print("="*60)

    coordinator = AgentCoordinator()

    context = """
    Multi-agent systems consist of multiple autonomous agents that interact
    to solve problems. Each agent has specific capabilities and can communicate
    with other agents to achieve complex goals.
    """

    plan = coordinator.create_qa_workflow(
        question="How do agents communicate in multi-agent systems?",
        context=context
    )

    print("\nQuestion: How do agents communicate in multi-agent systems?")
    print("\nExecuting Q&A workflow...")

    results = await coordinator.execute_plan(plan)

    for result in results:
        if result.agent_type == AgentType.QA_AGENT:
            print("\nAnswer generated successfully!")
            print(f"Result preview: {str(result.result)[:200]}...")


async def demo_parallel_execution():
    """Demo 4: Parallel agent execution"""
    print("\n" + "="*60)
    print("DEMO 4: Parallel Agent Execution")
    print("="*60)

    coordinator = AgentCoordinator()

    # Create multiple research tasks
    handoffs = [
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI safety",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI ethics",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI governance",
            context={}
        )
    ]

    print("\nResearching 3 topics in parallel:")
    print("  1. AI safety")
    print("  2. AI ethics")
    print("  3. AI governance")

    print("\nExecuting parallel research...")
    results = await coordinator.execute_parallel_handoffs(handoffs)

    print(f"\nCompleted {len(results)} parallel tasks")
    for i, result in enumerate(results, 1):
        status = "✅" if result.success else "❌"
        print(f"  {status} Task {i}: {result.agent_type.value}")


def main():
    """Run all demos"""
    print("\n" + "🔬 " + "="*56 + " 🔬")
    print("   RESEARCH HUB - Multi-Agent Framework Demo")
    print("🔬 " + "="*56 + " 🔬")

    # Demo 1: Orchestrator
    demo_orchestrator()

    # Demo 2-4: Async workflows
    asyncio.run(demo_research_workflow())
    asyncio.run(demo_qa_workflow())
    asyncio.run(demo_parallel_execution())

    print("\n" + "="*60)
    print("✅ All demos completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  • Run 'streamlit run frontend/app.py' for the web UI")
    print("  • Check examples/ folder for more usage patterns")
    print("  • Read docs/ for detailed documentation")
    print()


if __name__ == "__main__":
    # Load .env file if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

    # Ensure API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ Please set ANTHROPIC_API_KEY environment variable or create .env file")
        exit(1)

    main()
