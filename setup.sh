#!/bin/bash

# Setup script for DeepWiki-Like

echo "Setting up DeepWiki-Like..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env file and add your API keys:"
    echo "  - OPENAI_API_KEY (for OpenAI)"
    echo "  - or ANTHROPIC_API_KEY (for Claude)"
    echo "  - GITHUB_TOKEN (optional, for higher rate limits)"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run: python -m deepwiki --help"
