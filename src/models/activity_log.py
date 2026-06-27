from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict


class ActivityLog(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    log_id: str
    timestamp: datetime
    action: str
    status: str
    metadata: Dict
