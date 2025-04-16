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
    """Base exception for EOSC Data Transfer client."""
    pass

class EOSCClientError(EOSCError):
    """4xx Client-side errors (invalid request, auth, etc.)."""
    def __init__(self, status_code, message, response=None):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] Client Error: {message}")

class EOSCServerError(EOSCError):
    """5xx Server-side errors."""
    def __init__(self, status_code, message, response=None):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(f"[{status_code}] Server Error: {message}")

class EOSCRequestError(EOSCError):
    """Any other error like connection timeout, network down, etc."""
    def __init__(self, message):
        super().__init__(f"Request failed: {message}")

