"""LLM-as-a-Judge Evaluation System for DeepWiki Agent."""

import json
import os
from typing import List, Dict, Any
from pathlib import Path
import openai
from datetime import datetime


class LLMJudge:
    """Uses an LLM to evaluate agent responses."""

    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        """Initialize the LLM judge.

        Args:
            api_key: OpenAI API key
            model: Model to use for evaluation
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        openai.api_key = self.api_key

    def evaluate_response(
        self,
        question: str,
        answer: str,
        expected_topics: List[str],
        citations: List[Dict[str, Any]],
        context: str = "",
    ) -> Dict[str, Any]:
        """Evaluate a single response.

        Args:
            question: The user's question
            answer: The agent's answer
            expected_topics: Topics that should be covered
            citations: List of source citations
            context: Additional context about the question

        Returns:
            Dictionary with evaluation scores and feedback
        """
        evaluation_prompt = f"""You are evaluating a documentation Q&A system's response. Please assess the following:

**Question:** {question}

**Context:** {context}

**Expected Topics:** {', '.join(expected_topics)}

**Agent's Answer:**
{answer}

**Citations Provided:** {len(citations)} sources

**Evaluation Criteria:**

1. **Relevance (0-10):** How well does the answer address the question?
2. **Completeness (0-10):** Does it cover the expected topics?
3. **Accuracy (0-10):** Is the information correct and precise?
4. **Clarity (0-10):** Is the answer well-structured and easy to understand?
5. **Citation Quality (0-10):** Are sources properly cited and relevant?

Please provide:
- A score for each criterion (0-10)
- Brief justification for each score
- An overall score (average of all criteria)
- Specific suggestions for improvement

Format your response as JSON:
{{
  "relevance": {{"score": X, "justification": "..."}},
  "completeness": {{"score": X, "justification": "..."}},
  "accuracy": {{"score": X, "justification": "..."}},
  "clarity": {{"score": X, "justification": "..."}},
  "citation_quality": {{"score": X, "justification": "..."}},
  "overall_score": X.X,
  "suggestions": ["...", "..."]
}}
"""

        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert evaluator of AI assistant responses. Provide objective, constructive feedback.",
                    },
                    {"role": "user", "content": evaluation_prompt},
                ],
                temperature=0.3,
            )

            result_text = response.choices[0].message.content
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            evaluation = json.loads(result_text)
            return evaluation

        except Exception as e:
            print(f"Error in evaluation: {e}")
            return {
                "error": str(e),
                "relevance": {"score": 0, "justification": "Evaluation failed"},
                "completeness": {"score": 0, "justification": "Evaluation failed"},
                "accuracy": {"score": 0, "justification": "Evaluation failed"},
                "clarity": {"score": 0, "justification": "Evaluation failed"},
                "citation_quality": {"score": 0, "justification": "Evaluation failed"},
                "overall_score": 0,
                "suggestions": [],
            }


class SystemPromptEvaluator:
    """Evaluates different system prompts against test cases."""

    def __init__(self, judge: LLMJudge, deepwiki_module):
        """Initialize the evaluator.

        Args:
            judge: LLMJudge instance for evaluation
            deepwiki_module: DeepWiki QA module
        """
        self.judge = judge
        self.deepwiki = deepwiki_module

    def run_evaluation(
        self,
        test_cases: List[Dict[str, Any]],
        system_prompts: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """Run evaluation across all test cases and prompts.

        Args:
            test_cases: List of test case dictionaries
            system_prompts: List of system prompt configurations

        Returns:
            Complete evaluation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "test_cases_count": len(test_cases),
            "prompts_count": len(system_prompts),
            "prompt_results": {},
        }

        for prompt_config in system_prompts:
            prompt_id = prompt_config["id"]
            prompt_name = prompt_config["name"]
            system_prompt = prompt_config["system_prompt"]

            print(f"\nEvaluating prompt: {prompt_name}")
            print("=" * 60)

            prompt_results = {
                "prompt_id": prompt_id,
                "prompt_name": prompt_name,
                "system_prompt": system_prompt,
                "test_results": [],
                "aggregate_scores": {},
            }

            for test_case in test_cases:
                print(f"  Testing: {test_case['question'][:50]}...")

                # Get answer using this system prompt
                # Note: This is a placeholder - you'll need to modify QA system
                # to accept custom system prompts
                try:
                    answer_obj = self._get_answer_with_prompt(
                        test_case["question"], system_prompt
                    )

                    # Evaluate the response
                    evaluation = self.judge.evaluate_response(
                        question=test_case["question"],
                        answer=answer_obj["answer"],
                        expected_topics=test_case["expected_topics"],
                        citations=answer_obj["citations"],
                        context=test_case.get("context", ""),
                    )

                    test_result = {
                        "test_id": test_case["id"],
                        "question": test_case["question"],
                        "answer": answer_obj["answer"],
                        "citations_count": len(answer_obj["citations"]),
                        "evaluation": evaluation,
                    }

                    prompt_results["test_results"].append(test_result)

                except Exception as e:
                    print(f"    Error: {e}")
                    prompt_results["test_results"].append(
                        {
                            "test_id": test_case["id"],
                            "question": test_case["question"],
                            "error": str(e),
                        }
                    )

            # Calculate aggregate scores
            prompt_results["aggregate_scores"] = self._calculate_aggregates(
                prompt_results["test_results"]
            )

            results["prompt_results"][prompt_id] = prompt_results

        # Add comparison summary
        results["comparison"] = self._generate_comparison(results["prompt_results"])

        return results

    def _get_answer_with_prompt(
        self, question: str, system_prompt: str
    ) -> Dict[str, Any]:
        """Get answer using specific system prompt.

        This is a placeholder - needs integration with modified QA system.
        """
        # For now, use default QA system
        # In production, modify qa.py to accept custom system prompts
        from deepwiki.qa import QuestionAnswering

        qa = QuestionAnswering()
        answer = qa.answer(question)

        return {
            "answer": answer.answer,
            "citations": [c.to_dict() for c in answer.citations],
        }

    def _calculate_aggregates(self, test_results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate aggregate scores across all tests."""
        if not test_results:
            return {}

        scores = {
            "relevance": [],
            "completeness": [],
            "accuracy": [],
            "clarity": [],
            "citation_quality": [],
            "overall": [],
        }

        for result in test_results:
            if "evaluation" in result and "error" not in result["evaluation"]:
                eval_data = result["evaluation"]
                scores["relevance"].append(eval_data["relevance"]["score"])
                scores["completeness"].append(eval_data["completeness"]["score"])
                scores["accuracy"].append(eval_data["accuracy"]["score"])
                scores["clarity"].append(eval_data["clarity"]["score"])
                scores["citation_quality"].append(eval_data["citation_quality"]["score"])
                scores["overall"].append(eval_data["overall_score"])

        aggregates = {}
        for key, values in scores.items():
            if values:
                aggregates[f"{key}_mean"] = sum(values) / len(values)
                aggregates[f"{key}_min"] = min(values)
                aggregates[f"{key}_max"] = max(values)

        return aggregates

    def _generate_comparison(self, prompt_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison summary across prompts."""
        comparison = {"rankings": {}, "best_prompt": None, "insights": []}

        # Rank prompts by overall score
        rankings = []
        for prompt_id, results in prompt_results.items():
            if "aggregate_scores" in results and results["aggregate_scores"]:
                rankings.append(
                    {
                        "prompt_id": prompt_id,
                        "prompt_name": results["prompt_name"],
                        "overall_score": results["aggregate_scores"].get(
                            "overall_mean", 0
                        ),
                    }
                )

        rankings.sort(key=lambda x: x["overall_score"], reverse=True)
        comparison["rankings"] = rankings

        if rankings:
            comparison["best_prompt"] = rankings[0]

            # Generate insights
            best = rankings[0]
            worst = rankings[-1]
            score_diff = best["overall_score"] - worst["overall_score"]

            comparison["insights"] = [
                f"Best performing prompt: {best['prompt_name']} (score: {best['overall_score']:.2f})",
                f"Score difference between best and worst: {score_diff:.2f} points",
                f"Total prompts evaluated: {len(rankings)}",
            ]

        return comparison


def save_results(results: Dict[str, Any], output_path: str):
    """Save evaluation results to file."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")


def generate_report(results: Dict[str, Any], output_path: str):
    """Generate human-readable evaluation report."""
    report = []
    report.append("=" * 80)
    report.append("DEEPWIKI EVALUATION REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {results['timestamp']}")
    report.append(f"Test Cases: {results['test_cases_count']}")
    report.append(f"System Prompts: {results['prompts_count']}")
    report.append("\n")

    # Overall comparison
    if "comparison" in results and results["comparison"]["rankings"]:
        report.append("OVERALL RANKINGS")
        report.append("-" * 80)
        for i, ranking in enumerate(results["comparison"]["rankings"], 1):
            report.append(
                f"{i}. {ranking['prompt_name']}: {ranking['overall_score']:.2f}"
            )
        report.append("\n")

        if results["comparison"]["insights"]:
            report.append("KEY INSIGHTS")
            report.append("-" * 80)
            for insight in results["comparison"]["insights"]:
                report.append(f"• {insight}")
            report.append("\n")

    # Detailed results per prompt
    for prompt_id, prompt_data in results["prompt_results"].items():
        report.append(f"\nPROMPT: {prompt_data['prompt_name']}")
        report.append("=" * 80)

        if "aggregate_scores" in prompt_data and prompt_data["aggregate_scores"]:
            scores = prompt_data["aggregate_scores"]
            report.append("\nAggregate Scores:")
            report.append(f"  Overall:          {scores.get('overall_mean', 0):.2f}")
            report.append(f"  Relevance:        {scores.get('relevance_mean', 0):.2f}")
            report.append(f"  Completeness:     {scores.get('completeness_mean', 0):.2f}")
            report.append(f"  Accuracy:         {scores.get('accuracy_mean', 0):.2f}")
            report.append(f"  Clarity:          {scores.get('clarity_mean', 0):.2f}")
            report.append(f"  Citation Quality: {scores.get('citation_quality_mean', 0):.2f}")

        report.append("\n")

    # Write report
    with open(output_path, "w") as f:
        f.write("\n".join(report))

    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    # Load test cases
    with open("../logs/interaction_logs.json") as f:
        test_cases = json.load(f)

    # Load system prompts
    with open("../prompts/system_prompts.json") as f:
        prompts_data = json.load(f)
        system_prompts = prompts_data["prompts"]

    # Initialize evaluator
    judge = LLMJudge()
    evaluator = SystemPromptEvaluator(judge, None)

    print("Starting evaluation...")
    print(f"Test cases: {len(test_cases)}")
    print(f"System prompts: {len(system_prompts)}")

    # Run evaluation
    results = evaluator.run_evaluation(test_cases, system_prompts)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_results(results, f"../results/evaluation_{timestamp}.json")
    generate_report(results, f"../results/report_{timestamp}.txt")

    print("\nEvaluation complete!")
