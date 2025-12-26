# DeepWiki Evaluation System

A comprehensive LLM-as-a-Judge evaluation framework for testing and comparing different system prompts in the DeepWiki documentation Q&A system.

## Overview

This evaluation system allows you to:

1. **Collect interaction logs** - Record real user questions and expected outcomes
2. **Test multiple system prompts** - Compare different prompt strategies
3. **Automated evaluation** - Use GPT-4 as a judge to score responses
4. **Generate reports** - Get detailed analysis and comparisons

## Directory Structure

```
evaluation/
├── logs/                          # Interaction logs
│   └── interaction_logs.json     # 12 test cases
├── prompts/                       # System prompt variations
│   └── system_prompts.json       # 5 different prompts
├── scripts/                       # Evaluation scripts
│   ├── evaluator.py             # Main evaluation framework
│   └── run_evaluation.py        # Simple runner script
├── results/                       # Output directory
│   ├── evaluation_*.json        # Detailed JSON results
│   └── report_*.txt             # Human-readable reports
└── README.md                      # This file
```

## System Prompts

The evaluation includes 5 different system prompt strategies:

1. **Baseline** - Simple and direct responses
2. **Detailed** - Comprehensive, well-structured answers
3. **Concise** - Quick and focused responses
4. **Educational** - Teaching-oriented with explanations
5. **Technical** - Developer-focused with code examples

## Evaluation Criteria

Each response is evaluated on 5 dimensions (0-10 scale):

1. **Relevance** - How well does the answer address the question?
2. **Completeness** - Does it cover all expected topics?
3. **Accuracy** - Is the information correct and precise?
4. **Clarity** - Is the answer well-structured and understandable?
5. **Citation Quality** - Are sources properly cited and relevant?

## Test Cases

12 interaction logs covering:

- **anthropics/anthropic-sdk-python queries:**
  - Streaming usage
  - Authentication methods
  - Rate limiting
  - Async/await support
  - Available models
  - Error handling
  - Parameter customization

- **DataTalksClub/ai-dev-tools-zoomcamp queries:**
  - MCP module content
  - Homework requirements
  - Development setup
  - Course structure
  - Prerequisites

## Usage

### Quick Start

```bash
# Navigate to the evaluation scripts directory
cd evaluation/scripts

# Run the evaluation
python run_evaluation.py
```

### What Happens

1. Loads 12 test cases from `logs/interaction_logs.json`
2. Loads 5 system prompts from `prompts/system_prompts.json`
3. For each prompt:
   - Generates answers for all test cases
   - Uses GPT-4 to evaluate each response
   - Calculates aggregate scores
4. Compares all prompts and ranks them
5. Saves detailed results as JSON
6. Generates human-readable report

### Expected Output

```
DeepWiki Evaluation System
============================================================

Loaded 12 test cases
Loaded 5 system prompts

Starting evaluation...
This may take several minutes...

Evaluating prompt: Baseline - Simple and Direct
============================================================
  Testing: How do I use streaming with the SDK?...
  Testing: What are the authentication methods?...
  ...

Results saved to: ../results/evaluation_20251225_120000.json
Report saved to: ../results/report_20251225_120000.txt

Evaluation complete!
```

## Sample Report Format

```
================================================================================
DEEPWIKI EVALUATION REPORT
================================================================================

Generated: 2025-12-25T12:00:00
Test Cases: 12
System Prompts: 5

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

PROMPT: Technical - Developer-Focused
================================================================================

Aggregate Scores:
  Overall:          8.45
  Relevance:        8.72
  Completeness:     8.58
  Accuracy:         8.91
  Clarity:          8.45
  Citation Quality: 7.59
```

## Customization

### Adding New Test Cases

Edit `logs/interaction_logs.json`:

```json
{
  "id": 13,
  "timestamp": "2025-12-25T11:00:00Z",
  "repository": "your-repo/name",
  "question": "Your question here",
  "expected_topics": ["topic1", "topic2"],
  "context": "Additional context"
}
```

### Creating New System Prompts

Edit `prompts/system_prompts.json`:

```json
{
  "id": "my_prompt",
  "name": "My Custom Prompt",
  "system_prompt": "Your custom system prompt here..."
}
```

### Modifying Evaluation Criteria

Edit the `evaluate_response` method in `scripts/evaluator.py` to add or modify criteria.

## Integration with DeepWiki

To use custom system prompts in production:

1. Modify `deepwiki/qa.py` to accept a `system_prompt` parameter
2. Update the `QuestionAnswering` class constructor
3. Pass the custom prompt to the LLM when generating answers

Example modification:

```python
class QuestionAnswering:
    def __init__(self, system_prompt: str = None):
        self.system_prompt = system_prompt or "Default prompt..."

    def answer(self, question: str, top_k: int = 5):
        # Use self.system_prompt in LLM call
        ...
```

## Requirements

- OpenAI API key (for LLM-as-a-judge evaluation)
- Python 3.8+
- All DeepWiki dependencies

## Cost Estimation

Each evaluation run makes:
- N test cases × M prompts × 1 answer generation call
- N test cases × M prompts × 1 evaluation call

For 12 test cases × 5 prompts:
- 60 answer generation calls
- 60 evaluation calls (GPT-4)
- Estimated cost: ~$1-3 per full evaluation

## Future Enhancements

- [ ] Add metrics tracking over time
- [ ] Support for A/B testing in production
- [ ] Human evaluation comparison
- [ ] Automated prompt optimization
- [ ] Multi-model evaluation (Anthropic, OpenAI, etc.)
- [ ] Performance benchmarking (speed, tokens used)

## Troubleshooting

**Issue:** API key errors
- **Solution:** Ensure `OPENAI_API_KEY` is set in `.env`

**Issue:** No responses generated
- **Solution:** Check that DeepWiki index has documents

**Issue:** Evaluation fails
- **Solution:** Verify GPT-4 API access and rate limits

## License

Same as DeepWiki-Like main project (MIT)
