# Advanced Usage

This guide covers advanced features of our API.

## Custom Parameters

You can customize the behavior with various parameters:

```python
response = client.chat.create(
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,      # Control randomness (0-1)
    max_tokens=1000,      # Limit response length
    top_p=0.9,           # Nucleus sampling
)
```

## Batch Processing

Process multiple requests efficiently:

```python
requests = [
    {"messages": [{"role": "user", "content": "Question 1"}]},
    {"messages": [{"role": "user", "content": "Question 2"}]},
    {"messages": [{"role": "user", "content": "Question 3"}]},
]

results = client.chat.batch(requests)
for result in results:
    print(result.content)
```

## Rate Limiting

Handle rate limits gracefully:

```python
from awesome_sdk.exceptions import RateLimitError
import time

def call_with_retry(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if i < max_retries - 1:
                time.sleep(2 ** i)  # Exponential backoff
            else:
                raise
```

## Caching Responses

Cache responses to save costs:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_response(prompt):
    return client.chat.create(
        messages=[{"role": "user", "content": prompt}]
    )
```
