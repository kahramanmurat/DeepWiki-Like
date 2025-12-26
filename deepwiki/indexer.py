"""Document indexing with embeddings and vector storage."""

import re
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import openai
from .config import config
from .crawler import MarkdownDocument


class DocumentChunker:
    """Splits documents into chunks for indexing."""

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """Initialize the chunker.

        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or config.CHUNK_OVERLAP

    def chunk_document(self, document: MarkdownDocument) -> List[Dict[str, Any]]:
        """Split a document into chunks.

        Args:
            document: MarkdownDocument to chunk

        Returns:
            List of chunk dictionaries with metadata
        """
        # First, try to split by headers for better semantic chunks
        chunks = self._split_by_headers(document.content)

        # If chunks are too large, split them further
        final_chunks = []
        for i, chunk_text in enumerate(chunks):
            if len(chunk_text) > self.chunk_size:
                # Split large chunks by paragraphs
                sub_chunks = self._split_by_size(chunk_text)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk_text)

        # Create chunk objects with metadata
        chunk_objects = []
        for i, chunk_text in enumerate(final_chunks):
            chunk_objects.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        "repo_name": document.repo_name,
                        "file_path": document.path,
                        "url": document.url,
                        "chunk_index": i,
                        "total_chunks": len(final_chunks),
                    },
                }
            )

        return chunk_objects

    def _split_by_headers(self, text: str) -> List[str]:
        """Split text by Markdown headers.

        Args:
            text: Markdown text to split

        Returns:
            List of text chunks split by headers
        """
        # Split by headers (# ## ### etc.)
        header_pattern = r"^#{1,6}\s+.+$"
        lines = text.split("\n")

        chunks = []
        current_chunk = []

        for line in lines:
            if re.match(header_pattern, line) and current_chunk:
                # Start new chunk at header
                chunks.append("\n".join(current_chunk))
                current_chunk = [line]
            else:
                current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks if chunks else [text]

    def _split_by_size(self, text: str) -> List[str]:
        """Split text into chunks by size with overlap.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at paragraph boundary
            if end < len(text):
                # Look for double newline (paragraph break)
                paragraph_break = text.rfind("\n\n", start, end)
                if paragraph_break > start:
                    end = paragraph_break
                else:
                    # Look for single newline
                    newline = text.rfind("\n", start, end)
                    if newline > start:
                        end = newline

            chunks.append(text[start:end].strip())
            start = end - self.chunk_overlap

        return chunks


class VectorIndexer:
    """Manages vector embeddings and search index."""

    def __init__(self, collection_name: str = "deepwiki"):
        """Initialize the indexer.

        Args:
            collection_name: Name of the ChromaDB collection
        """
        config.validate()

        self.collection_name = collection_name
        self.chunker = DocumentChunker()

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(config.CHROMA_DB_DIR),
            settings=Settings(anonymized_telemetry=False),
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "DeepWiki markdown documentation"},
        )

        # Initialize OpenAI for embeddings
        if config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY

    def index_documents(self, documents: List[MarkdownDocument]) -> int:
        """Index a list of documents.

        Args:
            documents: List of MarkdownDocument objects to index

        Returns:
            Number of chunks indexed
        """
        print(f"Indexing {len(documents)} documents in streaming mode...")

        total_chunks = 0
        batch_size = 25  # Very small batches for low memory footprint
        current_batch_chunks = []

        # Process documents one at a time to minimize memory usage
        for doc_idx, doc in enumerate(documents, 1):
            print(f"  Processing document {doc_idx}/{len(documents)}: {doc.path}")

            # Chunk this document
            chunks = self.chunker.chunk_document(doc)
            print(f"    Created {len(chunks)} chunks")

            # Add chunks to current batch
            current_batch_chunks.extend(chunks)

            # Process batch when it reaches size limit or is last document
            while len(current_batch_chunks) >= batch_size or (doc_idx == len(documents) and current_batch_chunks):
                # Take next batch
                batch = current_batch_chunks[:batch_size]
                current_batch_chunks = current_batch_chunks[batch_size:]

                # Prepare batch data
                texts = [chunk["text"] for chunk in batch]
                metadatas = [chunk["metadata"] for chunk in batch]
                ids = [f"{chunk['metadata']['repo_name']}::{chunk['metadata']['file_path']}::{total_chunks + i}"
                       for i in range(len(batch))]

                print(f"    Generating embeddings for {len(batch)} chunks...")
                batch_embeddings = self._generate_embeddings(texts)

                print(f"    Saving to database...")
                self.collection.add(
                    embeddings=batch_embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids,
                )

                total_chunks += len(batch)
                print(f"    ✓ Indexed {total_chunks} total chunks so far")

                # Break if no more chunks to process
                if not current_batch_chunks:
                    break

        print(f"Successfully indexed {total_chunks} chunks from {len(documents)} documents")
        return total_chunks

    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts using OpenAI.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        # For small batches (< 25), send all at once
        # Otherwise, split into sub-batches
        if len(texts) <= 25:
            response = openai.embeddings.create(
                model=config.EMBEDDING_MODEL,
                input=texts,
            )
            return [item.embedding for item in response.data]

        # For larger batches, process in sub-batches
        embeddings = []
        batch_size = 25

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = openai.embeddings.create(
                model=config.EMBEDDING_MODEL,
                input=batch,
            )
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)

        return embeddings

    def clear_repository(self, repo_name: str) -> None:
        """Clear all documents from a specific repository.

        Args:
            repo_name: Name of the repository to clear
        """
        # ChromaDB doesn't support delete by metadata filter directly
        # We need to query and delete
        results = self.collection.get(where={"repo_name": repo_name})
        if results["ids"]:
            self.collection.delete(ids=results["ids"])
            print(f"Cleared {len(results['ids'])} chunks from {repo_name}")
        else:
            print(f"No documents found for {repo_name}")

    def clear_all(self) -> None:
        """Clear all documents from the index."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "DeepWiki markdown documentation"},
        )
        print("Cleared all indexed documents")

    def list_repositories(self) -> List[str]:
        """List all indexed repositories.

        Returns:
            List of repository names
        """
        # Get all items (this could be slow for large collections)
        results = self.collection.get()
        repo_names = set()

        if results["metadatas"]:
            for metadata in results["metadatas"]:
                repo_names.add(metadata["repo_name"])

        return sorted(list(repo_names))

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the index.

        Returns:
            Dictionary with index statistics
        """
        count = self.collection.count()
        repos = self.list_repositories()

        return {
            "total_chunks": count,
            "total_repositories": len(repos),
            "repositories": repos,
        }
