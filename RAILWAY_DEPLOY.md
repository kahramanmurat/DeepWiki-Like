# Deploy to Railway - Complete Guide

Railway is the **BEST free option** - it has persistent storage on the free tier! ✅

## Quick Deployment

### 1. Go to Railway
Visit https://railway.app

### 2. Sign In
Click "Login" → Sign in with GitHub

### 3. Create New Project
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Find and select: `kahramanmurat/DeepWiki-Like`
- Click on the repository

### 4. Railway Auto-Detects Everything! 🎉
Railway will automatically:
- Detect it's a Python project
- Find `requirements.txt`
- Install dependencies
- Start the application

### 5. Configure Start Command

Railway might need help with the start command:

1. Click on your deployment
2. Go to **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Set **"Custom Start Command"**:
   ```
   python3 -m deepwiki serve --host 0.0.0.0 --port $PORT
   ```
5. Click "Deploy" to restart

### 6. Add Environment Variables

1. Click **"Variables"** tab
2. Click **"New Variable"** for each:

| Variable Name | Value |
|---------------|-------|
| `OPENAI_API_KEY` | Your actual OpenAI API key |
| `GITHUB_TOKEN` | Your GitHub token (optional) |
| `LLM_PROVIDER` | `openai` |
| `EMBEDDING_MODEL` | `text-embedding-3-small` |

3. Railway will automatically redeploy

### 7. Get Your URL

1. Go to **"Settings"** tab
2. Scroll to **"Environment"** section
3. Click **"Generate Domain"**
4. Your app will be live at: `https://your-app.up.railway.app`

## ✅ Data Persistence

Railway free tier includes **persistent volumes**!

Your ChromaDB data will be saved automatically in `/app/data` and **persists across deployments**.

No additional configuration needed! 🎉

## Testing Your Deployment

### 1. Visit Your App
Open your Railway URL: `https://your-app.up.railway.app`

### 2. Index a Repository
- Click "Index Repository" tab
- Enter: `https://github.com/anthropics/anthropic-sdk-python`
- Click "Index Repository"
- Wait ~1-2 minutes

### 3. Ask Questions
- Switch to "Ask Question" tab
- Try: "How do I use streaming with the SDK?"
- Get AI-powered answers!

## Troubleshooting

### Error: "No start command found"

**Fix:**
1. Go to Settings → Deploy
2. Add custom start command:
   ```
   python3 -m deepwiki serve --host 0.0.0.0 --port $PORT
   ```
3. Redeploy

### Error: "Application failed to start"

**Check Logs:**
1. Click "Deployments" tab
2. Click on latest deployment
3. View logs for errors

**Common Issues:**
- Missing `OPENAI_API_KEY` - Add in Variables tab
- Wrong Python version - Railway uses Python 3.11 by default (should work)
- Port binding issue - Make sure start command includes `--port $PORT`

### Error: Module not found

**Solution:**
1. Check that `requirements.txt` exists in repo
2. Verify all dependencies are listed
3. Trigger a rebuild

### App Crashes on Startup

**Check:**
1. Environment variables are set correctly
2. API key is valid (no quotes around it)
3. Start command is correct
4. Check logs for specific error messages

## Railway Features

### Persistent Storage ✅
- Automatic persistent volumes
- Data survives restarts
- No configuration needed

### Free Tier
- **$5 credit per month**
- ~500 hours of runtime
- Persistent storage included
- Good for production use!

### Monitoring
- Real-time logs
- Deployment history
- Metrics dashboard

### Custom Domain
1. Go to Settings
2. Click "Add Custom Domain"
3. Enter your domain
4. Follow DNS instructions

## Cost Estimates

**Free Tier Usage:**
- Small app like DeepWiki: ~$3-4/month
- Stays within $5 free credit
- No credit card required initially

**If You Need More:**
- Add credit card
- Pay only for usage beyond $5/month
- Very reasonable pricing

## Viewing Logs

### Real-Time Logs
1. Click "Deployments"
2. Click active deployment
3. View live logs

### Common Log Messages

**Success:**
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

**Need to Index:**
```
Found X Markdown files
Chunking Y documents...
Successfully indexed Z chunks
```

## Managing Your App

### Redeploy
- Push to GitHub → Auto-deploys
- Or click "Deploy" in Railway dashboard

### Stop/Start
- Click service name
- Use power button to stop/start

### Delete
- Settings → Danger Zone → Delete Service

## Advanced: Railway CLI

Install Railway CLI for advanced control:

```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands
railway run python -m deepwiki index <repo_url>
```

## Environment-Specific Configuration

Railway automatically sets:
- `PORT` - Port your app should listen on
- `RAILWAY_ENVIRONMENT` - Usually "production"

Your app uses `$PORT` from the start command.

## Best Practices

1. **Use environment variables** for all secrets
2. **Check logs** after each deployment
3. **Test indexing** with a small repo first
4. **Monitor usage** in Railway dashboard
5. **Set up custom domain** for production

## Next Steps

After successful deployment:

1. ✅ Index your documentation repositories
2. ✅ Test with real questions
3. ✅ Share your app URL
4. ✅ Set up custom domain (optional)
5. ✅ Monitor usage and costs

## Why Railway > Render Free?

| Feature | Railway Free | Render Free |
|---------|--------------|-------------|
| Persistent Storage | ✅ Yes | ❌ No |
| Sleep on Idle | ❌ No | ✅ Yes (15 min) |
| Monthly Credit | $5 | N/A |
| Cold Start | Fast | Slow |
| Data Survival | ✅ Yes | ❌ No |

**Winner:** Railway for free tier! 🏆

---

Need help? Check the logs or visit https://docs.railway.app
