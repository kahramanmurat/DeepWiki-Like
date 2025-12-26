"""Simple script to run the evaluation system."""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluation.scripts.evaluator import LLMJudge, SystemPromptEvaluator, save_results, generate_report
from datetime import datetime


def main():
    """Run the evaluation."""
    print("DeepWiki Evaluation System")
    print("=" * 60)

    # Load test cases
    logs_path = Path(__file__).parent.parent / "logs" / "interaction_logs.json"
    with open(logs_path) as f:
        test_cases = json.load(f)

    # Load system prompts
    prompts_path = Path(__file__).parent.parent / "prompts" / "system_prompts.json"
    with open(prompts_path) as f:
        prompts_data = json.load(f)
        system_prompts = prompts_data["prompts"]

    print(f"\nLoaded {len(test_cases)} test cases")
    print(f"Loaded {len(system_prompts)} system prompts\n")

    # Initialize evaluator
    judge = LLMJudge()
    evaluator = SystemPromptEvaluator(judge, None)

    # Run evaluation
    print("Starting evaluation...")
    print("This may take several minutes...\n")

    results = evaluator.run_evaluation(test_cases, system_prompts)

    # Save results
    results_dir = Path(__file__).parent.parent / "results"
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = results_dir / f"evaluation_{timestamp}.json"
    report_path = results_dir / f"report_{timestamp}.txt"

    save_results(results, str(json_path))
    generate_report(results, str(report_path))

    print("\nEvaluation complete!")
    print(f"Results: {json_path}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
