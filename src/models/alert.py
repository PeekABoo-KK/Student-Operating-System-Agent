from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Alert(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    alert_id: str
    timestamp: datetime
    type: str
    severity: str
    message: str
    resolved: bool
