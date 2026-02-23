# esiosapy

<p align="center">
    <em>Unofficial ESIOS API Python library. Up to date and fully equipped.</em>
</p>

<p align="center">
<a href="https://github.com/M4RC0Sx/esiosapy/actions/workflows/test.yml/badge.svg?branch=develop" target="_blank">
    <img src="https://github.com/M4RC0Sx/esiosapy/actions/workflows/test.yml/badge.svg?branch=develop" alt="Test">
</a>
<a href="https://github.com/M4RC0Sx/esiosapy/actions/workflows/release.yml/badge.svg" target="_blank">
    <img src="https://github.com/M4RC0Sx/esiosapy/actions/workflows/release.yml/badge.svg" alt="Release">
</a>
<a href="https://pypi.org/project/esiosapy" target="_blank">
    <img src="https://img.shields.io/pypi/v/esiosapy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/esiosapy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esiosapy.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Documentation**: [https://m4rc0sx.github.io/esiosapy/](https://m4rc0sx.github.io/esiosapy/)

---

esiosapy allows you to communicate with the [ESIOS/REE API](https://api.esios.ree.es/) in a comfortable and abstract way, so that everything is handled by objects and you will not need to write any raw request.

## Features

- **Simple API**: Easy-to-use client for accessing ESIOS data
- **Sync & Async**: Both synchronous and asynchronous clients
- **Type Hints**: Full type annotations with strict mypy support
- **Retry Logic**: Automatic retry with exponential backoff for network errors
- **CLI**: Command-line interface for quick data exploration
- **Logging**: Built-in logging for debugging
- **Configurable Timeouts**: Customizable request timeouts

## Installation

esiosapy is available on PyPI and supports Python >=3.9:

```bash
pip install esiosapy
```

### Optional dependencies

```bash
# Async support (httpx)
pip install esiosapy[async]

# HTML description prettifying (beautifulsoup4)
pip install esiosapy[beautifulsoup]

# All optional dependencies
pip install esiosapy[all]
```

## Quick start

You need a personal token to use the ESIOS API. You can request one at [https://api.esios.ree.es/](https://api.esios.ree.es/).

### Indicators

```python
from esiosapy import ESIOSAPYClient
from esiosapy.models.indicator.time_trunc import TimeTrunc

client = ESIOSAPYClient(token="your_esios_api_token")

# Get all indicators
indicators = client.indicators.list_all()

# Search indicators by name
solar = client.indicators.search("solar")

# Get data for an indicator
indicator = indicators[0]
data = indicator.get_data("2021-01-01", "2021-01-02", time_trunc=TimeTrunc.HOUR)
```

### Archives

```python
from esiosapy import ESIOSAPYClient
from esiosapy.models.archive.archive_date_type import ArchiveDateType

client = ESIOSAPYClient(token="your_esios_api_token")

# Search files by date range
archives = client.archives.list_by_date_range(
    "2021-01-01T00:00:00.000+01:00",
    "2021-01-02T00:00:00.000+01:00",
    date_type=ArchiveDateType.PUBLICATION,
)

# Download, unzip, and clean up
archives[0].download_file(unzip=True, remove_zip=True)
```

### Async usage

```python
import asyncio
from esiosapy import AsyncESIOSAPYClient

async def main():
    async with AsyncESIOSAPYClient(token="your_esios_api_token") as client:
        indicators = await client.indicators.list_all()

asyncio.run(main())
```

### Context manager

Both sync and async clients support context managers for automatic resource cleanup:

```python
with ESIOSAPYClient(token="your_esios_api_token") as client:
    indicators = client.indicators.list_all()
```

### CLI

```bash
# List all indicators
esiosapy --token YOUR_TOKEN indicators

# List all archives
esiosapy --token YOUR_TOKEN archives

# Set custom timeout
esiosapy --token YOUR_TOKEN --timeout 60 indicators
```

## Dependencies

esiosapy depends on [Pydantic](https://docs.pydantic.dev/), [requests](https://requests.readthedocs.io/), and [tenacity](https://tenacity.readthedocs.io/).

## Contributing

All contributions are welcome! Please read the [contributing guide](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the GPL-3.0-or-later license. See the [LICENSE](LICENSE) file for details.
