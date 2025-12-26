"""Question answering with citations."""

from typing import List, Dict, Any, Optional
import openai
from anthropic import Anthropic
from .config import config
from .retriever import DocumentRetriever, SearchResult


class Citation:
    """Represents a source citation."""

    def __init__(self, repo_name: str, file_path: str, url: str, text_snippet: str):
        self.repo_name = repo_name
        self.file_path = file_path
        self.url = url
        self.text_snippet = text_snippet

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "repo_name": self.repo_name,
            "file_path": self.file_path,
            "url": self.url,
            "text_snippet": self.text_snippet,
        }

    def __repr__(self) -> str:
        return f"[{self.repo_name}/{self.file_path}]({self.url})"


class Answer:
    """Represents an answer with citations."""

    def __init__(self, question: str, answer: str, citations: List[Citation]):
        self.question = question
        self.answer = answer
        self.citations = citations

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "question": self.question,
            "answer": self.answer,
            "citations": [c.to_dict() for c in self.citations],
        }

    def format_markdown(self) -> str:
        """Format as Markdown with citations."""
        md = f"**Question:** {self.question}\n\n"
        md += f"**Answer:** {self.answer}\n\n"

        if self.citations:
            md += "**Sources:**\n"
            for i, citation in enumerate(self.citations, 1):
                md += f"{i}. [{citation.repo_name}/{citation.file_path}]({citation.url})\n"

        return md


class QuestionAnswering:
    """Question answering system with citations."""

    def __init__(self, retriever: DocumentRetriever = None):
        """Initialize the QA system.

        Args:
            retriever: DocumentRetriever instance
        """
        self.retriever = retriever or DocumentRetriever()

        # Initialize LLM client
        if config.LLM_PROVIDER == "openai":
            if not config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
            openai.api_key = config.OPENAI_API_KEY
            self.client = None  # Use openai module directly
        elif config.LLM_PROVIDER == "anthropic":
            if not config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider")
            self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")

    def answer(self, question: str, top_k: int = None) -> Answer:
        """Answer a question with citations.

        Args:
            question: Question to answer
            top_k: Number of documents to retrieve

        Returns:
            Answer object with citations
        """
        # Retrieve relevant documents
        search_results = self.retriever.search(question, top_k=top_k or config.TOP_K)

        if not search_results:
            return Answer(
                question=question,
                answer="I couldn't find any relevant information in the indexed documentation to answer this question.",
                citations=[],
            )

        # Generate answer using LLM
        answer_text = self._generate_answer(question, search_results)

        # Create citations
        citations = [
            Citation(
                repo_name=result.repo_name,
                file_path=result.file_path,
                url=result.url,
                text_snippet=result.text[:200] + "..." if len(result.text) > 200 else result.text,
            )
            for result in search_results
        ]

        return Answer(question=question, answer=answer_text, citations=citations)

    def _generate_answer(self, question: str, search_results: List[SearchResult]) -> str:
        """Generate answer using LLM.

        Args:
            question: Question to answer
            search_results: Retrieved documents

        Returns:
            Answer text
        """
        # Build context from search results
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"[Source {i}: {result.repo_name}/{result.file_path}]\n{result.text}\n"
            )
        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = self._build_prompt(question, context)

        # Generate answer based on provider
        if config.LLM_PROVIDER == "openai":
            return self._generate_openai(prompt)
        elif config.LLM_PROVIDER == "anthropic":
            return self._generate_anthropic(prompt)

    def _build_prompt(self, question: str, context: str) -> str:
        """Build prompt for LLM.

        Args:
            question: Question to answer
            context: Context from retrieved documents

        Returns:
            Formatted prompt
        """
        return f"""You are a helpful assistant that answers questions based on documentation.

Use the following documentation excerpts to answer the question. If the answer cannot be found in the provided context, say so.

Documentation:
{context}

Question: {question}

Provide a clear, accurate answer based on the documentation above. Reference specific sources when relevant."""

    def _generate_openai(self, prompt: str) -> str:
        """Generate answer using OpenAI.

        Args:
            prompt: Prompt text

        Returns:
            Generated answer
        """
        response = openai.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on provided documentation.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content

    def _generate_anthropic(self, prompt: str) -> str:
        """Generate answer using Anthropic Claude.

        Args:
            prompt: Prompt text

        Returns:
            Generated answer
        """
        response = self.client.messages.create(
            model=config.LLM_MODEL,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        return response.content[0].text
