from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UserProfileModel(BaseModel):
    uid: uuid.UUID
    email: str
    first_name: str
    last_name: str
    is_verified: bool 
    created_at: datetime
    updated_at: datetime