# esiosapy

Unofficial ESIOS API Python library for interacting with the Spanish Electricity System (Red Eléctrica de España) data API.

## Features

- **Simple API**: Easy-to-use client for accessing ESIOS data
- **Sync & Async**: Both synchronous and asynchronous clients
- **Type Hints**: Full type annotations for better IDE support
- **Retry Logic**: Automatic retry with exponential backoff
- **Logging**: Built-in logging for debugging
- **Timeouts**: Configurable request timeouts

## Installation

```bash
# Install esiosapy
pip install esiosapy

# Install with async support
pip install esiosapy[async]

# Install all extras
pip install esiosapy[all]
```

## Quick Start

```python
from esiosapy import ESIOSAPYClient

# Create a client
client = ESIOSAPYClient(token="your-api-token")

# List all indicators
indicators = client.indicators.list_all()

# Search for specific indicators
solar = client.indicators.search("solar")

# Get archives
archives = client.archives.list_all()
```

## Async Usage

```python
import asyncio
from esiosapy import AsyncESIOSAPYClient

async def main():
    client = AsyncESIOSAPYClient(token="your-api-token")

    async with client:
        indicators = await client.indicators.list_all()

asyncio.run(main())
```

## CLI Usage

```bash
# List indicators
esiosapy --token YOUR_TOKEN indicators

# List archives
esiosapy --token YOUR_TOKEN archives
```

## Configuration

### Timeouts

```python
# Set custom timeout (default: 30 seconds)
client = ESIOSAPYClient(token="xxx", timeout=60)
```

### Logging

```python
import logging

logging.basicConfig()
logging.getLogger("esiosapy").setLevel(logging.DEBUG)
```
