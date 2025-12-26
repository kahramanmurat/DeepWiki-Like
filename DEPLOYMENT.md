# DeepWiki Deployment Guide

Complete guide to deploying DeepWiki to the internet.

## Deployment Options

### Option 1: Render (Recommended - Free Tier Available) ⭐

**Pros:**
- Free tier available
- Easy deployment from GitHub
- Automatic SSL
- Zero configuration needed

**Steps:**

1. **Prepare for Deployment**

Create `requirements.txt` (already exists):
```
openai>=1.0.0
anthropic>=0.18.0
chromadb>=0.4.0
fastapi>=0.109.0
uvicorn>=0.27.0
pydantic>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
PyGithub>=2.1.1
tiktoken>=0.5.0
beautifulsoup4>=4.12.0
markdown>=3.5.0
aiohttp>=3.9.0
```

2. **Create Start Command File**

Create `start.sh`:
```bash
#!/bin/bash
python -m deepwiki serve
```

3. **Deploy to Render**

- Go to https://render.com
- Sign up/login with GitHub
- Click "New +" → "Web Service"
- Connect your GitHub repository: `kahramanmurat/DeepWiki-Like`
- Configure:
  - **Name**: `deepwiki` (or your choice)
  - **Branch**: `main` (after merging PR)
  - **Runtime**: `Python 3`
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python -m deepwiki serve`

4. **Set Environment Variables**

In Render dashboard, add:
```
OPENAI_API_KEY=your_actual_key
ANTHROPIC_API_KEY=your_actual_key (optional)
GITHUB_TOKEN=your_actual_token (optional)
```

5. **Deploy**

Click "Create Web Service" - Your app will be live at `https://deepwiki-xxx.onrender.com`

**Cost:** Free tier available (app sleeps after 15 min inactivity)

---

### Option 2: Railway ⚡

**Pros:**
- $5/month free credit
- Very fast deployments
- Great developer experience

**Steps:**

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `kahramanmurat/DeepWiki-Like`
5. Add environment variables (same as above)
6. Railway auto-detects Python and deploys

**Cost:** $5 free credit/month, then pay-as-you-go

---

### Option 3: Heroku

**Pros:**
- Well-established platform
- Good documentation

**Steps:**

1. **Install Heroku CLI**
```bash
brew install heroku/brew/heroku  # macOS
```

2. **Create Procfile**
```
web: python -m deepwiki serve --host 0.0.0.0 --port $PORT
```

3. **Deploy**
```bash
heroku login
heroku create deepwiki-app
heroku config:set OPENAI_API_KEY=your_key
heroku config:set GITHUB_TOKEN=your_token
git push heroku main
```

**Cost:** $7/month minimum (no free tier anymore)

---

### Option 4: Google Cloud Run 🚀

**Pros:**
- Only pay for actual usage
- Scales to zero
- Professional grade

**Steps:**

1. **Create Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "deepwiki", "serve", "--host", "0.0.0.0", "--port", "8080"]
```

2. **Deploy to Cloud Run**
```bash
# Install gcloud CLI
brew install google-cloud-sdk

# Login and setup
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud run deploy deepwiki \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

**Cost:** Free tier: 2M requests/month, pay only for usage after

---

### Option 5: DigitalOcean App Platform

**Pros:**
- $5/month tier
- Simple interface
- Good performance

**Steps:**

1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect GitHub repository
4. Configure:
   - **Type**: Web Service
   - **Run Command**: `python -m deepwiki serve --host 0.0.0.0 --port 8080`
5. Add environment variables
6. Deploy

**Cost:** Starting at $5/month

---

### Option 6: AWS (EC2 + Elastic Beanstalk)

**Pros:**
- Full control
- Scalable
- Industry standard

**Steps:**

1. **Create application.py** (for Elastic Beanstalk)
```python
import os
from deepwiki.api import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
```

2. **Deploy via Elastic Beanstalk CLI**
```bash
pip install awsebcli
eb init -p python-3.11 deepwiki
eb create deepwiki-env
eb setenv OPENAI_API_KEY=your_key
eb deploy
```

**Cost:** ~$10-20/month for basic EC2 instance

---

## Quick Deployment Files

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data/chroma_db

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "deepwiki", "serve", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  deepwiki:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    volumes:
      - ./data:/app/data
```

### render.yaml (for Render)
```yaml
services:
  - type: web
    name: deepwiki
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m deepwiki serve --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: GITHUB_TOKEN
        sync: false
```

---

## Recommended: Render (Easiest & Free)

**Step-by-step for Render:**

1. **Merge your PR first:**
```bash
gh pr merge 1 --squash
```

2. **Go to Render.com and sign up**

3. **Create New Web Service:**
   - Repository: `kahramanmurat/DeepWiki-Like`
   - Branch: `main`
   - Name: `deepwiki`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m deepwiki serve --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables in Render:**
   ```
   OPENAI_API_KEY = your_actual_openai_key
   GITHUB_TOKEN = your_actual_github_token (optional)
   ```

5. **Deploy!**

Your app will be live at: `https://deepwiki.onrender.com` (or custom domain)

---

## Important Configuration Changes

### Update deepwiki/api.py for Cloud Deployment

You may need to modify the serve command to accept host/port args:

```python
# In deepwiki/__main__.py
@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=8000, help='Port to bind to')
def serve(host, port):
    """Start the web server."""
    import uvicorn
    from .api import app

    print(f"Starting web server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
```

### Environment Variables

**Required:**
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`

**Optional:**
- `GITHUB_TOKEN` - For higher GitHub API rate limits
- `PORT` - Port to bind to (provided by hosting platform)

---

## Database Persistence

**Important:** ChromaDB data needs persistent storage!

### For Render/Railway/Heroku:
Add a persistent disk volume to store `/app/data/chroma_db`

### For Docker:
Use volumes: `- ./data:/app/data`

### For Cloud Providers:
Use cloud storage (S3, GCS) or managed databases

---

## Security Checklist

- [ ] `.env` is in `.gitignore` ✅ (already done)
- [ ] API keys set as environment variables (not in code)
- [ ] HTTPS enabled (automatic with Render/Railway/etc)
- [ ] Add rate limiting for production
- [ ] Set up authentication if needed
- [ ] Configure CORS if accessing from different domain

---

## Monitoring & Logs

Most platforms provide:
- Application logs
- Performance metrics
- Error tracking
- Uptime monitoring

**Render:** View logs in dashboard
**Railway:** Real-time logs in terminal
**Heroku:** `heroku logs --tail`

---

## Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | ✅ (sleeps after 15min) | $7/mo | Getting started |
| **Railway** | $5 credit/mo | Pay-as-you-go | Development |
| **Heroku** | ❌ | $7/mo minimum | Simple apps |
| **Cloud Run** | ✅ 2M req/mo | Pay-per-use | Production |
| **DigitalOcean** | ❌ | $5/mo | Budget hosting |
| **AWS** | ✅ 1 year free | Variable | Enterprise |

---

## Next Steps After Deployment

1. **Index your first repository:**
```bash
curl -X POST https://your-app.onrender.com/api/index \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/anthropics/anthropic-sdk-python"}'
```

2. **Test the API:**
```bash
curl -X POST https://your-app.onrender.com/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I use streaming?"}'
```

3. **Set up custom domain** (optional)

4. **Add monitoring/analytics**

---

## Troubleshooting

**App won't start:**
- Check logs for errors
- Verify environment variables are set
- Ensure port is configured correctly

**Database errors:**
- Check persistent storage is configured
- Verify ChromaDB directory has write permissions

**API rate limits:**
- Add GITHUB_TOKEN to environment
- Monitor API usage

**Out of memory:**
- Increase instance size
- Optimize chunk size/batch processing

---

Need help with deployment? Check the platform-specific docs or ask for help!
