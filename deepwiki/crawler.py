"""GitHub repository crawler for Markdown files."""

import re
from typing import List, Dict, Any
from pathlib import Path
import requests
from github import Github, GithubException
from .config import config


class MarkdownDocument:
    """Represents a Markdown document from a repository."""

    def __init__(self, path: str, content: str, url: str, repo_name: str):
        self.path = path
        self.content = content
        self.url = url
        self.repo_name = repo_name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "content": self.content,
            "url": self.url,
            "repo_name": self.repo_name,
        }


class GitHubCrawler:
    """Crawls GitHub repositories for Markdown files."""

    def __init__(self, github_token: str = None):
        """Initialize the crawler.

        Args:
            github_token: GitHub personal access token (optional, for higher rate limits)
        """
        self.github_token = github_token or config.GITHUB_TOKEN
        self.github = Github(self.github_token) if self.github_token else Github()

    def extract_repo_info(self, repo_url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL.

        Args:
            repo_url: GitHub repository URL

        Returns:
            Tuple of (owner, repo_name)
        """
        # Handle various GitHub URL formats
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                owner, repo = match.groups()
                # Remove .git suffix if present
                repo = repo.replace(".git", "")
                return owner, repo

        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    def crawl(self, repo_url: str) -> List[MarkdownDocument]:
        """Crawl a GitHub repository for Markdown files.

        Args:
            repo_url: GitHub repository URL

        Returns:
            List of MarkdownDocument objects
        """
        owner, repo_name = self.extract_repo_info(repo_url)
        full_repo_name = f"{owner}/{repo_name}"

        print(f"Crawling repository: {full_repo_name}")

        try:
            repo = self.github.get_repo(full_repo_name)
        except GithubException as e:
            raise Exception(f"Failed to access repository: {e}")

        documents = []
        self._crawl_tree(repo, repo.get_git_tree("HEAD", recursive=True), documents, full_repo_name)

        print(f"Found {len(documents)} Markdown files")
        return documents

    def _crawl_tree(self, repo, tree, documents: List[MarkdownDocument], repo_name: str) -> None:
        """Recursively crawl repository tree for Markdown files.

        Args:
            repo: GitHub repository object
            tree: Git tree object
            documents: List to append documents to
            repo_name: Full repository name (owner/repo)
        """
        for item in tree.tree:
            # Check if file is .md or .mdx
            if item.type == "blob" and (item.path.endswith(".md") or item.path.endswith(".mdx")):
                try:
                    # Get file content
                    content = repo.get_contents(item.path)
                    if content.encoding == "base64":
                        decoded_content = content.decoded_content.decode("utf-8")
                    else:
                        decoded_content = content.content

                    # Create document
                    doc = MarkdownDocument(
                        path=item.path,
                        content=decoded_content,
                        url=content.html_url,
                        repo_name=repo_name,
                    )
                    documents.append(doc)
                    print(f"  Found: {item.path}")

                except Exception as e:
                    print(f"  Error reading {item.path}: {e}")
                    continue

    def crawl_local(self, local_path: str) -> List[MarkdownDocument]:
        """Crawl a local directory for Markdown files.

        Args:
            local_path: Path to local directory

        Returns:
            List of MarkdownDocument objects
        """
        path = Path(local_path)
        if not path.exists():
            raise ValueError(f"Path does not exist: {local_path}")

        documents = []
        repo_name = f"local/{path.name}"

        # Find all .md and .mdx files
        for md_file in path.rglob("*.md"):
            self._add_local_file(md_file, path, repo_name, documents)

        for mdx_file in path.rglob("*.mdx"):
            self._add_local_file(mdx_file, path, repo_name, documents)

        print(f"Found {len(documents)} Markdown files in {local_path}")
        return documents

    def _add_local_file(
        self, file_path: Path, base_path: Path, repo_name: str, documents: List[MarkdownDocument]
    ) -> None:
        """Add a local file to the documents list.

        Args:
            file_path: Path to the file
            base_path: Base path for relative path calculation
            repo_name: Repository name
            documents: List to append to
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            relative_path = file_path.relative_to(base_path)

            doc = MarkdownDocument(
                path=str(relative_path),
                content=content,
                url=f"file://{file_path}",
                repo_name=repo_name,
            )
            documents.append(doc)
            print(f"  Found: {relative_path}")

        except Exception as e:
            print(f"  Error reading {file_path}: {e}")
