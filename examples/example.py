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

import os
import sys
import time
from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.models import TransferRequest, FileTransfer, TransferParameters
from eosc_data_transfer_client.endpoints import * 
from eosc_data_transfer_client.exceptions import EOSCError

token = os.environ.get('BEARER_TOKEN', 'my_token')

client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

params = TransferParameters(
    verifyChecksum=False,
    overwrite=False
)

transfer = FileTransfer(
    sources = ["mock://source.io/path/to/file.txt?checksum=88a2d31f"],
    destinations = ["mock://destination.io/path/to/file.txt?checksum=88a2d31f&time=60"],
    checksum = "ADLER32:88a2d31f",
    filesize = 1234
)

request = TransferRequest(
    files = [transfer],
    params = params
)

try:
    # Create a transfer on the server
    response = create_transfer(client, request)
    print(f"Job submitted:\n\tjobId={response.jobId}")
    # Query the status of the transfer
    status = get_transfer_status(client, response.jobId)
    print(f"Job status:\n\t{status.model_dump()}")
    # Get jobState field from job status
    state = get_transfer_field(client, response.jobId, "jobState")
    print(f"Job state:\n\t{state}")
    # Get all transfers assigined to my vo
    transfer_list = list_transfers(client, vo_name=status.vo_name)
    print(f"There are {transfer_list.count} active transfers for the {status.vo_name} vo")
    # Cancel the transfer and print new status
    status = cancel_transfer(client, response.jobId)
    print(f"Job status:\n\t{status.model_dump()}")
    state = get_transfer_field(client, response.jobId, "jobState")
    print(f"Job state:\n\t{state}")
except EOSCError as e:
    print(f"[ERROR] {e}\n")
    sys.exit()
