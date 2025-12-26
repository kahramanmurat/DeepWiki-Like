"""Document retrieval and search."""

from typing import List, Dict, Any
import openai
from .config import config
from .indexer import VectorIndexer


class SearchResult:
    """Represents a search result."""

    def __init__(self, text: str, metadata: Dict[str, Any], score: float):
        self.text = text
        self.metadata = metadata
        self.score = score
        self.repo_name = metadata.get("repo_name", "")
        self.file_path = metadata.get("file_path", "")
        self.url = metadata.get("url", "")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "metadata": self.metadata,
            "score": self.score,
            "repo_name": self.repo_name,
            "file_path": self.file_path,
            "url": self.url,
        }

    def __repr__(self) -> str:
        return f"SearchResult(repo={self.repo_name}, file={self.file_path}, score={self.score:.3f})"


class DocumentRetriever:
    """Retrieves relevant documents for queries."""

    def __init__(self, indexer: VectorIndexer = None):
        """Initialize the retriever.

        Args:
            indexer: VectorIndexer instance (creates new one if not provided)
        """
        self.indexer = indexer or VectorIndexer()

        # Initialize OpenAI for embeddings
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY

    def search(self, query: str, top_k: int = None) -> List[SearchResult]:
        """Search for documents relevant to the query.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of SearchResult objects
        """
        top_k = top_k or config.TOP_K

        # Generate query embedding
        query_embedding = self._generate_query_embedding(query)

        # Search in ChromaDB
        results = self.indexer.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        # Convert to SearchResult objects
        search_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                search_results.append(
                    SearchResult(
                        text=doc,
                        metadata=results["metadatas"][0][i],
                        score=1.0 - results["distances"][0][i],  # Convert distance to similarity
                    )
                )

        return search_results

    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query.

        Args:
            query: Query text

        Returns:
            Embedding vector
        """
        response = openai.embeddings.create(
            model=config.EMBEDDING_MODEL,
            input=query,
        )
        return response.data[0].embedding
