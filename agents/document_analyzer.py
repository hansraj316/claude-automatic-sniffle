"""
Document Analyzer Agent
Specializes in document analysis, insight extraction, and data processing
"""
import os
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import DOCUMENT_ANALYZER_PROMPT


class DocumentAnalyzerAgent:
    """
    Sub-agent specialized in document analysis and insight extraction
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Load system prompt from file
        self.system_prompt = DOCUMENT_ANALYZER_PROMPT

    def analyze_document(self, content: str, analysis_type: str = "general", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a document and extract insights
        """
        context = context or {}

        analysis_prompt = f"""Analyze this document:

Analysis Type: {analysis_type}
Context: {context}

Document Content:
{content[:10000]}  # Limit to 10k chars

Provide analysis in JSON format:
{{
    "document_type": "type of document",
    "main_themes": ["theme1", "theme2"],
    "key_points": [
        {{"point": "...", "importance": "high/medium/low", "evidence": "..."}}
    ],
    "entities": {{
        "people": [],
        "organizations": [],
        "locations": [],
        "concepts": []
    }},
    "sentiment": {{
        "overall": "positive/neutral/negative",
        "confidence": 0-100
    }},
    "insights": ["insight1", "insight2"],
    "summary": "concise summary",
    "recommendations": ["recommendation1"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        return {
            "agent": "document_analyzer",
            "analysis_type": analysis_type,
            "result": response.content[0].text,
            "status": "completed"
        }

    def compare_documents(self, documents: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Compare multiple documents
        """
        docs_text = "\n\n---\n\n".join([
            f"Document {i+1} ({doc.get('title', 'Untitled')}):\n{doc.get('content', '')[:3000]}"
            for i, doc in enumerate(documents)
        ])

        comparison_prompt = f"""Compare these documents:

{docs_text}

Provide comparison in JSON format:
{{
    "similarities": ["similarity1", "similarity2"],
    "differences": ["difference1", "difference2"],
    "unique_insights": {{
        "doc1": ["insight1"],
        "doc2": ["insight1"]
    }},
    "synthesis": "overall synthesis of all documents",
    "recommendations": ["which document for what purpose"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": comparison_prompt}]
        )

        return {
            "agent": "document_analyzer",
            "comparison_result": response.content[0].text
        }

    def extract_structured_data(self, content: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data from document based on schema
        """
        schema_str = str(schema)

        extraction_prompt = f"""Extract structured data from this document according to the schema:

Schema:
{schema_str}

Document:
{content[:8000]}

Return data matching the schema structure exactly.
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": extraction_prompt}]
        )

        return {
            "agent": "document_analyzer",
            "structured_data": response.content[0].text
        }

    def identify_relationships(self, content: str) -> Dict[str, Any]:
        """
        Identify relationships between concepts in document
        """
        relationship_prompt = f"""Identify key relationships between concepts in this document:

{content[:8000]}

Provide relationships in JSON format:
{{
    "relationships": [
        {{
            "entity1": "concept/entity 1",
            "relationship_type": "causes/influences/is_part_of/etc",
            "entity2": "concept/entity 2",
            "strength": "strong/moderate/weak",
            "evidence": "supporting text"
        }}
    ],
    "concept_map": "description of how concepts relate",
    "key_insights": ["insight from relationships"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": relationship_prompt}]
        )

        return {
            "agent": "document_analyzer",
            "relationships": response.content[0].text
        }


# Example usage
if __name__ == "__main__":
    agent = DocumentAnalyzerAgent()
    result = agent.analyze_document(
        "Sample document content here...",
        analysis_type="general"
    )
    print(result)
