# EOSC Data Transfer Python Client

A simple, typed Python client for interacting with the [EOSC Data Transfer API](https://data-transfer.service.eosc-beyond.eu/swagger-ui/), built with `requests` and `pydantic`.

Look at the complete [documentation](https://eosc-data-transfer-client.docs.cern.ch/) for usage examples, models, and API details.

## Features

* Authenticated API access
* Submit and monitor data transfers
* Cancel data transfer jobs
* Filter and search transfers
* Digital Object Indetifier (DIO) parsing
* Robust error handling with custom exceptions
* Pydantic models for easy validation
* Unit tests included with pytest

## Installation

```bash
git clone https://gitlab.com/fts/eosc-data-transfer-client.git
cd eosc-data-transfer-client
pip install -r requirements.txt
```

## Usage

```python
from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.models import TransferRequest, FileTransfer, TransferParameters
from eosc_data_transfer_client.endpoints import create_transfer, get_transfer_status
import os

token = os.environ.get('BEARER_TOKEN', 'my_token')

client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

params = TransferParameters(
    verifyChecksum=False,
    overwrite=False
)

transfer = FileTransfer(
    sources = ["mock://source.io/path/to/file.txt?checksum=88a2d31f "],
    destinations = ["mock://destination.io/path/to/file.txt?checksum=88a2d31f&time=60"],
    checksum = "ADLER32:88a2d31f",
    filesize = 1234
)

request = TransferRequest(
    files = [transfer],
    params = params
)

result = create_transfer(client, request)
print(result.jobId)

status = get_transfer_status(client, result.jobId)
```

## Development

To contribute or modify:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the tests
```bash
pip install pytest requests-mock
pytest tests/
```

## Licence
The eosc-data-transfer-client is under the Apache License 2.0

