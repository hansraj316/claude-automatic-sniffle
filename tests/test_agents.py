"""
Tests for individual agents
"""
import pytest
import os
from agents import (
    WebResearcherAgent,
    DocumentAnalyzerAgent,
    SummaryGeneratorAgent,
    QAAgent,
    CitationManagerAgent
)


@pytest.fixture
def api_key():
    """Get API key from environment"""
    return os.getenv("ANTHROPIC_API_KEY", "test_key")


class TestWebResearcherAgent:
    def test_initialization(self, api_key):
        agent = WebResearcherAgent(api_key=api_key)
        assert agent.api_key == api_key
        assert agent.system_prompt is not None

    def test_research(self, api_key):
        agent = WebResearcherAgent(api_key=api_key)
        result = agent.research("test query")
        assert "agent" in result
        assert result["agent"] == "web_researcher"

    def test_validate_source(self, api_key):
        agent = WebResearcherAgent(api_key=api_key)
        result = agent.validate_source("https://example.com")
        assert "agent" in result
        assert "validation" in result


class TestDocumentAnalyzerAgent:
    def test_initialization(self, api_key):
        agent = DocumentAnalyzerAgent(api_key=api_key)
        assert agent.api_key == api_key
        assert agent.system_prompt is not None

    def test_analyze_document(self, api_key):
        agent = DocumentAnalyzerAgent(api_key=api_key)
        result = agent.analyze_document("Test content", analysis_type="general")
        assert "agent" in result
        assert result["agent"] == "document_analyzer"

    def test_compare_documents(self, api_key):
        agent = DocumentAnalyzerAgent(api_key=api_key)
        docs = [
            {"title": "Doc 1", "content": "Content 1"},
            {"title": "Doc 2", "content": "Content 2"}
        ]
        result = agent.compare_documents(docs)
        assert "agent" in result
        assert "comparison_result" in result


class TestSummaryGeneratorAgent:
    def test_initialization(self, api_key):
        agent = SummaryGeneratorAgent(api_key=api_key)
        assert agent.api_key == api_key
        assert agent.system_prompt is not None

    def test_generate_summary(self, api_key):
        agent = SummaryGeneratorAgent(api_key=api_key)
        result = agent.generate_summary(
            "Long content here...",
            summary_type="standard",
            length="medium"
        )
        assert "agent" in result
        assert result["agent"] == "summary_generator"

    def test_generate_multi_level_summary(self, api_key):
        agent = SummaryGeneratorAgent(api_key=api_key)
        result = agent.generate_multi_level_summary("Content to summarize")
        assert "agent" in result
        assert "multi_level_summary" in result


class TestQAAgent:
    def test_initialization(self, api_key):
        agent = QAAgent(api_key=api_key)
        assert agent.api_key == api_key
        assert agent.system_prompt is not None

    def test_answer_question(self, api_key):
        agent = QAAgent(api_key=api_key)
        result = agent.answer_question(
            "What is AI?",
            context="AI is artificial intelligence"
        )
        assert "agent" in result
        assert result["agent"] == "qa_agent"

    def test_explain_concept(self, api_key):
        agent = QAAgent(api_key=api_key)
        result = agent.explain_concept("Machine Learning", depth="standard")
        assert "agent" in result
        assert "explanation" in result


class TestCitationManagerAgent:
    def test_initialization(self, api_key):
        agent = CitationManagerAgent(api_key=api_key)
        assert agent.api_key == api_key
        assert agent.system_prompt is not None

    def test_create_citation(self, api_key):
        agent = CitationManagerAgent(api_key=api_key)
        source_info = {
            "author": "Smith, J.",
            "year": "2024",
            "title": "Test Article"
        }
        result = agent.create_citation(source_info, citation_style="APA")
        assert "agent" in result
        assert result["agent"] == "citation_manager"

    def test_generate_bibliography(self, api_key):
        agent = CitationManagerAgent(api_key=api_key)
        citations = [
            {"author": "Smith, J.", "year": "2024", "title": "Article 1"},
            {"author": "Jones, A.", "year": "2023", "title": "Article 2"}
        ]
        result = agent.generate_bibliography(citations, style="APA")
        assert "agent" in result
        assert "bibliography" in result
