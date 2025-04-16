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
    verifyChecksum: Optional[bool] = Field(default=False, description="Verify the checksum of the destination file")
    overwrite: Optional[bool] = Field(default=False, description="Should the destination file be overwritten if it already exists")
    retry: Optional[int] = Field(default=0, description="How many times a failed transfer should be retried")
    priority: Optional[int] = Field(default=3, description="Priority of the transfer")

class FileTransfer(BaseModel):
    sources: List[str]
    destinations: List[str]
    checksum: str
    filesize: int
    activity: Optional[str] = Field(default="default", description="The activity share to be used")
    #metadata: Optional[Dict[str, str]] = None

class TransferRequest(BaseModel):
    files: List[FileTransfer]
    params: TransferParameters

class TransferResponse(BaseModel):
    kind: str
    jobId: str

class TransferStatus(BaseModel):
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
    kind: str
    count: int
    transfers: List[TransferStatus]
