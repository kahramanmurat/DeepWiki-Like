# Getting Started with Our API

Welcome to our API documentation! This guide will help you get started quickly.

## Installation

To install our SDK, run:

```bash
pip install our-awesome-sdk
```

## Authentication

You need an API key to use our service. Get one from our dashboard.

```python
from awesome_sdk import Client

client = Client(api_key="your-api-key")
```

## Making Your First Request

Here's how to make a simple request:

```python
response = client.chat.create(
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)
```

## Error Handling

Always wrap your API calls in try-except blocks:

```python
try:
    response = client.chat.create(messages=[...])
except Exception as e:
    print(f"Error: {e}")
```
