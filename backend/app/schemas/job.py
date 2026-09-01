from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class JobDescriptionCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    company_name: Optional[str] = Field(None, max_length=255)
    raw_text: str = Field(..., min_length=10)


class JobDescriptionOut(BaseModel):
    id: str
    user_id: str
    title: str
    company_name: Optional[str] = None
    raw_text: str
    parsed_requirements: Dict[str, Any] = Field(default_factory=dict)
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size_bytes: Optional[int] = None
    scan_status: str = "CLEAN"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobDescriptionListOut(BaseModel):
    items: List[JobDescriptionOut]
    total: int
