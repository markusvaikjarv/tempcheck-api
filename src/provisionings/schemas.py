from sys import displayhook
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Provisioning(BaseModel):
    id: UUID
    display_name: str
    created_at: datetime
    updated_at: datetime

class NewProvisioning(BaseModel):
    display_name: str
