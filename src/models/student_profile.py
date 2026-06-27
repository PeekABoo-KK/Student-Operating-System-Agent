from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


class StudentProfile(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    student_id: str
    name: str
    gpa: float = Field(ge=0.0, le=4.0)
    major: str
    year: int = Field(ge=1, le=5)
    tags: List[str] = []

    created_at: datetime
    updated_at: datetime
