"""CLI interface for DeepWiki-Like."""

import sys
import argparse
from .crawler import GitHubCrawler
from .indexer import VectorIndexer
from .qa import QuestionAnswering


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DeepWiki-Like: Index and query GitHub repository documentation"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Index command
    index_parser = subparsers.add_parser("index", help="Index a GitHub repository")
    index_parser.add_argument("repo_url", help="GitHub repository URL or local path")
    index_parser.add_argument(
        "--local", action="store_true", help="Index a local directory instead of GitHub repo"
    )

    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument("--top-k", type=int, default=5, help="Number of sources to use")

    # List command
    subparsers.add_parser("list", help="List indexed repositories")

    # Stats command
    subparsers.add_parser("stats", help="Show index statistics")

    # Clear command
    clear_parser = subparsers.add_parser("clear", help="Clear index")
    clear_parser.add_argument("--repo", help="Clear specific repository (or all if not specified)")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start web server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to bind to")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "index":
            cmd_index(args)
        elif args.command == "ask":
            cmd_ask(args)
        elif args.command == "list":
            cmd_list(args)
        elif args.command == "stats":
            cmd_stats(args)
        elif args.command == "clear":
            cmd_clear(args)
        elif args.command == "serve":
            cmd_serve(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_index(args):
    """Handle index command."""
    print(f"Indexing: {args.repo_url}")

    # Crawl repository
    crawler = GitHubCrawler()
    if args.local:
        documents = crawler.crawl_local(args.repo_url)
    else:
        documents = crawler.crawl(args.repo_url)

    if not documents:
        print("No Markdown files found!")
        return

    # Index documents
    indexer = VectorIndexer()
    chunk_count = indexer.index_documents(documents)

    print(f"\nSuccessfully indexed {len(documents)} files ({chunk_count} chunks)")


def cmd_ask(args):
    """Handle ask command."""
    print(f"Question: {args.question}\n")

    # Answer question
    qa = QuestionAnswering()
    answer = qa.answer(args.question, top_k=args.top_k)

    # Print answer
    print(f"Answer:\n{answer.answer}\n")

    # Print citations
    if answer.citations:
        print("Sources:")
        for i, citation in enumerate(answer.citations, 1):
            print(f"{i}. {citation.repo_name}/{citation.file_path}")
            print(f"   {citation.url}")
            print()


def cmd_list(args):
    """Handle list command."""
    indexer = VectorIndexer()
    repos = indexer.list_repositories()

    if repos:
        print("Indexed repositories:")
        for repo in repos:
            print(f"  - {repo}")
    else:
        print("No repositories indexed yet")


def cmd_stats(args):
    """Handle stats command."""
    indexer = VectorIndexer()
    stats = indexer.get_stats()

    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Total repositories: {stats['total_repositories']}")

    if stats["repositories"]:
        print("\nRepositories:")
        for repo in stats["repositories"]:
            print(f"  - {repo}")


def cmd_clear(args):
    """Handle clear command."""
    indexer = VectorIndexer()

    if args.repo:
        print(f"Clearing repository: {args.repo}")
        indexer.clear_repository(args.repo)
    else:
        confirm = input("Clear all indexed documents? [y/N]: ")
        if confirm.lower() == "y":
            indexer.clear_all()
            print("All documents cleared")
        else:
            print("Cancelled")


def cmd_serve(args):
    """Handle serve command."""
    print(f"Starting web server on {args.host}:{args.port}")
    print("Press Ctrl+C to stop")

    from .api import app
    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
