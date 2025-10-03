"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def test_api_key():
    """API key for testing"""
    return os.getenv("ANTHROPIC_API_KEY", "test_api_key")


@pytest.fixture(scope="session")
def test_data_dir():
    """Test data directory"""
    test_dir = Path(__file__).parent / "test_data"
    test_dir.mkdir(exist_ok=True)
    return test_dir


@pytest.fixture
def sample_document():
    """Sample document for testing"""
    return """
    Artificial Intelligence (AI) refers to the simulation of human intelligence
    in machines that are programmed to think and learn. AI agents are autonomous
    entities that perceive their environment and take actions to achieve goals.
    """


@pytest.fixture
def sample_research_data():
    """Sample research data"""
    return {
        "query": "AI developments 2025",
        "sources": [
            {
                "url": "https://example.com/ai-2025",
                "title": "AI Trends 2025",
                "content": "AI is advancing rapidly..."
            }
        ],
        "findings": [
            "Multi-agent systems are growing",
            "LLMs are becoming more capable"
        ]
    }
