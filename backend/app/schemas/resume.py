from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ResumeBase(BaseModel):
    file_name: str
    file_type: str
    file_size_bytes: int


class ResumeOut(ResumeBase):
    id: str
    user_id: str
    file_path: str
    scan_status: str = "CLEAN"
    parsed_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeListOut(BaseModel):
    items: List[ResumeOut]
    total: int
