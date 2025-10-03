"""
Basic usage examples for Research Hub
"""
import os
import asyncio
from agents import DocumentOrchestrator, AgentCoordinator, AgentHandoff, AgentType


def example_1_orchestrator():
    """Example 1: Using the Document Orchestrator"""
    print("=" * 60)
    print("Example 1: Document Orchestrator")
    print("=" * 60)

    # Initialize orchestrator
    orchestrator = DocumentOrchestrator()

    # Simple question
    response = orchestrator.process_message(
        "What are the key benefits of multi-agent systems?"
    )
    print(f"\nResponse: {response}\n")


async def example_2_research_workflow():
    """Example 2: Research Workflow"""
    print("=" * 60)
    print("Example 2: Research Workflow")
    print("=" * 60)

    # Initialize coordinator
    coordinator = AgentCoordinator()

    # Create research workflow
    plan = coordinator.create_research_workflow(
        "Latest developments in AI agents for 2025"
    )

    # Execute workflow
    results = await coordinator.execute_plan(plan)

    print(f"\nWorkflow completed with {len(results)} steps:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result.agent_type.value}: {'✓' if result.success else '✗'}")


async def example_3_qa_workflow():
    """Example 3: Question & Answer Workflow"""
    print("=" * 60)
    print("Example 3: Q&A Workflow")
    print("=" * 60)

    coordinator = AgentCoordinator()

    # Context about AI agents
    context = """
    AI agents are autonomous software entities that perceive their environment
    and take actions to achieve specific goals. They can be reactive, deliberative,
    or hybrid systems.
    """

    # Create Q&A workflow
    plan = coordinator.create_qa_workflow(
        question="What are the main types of AI agents?",
        context=context
    )

    # Execute
    results = await coordinator.execute_plan(plan)

    print(f"\nAnswer generated successfully: {results[-1].success}")


async def example_4_custom_workflow():
    """Example 4: Custom Workflow"""
    print("=" * 60)
    print("Example 4: Custom Workflow")
    print("=" * 60)

    coordinator = AgentCoordinator()

    # Manual handoffs
    # Step 1: Research
    research_result = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research Claude Agent SDK",
            context={}
        )
    )

    print(f"Research completed: {research_result.success}")

    # Step 2: Analyze
    if research_result.success:
        analysis_result = await coordinator.execute_handoff(
            AgentHandoff(
                agent_type=AgentType.DOCUMENT_ANALYZER,
                task="Analyze research findings",
                context={"research": research_result.result}
            )
        )
        print(f"Analysis completed: {analysis_result.success}")

        # Step 3: Summarize
        if analysis_result.success:
            summary_result = await coordinator.execute_handoff(
                AgentHandoff(
                    agent_type=AgentType.SUMMARY_GENERATOR,
                    task="Create executive summary",
                    context={
                        "content": analysis_result.result,
                        "summary_type": "executive",
                        "length": "brief"
                    }
                )
            )
            print(f"Summary created: {summary_result.success}")


async def example_5_parallel_execution():
    """Example 5: Parallel Agent Execution"""
    print("=" * 60)
    print("Example 5: Parallel Execution")
    print("=" * 60)

    coordinator = AgentCoordinator()

    # Research multiple topics in parallel
    handoffs = [
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI ethics",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI safety",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI governance",
            context={}
        )
    ]

    # Execute in parallel
    results = await coordinator.execute_parallel_handoffs(handoffs)

    print(f"\nCompleted {len(results)} parallel research tasks")
    for i, result in enumerate(results):
        print(f"Task {i+1}: {'✓' if result.success else '✗'}")


def main():
    """Run all examples"""
    # Example 1: Orchestrator (synchronous)
    example_1_orchestrator()

    # Examples 2-5: Async workflows
    asyncio.run(example_2_research_workflow())
    asyncio.run(example_3_qa_workflow())
    asyncio.run(example_4_custom_workflow())
    asyncio.run(example_5_parallel_execution())


if __name__ == "__main__":
    # Set API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        exit(1)

    main()
