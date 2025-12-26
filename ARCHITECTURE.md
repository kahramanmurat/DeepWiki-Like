# DeepWiki-Like Architecture

## Overview

DeepWiki-Like is a documentation indexing and question-answering system that crawls GitHub repositories for Markdown files, indexes them using vector embeddings, and enables semantic search with AI-powered answers and citations.

## System Architecture

```
┌─────────────────┐
│  User Interface │
│   CLI / Web UI  │
└────────┬────────┘
         │
         v
┌─────────────────────────────────────────┐
│         Application Layer               │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐│
│  │ Crawler  │  │ Indexer  │  │  QA   ││
│  └──────────┘  └──────────┘  └───────┘│
└─────────┬───────────┬──────────┬───────┘
          │           │          │
          v           v          v
┌─────────────┐ ┌──────────┐ ┌──────────┐
│   GitHub    │ │ ChromaDB │ │   LLM    │
│     API     │ │  Vector  │ │ (OpenAI/ │
│             │ │   Store  │ │ Claude)  │
└─────────────┘ └──────────┘ └──────────┘
```

## Components

### 1. Crawler (`crawler.py`)

**Purpose**: Fetch Markdown files from GitHub repositories

**Key Classes**:
- `GitHubCrawler`: Crawls GitHub repos using PyGithub
- `MarkdownDocument`: Represents a single Markdown file

**Features**:
- Supports GitHub URLs and local paths
- Filters for `.md` and `.mdx` files only
- Recursive tree traversal
- Optional GitHub token for higher rate limits

**Flow**:
1. Parse GitHub URL to extract owner/repo
2. Use GitHub API to get repository tree
3. Filter for Markdown files
4. Download file contents
5. Create MarkdownDocument objects

### 2. Indexer (`indexer.py`)

**Purpose**: Chunk documents and create searchable vector index

**Key Classes**:
- `DocumentChunker`: Splits documents into semantic chunks
- `VectorIndexer`: Manages ChromaDB collection and embeddings

**Features**:
- Smart chunking by headers and size
- Overlap between chunks for context
- OpenAI embeddings (text-embedding-3-small)
- Persistent ChromaDB storage
- Batch processing for efficiency

**Chunking Strategy**:
1. Split by Markdown headers (# ## ###)
2. If chunks > max size, split by paragraphs
3. Apply overlap between chunks
4. Preserve metadata (repo, file path, URL)

**Flow**:
1. Chunk each document
2. Generate embeddings for chunks
3. Store in ChromaDB with metadata
4. Index for fast retrieval

### 3. Retriever (`retriever.py`)

**Purpose**: Search indexed documents using semantic similarity

**Key Classes**:
- `DocumentRetriever`: Performs vector similarity search
- `SearchResult`: Represents a single search result

**Features**:
- Vector similarity search
- Configurable top-k results
- Score normalization
- Metadata preservation

**Flow**:
1. Generate query embedding
2. Search ChromaDB for similar vectors
3. Return top-k results with metadata

### 4. Question Answering (`qa.py`)

**Purpose**: Generate answers with citations using LLM

**Key Classes**:
- `QuestionAnswering`: Orchestrates retrieval + generation
- `Answer`: Contains answer text and citations
- `Citation`: Represents a source reference

**Features**:
- Retrieval-augmented generation (RAG)
- Multi-provider support (OpenAI, Anthropic)
- Source citations with URLs
- Formatted output

**Flow**:
1. Retrieve relevant chunks
2. Build prompt with context
3. Generate answer using LLM
4. Extract citations from sources
5. Return structured answer

### 5. CLI (`__main__.py`)

**Purpose**: Command-line interface

**Commands**:
- `index <repo_url>`: Index a repository
- `ask <question>`: Ask a question
- `list`: List indexed repositories
- `stats`: Show index statistics
- `clear`: Clear index
- `serve`: Start web server

### 6. Web API (`api.py`)

**Purpose**: FastAPI web server and UI

**Endpoints**:
- `GET /`: Web UI
- `POST /api/index`: Index repository
- `POST /api/ask`: Ask question
- `GET /api/stats`: Get statistics
- `DELETE /api/clear`: Clear index

**Features**:
- Beautiful web UI
- Real-time statistics
- Citation links
- Responsive design

## Data Flow

### Indexing Flow

```
GitHub Repo
    ↓
Crawler extracts .md/.mdx files
    ↓
DocumentChunker splits into chunks
    ↓
OpenAI generates embeddings
    ↓
ChromaDB stores vectors + metadata
```

### Query Flow

```
User Question
    ↓
Generate query embedding
    ↓
ChromaDB vector search
    ↓
Retrieve top-k chunks
    ↓
Build prompt with context
    ↓
LLM generates answer
    ↓
Return answer + citations
```

## Storage

### ChromaDB Collection

**Schema**:
```python
{
    "id": "repo_name::file_path::chunk_index",
    "document": "chunk text content",
    "embedding": [vector of floats],
    "metadata": {
        "repo_name": "owner/repo",
        "file_path": "path/to/file.md",
        "url": "https://github.com/...",
        "chunk_index": 0,
        "total_chunks": 5
    }
}
```

### Directory Structure

```
DeepWiki-Like/
├── deepwiki/           # Application code
│   ├── __init__.py
│   ├── __main__.py     # CLI entry point
│   ├── config.py       # Configuration
│   ├── crawler.py      # GitHub crawler
│   ├── indexer.py      # Document indexing
│   ├── retriever.py    # Search
│   ├── qa.py          # Question answering
│   └── api.py         # Web API
├── data/              # Created at runtime
│   └── chroma_db/     # Vector database
├── .env               # Configuration
└── requirements.txt   # Dependencies
```

## Configuration

### Environment Variables

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...

# LLM Configuration
LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval
TOP_K=5
```

## Scalability Considerations

### Current Limitations

- In-memory ChromaDB (suitable for small to medium repos)
- Synchronous processing
- Single-threaded indexing

### Scaling Options

1. **Large Repositories**:
   - Use batch processing
   - Implement progress tracking
   - Add resume capability

2. **Multiple Users**:
   - Deploy ChromaDB server
   - Add authentication
   - Implement rate limiting

3. **Performance**:
   - Cache embeddings
   - Parallel document processing
   - Async API endpoints

## Extension Points

### Adding New LLM Providers

1. Add provider configuration in `config.py`
2. Implement generation method in `qa.py`
3. Add API key validation

### Custom Chunking Strategies

1. Extend `DocumentChunker` class
2. Implement custom splitting logic
3. Preserve metadata structure

### Alternative Vector Stores

1. Replace ChromaDB client in `indexer.py`
2. Implement same interface:
   - `add()`
   - `query()`
   - `delete()`
   - `get()`

## Security

### API Keys

- Stored in `.env` (not committed)
- Validated on startup
- Never exposed in logs or UI

### GitHub Access

- Optional token for higher limits
- Read-only access
- Public repos only by default

### Input Validation

- URL parsing with regex
- File type filtering
- Size limits on chunks

## Best Practices

### Indexing

- Index related repositories together
- Use descriptive repository names
- Periodically refresh indexes
- Monitor chunk counts

### Querying

- Start with specific questions
- Adjust top-k based on question complexity
- Review citations for accuracy
- Iterate on question phrasing

### Configuration

- Use GPT-4/Claude for accuracy
- Adjust chunk size based on content
- Balance overlap vs. redundancy
- Set appropriate top-k values

## Future Enhancements

- [ ] Incremental indexing (update only changed files)
- [ ] Multi-language support
- [ ] Image and diagram extraction
- [ ] Code snippet execution
- [ ] Conversation history
- [ ] Custom filters and tags
- [ ] Export to various formats
- [ ] Analytics and usage tracking
