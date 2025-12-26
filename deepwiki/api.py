"""FastAPI web server for DeepWiki-Like."""

from typing import List, Optional
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .crawler import GitHubCrawler
from .indexer import VectorIndexer
from .qa import QuestionAnswering

app = FastAPI(title="DeepWiki-Like", description="Index and query GitHub repository documentation")

# Track indexing status
indexing_status = {
    "in_progress": False,
    "current_repo": None,
    "status": "idle",
    "message": ""
}


class IndexRequest(BaseModel):
    """Request to index a repository."""

    repo_url: str
    is_local: bool = False


class QuestionRequest(BaseModel):
    """Request to ask a question."""

    question: str
    top_k: Optional[int] = 5


class AnswerResponse(BaseModel):
    """Response with answer and citations."""

    question: str
    answer: str
    citations: List[dict]


class StatsResponse(BaseModel):
    """Response with index statistics."""

    total_chunks: int
    total_repositories: int
    repositories: List[str]


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {
        "status": "healthy",
        "indexing_in_progress": indexing_status["in_progress"],
        "indexing_status": indexing_status["status"]
    }


@app.get("/")
async def root():
    """Serve the web UI."""
    return HTMLResponse(content=get_html_ui())


def index_in_background(repo_url: str, is_local: bool = False):
    """Background task to index a repository."""
    import traceback

    try:
        print(f"[INDEXING] Starting background indexing for {repo_url}")
        indexing_status["in_progress"] = True
        indexing_status["current_repo"] = repo_url
        indexing_status["status"] = "crawling"
        indexing_status["message"] = f"Crawling repository: {repo_url}"

        # Crawl repository
        print("[INDEXING] Initializing crawler...")
        crawler = GitHubCrawler()

        print(f"[INDEXING] Crawling {'local' if is_local else 'remote'} repository...")
        if is_local:
            documents = crawler.crawl_local(repo_url)
        else:
            documents = crawler.crawl(repo_url)

        print(f"[INDEXING] Found {len(documents) if documents else 0} documents")

        if not documents:
            indexing_status["status"] = "error"
            indexing_status["message"] = "No Markdown files found"
            indexing_status["in_progress"] = False
            print("[INDEXING] No documents found, aborting")
            return

        indexing_status["status"] = "indexing"
        indexing_status["message"] = f"Indexing {len(documents)} files (generating embeddings)..."
        print(f"[INDEXING] Starting to index {len(documents)} documents...")

        # Index documents
        print("[INDEXING] Initializing indexer...")
        indexer = VectorIndexer()
        print("[INDEXING] Starting indexer.index_documents...")
        chunk_count = indexer.index_documents(documents)
        print(f"[INDEXING] indexer.index_documents completed, {chunk_count} chunks indexed")

        indexing_status["status"] = "completed"
        indexing_status["message"] = f"Successfully indexed {len(documents)} files ({chunk_count} chunks)"
        indexing_status["in_progress"] = False
        print(f"[INDEXING] Completed! {chunk_count} chunks indexed")
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[INDEXING ERROR] {str(e)}")
        print(f"[INDEXING ERROR] Traceback:\n{error_trace}")
        indexing_status["status"] = "error"
        indexing_status["message"] = f"{str(e)[:200]}"  # Truncate long errors
        indexing_status["in_progress"] = False


@app.post("/api/index")
async def index_repository(request: IndexRequest, background_tasks: BackgroundTasks):
    """Index a GitHub repository (runs in background)."""
    if indexing_status["in_progress"]:
        raise HTTPException(
            status_code=409,
            detail=f"Indexing already in progress for {indexing_status['current_repo']}"
        )

    # Start indexing in background
    background_tasks.add_task(index_in_background, request.repo_url, request.is_local)

    return {
        "success": True,
        "message": f"Started indexing {request.repo_url}. Check /api/index/status for progress.",
        "status": "started"
    }


@app.get("/api/index/status")
async def get_index_status():
    """Get the current indexing status."""
    return indexing_status


@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer with citations."""
    try:
        qa = QuestionAnswering()
        answer = qa.answer(request.question, top_k=request.top_k)

        return AnswerResponse(
            question=answer.question,
            answer=answer.answer,
            citations=[c.to_dict() for c in answer.citations],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get index statistics."""
    try:
        indexer = VectorIndexer()
        stats = indexer.get_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/clear")
async def clear_index(repo_name: Optional[str] = None):
    """Clear the index."""
    try:
        indexer = VectorIndexer()
        if repo_name:
            indexer.clear_repository(repo_name)
            return {"success": True, "message": f"Cleared repository: {repo_name}"}
        else:
            indexer.clear_all()
            return {"success": True, "message": "Cleared all documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_html_ui() -> str:
    """Get the HTML for the web UI."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepWiki-Like</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background: none;
            border: none;
            font-size: 1em;
            color: #666;
            transition: all 0.3s;
        }
        .tab.active {
            color: #667eea;
            border-bottom: 2px solid #667eea;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #eee;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .answer {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .citations {
            margin-top: 20px;
        }
        .citation {
            padding: 10px;
            margin-bottom: 10px;
            background: white;
            border-radius: 6px;
            border: 1px solid #eee;
        }
        .citation-title {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
        }
        .citation-snippet {
            font-size: 0.9em;
            color: #666;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-box {
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .repo-list {
            list-style: none;
        }
        .repo-list li {
            padding: 10px;
            background: #f8f9fa;
            margin-bottom: 8px;
            border-radius: 6px;
        }
        .message {
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>DeepWiki-Like</h1>
            <p>Index and query GitHub repository documentation</p>
        </div>

        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('ask')">Ask Question</button>
                <button class="tab" onclick="switchTab('index')">Index Repository</button>
                <button class="tab" onclick="switchTab('stats')">Statistics</button>
            </div>

            <div id="ask-tab" class="tab-content active">
                <div class="form-group">
                    <label for="question">Ask a Question</label>
                    <textarea id="question" placeholder="e.g., How do I use streaming with the SDK?"></textarea>
                </div>
                <button onclick="askQuestion()">Get Answer</button>
                <div id="answer-container"></div>
            </div>

            <div id="index-tab" class="tab-content">
                <div class="form-group">
                    <label for="repo-url">GitHub Repository URL</label>
                    <input type="text" id="repo-url" placeholder="https://github.com/owner/repo">
                </div>
                <button onclick="indexRepository()">Index Repository</button>
                <div id="index-message"></div>
            </div>

            <div id="stats-tab" class="tab-content">
                <button onclick="loadStats()">Refresh Stats</button>
                <div id="stats-container"></div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');

            if (tabName === 'stats') {
                loadStats();
            }
        }

        async function askQuestion() {
            const question = document.getElementById('question').value;
            if (!question) {
                alert('Please enter a question');
                return;
            }

            const container = document.getElementById('answer-container');
            container.innerHTML = '<div class="loading">Thinking...</div>';

            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question, top_k: 5})
                });

                if (!response.ok) throw new Error('Failed to get answer');

                const data = await response.json();

                let html = '<div class="answer">';
                html += '<h3>Answer</h3>';
                html += '<p>' + data.answer + '</p>';
                html += '</div>';

                if (data.citations && data.citations.length > 0) {
                    html += '<div class="citations">';
                    html += '<h3>Sources</h3>';
                    data.citations.forEach((citation, i) => {
                        html += '<div class="citation">';
                        html += '<div class="citation-title">' + (i+1) + '. ' + citation.repo_name + '/' + citation.file_path + '</div>';
                        html += '<a href="' + citation.url + '" target="_blank">View source</a>';
                        html += '</div>';
                    });
                    html += '</div>';
                }

                container.innerHTML = html;
            } catch (error) {
                container.innerHTML = '<div class="message error">Error: ' + error.message + '</div>';
            }
        }

        async function indexRepository() {
            const repoUrl = document.getElementById('repo-url').value;
            if (!repoUrl) {
                alert('Please enter a repository URL');
                return;
            }

            const container = document.getElementById('index-message');
            container.innerHTML = '<div class="loading">Starting indexing...</div>';

            try {
                const response = await fetch('/api/index', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({repo_url: repoUrl})
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to start indexing');
                }

                const data = await response.json();
                container.innerHTML = '<div class="message success">' + data.message + '</div>';

                // Start polling for status
                pollIndexStatus(container);
            } catch (error) {
                container.innerHTML = '<div class="message error">Error: ' + error.message + '</div>';
            }
        }

        async function pollIndexStatus(container) {
            const interval = setInterval(async () => {
                try {
                    const response = await fetch('/api/index/status');
                    const status = await response.json();

                    let html = '<div class="message">';
                    html += '<strong>Status:</strong> ' + status.status + '<br>';
                    html += '<strong>Message:</strong> ' + status.message;
                    html += '</div>';

                    if (status.status === 'completed') {
                        html = '<div class="message success">' + status.message + '</div>';
                        container.innerHTML = html;
                        clearInterval(interval);
                    } else if (status.status === 'error') {
                        html = '<div class="message error">Error: ' + status.message + '</div>';
                        container.innerHTML = html;
                        clearInterval(interval);
                    } else {
                        container.innerHTML = html;
                    }
                } catch (error) {
                    console.error('Error polling status:', error);
                }
            }, 2000); // Poll every 2 seconds
        }

        async function loadStats() {
            const container = document.getElementById('stats-container');
            container.innerHTML = '<div class="loading">Loading statistics...</div>';

            try {
                const response = await fetch('/api/stats');
                if (!response.ok) throw new Error('Failed to load stats');

                const data = await response.json();

                let html = '<div class="stats-grid">';
                html += '<div class="stat-box"><div class="stat-value">' + data.total_chunks + '</div><div class="stat-label">Total Chunks</div></div>';
                html += '<div class="stat-box"><div class="stat-value">' + data.total_repositories + '</div><div class="stat-label">Repositories</div></div>';
                html += '</div>';

                if (data.repositories.length > 0) {
                    html += '<h3>Indexed Repositories</h3>';
                    html += '<ul class="repo-list">';
                    data.repositories.forEach(repo => {
                        html += '<li>' + repo + '</li>';
                    });
                    html += '</ul>';
                }

                container.innerHTML = html;
            } catch (error) {
                container.innerHTML = '<div class="message error">Error: ' + error.message + '</div>';
            }
        }
    </script>
</body>
</html>
"""
