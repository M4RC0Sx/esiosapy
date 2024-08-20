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

```python
from esiosapy.client import ESIOSAPYClient
from esiosapy.models.indicator.time_trunc import TimeTrunc

client = ESIOSAPYClient(
    token="your_token"
)

indicators = client.indicators.list_all()
indicator = indicators[0]

data = indicator.get_data("2021-01-01", "2021-01-02", time_trunc=TimeTrunc.HOUR)
```

esiosapy allows you to communicate with the ESIOS/REE API in a comfortable and abstract way, so that everything is handled by objects and you will not need to write any raw request.


## Installing esiosapy
esiosapy is available on PyPi and it supports Python >=3.8:

```bash
pip install esiosapy
```

## User guide
**There will be a more detailed in the future.**

You need a personal token in order to use the ESIOS API. You can request it in [https://api.esios.ree.es/](https://api.esios.ree.es/)

### Archives
```python
from esiosapy.client import ESIOSAPYClient
from esiosapy.models.archive.archive_date_type import ArchiveDateType


# Init client
client = ESIOSAPYClient(
    "your_esios_api_token"
)

# Search files by date range
archives = client.archives.list_by_date_range(
    "2021-01-01T00:00:00.000+01:00",
    "2021-01-02T00:00:00.000+01:00",
    date_type=ArchiveDateType.PUBLICATION,
)

# Get first file. here you should filter with your needed criteria
x = archives[0]

# Download file in current path, unzip and remove zip
x.download_file(unzip=True, remove_zip=True)
```

To elaborate your filtering criteria, you can check out [the attributes of the Archive model](https://github.com/M4RC0Sx/esiosapy/blob/master/esiosapy/models/archive/archive.py).

### Indicators
```python
from esiosapy.client import ESIOSAPYClient
from esiosapy.models.indicator.time_trunc import TimeTrunc

# Init client
client = ESIOSAPYClient(
    token="you_esios_api_token"
)

# Get all indicators
indicators = client.indicators.list_all()

# Get first file. here you should filter with your needed criteria
# Usually, you are looking for a specific indicator
indicator = indicators[0]

# Get data between 2 dates, with time_trunc of 1 hour
data = indicator.get_data("2021-01-01", "2021-01-02", time_trunc=TimeTrunc.HOUR)
```

To elaborate your filtering criteria, you can check out [the attributes of the Indicator model](https://github.com/M4RC0Sx/esiosapy/blob/master/esiosapy/models/indicator/indicator.py).


## TO-DO List
- [x] Archive model handling.
- [x] Indicator model handling.
- [x] OfferIndicator model handling.
- [x] Add docstrings to the entire project.
- [ ] Archive JSON model handling.
- [ ] Auction model handling.
- [ ] Generate wiki with/and more elaborated docs.
- [ ] Add more unit tests.
- [ ] Support date range slicing to avoid long requests/responses.

## Dependencies
esiosapy depends on Pydantic and requests.

## Contributing
All contributions are welcome via direct contact with me or pull requests, as long as they are well elaborated and follow the conventional commits format.

