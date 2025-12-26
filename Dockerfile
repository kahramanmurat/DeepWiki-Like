FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY deepwiki ./deepwiki
COPY .env.example .env.example

# Create data directory for ChromaDB
RUN mkdir -p /app/data/chroma_db

# Expose port
EXPOSE 8000

# Set environment variable for data directory
ENV DATA_DIR=/app/data

# Run the application
CMD ["python", "-m", "deepwiki", "serve", "--host", "0.0.0.0", "--port", "8000"]
