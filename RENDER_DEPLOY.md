# Deploy to Render - Manual Setup (Recommended)

The Blueprint/render.yaml approach has some issues. Use this manual setup instead - it's actually easier!

## Step-by-Step Deployment

### 1. Go to Render
Visit https://render.com and sign up/login with GitHub

### 2. Create New Web Service
- Click **"New +"** button
- Select **"Web Service"**

### 3. Connect Repository
- Click **"Connect account"** if needed
- Find and select: `kahramanmurat/DeepWiki-Like`
- Click **"Connect"**

### 4. Configure Service

Fill in these settings:

**Basic Settings:**
- **Name**: `deepwiki` (or any name you want)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main` (or `elated-germain` if not merged yet)
- **Root Directory**: Leave blank
- **Runtime**: Auto-detected as `Python`

**Build & Deploy:**
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```
  python3 -m deepwiki serve --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (or upgrade to Starter $7/mo for persistence)

### 5. Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

| Key | Value |
|-----|-------|
| `OPENAI_API_KEY` | Your actual OpenAI API key |
| `GITHUB_TOKEN` | Your actual GitHub token (optional) |
| `LLM_PROVIDER` | `openai` |
| `EMBEDDING_MODEL` | `text-embedding-3-small` |

**Important:**
- Don't use quotes around the values
- Copy-paste your actual API keys

### 6. Deploy!

- Click **"Create Web Service"**
- Wait 2-5 minutes for build and deployment
- Your app will be live at: `https://deepwiki-xxx.onrender.com`

## After Deployment

### Test Your App

Visit your app URL: `https://deepwiki-xxx.onrender.com`

You should see the DeepWiki web interface!

### Index a Repository

In the web UI:
1. Click "Index Repository" tab
2. Enter a GitHub repo URL, e.g.:
   ```
   https://github.com/anthropics/anthropic-sdk-python
   ```
3. Click "Index Repository"
4. Wait 1-2 minutes for indexing

### Ask Questions

1. Switch to "Ask Question" tab
2. Enter a question like:
   ```
   How do I use streaming with the SDK?
   ```
3. Get AI-powered answers with citations!

## Important Notes

### ⚠️ Free Tier Limitations

**Data Loss on Restart:**
- Free tier has **no persistent storage**
- Indexed data is **lost when app restarts**
- App **sleeps after 15 minutes** of inactivity

**Solutions:**
1. **Accept it for testing** - Just re-index when needed
2. **Upgrade to Starter ($7/mo)** - Gets persistent disk
3. **Use Railway instead** - Free tier has persistence

### Upgrade to Paid Tier

For production use with data persistence:

1. Go to your service dashboard
2. Click "Settings"
3. Select "Starter" plan ($7/month)
4. In dashboard, add a persistent disk:
   - Name: `data`
   - Mount Path: `/app/data`
   - Size: 1 GB

### Custom Domain

1. In service settings, go to "Custom Domain"
2. Add your domain (e.g., `deepwiki.yourdomain.com`)
3. Configure DNS as instructed

## Troubleshooting

### Build Fails

**Error: `No module named 'deepwiki'`**
- Check that branch has all code files
- Verify `deepwiki/` folder exists in repo

**Error: `requirements.txt not found`**
- Make sure PR is merged to main branch
- Or deploy from `elated-germain` branch

### Deployment Fails

**Error: `Application failed to respond`**
- Check logs in Render dashboard
- Verify API keys are set correctly
- Ensure start command is exact:
  ```
  python3 -m deepwiki serve --host 0.0.0.0 --port $PORT
  ```

### App Crashes

**Check the Logs:**
1. Click "Logs" in Render dashboard
2. Look for error messages
3. Common issues:
   - Missing API key
   - Invalid API key format
   - Python version mismatch

**Fix:**
- Add/update environment variables
- Redeploy the service

### Data Lost After Sleep

This is expected on free tier! Solutions:
- Upgrade to paid tier ($7/mo)
- Use Railway (free tier with persistence)
- Re-index repositories after wake up

## Alternative: Railway Deployment

For free tier WITH data persistence:

1. Go to https://railway.app
2. Sign in with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select `kahramanmurat/DeepWiki-Like`
5. Railway auto-detects and deploys
6. Add environment variables in settings
7. Data persists! ✅

**Cost:** $5 free credit/month

## Need Help?

- Check Render logs for errors
- See main `DEPLOYMENT.md` for other platforms
- Render docs: https://render.com/docs
