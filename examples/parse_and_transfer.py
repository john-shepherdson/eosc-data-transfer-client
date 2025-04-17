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
from eosc_data_transfer_client.client import EOSCClient
from eosc_data_transfer_client.models import TransferRequest, FileTransfer, TransferParameters
from eosc_data_transfer_client.endpoints import * 
from eosc_data_transfer_client.exceptions import EOSCError

"""
    This simple script demonstrates how the EOSC Data Transfer API can be used to transfer
    data sets from public repositories (ex: Zenodo) to remote storage systems (ex: EOS)

    1) Using a Zenodo data set DOI the EOSC Data Transfer API is called to obtain the list
    of downloadable files and their digital location.

    2) With the list of urls obtained a file transfer request is created in the EOSC Data
    Transfer API
"""


token = os.environ.get('BEARER_TOKEN', 'my_token')

client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

doi = "doi:10.5281/zenodo.6511035"

destination_storage = "https://eospilot.cern.ch:443//eos/pilot/opstest/dteam/batistal/"

# Parse DOI to obtain a list of file urls
try:
    storage_elements = parse_doi(client, doi)
except EOSCError as e:
    print(f"[ERROR] {e}\n")
    sys.exit()

# Create transfer for the data transfer service
transfers = []
for element in storage_elements.elements:
    transfers.append(FileTransfer(
        sources = [element.downloadUrl],
        destinations = [destination_storage + element.name],
        checksum = element.checksum,
        filesize = element.size
    ))

# Create tranfer paramenters
params = TransferParameters(
    verifyChecksum=True,
    overwrite=False,
    retry=2
)

# Create the file transfer request
request = TransferRequest(
    files = transfers,
    params = params
)


# Submit file transfer request to the EOSC data transfer API
try:
    response = create_transfer(client, request)
    print(f"Job submitted:\n\tjobId={response.jobId}")
except EOSCError as e:
    print(f"[ERROR] {e}\n")
    sys.exit()
