"""Demo script showing evaluation system with mock data."""

import json
from datetime import datetime
from pathlib import Path


def generate_mock_evaluation():
    """Generate mock evaluation results for demonstration."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "test_cases_count": 12,
        "prompts_count": 5,
        "prompt_results": {},
    }

    # Mock data for each prompt
    prompts_data = [
        {
            "id": "baseline",
            "name": "Baseline - Simple and Direct",
            "overall": 7.56,
            "relevance": 7.8,
            "completeness": 7.2,
            "accuracy": 8.1,
            "clarity": 7.9,
            "citation": 7.3,
        },
        {
            "id": "detailed",
            "name": "Detailed - Comprehensive Answers",
            "overall": 8.23,
            "relevance": 8.5,
            "completeness": 8.7,
            "accuracy": 8.4,
            "clarity": 7.8,
            "citation": 7.8,
        },
        {
            "id": "concise",
            "name": "Concise - Quick and Focused",
            "overall": 7.12,
            "relevance": 7.5,
            "completeness": 6.2,
            "accuracy": 7.8,
            "clarity": 8.1,
            "citation": 7.0,
        },
        {
            "id": "educational",
            "name": "Educational - Teaching-Oriented",
            "overall": 7.98,
            "relevance": 8.2,
            "completeness": 8.4,
            "accuracy": 7.9,
            "clarity": 8.3,
            "citation": 7.1,
        },
        {
            "id": "technical",
            "name": "Technical - Developer-Focused",
            "overall": 8.45,
            "relevance": 8.7,
            "completeness": 8.6,
            "accuracy": 8.9,
            "clarity": 8.5,
            "citation": 7.6,
        },
    ]

    for prompt_data in prompts_data:
        results["prompt_results"][prompt_data["id"]] = {
            "prompt_id": prompt_data["id"],
            "prompt_name": prompt_data["name"],
            "system_prompt": f"Mock system prompt for {prompt_data['name']}",
            "test_results": generate_mock_test_results(12),
            "aggregate_scores": {
                "overall_mean": prompt_data["overall"],
                "overall_min": prompt_data["overall"] - 1.2,
                "overall_max": prompt_data["overall"] + 0.8,
                "relevance_mean": prompt_data["relevance"],
                "completeness_mean": prompt_data["completeness"],
                "accuracy_mean": prompt_data["accuracy"],
                "clarity_mean": prompt_data["clarity"],
                "citation_quality_mean": prompt_data["citation"],
            },
        }

    # Generate comparison
    rankings = sorted(
        prompts_data, key=lambda x: x["overall"], reverse=True
    )

    results["comparison"] = {
        "rankings": [
            {
                "prompt_id": r["id"],
                "prompt_name": r["name"],
                "overall_score": r["overall"],
            }
            for r in rankings
        ],
        "best_prompt": {
            "prompt_id": rankings[0]["id"],
            "prompt_name": rankings[0]["name"],
            "overall_score": rankings[0]["overall"],
        },
        "insights": [
            f"Best performing prompt: {rankings[0]['name']} (score: {rankings[0]['overall']:.2f})",
            f"Score difference between best and worst: {rankings[0]['overall'] - rankings[-1]['overall']:.2f} points",
            f"Total prompts evaluated: {len(prompts_data)}",
            "Technical prompts performed best for developer-focused documentation",
            "Concise prompts scored lowest on completeness but highest on clarity",
        ],
    }

    return results


def generate_mock_test_results(count: int):
    """Generate mock test results."""
    results = []
    questions = [
        "How do I use streaming with the SDK?",
        "What are the authentication methods?",
        "How do I handle rate limits?",
        "What topics are covered in the MCP module?",
        "What are the homework requirements for week 1?",
        "Can I use this SDK with async/await?",
        "How do I set up the development environment?",
        "What models are available?",
        "What's the difference between modules?",
        "How do I handle errors and exceptions?",
        "Are there any prerequisites for this course?",
        "Can I customize the temperature and max tokens?",
    ]

    for i in range(count):
        results.append(
            {
                "test_id": i + 1,
                "question": questions[i % len(questions)],
                "answer": f"Mock answer for question {i+1}",
                "citations_count": 3,
                "evaluation": {
                    "relevance": {"score": 8, "justification": "Directly addresses the question"},
                    "completeness": {"score": 7, "justification": "Covers main points"},
                    "accuracy": {"score": 9, "justification": "Information is correct"},
                    "clarity": {"score": 8, "justification": "Well structured"},
                    "citation_quality": {"score": 7, "justification": "Good source references"},
                    "overall_score": 7.8,
                    "suggestions": ["Add more code examples", "Include edge cases"],
                },
            }
        )

    return results


def save_mock_results():
    """Generate and save mock results."""
    print("Generating mock evaluation results...")

    results = generate_mock_evaluation()

    # Save JSON results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = results_dir / f"demo_evaluation_{timestamp}.json"

    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nMock results saved to: {json_path}")

    # Generate text report
    report = generate_text_report(results)
    report_path = results_dir / f"demo_report_{timestamp}.txt"

    with open(report_path, "w") as f:
        f.write(report)

    print(f"Mock report saved to: {report_path}")
    print("\n" + "=" * 80)
    print("DEMO REPORT PREVIEW")
    print("=" * 80)
    print(report)

    return json_path


def generate_text_report(results):
    """Generate a text report from results."""
    lines = []

    lines.append("=" * 80)
    lines.append("DEEPWIKI EVALUATION REPORT (DEMO)")
    lines.append("=" * 80)
    lines.append(f"\nGenerated: {results['timestamp']}")
    lines.append(f"Test Cases: {results['test_cases_count']}")
    lines.append(f"System Prompts: {results['prompts_count']}")
    lines.append("\n")

    # Rankings
    lines.append("OVERALL RANKINGS")
    lines.append("-" * 80)
    for i, ranking in enumerate(results["comparison"]["rankings"], 1):
        lines.append(f"{i}. {ranking['prompt_name']}: {ranking['overall_score']:.2f}")
    lines.append("\n")

    # Insights
    lines.append("KEY INSIGHTS")
    lines.append("-" * 80)
    for insight in results["comparison"]["insights"]:
        lines.append(f"• {insight}")
    lines.append("\n")

    # Detailed scores
    for prompt_id, prompt_data in results["prompt_results"].items():
        lines.append(f"\nPROMPT: {prompt_data['prompt_name']}")
        lines.append("=" * 80)

        scores = prompt_data["aggregate_scores"]
        lines.append("\nAggregate Scores:")
        lines.append(f"  Overall:          {scores['overall_mean']:.2f}")
        lines.append(f"  Relevance:        {scores['relevance_mean']:.2f}")
        lines.append(f"  Completeness:     {scores['completeness_mean']:.2f}")
        lines.append(f"  Accuracy:         {scores['accuracy_mean']:.2f}")
        lines.append(f"  Clarity:          {scores['clarity_mean']:.2f}")
        lines.append(f"  Citation Quality: {scores['citation_quality_mean']:.2f}")
        lines.append("\n")

    return "\n".join(lines)


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("DeepWiki Evaluation System - Demo Mode")
    print("=" * 80)
    print("\nThis script generates mock evaluation results for demonstration.")
    print("To run a real evaluation, use: python run_evaluation.py")
    print("\n" + "=" * 80 + "\n")

    json_path = save_mock_results()

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("\n1. View the results:")
    print(f"   cat {json_path}")
    print("\n2. Visualize with the visualization tool:")
    print(f"   python visualize_results.py {json_path} --summary")
    print("\n3. Generate markdown report:")
    print(f"   python visualize_results.py {json_path} --markdown demo_report.md")
    print("\n4. Run a real evaluation:")
    print("   python run_evaluation.py")
    print("\n" + "=" * 80)
