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

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class TransferParameters(BaseModel):
    """
    Defines optional parameters to control the behavior of a transfer job.

    Attributes:
        verifyChecksum (Optional[bool]): Whether to verify the checksum of the destination file.
        overwrite (Optional[bool]): Whether to overwrite the destination file if it already exists.
        retry (Optional[int]): Number of times a failed transfer should be retried.
        priority (Optional[int]): The priority level of the transfer.
    """
    verifyChecksum: Optional[bool] = Field(default=False, description="Verify the checksum of the destination file")
    overwrite: Optional[bool] = Field(default=False, description="Should the destination file be overwritten if it already exists")
    retry: Optional[int] = Field(default=0, description="How many times a failed transfer should be retried")
    priority: Optional[int] = Field(default=3, description="Priority of the transfer")

class FileTransfer(BaseModel):
    """
    Represents the details of a file transfer.

    Attributes:
        sources (List[str]): List of source file paths.
        destinations (List[str]): List of destination file paths.
        checksum (str): Checksum of the file to verify integrity.
        filesize (int): Size of the file in bytes.
        activity (Optional[str]): Activity associated with the transfer (default: 'default').
    """
    sources: List[str]
    destinations: List[str]
    checksum: str
    filesize: int
    activity: Optional[str] = Field(default="default", description="The activity share to be used")
    #metadata: Optional[Dict[str, str]] = None

class TransferRequest(BaseModel):
    """
    Represents a request to initiate a transfer job.

    Attributes:
        files (List[FileTransfer]): List of file transfers to be executed.
        params (TransferParameters): Parameters controlling the behavior of the transfer job.
    """
    files: List[FileTransfer]
    params: TransferParameters

class TransferResponse(BaseModel):
    """
    Represents the response received after initiating a transfer job.

    Attributes:
        kind (str): The kind of transfer job.
        jobId (str): The unique job ID for the transfer.
    """
    kind: str
    jobId: str

class TransferStatus(BaseModel):
    """
    Represents the status of an ongoing or completed transfer job.

    Attributes:
        kind (str): The kind of transfer job.
        jobId (str): The unique job ID for the transfer.
        source_se (str): The source storage element.
        destination_se (Optional[str]): The destination storage element (if any).
        jobState (str): The state of the job (e.g., 'completed', 'in-progress').
        verifyChecksum (str): Whether checksum verification is enabled.
        overwrite (Optional[bool]): Whether overwriting is allowed.
        priority (int): Priority of the transfer.
        retry (int): Retry count.
        retryDelay (int): Retry delay time.
        cancel (bool): Whether the job has been canceled.
        submittedAt (datetime): Timestamp when the job was submitted.
        submittedTo (str): The system to which the job was submitted.
        finishedAt (Optional[datetime]): Timestamp when the job finished.
        reason (Optional[str]): The error reason (if any).
        vo_name (str): The VO name associated with the transfer.
        user_dn (str): The user distinguished name.
        cred_id (str): The credential ID.
    """
    kind: str
    jobId: str
    source_se: str
    destination_se: Optional[str] = None
    jobState: str
    verifyChecksum: str
    overwrite: Optional[bool] = False
    priority: int
    retry: int
    retryDelay: int
    cancel: bool
    submittedAt: datetime
    submittedTo: str
    finishedAt: Optional[datetime] = None
    reason: Optional[str] = Field(default="", description="The error reason")
    vo_name: str
    user_dn: str
    cred_id: str

class TransferStatusList(BaseModel):
    """
    Represents a list of transfer statuses.

    Attributes:
        kind (str): The kind of transfer status list.
        count (int): The number of transfers in the list.
        transfers (List[TransferStatus]): List of individual transfer statuses.
    """
    kind: str
    count: int
    transfers: List[TransferStatus]

class StorageElement(BaseModel):
    """
    Represents a single file or folder item parsed from a DOI.
    Attributes:
        kind (str): The type of content (should be 'StorageElement').
        name (str): Name of the file.
        path (str): Path to the file.
        isFolder (bool): Whether the storage element corresponds to a folder.
        isAccessible (bool): Whether the storage element is publicly accessible.
        mediaType (str): The storage element media type.
        accessUrl (str): The url to access the storage element.
        downloadUrl (str): The url to download the storage element.
        checksum (str): The checksum of the storage element.
    """
    kind: str
    name: str
    path: str
    isFolder: bool
    isAccessible: bool
    size: int
    mediaType: str
    accessUrl: str
    downloadUrl: str
    checksum: str

class StorageContent(BaseModel):
    """
    Represents the parsed content result of a DOI, including a list of downloadable elements.

    Attributes:
        kind (str): The type of content (should be 'StorageContent').
        count (int): Number of elements parsed.
        elements (List[StorageElement]): List of parsed file or folder items.
    """
    kind: str
    count: int
    elements: List[StorageElement]

class UserInfo(BaseModel):
    """
    Represents information about the current user, retrieved from the /userinfo endpoint.

    Fields vary depending on authentication status.

    Attributes:
        kind (str): The type of content (should be 'StorageContent').
        base_id (base_id): Number of elements parsed.
        user_dn (str): List of parsed file or folder items.
    """
    kind: str
    base_id: str
    user_dn: str
    delegation_id: Optional[str] = None
    vos: Optional[List[str]] = None
    vos_id: Optional[List[str]] = None
    voms_cred: Optional[List[str]] = None

    class Config:
        extra = "allow"  # Allow unrecognized fields in future responses
