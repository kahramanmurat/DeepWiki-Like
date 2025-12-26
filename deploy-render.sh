#!/bin/bash

echo "🚀 DeepWiki Deployment Helper for Render"
echo "=========================================="
echo ""

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found!"
    exit 1
fi

echo "✅ Found render.yaml"
echo ""
echo "📋 Next steps to deploy to Render:"
echo ""
echo "1. Go to https://render.com and sign up/login"
echo ""
echo "2. Click 'New +' → 'Blueprint'"
echo ""
echo "3. Connect your GitHub repository:"
echo "   Repository: kahramanmurat/DeepWiki-Like"
echo "   Branch: main"
echo ""
echo "4. Render will detect render.yaml automatically"
echo ""
echo "5. Add your environment variables in the Render dashboard:"
echo "   OPENAI_API_KEY = [your OpenAI API key]"
echo "   GITHUB_TOKEN = [your GitHub token] (optional)"
echo ""
echo "6. Click 'Apply' to deploy!"
echo ""
echo "🌐 Your app will be live at: https://deepwiki.onrender.com"
echo ""
echo "⚠️  Important notes:"
echo "   - Free tier: App sleeps after 15 minutes of inactivity"
echo "   - First request after sleep may take 30-60 seconds"
echo "   - Upgrade to paid tier ($7/mo) for always-on service"
echo ""
echo "📚 Need help? Check DEPLOYMENT.md for full guide"
