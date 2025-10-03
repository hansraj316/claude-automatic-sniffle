"""
Q&A Agent
Specializes in answering questions using retrieved context and knowledge
"""
import os
import sys
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from prompts import QA_AGENT_PROMPT


class QAAgent:
    """
    Sub-agent specialized in question answering
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=self.api_key)
        self.model = model

        # Load system prompt from file
        self.system_prompt = QA_AGENT_PROMPT

    def answer_question(
        self,
        question: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using available context
        """
        conversation_history = conversation_history or []

        # Build conversation context
        history_text = ""
        if conversation_history:
            history_text = "Previous conversation:\n" + "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history[-5:]  # Last 5 messages
            ])

        qa_prompt = f"""Answer this question comprehensively:

Question: {question}

{f'Context: {context}' if context else ''}

{history_text if history_text else ''}

Provide your answer in JSON format:
{{
    "question": "{question}",
    "answer": "comprehensive answer",
    "confidence": "high/medium/low",
    "sources": [
        {{
            "type": "context/knowledge/inference",
            "content": "specific source or reasoning"
        }}
    ],
    "key_points": ["point1", "point2"],
    "follow_up_questions": ["suggested question1", "suggested question2"],
    "caveats": ["any limitations or uncertainties"],
    "related_topics": ["topic1", "topic2"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2500,
            system=self.system_prompt,
            messages=[{"role": "user", "content": qa_prompt}]
        )

        return {
            "agent": "qa_agent",
            "question": question,
            "result": response.content[0].text,
            "status": "completed"
        }

    def explain_concept(self, concept: str, depth: str = "standard", audience: str = "general") -> Dict[str, Any]:
        """
        Explain a concept at appropriate depth for audience
        """
        depth_guide = {
            "brief": "2-3 sentences, high-level overview",
            "standard": "2-3 paragraphs, balanced explanation",
            "detailed": "comprehensive explanation with examples"
        }

        explanation_prompt = f"""Explain this concept:

Concept: {concept}
Depth: {depth} ({depth_guide.get(depth, 'standard')})
Audience: {audience}

Provide explanation in JSON format:
{{
    "concept": "{concept}",
    "simple_definition": "one sentence definition",
    "detailed_explanation": "full explanation at requested depth",
    "key_characteristics": ["characteristic1", "characteristic2"],
    "examples": [
        {{
            "example": "example description",
            "relevance": "why this example helps understanding"
        }}
    ],
    "analogies": ["helpful analogy1"],
    "common_misconceptions": ["misconception1"],
    "related_concepts": ["related1", "related2"],
    "practical_applications": ["application1"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": explanation_prompt}]
        )

        return {
            "agent": "qa_agent",
            "explanation": response.content[0].text
        }

    def compare_concepts(self, concept1: str, concept2: str) -> Dict[str, Any]:
        """
        Compare and contrast two concepts
        """
        comparison_prompt = f"""Compare and contrast these concepts:

Concept 1: {concept1}
Concept 2: {concept2}

Provide comparison in JSON format:
{{
    "concepts": ["{concept1}", "{concept2}"],
    "similarities": [
        {{
            "aspect": "what's similar",
            "description": "how they're similar"
        }}
    ],
    "differences": [
        {{
            "aspect": "what differs",
            "concept1": "how concept1 approaches this",
            "concept2": "how concept2 approaches this"
        }}
    ],
    "use_cases": {{
        "{concept1}": "when to use concept1",
        "{concept2}": "when to use concept2"
    }},
    "relationship": "how the concepts relate to each other",
    "summary": "overall comparison summary"
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": comparison_prompt}]
        )

        return {
            "agent": "qa_agent",
            "comparison": response.content[0].text
        }

    def generate_faq(self, topic: str, num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate frequently asked questions about a topic
        """
        faq_prompt = f"""Generate {num_questions} frequently asked questions about this topic:

Topic: {topic}

Include a mix of:
- Basic/foundational questions
- Practical application questions
- Common confusion points

Provide FAQ in JSON format:
{{
    "topic": "{topic}",
    "faqs": [
        {{
            "question": "the question",
            "category": "basic/intermediate/advanced",
            "answer": "clear, concise answer",
            "why_important": "why this question matters"
        }}
    ],
    "additional_resources": ["resource1", "resource2"]
}}
"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=self.system_prompt,
            messages=[{"role": "user", "content": faq_prompt}]
        )

        return {
            "agent": "qa_agent",
            "faq": response.content[0].text
        }


# Example usage
if __name__ == "__main__":
    agent = QAAgent()
    result = agent.answer_question(
        "What are AI agents?",
        context="AI agents are autonomous systems that can perceive, decide, and act..."
    )
    print(result)
