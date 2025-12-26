# Streaming Responses

Our API supports streaming for real-time responses.

## Basic Streaming

Use the `stream=True` parameter to enable streaming:

```python
from awesome_sdk import Client

client = Client(api_key="your-api-key")

stream = client.chat.create(
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    print(chunk.content, end="", flush=True)
```

## Streaming with Event Handlers

You can also use event handlers for more control:

```python
def on_chunk(chunk):
    print(f"Received: {chunk.content}")

client.chat.create(
    messages=[{"role": "user", "content": "Hello"}],
    stream=True,
    on_chunk=on_chunk
)
```

## Benefits of Streaming

- Lower perceived latency
- Real-time user feedback
- Better UX for long responses
- Handles network interruptions gracefully
