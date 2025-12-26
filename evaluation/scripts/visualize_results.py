"""Generate visualizations from evaluation results."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def print_comparison_table(results: Dict[str, Any]):
    """Print a formatted comparison table."""
    print("\n" + "=" * 100)
    print("SYSTEM PROMPT COMPARISON")
    print("=" * 100)

    if "comparison" not in results or not results["comparison"]["rankings"]:
        print("No comparison data available")
        return

    # Header
    header = f"{'Rank':<6} {'Prompt Name':<35} {'Overall':<10} {'Rel':<8} {'Comp':<8} {'Acc':<8} {'Clar':<8} {'Cite':<8}"
    print(header)
    print("-" * 100)

    # Data rows
    for i, ranking in enumerate(results["comparison"]["rankings"], 1):
        prompt_id = ranking["prompt_id"]
        prompt_data = results["prompt_results"][prompt_id]

        if "aggregate_scores" in prompt_data:
            scores = prompt_data["aggregate_scores"]
            row = (
                f"{i:<6} "
                f"{ranking['prompt_name'][:34]:<35} "
                f"{scores.get('overall_mean', 0):<10.2f} "
                f"{scores.get('relevance_mean', 0):<8.2f} "
                f"{scores.get('completeness_mean', 0):<8.2f} "
                f"{scores.get('accuracy_mean', 0):<8.2f} "
                f"{scores.get('clarity_mean', 0):<8.2f} "
                f"{scores.get('citation_quality_mean', 0):<8.2f}"
            )
            print(row)

    print("=" * 100)


def print_detailed_results(results: Dict[str, Any], prompt_id: str = None):
    """Print detailed results for a specific prompt or all prompts."""
    if prompt_id:
        if prompt_id not in results["prompt_results"]:
            print(f"Prompt '{prompt_id}' not found")
            return
        prompts_to_show = {prompt_id: results["prompt_results"][prompt_id]}
    else:
        prompts_to_show = results["prompt_results"]

    for pid, prompt_data in prompts_to_show.items():
        print("\n" + "=" * 100)
        print(f"PROMPT: {prompt_data['prompt_name']}")
        print("=" * 100)

        if "test_results" not in prompt_data:
            continue

        for test_result in prompt_data["test_results"]:
            print(f"\nQuestion: {test_result['question']}")
            print("-" * 100)

            if "error" in test_result:
                print(f"Error: {test_result['error']}")
                continue

            if "evaluation" in test_result:
                eval_data = test_result["evaluation"]
                if "error" not in eval_data:
                    print(
                        f"Overall Score: {eval_data['overall_score']:.2f}/10"
                    )
                    print(f"  Relevance:        {eval_data['relevance']['score']}/10 - {eval_data['relevance']['justification']}")
                    print(f"  Completeness:     {eval_data['completeness']['score']}/10 - {eval_data['completeness']['justification']}")
                    print(f"  Accuracy:         {eval_data['accuracy']['score']}/10 - {eval_data['accuracy']['justification']}")
                    print(f"  Clarity:          {eval_data['clarity']['score']}/10 - {eval_data['clarity']['justification']}")
                    print(f"  Citation Quality: {eval_data['citation_quality']['score']}/10 - {eval_data['citation_quality']['justification']}")

                    if eval_data.get("suggestions"):
                        print("\nSuggestions:")
                        for suggestion in eval_data["suggestions"]:
                            print(f"  • {suggestion}")


def generate_markdown_report(results: Dict[str, Any], output_path: str):
    """Generate a markdown report."""
    lines = []

    lines.append("# DeepWiki Evaluation Results\n")
    lines.append(f"**Generated:** {results['timestamp']}\n")
    lines.append(f"**Test Cases:** {results['test_cases_count']}\n")
    lines.append(f"**Prompts Evaluated:** {results['prompts_count']}\n")

    # Overall Rankings
    lines.append("## Overall Rankings\n")
    lines.append("| Rank | Prompt | Overall | Relevance | Completeness | Accuracy | Clarity | Citations |")
    lines.append("|------|--------|---------|-----------|--------------|----------|---------|-----------|")

    if "comparison" in results and results["comparison"]["rankings"]:
        for i, ranking in enumerate(results["comparison"]["rankings"], 1):
            prompt_id = ranking["prompt_id"]
            prompt_data = results["prompt_results"][prompt_id]

            if "aggregate_scores" in prompt_data:
                scores = prompt_data["aggregate_scores"]
                lines.append(
                    f"| {i} | {prompt_data['prompt_name']} | "
                    f"{scores.get('overall_mean', 0):.2f} | "
                    f"{scores.get('relevance_mean', 0):.2f} | "
                    f"{scores.get('completeness_mean', 0):.2f} | "
                    f"{scores.get('accuracy_mean', 0):.2f} | "
                    f"{scores.get('clarity_mean', 0):.2f} | "
                    f"{scores.get('citation_quality_mean', 0):.2f} |"
                )

    lines.append("\n")

    # Key Insights
    if "comparison" in results and results["comparison"].get("insights"):
        lines.append("## Key Insights\n")
        for insight in results["comparison"]["insights"]:
            lines.append(f"- {insight}")
        lines.append("\n")

    # Detailed Results by Prompt
    lines.append("## Detailed Results\n")

    for prompt_id, prompt_data in results["prompt_results"].items():
        lines.append(f"### {prompt_data['prompt_name']}\n")

        if "aggregate_scores" in prompt_data and prompt_data["aggregate_scores"]:
            scores = prompt_data["aggregate_scores"]
            lines.append("**Aggregate Scores:**\n")
            lines.append(f"- Overall: {scores.get('overall_mean', 0):.2f}")
            lines.append(f"- Relevance: {scores.get('relevance_mean', 0):.2f}")
            lines.append(f"- Completeness: {scores.get('completeness_mean', 0):.2f}")
            lines.append(f"- Accuracy: {scores.get('accuracy_mean', 0):.2f}")
            lines.append(f"- Clarity: {scores.get('clarity_mean', 0):.2f}")
            lines.append(f"- Citation Quality: {scores.get('citation_quality_mean', 0):.2f}\n")

        lines.append(f"**System Prompt:**\n```\n{prompt_data['system_prompt']}\n```\n")

    # Write to file
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\nMarkdown report saved to: {output_path}")


def main():
    """Main function to visualize results."""
    if len(sys.argv) < 2:
        print("Usage: python visualize_results.py <results_json_file> [options]")
        print("\nOptions:")
        print("  --summary              Show summary table only")
        print("  --detailed [prompt_id] Show detailed results")
        print("  --markdown <output>    Generate markdown report")
        return

    results_file = sys.argv[1]

    # Load results
    with open(results_file) as f:
        results = json.load(f)

    # Parse options
    if "--summary" in sys.argv or len(sys.argv) == 2:
        print_comparison_table(results)

    if "--detailed" in sys.argv:
        idx = sys.argv.index("--detailed")
        prompt_id = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
        print_detailed_results(results, prompt_id)

    if "--markdown" in sys.argv:
        idx = sys.argv.index("--markdown")
        output_path = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "report.md"
        generate_markdown_report(results, output_path)


if __name__ == "__main__":
    main()
