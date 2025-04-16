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

import requests
from typing import Any, Union
from .exceptions import EOSCClientError, EOSCServerError, EOSCRequestError

class EOSCClient:
    """
    A client for interacting with the EOSC Data Transfer API.
    Handles authentication, request sending, and error parsing.
    """
    def __init__(self, base_url: str, token: str = None):
        """
        Initializes the EOSCClient.

        Args:
            base_url (str): The base URL of the EOSC API.
            token (str, optional): Bearer token for authorization.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def request(self, method, endpoint, **kwargs: Any) -> Union[dict, str]:
        """
        Send a request to the API and handle errors.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            endpoint (str): API endpoint path.
            **kwargs: Additional request options.

        Returns:
            Union[dict, str]: Parsed response from the API.

        Raises:
            EOSCClientError: For 4xx errors.
            EOSCServerError: For 5xx errors.
            EOSCRequestError: For network issues.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs, verify=False)
            if 400 <= response.status_code < 500:
                try:
                    message = response.json()
                except ValueError:
                    message = response.text
                raise EOSCClientError(response.status_code, message, response=response)

            elif 500 <= response.status_code < 600:
                try:
                    message = response.json()
                except ValueError:
                    message = response.text
                raise EOSCServerError(response.status_code, message, response=response)

            if response.content:
                try:
                    return response.json()
                except ValueError:
                    return response.text
            else:
                return {}

        except requests.exceptions.RequestException as e:
            raise EOSCRequestError(str(e)) from e
