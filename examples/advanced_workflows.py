"""
Advanced workflow examples
"""
import asyncio
from agents import (
    AgentCoordinator,
    AgentHandoff,
    AgentType,
    HandoffPlan,
    HandoffStrategy
)


async def document_comparison_workflow():
    """Compare two documents and create a synthesis"""
    print("Document Comparison Workflow")
    print("-" * 40)

    coordinator = AgentCoordinator()

    doc1 = "Document 1 content about AI agents..."
    doc2 = "Document 2 content about AI agents..."

    # Analyze both in parallel
    analysis_results = await coordinator.execute_parallel_handoffs([
        AgentHandoff(
            agent_type=AgentType.DOCUMENT_ANALYZER,
            task="Analyze document 1",
            context={"content": doc1, "analysis_type": "comparative"}
        ),
        AgentHandoff(
            agent_type=AgentType.DOCUMENT_ANALYZER,
            task="Analyze document 2",
            context={"content": doc2, "analysis_type": "comparative"}
        )
    ])

    # Synthesize comparison
    synthesis = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create comparison synthesis",
            context={
                "sources": [r.result for r in analysis_results],
                "summary_type": "comparative"
            }
        )
    )

    print(f"Comparison completed: {synthesis.success}\n")


async def research_with_citations_workflow():
    """Research a topic and generate properly cited report"""
    print("Research with Citations Workflow")
    print("-" * 40)

    coordinator = AgentCoordinator()

    # Step 1: Research
    research = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Research AI agent frameworks",
            context={}
        )
    )

    # Step 2: Analyze
    analysis = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.DOCUMENT_ANALYZER,
            task="Analyze research findings",
            context={"research": research.result}
        )
    )

    # Step 3: Generate summary
    summary = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create research report",
            context={
                "analysis": analysis.result,
                "report_type": "research_report"
            }
        )
    )

    # Step 4: Generate citations
    citations = await coordinator.execute_handoff(
        AgentHandoff(
            agent_type=AgentType.CITATION_MANAGER,
            task="Create bibliography",
            context={
                "sources": research.result,
                "style": "APA"
            }
        )
    )

    print(f"Research report with citations: {citations.success}\n")


async def multi_level_summary_workflow():
    """Create summaries at multiple levels"""
    print("Multi-Level Summary Workflow")
    print("-" * 40)

    coordinator = AgentCoordinator()

    content = """
    Long research paper content here...
    This would typically be several pages of detailed research.
    """

    # Create summaries at different levels in parallel
    summaries = await coordinator.execute_parallel_handoffs([
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create executive summary",
            context={
                "content": content,
                "summary_type": "executive",
                "length": "brief"
            }
        ),
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create standard summary",
            context={
                "content": content,
                "summary_type": "standard",
                "length": "medium"
            }
        ),
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create detailed summary",
            context={
                "content": content,
                "summary_type": "technical",
                "length": "detailed"
            }
        )
    ])

    print(f"Created {len(summaries)} summary levels\n")


async def conditional_research_workflow():
    """Research with quality checks and refinement"""
    print("Conditional Research Workflow")
    print("-" * 40)

    coordinator = AgentCoordinator()

    def quality_check(response):
        """Check if research quality is sufficient"""
        if not response.success:
            return False
        # In real implementation, check quality metrics
        return True

    # Research with conditional continuation
    handoffs = [
        AgentHandoff(
            agent_type=AgentType.WEB_RESEARCHER,
            task="Initial research on topic",
            context={}
        ),
        AgentHandoff(
            agent_type=AgentType.DOCUMENT_ANALYZER,
            task="Quality check research",
            context={"check_quality": True}
        ),
        # This will only execute if quality check passes
        AgentHandoff(
            agent_type=AgentType.SUMMARY_GENERATOR,
            task="Create final report",
            context={}
        )
    ]

    results = await coordinator.execute_conditional_handoffs(
        handoffs,
        condition_func=quality_check
    )

    print(f"Completed {len(results)} conditional steps\n")


async def iterative_refinement_workflow():
    """Iteratively refine research"""
    print("Iterative Refinement Workflow")
    print("-" * 40)

    coordinator = AgentCoordinator()

    context = {}
    max_iterations = 3

    for i in range(max_iterations):
        print(f"Iteration {i+1}...")

        # Research
        research = await coordinator.execute_handoff(
            AgentHandoff(
                agent_type=AgentType.WEB_RESEARCHER,
                task="Research AI agent patterns",
                context=context
            )
        )

        # Analyze completeness
        analysis = await coordinator.execute_handoff(
            AgentHandoff(
                agent_type=AgentType.DOCUMENT_ANALYZER,
                task="Check research completeness",
                context={"research": research.result}
            )
        )

        # Check if complete (simplified)
        if analysis.success:
            print("Research complete!")
            break

        # Update context with gaps
        context["previous_research"] = research.result

    print()


async def main():
    """Run advanced workflows"""
    await document_comparison_workflow()
    await research_with_citations_workflow()
    await multi_level_summary_workflow()
    await conditional_research_workflow()
    await iterative_refinement_workflow()


if __name__ == "__main__":
    asyncio.run(main())
