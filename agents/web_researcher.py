"""
Web Research Agent
Specializes in web search, source validation, and information extraction
"""
import os
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import WEB_RESEARCHER_PROMPT


class WebResearcherAgent:
    """
    Sub-agent specialized in web research and information gathering
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Load system prompt from file
        self.system_prompt = WEB_RESEARCHER_PROMPT

    def research(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Conduct web research on a given query
        """
        context = context or {}

        research_prompt = f"""Conduct web research on the following query:

Query: {query}

Additional context: {context}

Steps to follow:
1. Formulate effective search queries
2. Identify credible sources
3. Extract relevant information
4. Validate and cross-reference findings
5. Organize findings coherently

Provide your research results in JSON format:
{{
    "query": "original query",
    "search_queries_used": ["query1", "query2"],
    "sources": [
        {{
            "url": "source URL",
            "title": "source title",
            "credibility": "high/medium/low",
            "key_findings": ["finding1", "finding2"],
            "publication_date": "date if available"
        }}
    ],
    "summary": "overall summary of findings",
    "confidence": "high/medium/low",
    "recommendations": ["recommendation1", "recommendation2"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": research_prompt}]
        )

        # In a real implementation, this would use MCP web search tools
        # For now, we return the structured response
        return {
            "agent": "web_researcher",
            "query": query,
            "result": response.content[0].text,
            "status": "completed"
        }

    def validate_source(self, url: str) -> Dict[str, Any]:
        """
        Validate the credibility of a web source
        """
        validation_prompt = f"""Analyze the credibility of this source:

URL: {url}

Consider:
1. Domain authority (.edu, .gov, established organizations)
2. Author credentials
3. Publication date and currency
4. Bias and objectivity
5. Citations and references
6. Overall reliability

Provide validation results in JSON format:
{{
    "url": "{url}",
    "credibility_score": 0-100,
    "factors": {{
        "domain_authority": "high/medium/low",
        "content_quality": "high/medium/low",
        "bias_level": "low/medium/high",
        "currency": "current/outdated/unknown"
    }},
    "recommendation": "use/use_with_caution/avoid",
    "notes": "additional observations"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": validation_prompt}]
        )

        return {
            "agent": "web_researcher",
            "validation": response.content[0].text
        }

    def extract_information(self, content: str, extraction_goals: List[str]) -> Dict[str, Any]:
        """
        Extract specific information from web content
        """
        goals_str = "\n".join(f"- {goal}" for goal in extraction_goals)

        extraction_prompt = f"""Extract the following information from this content:

Extraction goals:
{goals_str}

Content:
{content[:5000]}  # Limit content length

Provide extracted information in JSON format with each goal as a key.
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": extraction_prompt}]
        )

        return {
            "agent": "web_researcher",
            "extracted_info": response.content[0].text
        }


# Example usage
if __name__ == "__main__":
    agent = WebResearcherAgent()
    result = agent.research("Latest developments in AI agents")
    print(result)
