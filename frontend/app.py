"""
Research Hub - Streamlit Frontend
Multi-agent knowledge management and research assistant
"""
import streamlit as st
import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import DocumentOrchestrator
from agents.agent_coordinator import AgentCoordinator, HandoffPlan, HandoffStrategy
from agents.orchestrator import AgentHandoff, AgentType


# Page configuration
st.set_page_config(
    page_title="Research Hub",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .agent-name {
        font-weight: 600;
        color: #1f77b4;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'orchestrator' not in st.session_state:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        st.session_state.orchestrator = DocumentOrchestrator(api_key=api_key)
    if 'coordinator' not in st.session_state:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        st.session_state.coordinator = AgentCoordinator(api_key=api_key)
    if 'workflow_mode' not in st.session_state:
        st.session_state.workflow_mode = "auto"
    if 'handoff_history' not in st.session_state:
        st.session_state.handoff_history = []


def display_agent_status(handoff_history: List[Dict]):
    """Display active agents and their status"""
    if handoff_history:
        st.sidebar.markdown("### 🤖 Active Agents")
        for handoff in handoff_history[-5:]:  # Show last 5
            status_icon = "✅" if handoff.get("success") else "❌"
            agent_name = handoff.get("agent", "Unknown").replace("_", " ").title()
            st.sidebar.markdown(f"{status_icon} **{agent_name}**")
            if handoff.get("task"):
                st.sidebar.caption(handoff["task"][:50] + "..." if len(handoff["task"]) > 50 else handoff["task"])


def render_sidebar():
    """Render sidebar with configuration options"""
    st.sidebar.markdown("# ⚙️ Configuration")

    # API Key status
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        st.sidebar.success("✅ API Key Configured")
    else:
        st.sidebar.error("❌ API Key Missing")
        st.sidebar.caption("Set ANTHROPIC_API_KEY environment variable")

    st.sidebar.markdown("---")

    # Workflow mode selection
    st.sidebar.markdown("### 🔄 Workflow Mode")
    workflow_mode = st.sidebar.radio(
        "Select Mode",
        ["auto", "research", "qa", "summary", "custom"],
        index=["auto", "research", "qa", "summary", "custom"].index(st.session_state.workflow_mode),
        help="Auto: Orchestrator decides | Others: Predefined workflows"
    )
    st.session_state.workflow_mode = workflow_mode

    st.sidebar.markdown("---")

    # Agent status
    display_agent_status(st.session_state.handoff_history)

    st.sidebar.markdown("---")

    # Model selection
    st.sidebar.markdown("### 🧠 Model Settings")
    model = st.sidebar.selectbox(
        "Claude Model",
        ["claude-sonnet-4-5-20250929", "claude-opus-4-20250514"],
        index=0
    )

    st.sidebar.markdown("---")

    # Clear history button
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.handoff_history = []
        st.session_state.orchestrator.clear_history()
        st.session_state.coordinator.clear_history()
        st.rerun()

    return workflow_mode, model


def render_agent_info():
    """Render information about available agents"""
    with st.expander("📚 Available Agents", expanded=False):
        cols = st.columns(3)

        with cols[0]:
            st.markdown("**🔍 Web Researcher**")
            st.caption("Searches web, validates sources, extracts information")

            st.markdown("**📄 Document Analyzer**")
            st.caption("Analyzes documents, extracts insights, processes data")

        with cols[1]:
            st.markdown("**📝 Summary Generator**")
            st.caption("Creates summaries, reports, distilled insights")

            st.markdown("**💬 Q&A Agent**")
            st.caption("Answers questions using retrieved context")

        with cols[2]:
            st.markdown("**📖 Citation Manager**")
            st.caption("Manages citations, references, bibliographies")


async def execute_workflow(user_message: str, workflow_mode: str, model: str):
    """Execute the appropriate workflow based on mode"""
    coordinator = st.session_state.coordinator

    if workflow_mode == "auto":
        # Use orchestrator for automatic workflow
        response = st.session_state.orchestrator.process_message(user_message)
        return response, []

    elif workflow_mode == "research":
        # Research workflow: Web Research → Analysis → Summary
        plan = coordinator.create_research_workflow(user_message)
        results = await coordinator.execute_plan(plan)

        # Extract final summary
        summary_result = results[-1] if results else None
        response = summary_result.result.get("result", "No summary generated") if summary_result and summary_result.success else "Workflow failed"

        return response, results

    elif workflow_mode == "qa":
        # Q&A workflow
        plan = coordinator.create_qa_workflow(user_message)
        results = await coordinator.execute_plan(plan)

        qa_result = results[-1] if results else None
        response = qa_result.result.get("result", "No answer generated") if qa_result and qa_result.success else "Workflow failed"

        return response, results

    elif workflow_mode == "summary":
        # Summary workflow: Analyze → Summarize
        plan = HandoffPlan(
            strategy=HandoffStrategy.SEQUENTIAL,
            agents=[
                AgentHandoff(
                    agent_type=AgentType.SUMMARY_GENERATOR,
                    task=f"Summarize: {user_message}",
                    context={"content": user_message, "summary_type": "standard", "length": "medium"},
                    priority=1
                )
            ]
        )
        results = await coordinator.execute_plan(plan)

        summary_result = results[0] if results else None
        response = summary_result.result.get("result", "No summary generated") if summary_result and summary_result.success else "Workflow failed"

        return response, results

    else:  # custom
        # Let user decide
        response = "Custom workflow mode - please specify which agents to use"
        return response, []


def main():
    """Main application"""
    initialize_session_state()

    # Render header
    st.markdown('<div class="main-header">🔬 Research Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multi-Agent Knowledge Management & Research Assistant</div>', unsafe_allow_html=True)

    # Render sidebar
    workflow_mode, model = render_sidebar()

    # Render agent info
    render_agent_info()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show agent workflow if available
            if "agents_used" in message and message["agents_used"]:
                with st.expander("Agent Workflow", expanded=False):
                    for agent_info in message["agents_used"]:
                        st.markdown(f"**{agent_info.get('agent', 'Unknown')}**: {agent_info.get('status', 'unknown')}")

    # Chat input
    if prompt := st.chat_input("Ask me anything about research, documents, or get summaries..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process with agents
        with st.chat_message("assistant"):
            with st.spinner("Agents working..."):
                # Run async workflow
                response, results = asyncio.run(execute_workflow(prompt, workflow_mode, model))

                # Update handoff history
                handoff_history = st.session_state.coordinator.get_handoff_history()
                st.session_state.handoff_history = handoff_history

                # Display response
                st.markdown(response)

                # Show agent workflow
                if results:
                    with st.expander("Agent Workflow", expanded=False):
                        for result in results:
                            status = "✅" if result.success else "❌"
                            st.markdown(f"{status} **{result.agent_type.value.replace('_', ' ').title()}**")
                            if result.error:
                                st.error(result.error)

        # Add assistant message
        agents_used = [
            {"agent": r.agent_type.value, "status": "success" if r.success else "failed"}
            for r in results
        ] if results else []

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "agents_used": agents_used
        })

    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #666;">Powered by Claude Sonnet 4.5 & Multi-Agent Framework</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
