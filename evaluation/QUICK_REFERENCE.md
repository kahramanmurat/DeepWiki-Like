# DeepWiki Evaluation System - Quick Reference

## 🚀 Quick Commands

### Demo Mode (No API costs)
```bash
cd evaluation/scripts
python3 demo_evaluation.py
python3 visualize_results.py ../results/demo_evaluation_*.json --summary
```

### Full Evaluation (~$1-3, 5-10 min)
```bash
cd evaluation/scripts
python3 run_evaluation.py
python3 visualize_results.py ../results/evaluation_*.json --summary
```

## 📊 What Gets Evaluated

### Test Cases (12 total)
- Anthropic SDK queries: streaming, auth, rate limits, async, models, errors
- Zoomcamp queries: modules, homework, setup, prerequisites

### System Prompts (5 variations)
1. Baseline - Simple and direct
2. Detailed - Comprehensive answers
3. Concise - Quick and focused  
4. Educational - Teaching-oriented
5. Technical - Developer-focused

### Evaluation Criteria (0-10 each)
- Relevance
- Completeness
- Accuracy
- Clarity
- Citation Quality

## 📁 File Locations

```
evaluation/
├── logs/interaction_logs.json          # Test cases
├── prompts/system_prompts.json         # Prompt variations
├── scripts/
│   ├── run_evaluation.py              # Main runner
│   ├── demo_evaluation.py             # Quick demo
│   └── visualize_results.py           # View results
└── results/                            # Output files
```

## 🔧 Customization

### Add Test Case
Edit `evaluation/logs/interaction_logs.json`:
```json
{"id": 13, "question": "...", "expected_topics": [...], "context": "..."}
```

### Add Prompt
Edit `evaluation/prompts/system_prompts.json`:
```json
{"id": "new", "name": "My Prompt", "system_prompt": "..."}
```

## 📈 View Results

```bash
# Summary table
python3 visualize_results.py RESULTS.json --summary

# Detailed breakdown
python3 visualize_results.py RESULTS.json --detailed

# Markdown report
python3 visualize_results.py RESULTS.json --markdown report.md
```

## 💰 Cost

- **Demo mode**: FREE
- **Full evaluation**: ~$1-3 (12 tests × 5 prompts × 2 API calls)
- Reduce costs: Edit files to use fewer tests/prompts

## ⚡ Typical Workflow

1. Run demo to understand system
2. Review test cases and prompts
3. Run full evaluation
4. Analyze results
5. Implement best prompt
6. Add real user queries as test cases
7. Re-evaluate periodically

## 🎯 Expected Output

```
OVERALL RANKINGS
1. Technical - Developer-Focused: 8.45
2. Detailed - Comprehensive: 8.23
3. Educational - Teaching: 7.98
4. Baseline - Simple: 7.56
5. Concise - Quick: 7.12
```

## 📚 Documentation

- `README.md` - Complete documentation
- `QUICKSTART.md` - Step-by-step tutorial
- `EVALUATION_SYSTEM_SUMMARY.md` - Full overview

## 🐛 Troubleshooting

**Error: API key not found**
→ Check `.env` has `OPENAI_API_KEY`

**Error: No documents indexed**
→ Run `python -m deepwiki index <repo_url>` first

**Slow evaluation**
→ Normal! Each test takes ~10 seconds

**Want faster testing**
→ Reduce test cases or use `demo_evaluation.py`

## ✅ Success Criteria

All requirements met:
- ✅ 12+ interaction logs
- ✅ LLM-as-a-judge evaluation
- ✅ Multiple system prompts tested
- ✅ Automated comparison
- ✅ Complete documentation

---

**Need help?** See `README.md` or `QUICKSTART.md`
