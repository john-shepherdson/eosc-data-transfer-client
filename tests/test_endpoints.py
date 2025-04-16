#   Copyright 2025 CERN
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import pytest
import requests_mock
from datetime import datetime

from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.endpoints import (
    create_transfer,
    get_transfer_status,
    get_transfer_field,
    cancel_transfer,
    list_transfers,
)
from eosc_data_transfer_client.models import (
    TransferRequest,
    FileTransfer,
    TransferParameters,
)
from eosc_data_transfer_client.exceptions import EOSCClientError, EOSCServerError

BASE_URL = "https://data-transfer.service.eosc-beyond.eu"
TOKEN = "fake-token"

def make_client():
    return EOSCClient(BASE_URL, token=TOKEN)

def make_dummy_request():
    params = TransferParameters(verifyChecksum=False, overwrite=False)
    transfer = FileTransfer(
        sources=["mock://source"],
        destinations=["mock://destination"],
        checksum="ADLER32:deadbeef",
        filesize=42
    )
    return TransferRequest(files=[transfer], params=params)

# Creates a valid transfer request
def test_create_transfer_success():
    client = make_client()
    request = make_dummy_request()
    mock_response = {"kind": "tranferStatus", "jobId": "abc-123"}

    with requests_mock.Mocker() as m:
        m.post(f"{BASE_URL}/transfers", json=mock_response)
        response = create_transfer(client, request)
        assert response.jobId == "abc-123"

# Invalid field name for get_transfer_field
def test_get_transfer_field_invalid_field():
    client = make_client()
    with pytest.raises(ValueError, match="Unsupported field name"):
        get_transfer_field(client, "job-123", "nonexistentField")

# 404 client error from API
def test_get_transfer_status_404():
    client = make_client()
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/transfer/invalid-job", status_code=404, json={"error": "Not found"})
        with pytest.raises(EOSCClientError):
            get_transfer_status(client, "invalid-job")

# 500 server error from API
def test_create_transfer_500():
    client = make_client()
    request = make_dummy_request()
    with requests_mock.Mocker() as m:
        m.post(f"{BASE_URL}/transfers", status_code=500, json={"error": "Internal Server Error"})
        with pytest.raises(EOSCServerError):
            create_transfer(client, request)

# Field parsing to int
def test_get_transfer_field_parses_int():
    client = make_client()
    job_id = "job-abc"
    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/transfer/{job_id}/priority", json={"entity": 42})
        result = get_transfer_field(client, job_id, "priority")
        assert isinstance(result, int)
        assert result == 42

# Listing transfers with a filter
def test_list_transfers_with_vo_filter():
    client = make_client()
    mock_response = {
        "kind": "transfer-list",
        "count": 1,
        "transfers": [
            {
                "kind": "transfer",
                "jobId": "abc-123",
                "jobState": "FINISHED",
                "jobStateTS": "2023-01-01T00:00:00",
                "jobType": "copy",
                "jobMetadata": {},
                "source_se": "src",
                "destination_se": "dst",
                "verifyChecksum": "true",
                "overwrite": True,
                "priority": 1,
                "retry": 0,
                "retryDelay": 0,
                "maxTimeInQueue": 0,
                "cancel": False,
                "submittedAt": "2023-01-01T00:00:00",
                "submittedTo": "host",
                "finishedAt": "2023-01-01T00:01:00",
                "reason": "",
                "vo_name": "my-vo",
                "user_dn": "dn",
                "cred_id": "cred"
            }
        ]
    }

    with requests_mock.Mocker() as m:
        m.get(f"{BASE_URL}/transfers", json=mock_response)
        response = list_transfers(client, vo_name="my-vo")
        assert response.count == 1
        assert response.transfers[0].jobId == "abc-123"

