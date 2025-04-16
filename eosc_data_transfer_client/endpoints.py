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

from .client import EOSCClient
from .models import TransferRequest, TransferResponse, TransferStatus, TransferStatusList
from datetime import datetime
from typing import Optional, Any, Union

def create_transfer(client: EOSCClient, transfer: TransferRequest) -> TransferResponse:
    """
    Initiate a new data transfer.

    This function sends a `POST` request to the EOSC Data Transfer API to create a new transfer job.

    Arguments:
        client: An instance of `EOSCClient` configured with base URL and authentication.
        transfer: A `TransferRequest` object describing the files to transfer and transfer parameters.

    Returns:
        TransferResponse: An object containing details about the submitted transfer, including job ID and status.

    Raises:
        EOSCClientError: If the API returns a 4xx error (e.g., invalid input).
        EOSCServerError: If the API returns a 5xx error (e.g., internal server error).
    """
    response = client.request("POST", "/transfers", json=transfer.dict())
    return TransferResponse(**response)

def get_transfer_status(client: EOSCClient, transfer_id: str) -> TransferStatus:
    """
    Retrieve the status of a transfer job.

    This function sends a `GET` request to the API to fetch full details about a specific transfer job
    using its job ID.

    Arguments:
        client: An instance of `EOSCClient` for making authenticated requests.
        transfer_id: The ID of the transfer job to retrieve.

    Returns:
        TransferStatus: An object with detailed information about the job, including state, timestamps, and metadata.

    Raises:
        EOSCClientError: If the job ID is invalid or not found.
        EOSCServerError: If the API encounters an internal issue.
    """
    response = client.request("GET", f"/transfer/{transfer_id}")
    return TransferStatus(**response)

def get_transfer_field(client: EOSCClient, job_id: str, field_name: str) -> Union[str, int, bool, dict, datetime]:
    """
    Retrieve a specific field from a transfer job, using TransferStatus model for type resolution.

    Args:
        client: The API client.
        job_id: Transfer job ID.
        field_name: Field to retrieve.

    Returns:
        The value of the requested field, properly typed.

    Raises:
        ValueError: If the field name is invalid or type conversion fails.
    """
    model_fields = TransferStatus.model_fields
    if field_name not in model_fields:
        raise ValueError(f"Unsupported field name: '{field_name}'. Must be one of: {list(model_fields.keys())}")

    expected_type = model_fields[field_name].annotation
    raw_response = client.request("GET", f"/transfer/{job_id}/{field_name}")

    # Extract from "entity"
    value = raw_response.get("entity", None)
    if value is None:
        raise ValueError(f"No 'entity' found in response for field '{field_name}'")

    # Parse value based on expected type
    try:
        if expected_type is int:
            return int(value)
        elif expected_type is float:
            return float(value)
        elif expected_type is datetime:
            return datetime.fromisoformat(value)
        elif expected_type is bool:
            return str(value).lower() in {"true", "1", "yes"}
        elif expected_type is dict:
            return value if isinstance(value, dict) else {}
        else:
            return str(value)
    except Exception as e:
        raise ValueError(f"Failed to convert value for field '{field_name}' to {expected_type}: {e}")

def cancel_transfer(client: EOSCClient, job_id: str) -> TransferStatus:
    """
    Cancel a transfer job with a job_id

    Args:
        client: The API client.
        job_id: Transfer job ID.

    Returns:
        TransferStatus: The canceled transfer with its current status (canceled or any other final status).
    """
    response = client.request("DELETE", f"/transfer/{job_id}")
    return TransferStatus(**response)

def list_transfers(client: EOSCClient, **filters: Optional[Any]) -> TransferStatusList:
    """
    Find transfers matching search criteria.

    Args:
        client: The API client.
        **filters: Optional query parameters to filter the search.

    Returns:
        TransferStatusList: A list of transfers matching the criteria.
    """
    # Filter out None values
    query_params = {k: v for k, v in filters.items() if v is not None}
    response = client.request("GET", "/transfers", params=query_params)
    return TransferStatusList(**response)

