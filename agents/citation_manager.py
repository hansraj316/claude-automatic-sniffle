"""
Citation Manager Agent
Specializes in managing citations, references, and bibliographies
"""
import os
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import CITATION_MANAGER_PROMPT


class CitationManagerAgent:
    """
    Sub-agent specialized in citation and reference management
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Load system prompt from file
        self.system_prompt = CITATION_MANAGER_PROMPT

    def create_citation(
        self,
        source_info: Dict[str, Any],
        citation_style: str = "APA",
        citation_type: str = "full"
    ) -> Dict[str, Any]:
        """
        Create a citation from source information
        """
        source_str = "\n".join([f"{k}: {v}" for k, v in source_info.items()])

        citation_prompt = f"""Create a {citation_style} citation for this source:

Source Information:
{source_str}

Citation Type: {citation_type} (full/in-text/parenthetical)

Provide citation in JSON format:
{{
    "citation_style": "{citation_style}",
    "full_citation": "complete formatted citation",
    "in_text_citation": "in-text citation format",
    "bibtex": "BibTeX entry if applicable",
    "source_type": "journal/book/website/etc",
    "key_elements": {{
        "author": "formatted author name(s)",
        "year": "publication year",
        "title": "title",
        "source": "journal/publisher/website"
    }},
    "citation_key": "unique identifier for this source"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": citation_prompt}]
        )

        return {
            "agent": "citation_manager",
            "citation_style": citation_style,
            "result": response.content[0].text,
            "status": "completed"
        }

    def generate_bibliography(
        self,
        citations: List[Dict[str, Any]],
        style: str = "APA",
        organize_by: str = "alphabetical"
    ) -> Dict[str, Any]:
        """
        Generate a bibliography from multiple citations
        """
        citations_text = "\n\n".join([
            f"Citation {i+1}:\n" + "\n".join([f"{k}: {v}" for k, v in cit.items()])
            for i, cit in enumerate(citations)
        ])

        bibliography_prompt = f"""Generate a bibliography in {style} format:

Citations:
{citations_text}

Organization: {organize_by} (alphabetical/chronological/by-type)

Provide bibliography in JSON format:
{{
    "style": "{style}",
    "organization": "{organize_by}",
    "bibliography": [
        {{
            "formatted_entry": "full formatted citation",
            "order": number,
            "category": "if organized by type"
        }}
    ],
    "total_sources": count,
    "source_breakdown": {{
        "journals": count,
        "books": count,
        "websites": count,
        "other": count
    }},
    "formatted_text": "ready-to-use bibliography text"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": bibliography_prompt}]
        )

        return {
            "agent": "citation_manager",
            "bibliography": response.content[0].text
        }

    def extract_citation_info(self, source_text: str, source_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract citation information from source text
        """
        extraction_prompt = f"""Extract citation information from this source:

Source Text:
{source_text[:5000]}

{f'URL: {source_url}' if source_url else ''}

Extract in JSON format:
{{
    "source_type": "journal/book/website/report/etc",
    "authors": [
        {{
            "full_name": "Author Name",
            "formatted": "Last, First"
        }}
    ],
    "title": "article or book title",
    "publication_info": {{
        "journal_name": "if journal article",
        "publisher": "if book",
        "website_name": "if online",
        "year": "publication year",
        "volume": "if applicable",
        "issue": "if applicable",
        "pages": "page range if applicable",
        "doi": "if available",
        "url": "{source_url if source_url else 'if available'}"
    }},
    "access_date": "{datetime.now().strftime('%Y-%m-%d')}",
    "confidence": "high/medium/low"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": extraction_prompt}]
        )

        return {
            "agent": "citation_manager",
            "extracted_info": response.content[0].text
        }

    def validate_citations(self, citations: List[str], style: str = "APA") -> Dict[str, Any]:
        """
        Validate citations for correctness and consistency
        """
        citations_text = "\n".join([f"{i+1}. {cit}" for i, cit in enumerate(citations)])

        validation_prompt = f"""Validate these {style} citations for correctness:

Citations to validate:
{citations_text}

Check for:
- Proper formatting according to {style} style
- Required elements present
- Consistency across citations
- Common errors (punctuation, capitalization, etc.)

Provide validation in JSON format:
{{
    "style": "{style}",
    "overall_validity": "valid/has_issues",
    "citations_checked": count,
    "issues_found": [
        {{
            "citation_number": number,
            "issue_type": "formatting/missing_element/inconsistency",
            "description": "what's wrong",
            "suggestion": "how to fix"
        }}
    ],
    "corrected_citations": [
        {{
            "original": "original citation",
            "corrected": "corrected version"
        }}
    ],
    "consistency_report": "overall consistency assessment"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": validation_prompt}]
        )

        return {
            "agent": "citation_manager",
            "validation": response.content[0].text
        }

    def convert_citation_style(self, citation: str, from_style: str, to_style: str) -> Dict[str, Any]:
        """
        Convert a citation from one style to another
        """
        conversion_prompt = f"""Convert this citation:

Original Citation ({from_style}):
{citation}

Convert to: {to_style}

Provide conversion in JSON format:
{{
    "original_style": "{from_style}",
    "target_style": "{to_style}",
    "original_citation": "{citation}",
    "converted_citation": "citation in new format",
    "conversion_notes": ["any notable changes or considerations"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": conversion_prompt}]
        )

        return {
            "agent": "citation_manager",
            "conversion": response.content[0].text
        }


# Example usage
if __name__ == "__main__":
    agent = CitationManagerAgent()
    result = agent.create_citation(
        {
            "author": "Smith, John",
            "year": "2024",
            "title": "AI Agents in Practice",
            "journal": "Journal of AI Research",
            "volume": "15",
            "pages": "120-135"
        },
        citation_style="APA"
    )
    print(result)
