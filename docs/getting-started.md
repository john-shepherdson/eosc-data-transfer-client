# Getting Started

This guide will walk you through setting up and using the **EOSC Data Transfer Client**.

## Prerequisites

- Python 3.8 or higher
- A valid EOSC Bearer token (environment variable `BEARER_TOKEN`)
- A working virtual environment (optional but recommended)

---

## Installation

```bash
git clone https://your.repo.url/eosc-data-transfer-client.git
cd eosc-data-transfer-client
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Submitting a Transfer

```python
from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.models import TransferRequest, FileTransfer, TransferParameters
from eosc_data_transfer_client.endpoints import create_transfer

token = os.environ.get("BEARER_TOKEN")
client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

params = TransferParameters(
    verifyChecksum=False,
    overwrite=True
)

file = FileTransfer(
    sources=["https://source.example.org/file1.txt"],
    destinations=["https://dest.example.org/file1.txt"],
    checksum="ADLER32:88a2d31f",
    filesize=1234
)

request = TransferRequest(
    files=[file],
    params=params
)

response = create_transfer(client, request)
print(f"Transfer Job ID: {response.jobId}")
```

## Next Steps

- See the API Reference for all available endpoints.
- Use `get_transfer_status()` to inspect jobs status.
- Try `list_transfers()` to search on past tranfers.
