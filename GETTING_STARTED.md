# Getting Started with DeepWiki-Like

This guide will get you up and running in less than 5 minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning repositories)
- OpenAI API key OR Anthropic API key

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
bash setup.sh

# Activate virtual environment
source venv/bin/activate

# Add your API key to .env
nano .env  # or use your favorite editor
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
```

## Configuration

Edit `.env` and add your API key:

```bash
# For OpenAI (recommended for beginners)
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

### Getting API Keys

**OpenAI**:
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key to `.env`

**Anthropic**:
1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new key and copy to `.env`

## First Run: Interactive Quick Start

```bash
python quickstart.py
```

This will:
1. Prompt you for a GitHub repository URL
2. Index all Markdown files
3. Let you ask questions interactively

Example session:
```
Enter a GitHub repository URL: https://github.com/anthropics/anthropic-sdk-python

[Indexing happens...]

Ask a question: How do I use streaming?

Answer: [AI-generated answer with sources]
```

## Using the CLI

### Index a Repository

```bash
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python
```

Expected output:
```
Crawling repository: anthropics/anthropic-sdk-python
  Found: README.md
  Found: docs/api.md
  Found: docs/streaming.md
Found 15 Markdown files

Chunking 15 documents...
Created 73 chunks
Generating embeddings and indexing...
  Indexed 73/73 chunks
Successfully indexed 73 chunks
```

### Ask Questions

```bash
python -m deepwiki ask "How do I handle errors?"
```

Expected output:
```
Question: How do I handle errors?

Answer:
[AI-generated answer based on the documentation]

Sources:
1. anthropics/anthropic-sdk-python/docs/error-handling.md
   https://github.com/anthropics/anthropic-sdk-python/blob/main/docs/error-handling.md
```

### View Statistics

```bash
python -m deepwiki stats
```

### List Indexed Repositories

```bash
python -m deepwiki list
```

### Clear Index

```bash
# Clear specific repository
python -m deepwiki clear --repo "anthropics/anthropic-sdk-python"

# Clear everything
python -m deepwiki clear
```

## Using the Web UI

### Start the Server

```bash
python -m deepwiki serve
```

Expected output:
```
Starting web server on 0.0.0.0:8000
Press Ctrl+C to stop
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Access the UI

Open your browser to: http://localhost:8000

The web UI has three tabs:

1. **Ask Question**: Query indexed documentation
2. **Index Repository**: Add new repositories
3. **Statistics**: View index stats

## Example Workflows

### Workflow 1: Learn a New Framework

```bash
# Index FastAPI documentation
python -m deepwiki index https://github.com/tiangolo/fastapi

# Ask questions
python -m deepwiki ask "How do I add authentication?"
python -m deepwiki ask "What's the difference between Path and Query parameters?"
python -m deepwiki ask "How do I handle file uploads?"
```

### Workflow 2: Compare Multiple Libraries

```bash
# Index multiple repositories
python -m deepwiki index https://github.com/openai/openai-python
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python

# Ask comparative questions
python -m deepwiki ask "What are the differences in streaming implementations?"
python -m deepwiki ask "How do error handling approaches differ?"
```

### Workflow 3: Index Local Documentation

```bash
# Index your project's docs folder
python -m deepwiki index /path/to/your/project/docs --local

# Ask questions about your own docs
python -m deepwiki ask "How does our authentication system work?"
```

### Workflow 4: Team Knowledge Base

```bash
# Index multiple internal repositories
python -m deepwiki index https://github.com/yourcompany/api-docs
python -m deepwiki index https://github.com/yourcompany/user-guide
python -m deepwiki index https://github.com/yourcompany/architecture

# Start web server for team access
python -m deepwiki serve --host 0.0.0.0 --port 8000

# Share http://your-ip:8000 with your team
```

## Tips for Best Results

### Indexing Tips

1. **Index related repositories together** for cross-referencing
2. **Use GitHub tokens** to avoid rate limits (add `GITHUB_TOKEN` to `.env`)
3. **Start with smaller repos** to test before indexing large ones
4. **Re-index periodically** to get updated documentation

### Querying Tips

1. **Be specific** in your questions
   - Good: "How do I implement OAuth2 authentication in FastAPI?"
   - Bad: "How do I use this?"

2. **Adjust top-k** based on question complexity
   - Simple questions: `--top-k 2`
   - Complex questions: `--top-k 10`

3. **Check citations** to verify accuracy
   - Always review the source links
   - Cross-reference multiple sources

4. **Rephrase if needed**
   - Try different wordings
   - Break complex questions into parts

### Model Selection

```bash
# For best quality (higher cost)
LLM_MODEL=gpt-4-turbo-preview

# For speed and cost (still good)
LLM_MODEL=gpt-3.5-turbo

# For privacy and latest features
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
```

## Troubleshooting

### Virtual Environment Issues

```bash
# Deactivate and recreate
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### API Key Not Found

```bash
# Check .env file exists
ls -la .env

# Check .env has your key
cat .env | grep API_KEY

# Make sure you're running from project root
pwd  # Should be /path/to/DeepWiki-Like
```

### ChromaDB Errors

```bash
# Clear and reset the database
rm -rf data/chroma_db
python -m deepwiki index <your-repo-url>
```

## Next Steps

1. Read [EXAMPLES.md](EXAMPLES.md) for more usage patterns
2. Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
3. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
4. Start indexing your favorite documentation repositories!

## Getting Help

- Check the documentation files in this repository
- Review error messages carefully (they're usually helpful)
- Make sure your API keys are valid and have credits
- Verify you're in the virtual environment (`which python` should show venv)

## Common Questions

**Q: How much does it cost to run?**
A: Indexing a medium repo (~50 files): ~$0.10. Asking questions: ~$0.01-0.05 per question.

**Q: Can I use it offline?**
A: No, it requires API access to OpenAI or Anthropic for embeddings and LLM.

**Q: Can I index private repositories?**
A: Yes, add a GitHub token with appropriate permissions to `.env`.

**Q: How long does indexing take?**
A: Depends on repository size. Small (10-20 files): 1-2 minutes. Medium (50-100 files): 5-10 minutes.

**Q: Is my data sent to OpenAI/Anthropic?**
A: Yes, document chunks are sent for embedding, and retrieved chunks are sent for answer generation.

**Q: Can I use local models?**
A: Not currently, but you could extend the code to support local LLMs like Ollama.

---

You're ready to go! Start with:
```bash
python quickstart.py
```
