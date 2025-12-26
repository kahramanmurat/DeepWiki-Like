# DeepWiki-Like

A powerful tool to index Markdown documentation from GitHub repositories and ask questions with AI-powered answers and citations.

## Features

- 📚 Index `.md` and `.mdx` files from any GitHub repository
- 🔍 Semantic search with vector embeddings
- 💬 AI-powered question answering with source citations
- 🎯 Multiple LLM providers (OpenAI, Anthropic)
- 🚀 Fast retrieval with ChromaDB
- 🌐 Web UI and CLI interface

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your API keys:
```bash
cp .env.example .env
```

4. Edit `.env` with your API keys

## Usage

### Index a Repository

```bash
python -m deepwiki index <github_repo_url>
```

Example:
```bash
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python
```

### Ask Questions

```bash
python -m deepwiki ask "How do I use streaming with the SDK?"
```

### Start Web UI

```bash
python -m deepwiki serve
```

Then open http://localhost:8000 in your browser.

### List Indexed Repositories

```bash
python -m deepwiki list
```

### Clear Index

```bash
python -m deepwiki clear
```

## How It Works

1. **Crawling**: Fetches all `.md` and `.mdx` files from the specified GitHub repository
2. **Chunking**: Splits documents into manageable chunks with overlap
3. **Embedding**: Generates vector embeddings using OpenAI or similar models
4. **Indexing**: Stores embeddings in ChromaDB for fast retrieval
5. **Question Answering**: Retrieves relevant chunks and uses LLM to generate answers with citations

## Architecture

```
deepwiki/
├── __init__.py
├── __main__.py          # CLI entry point
├── config.py            # Configuration management
├── crawler.py           # GitHub repository crawler
├── indexer.py           # Document chunking and indexing
├── retriever.py         # Search and retrieval
├── qa.py                # Question answering with citations
└── api.py               # FastAPI web server
```

## Configuration

Edit `.env` to customize:

- `LLM_PROVIDER`: Choose `openai` or `anthropic`
- `EMBEDDING_MODEL`: Embedding model to use
- `CHUNK_SIZE`: Size of text chunks for indexing
- `CHUNK_OVERLAP`: Overlap between chunks

## Requirements

- Python 3.8+
- OpenAI API key or Anthropic API key
- GitHub token (optional, for higher rate limits)

## License

MIT
