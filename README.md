# EOSC Data Transfer Python Client

A simple, typed Python client for interacting with the [EOSC Data Transfer API](https://eosc-data-transfer.cern.ch/swagger-ui/), built with `requests` and `pydantic`.

## Features

- Authenticated API access
- Typed request/response models
- Supports creating and listing data transfers

## Installation

```bash
git clone https://gitlab.com/fts/eosc-data-transfer-client.git
cd eosc-data-transfer-client
pip install -r requirements.txt
```

## Usage

```python
from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.models import TransferRequest
from eosc_data_transfer_client.endpoints import create_transfer

client = EOSCClient("https://eosc-data-transfer.cern.ch", token="your_token")

params = TransferParameters(
    verifyChecksum=False,
    overwrite=False
)

transfer = FileTransfer(
    sources = ["mock://source.io/path/to/file.txt"],
    destinations = ["mock://destination.io/path/to/file.txt"]
)

request = TransferRequest(
    files = transfer,
    params = params
)

result = create_transfer(client, transfer)
print(result.jobId)
```

## Development

To contribute or modify:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Licence
The eosc-data-transfer-client is under the Apache License 2.0

