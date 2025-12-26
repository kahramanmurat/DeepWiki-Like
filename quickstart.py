#!/usr/bin/env python3
"""Quick start script for DeepWiki-Like."""

import os
import sys


def check_env():
    """Check if environment is set up."""
    if not os.path.exists(".env"):
        print("Error: .env file not found!")
        print("Please copy .env.example to .env and add your API keys:")
        print("  cp .env.example .env")
        print("  # Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY")
        return False

    from dotenv import load_dotenv
    load_dotenv()

    has_openai = os.getenv("OPENAI_API_KEY")
    has_anthropic = os.getenv("ANTHROPIC_API_KEY")

    if not has_openai and not has_anthropic:
        print("Error: No API key found in .env!")
        print("Please add either OPENAI_API_KEY or ANTHROPIC_API_KEY to .env")
        return False

    return True


def quickstart():
    """Run quick start demo."""
    if not check_env():
        sys.exit(1)

    print("DeepWiki-Like Quick Start")
    print("=" * 50)
    print()

    # Get user input
    print("Let's index a GitHub repository!")
    print()
    print("Examples:")
    print("  - https://github.com/anthropics/anthropic-sdk-python")
    print("  - https://github.com/openai/openai-python")
    print("  - https://github.com/tiangolo/fastapi")
    print()

    repo_url = input("Enter a GitHub repository URL: ").strip()
    if not repo_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    print()
    print(f"Indexing {repo_url}...")
    print()

    from deepwiki.crawler import GitHubCrawler
    from deepwiki.indexer import VectorIndexer
    from deepwiki.qa import QuestionAnswering

    try:
        # Crawl
        crawler = GitHubCrawler()
        docs = crawler.crawl(repo_url)

        if not docs:
            print("No Markdown files found!")
            sys.exit(1)

        # Index
        indexer = VectorIndexer()
        chunk_count = indexer.index_documents(docs)

        print()
        print(f"Successfully indexed {len(docs)} files ({chunk_count} chunks)")
        print()

        # Ask questions
        qa = QuestionAnswering()

        while True:
            print("-" * 50)
            question = input("\nAsk a question (or 'quit' to exit): ").strip()

            if question.lower() in ["quit", "exit", "q"]:
                break

            if not question:
                continue

            print()
            print("Thinking...")
            print()

            answer = qa.answer(question)

            print("Answer:")
            print(answer.answer)
            print()

            if answer.citations:
                print("Sources:")
                for i, citation in enumerate(answer.citations, 1):
                    print(f"{i}. {citation.repo_name}/{citation.file_path}")
                    print(f"   {citation.url}")
                print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    quickstart()
