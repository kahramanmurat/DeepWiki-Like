# Quick Start Guide - DeepWiki Evaluation System

## Prerequisites

1. DeepWiki is installed and working
2. OpenAI API key is configured in `.env`
3. At least one repository is indexed

## Step 1: Review Test Cases

Check the interaction logs to see what questions will be tested:

```bash
cat evaluation/logs/interaction_logs.json | python -m json.tool
```

You'll see 12 test cases covering various documentation queries.

## Step 2: Review System Prompts

Check the different prompt strategies:

```bash
cat evaluation/prompts/system_prompts.json | python -m json.tool
```

5 prompts will be evaluated:
- Baseline (simple)
- Detailed (comprehensive)
- Concise (focused)
- Educational (teaching)
- Technical (developer-focused)

## Step 3: Run the Evaluation

**Warning:** This will make ~120 API calls to OpenAI (60 for answers, 60 for evaluation).
Estimated cost: $1-3 depending on your API plan.

```bash
cd evaluation/scripts
python run_evaluation.py
```

The script will:
1. Load all test cases and prompts
2. Generate answers using each prompt
3. Use GPT-4 to evaluate each answer
4. Calculate aggregate scores
5. Save results and generate reports

This will take 5-10 minutes to complete.

## Step 4: View Results

### Quick Summary

```bash
python visualize_results.py ../results/evaluation_XXXXXX.json --summary
```

This shows a comparison table ranking all prompts.

### Detailed Analysis

```bash
python visualize_results.py ../results/evaluation_XXXXXX.json --detailed
```

Shows evaluation details for each test case.

### Generate Markdown Report

```bash
python visualize_results.py ../results/evaluation_XXXXXX.json --markdown ../results/report.md
```

Creates a shareable markdown report.

## Step 5: Analyze Results

Look at the generated text report:

```bash
cat ../results/report_XXXXXX.txt
```

Key things to check:
- Which prompt scored highest overall?
- Which criteria show the biggest differences?
- What suggestions did the judge provide?
- Are there consistent patterns across test cases?

## Example Output

```
================================================================================
DEEPWIKI EVALUATION REPORT
================================================================================

OVERALL RANKINGS
--------------------------------------------------------------------------------
1. Technical - Developer-Focused: 8.45
2. Detailed - Comprehensive Answers: 8.23
3. Educational - Teaching-Oriented: 7.98
4. Baseline - Simple and Direct: 7.56
5. Concise - Quick and Focused: 7.12

KEY INSIGHTS
--------------------------------------------------------------------------------
• Best performing prompt: Technical - Developer-Focused (score: 8.45)
• Score difference between best and worst: 1.33 points
• Total prompts evaluated: 5
```

## Next Steps

### 1. Implement the Best Prompt

Once you identify the best-performing prompt, integrate it into DeepWiki:

```python
# In deepwiki/qa.py
SYSTEM_PROMPT = """
[Your best-performing prompt here]
"""
```

### 2. Add More Test Cases

Edit `evaluation/logs/interaction_logs.json` to add real user queries:

```json
{
  "id": 13,
  "timestamp": "2025-12-25T12:00:00Z",
  "repository": "your/repo",
  "question": "Your real user question",
  "expected_topics": ["topic1", "topic2"],
  "context": "Why the user asked this"
}
```

### 3. Test New Prompt Ideas

Edit `evaluation/prompts/system_prompts.json`:

```json
{
  "id": "my_experiment",
  "name": "My Experimental Prompt",
  "system_prompt": "Your new prompt strategy..."
}
```

Then re-run the evaluation to compare.

### 4. Track Performance Over Time

```bash
# Run weekly evaluations
python run_evaluation.py

# Compare results
diff ../results/report_20251225.txt ../results/report_20260101.txt
```

## Troubleshooting

**Error: No module named 'deepwiki'**
```bash
# Make sure you're in the right directory
cd /path/to/DeepWiki-Like
python evaluation/scripts/run_evaluation.py
```

**Error: API key not found**
```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY
```

**Error: No documents indexed**
```bash
# Index a repository first
python -m deepwiki index https://github.com/anthropics/anthropic-sdk-python
```

**Evaluation is slow**
- This is normal - GPT-4 evaluation takes time
- You can reduce test cases for faster iterations
- Consider using a faster model for initial testing

## Cost Management

To reduce costs during testing:

1. **Use fewer test cases:** Edit `interaction_logs.json` to keep only 3-5 cases
2. **Use fewer prompts:** Comment out prompts in `system_prompts.json`
3. **Use GPT-3.5:** Change model in `evaluator.py` (less accurate but cheaper)

Example for quick testing:

```python
# In evaluator.py, line 13
judge = LLMJudge(model="gpt-3.5-turbo")  # Instead of "gpt-4"
```

## Advanced Usage

### Custom Evaluation Criteria

Edit `evaluator.py` to add your own criteria:

```python
# Add to evaluation_prompt
6. **Custom Criterion (0-10):** Your description here
```

### Batch Evaluation

Create multiple test case files and run in batch:

```bash
for file in logs/*.json; do
    python run_evaluation.py --input $file
done
```

### A/B Testing in Production

Use the evaluation results to set up A/B tests:

```python
# Randomly assign users to different prompts
import random

prompts = ["baseline", "technical", "educational"]
user_prompt = random.choice(prompts)
```

## Getting Help

- Check `evaluation/README.md` for detailed documentation
- Review example results in `evaluation/results/`
- Inspect the evaluation code in `evaluation/scripts/evaluator.py`

Happy evaluating! 🚀
