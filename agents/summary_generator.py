"""
Summary Generator Agent
Specializes in creating summaries, reports, and distilled insights
"""
import os
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import SUMMARY_GENERATOR_PROMPT


class SummaryGeneratorAgent:
    """
    Sub-agent specialized in generating summaries and reports
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Load system prompt from file
        self.system_prompt = SUMMARY_GENERATOR_PROMPT

    def generate_summary(
        self,
        content: str,
        summary_type: str = "standard",
        length: str = "medium",
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a summary of content
        """
        context = context or {}

        length_guide = {
            "brief": "2-3 sentences, <100 words",
            "medium": "1-2 paragraphs, 100-300 words",
            "detailed": "3-5 paragraphs, 300-600 words"
        }

        summary_prompt = f"""Generate a {summary_type} summary of this content:

Length: {length} ({length_guide.get(length, 'medium')})
Context: {context}

Content to summarize:
{content[:15000]}  # Limit to 15k chars

Provide summary in JSON format:
{{
    "title": "appropriate title for the summary",
    "summary_type": "{summary_type}",
    "summary": "the actual summary text",
    "key_points": ["point1", "point2", "point3"],
    "length": {{
        "word_count": approximate_count,
        "reading_time": "X minutes"
    }},
    "tags": ["tag1", "tag2"],
    "metadata": {{
        "completeness": "percentage of original info retained",
        "focus_areas": ["what was emphasized"]
    }}
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": summary_prompt}]
        )

        return {
            "agent": "summary_generator",
            "summary_type": summary_type,
            "result": response.content[0].text,
            "status": "completed"
        }

    def generate_multi_level_summary(self, content: str) -> Dict[str, Any]:
        """
        Generate summaries at multiple levels of detail
        """
        multi_level_prompt = f"""Create multi-level summaries of this content:

Content:
{content[:12000]}

Provide three levels in JSON format:
{{
    "executive_summary": {{
        "text": "2-3 sentences for executives/decision-makers",
        "key_takeaway": "single most important point"
    }},
    "standard_summary": {{
        "text": "1-2 paragraphs for general audience",
        "main_points": ["point1", "point2", "point3"]
    }},
    "detailed_summary": {{
        "text": "3-5 paragraphs with comprehensive coverage",
        "sections": [
            {{"title": "section name", "summary": "section summary"}}
        ],
        "insights": ["insight1", "insight2"]
    }}
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": multi_level_prompt}]
        )

        return {
            "agent": "summary_generator",
            "multi_level_summary": response.content[0].text
        }

    def generate_report(
        self,
        research_data: Dict[str, Any],
        report_type: str = "research_report",
        target_audience: str = "general"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report from research data
        """
        data_str = str(research_data)

        report_prompt = f"""Generate a {report_type} for {target_audience} audience:

Research Data:
{data_str[:10000]}

Structure the report with:
1. Executive Summary
2. Introduction/Background
3. Main Findings
4. Analysis/Discussion
5. Conclusions
6. Recommendations

Provide in JSON format:
{{
    "title": "report title",
    "executive_summary": "brief overview",
    "sections": [
        {{
            "section_title": "...",
            "content": "...",
            "key_points": []
        }}
    ],
    "conclusions": ["conclusion1", "conclusion2"],
    "recommendations": [
        {{
            "recommendation": "...",
            "priority": "high/medium/low",
            "rationale": "..."
        }}
    ],
    "metadata": {{
        "report_type": "{report_type}",
        "target_audience": "{target_audience}",
        "total_sections": count
    }}
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": report_prompt}]
        )

        return {
            "agent": "summary_generator",
            "report": response.content[0].text
        }

    def synthesize_multiple_sources(self, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synthesize information from multiple sources
        """
        sources_text = "\n\n".join([
            f"Source {i+1}: {src.get('title', 'Untitled')}\n{src.get('content', '')[:2000]}"
            for i, src in enumerate(sources)
        ])

        synthesis_prompt = f"""Synthesize information from these multiple sources:

{sources_text}

Create a synthesis in JSON format:
{{
    "unified_narrative": "coherent narrative combining all sources",
    "common_themes": ["theme1", "theme2"],
    "divergent_points": ["where sources disagree"],
    "comprehensive_insights": ["insight1", "insight2"],
    "source_contributions": {{
        "source1": "what this source contributed",
        "source2": "what this source contributed"
    }},
    "integrated_summary": "final synthesized summary"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )

        return {
            "agent": "summary_generator",
            "synthesis": response.content[0].text
        }


# Example usage
if __name__ == "__main__":
    agent = SummaryGeneratorAgent()
    result = agent.generate_summary(
        "Long document content here...",
        summary_type="executive",
        length="brief"
    )
    print(result)
