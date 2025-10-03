"""
Agent Workflow Visualizer Component
"""
import streamlit as st
from typing import List, Dict, Any
import json


def render_agent_workflow(results: List[Any], detailed: bool = False):
    """
    Render agent workflow visualization
    """
    if not results:
        st.info("No agent workflow to display")
        return

    st.markdown("### 🔄 Agent Workflow")

    for i, result in enumerate(results):
        status_color = "🟢" if result.success else "🔴"
        agent_name = result.agent_type.value.replace("_", " ").title()

        # Agent card
        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"{status_color} **Step {i+1}: {agent_name}**")

            with col2:
                if result.success:
                    st.success("Success")
                else:
                    st.error("Failed")

            if detailed and result.result:
                with st.expander(f"Details for {agent_name}"):
                    st.json(result.result)

            if result.error:
                st.error(f"Error: {result.error}")

        # Arrow to next step
        if i < len(results) - 1:
            st.markdown("↓")


def render_agent_metrics(handoff_history: List[Dict[str, Any]]):
    """
    Render agent performance metrics
    """
    if not handoff_history:
        return

    st.markdown("### 📊 Agent Metrics")

    # Count agent usage
    agent_counts = {}
    success_counts = {}

    for handoff in handoff_history:
        agent = handoff.get("agent", "unknown")
        agent_counts[agent] = agent_counts.get(agent, 0) + 1

        if handoff.get("success"):
            success_counts[agent] = success_counts.get(agent, 0) + 1

    # Display metrics
    cols = st.columns(len(agent_counts))

    for i, (agent, count) in enumerate(agent_counts.items()):
        with cols[i]:
            agent_name = agent.replace("_", " ").title()
            success_rate = (success_counts.get(agent, 0) / count * 100) if count > 0 else 0

            st.metric(
                label=agent_name,
                value=f"{count} calls",
                delta=f"{success_rate:.0f}% success"
            )


def render_handoff_timeline(handoff_history: List[Dict[str, Any]]):
    """
    Render handoff timeline
    """
    if not handoff_history:
        return

    st.markdown("### ⏱️ Handoff Timeline")

    for handoff in handoff_history[-10:]:  # Last 10
        agent = handoff.get("agent", "unknown").replace("_", " ").title()
        task = handoff.get("task", "No task")
        timestamp = handoff.get("timestamp", 0)
        success = handoff.get("success", False)

        status_icon = "✅" if success else "❌"

        st.markdown(f"{status_icon} **{agent}** - {task[:60]}{'...' if len(task) > 60 else ''}")
        st.caption(f"Time: {timestamp:.2f}s" if timestamp else "Time: N/A")
        st.markdown("---")
