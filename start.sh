#!/bin/bash
# Start script for Railway deployment

# Use Railway's PORT environment variable, or default to 8000
PORT=${PORT:-8000}

echo "Starting DeepWiki on port $PORT"
python3 -m deepwiki serve --host 0.0.0.0 --port $PORT
