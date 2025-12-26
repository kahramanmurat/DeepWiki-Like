# DeepWiki-Like Examples

This document provides practical examples of using DeepWiki-Like.

## Setup

1. Install dependencies:
```bash
bash setup.sh
```

2. Activate virtual environment:
```bash
source venv/bin/activate
```

3. Configure `.env` with your API keys

## Example 1: Index Anthropic SDK Documentation

```bash
# Index the Anthropic Python SDK repository
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python

# Ask questions about it
python -m deepwiki ask "How do I use streaming with the Anthropic SDK?"
python -m deepwiki ask "What are the available models?"
python -m deepwiki ask "How do I handle errors?"
```

## Example 2: Index Multiple Repositories

```bash
# Index multiple documentation repositories
python -m deepwiki index https://github.com/openai/openai-python
python -m deepwiki index https://github.com/langchain-ai/langchain
python -m deepwiki index https://github.com/tiangolo/fastapi

# List all indexed repos
python -m deepwiki list

# Ask cross-repository questions
python -m deepwiki ask "How do I use async/await with these libraries?"
```

## Example 3: Index Local Documentation

```bash
# Index a local directory
python -m deepwiki index /path/to/your/docs --local

# Ask questions
python -m deepwiki ask "How does the authentication work?"
```

## Example 4: Use the Web Interface

```bash
# Start the web server
python -m deepwiki serve

# Open http://localhost:8000 in your browser
# Use the web UI to:
# - Index repositories
# - Ask questions
# - View statistics
```

## Example 5: Custom Configuration

Edit `.env` to customize:

```env
# Use Claude instead of GPT
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_API_KEY=your_key_here

# Adjust chunking
CHUNK_SIZE=1500
CHUNK_OVERLAP=300

# More sources in answers
TOP_K=10
```

## Example 6: Clear and Rebuild Index

```bash
# Clear a specific repository
python -m deepwiki clear --repo "anthropics/anthropic-sdk-python"

# Clear everything
python -m deepwiki clear

# Rebuild
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python
```

## Example 7: View Statistics

```bash
# Show index statistics
python -m deepwiki stats
```

Output:
```
Total chunks: 1234
Total repositories: 3

Repositories:
  - anthropics/anthropic-sdk-python
  - openai/openai-python
  - tiangolo/fastapi
```

## Example 8: API Usage

```python
from deepwiki.crawler import GitHubCrawler
from deepwiki.indexer import VectorIndexer
from deepwiki.qa import QuestionAnswering

# Programmatic usage
crawler = GitHubCrawler()
docs = crawler.crawl("https://github.com/anthropics/anthropic-sdk-python")

indexer = VectorIndexer()
indexer.index_documents(docs)

qa = QuestionAnswering()
answer = qa.answer("How do I use streaming?")

print(answer.answer)
for citation in answer.citations:
    print(f"Source: {citation.url}")
```

## Example 9: Advanced Search

```bash
# Get more sources for detailed questions
python -m deepwiki ask "Explain the architecture of this codebase" --top-k 10

# Quick lookup with fewer sources
python -m deepwiki ask "What's the installation command?" --top-k 2
```

## Common Use Cases

### Documentation Search
Perfect for searching through large documentation repositories:
- Framework docs (React, Vue, FastAPI, etc.)
- SDK documentation
- Internal company wikis

### Learning a New Codebase
Index a project's README and docs to quickly understand:
- Architecture
- Setup instructions
- API usage
- Best practices

### Multi-Repository Knowledge Base
Create a unified knowledge base across multiple repos:
- All your company's microservices
- Related open-source projects
- Language ecosystem docs

## Tips

1. **GitHub Rate Limits**: Add a `GITHUB_TOKEN` to avoid rate limits when indexing
2. **Model Selection**: Use GPT-4 or Claude for better answers, GPT-3.5 for speed
3. **Chunk Size**: Smaller chunks (500-1000) for precise answers, larger (1500-2000) for context
4. **Top K**: More sources (7-10) for comprehensive answers, fewer (3-5) for quick lookups
