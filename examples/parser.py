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
from eosc_data_transfer_client.endpoints import *
from eosc_data_transfer_client.exceptions import EOSCError

token = os.environ.get('BEARER_TOKEN', 'my_token')

client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

client = EOSCClient(base_url="https://data-transfer.service.eosc-beyond.eu", token="your-access-token")
doi = "doi:10.5281/zenodo.6511035"

try:
    parsed_metadata = parse_doi(client, doi)
    print(parsed_metadata.model_dump(mode='json'))
except EOSCError as e:
    print(f"[ERROR] {e}\n")
    sys.exit()
