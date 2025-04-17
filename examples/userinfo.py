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
from eosc_data_transfer_client.endpoints import get_user_info
from eosc_data_transfer_client.exceptions import EOSCError

token = os.environ.get('BEARER_TOKEN', 'my_token')

client = EOSCClient("https://data-transfer.service.eosc-beyond.eu", token=token)

try:
    user_info = get_user_info(client)
    print(user_info.model_dump(mode='json'))
except EOSCError as e:
    print(f"[ERROR] {e}\n")
    sys.exit()
