"""Agent System Prompts"""
import os
from pathlib import Path


def load_prompt(prompt_name: str) -> str:
    """Load a prompt from file"""
    prompt_file = Path(__file__).parent / f"{prompt_name}_prompt.txt"
    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")


# Load all prompts
ORCHESTRATOR_PROMPT = load_prompt("orchestrator")
WEB_RESEARCHER_PROMPT = load_prompt("web_researcher")
DOCUMENT_ANALYZER_PROMPT = load_prompt("document_analyzer")
SUMMARY_GENERATOR_PROMPT = load_prompt("summary_generator")
QA_AGENT_PROMPT = load_prompt("qa_agent")
CITATION_MANAGER_PROMPT = load_prompt("citation_manager")

__all__ = [
    "load_prompt",
    "ORCHESTRATOR_PROMPT",
    "WEB_RESEARCHER_PROMPT",
    "DOCUMENT_ANALYZER_PROMPT",
    "SUMMARY_GENERATOR_PROMPT",
    "QA_AGENT_PROMPT",
    "CITATION_MANAGER_PROMPT"
]
