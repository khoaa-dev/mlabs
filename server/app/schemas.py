from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Contact creation schema
class ContactCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    role: Optional[str] = None
    notes: Optional[str] = None

# Contact response schemas
class ContactOut(ContactCreate):
    id: int
    class Config:
        from_attributes = True

# Message creation schema
class MessageCreate(BaseModel):
    contact_id: int
    message_type: str
    prompt_hint: Optional[str] = None

# Message response schemas
class MessageOut(BaseModel):
    id: int
    contact_id: int
    message_type: str
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

