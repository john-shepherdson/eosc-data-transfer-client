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

class EOSCError(Exception):
    """Base exception for EOSC Data Transfer client.

    All custom exceptions inherit from this class.
    """
    pass

class EOSCClientError(EOSCError):
    """Raised for 4xx client-side HTTP errors (e.g., invalid request, authentication issues)."""

    def __init__(self, status_code, message, response=None):
        """
        Initialize a client error.

        Args:
            status_code (int): HTTP status code.
            message (str): Error message from the server or client.
            response (object, optional): Full response object from the request library.
        """
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] Client Error: {message}")

class EOSCServerError(EOSCError):
    """Raised for 5xx server-side HTTP errors."""

    def __init__(self, status_code, message, response=None):
        """
        Initialize a server error.

        Args:
            status_code (int): HTTP status code.
            message (str): Error message returned from the server.
            response (object, optional): Full response object from the request library.
        """
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] Server Error: {message}")

class EOSCRequestError(EOSCError):
    """Raised for request failures like timeouts, network issues, or invalid URLs."""
    def __init__(self, message):
        """
        Initialize a request error.

        Args:
            message (str): A description of the request failure.
        """
        super().__init__(f"Request failed: {message}")

