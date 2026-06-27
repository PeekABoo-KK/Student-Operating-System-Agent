import json
from datetime import timezone
from typing import List

from src.models.activity_log import ActivityLog

ACTIVITY_PATH = "memory/activity_log.json"


def load_activity_logs() -> List[ActivityLog]:
    with open(ACTIVITY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [ActivityLog.model_validate(item) for item in data]


def validate_activity_logs():
    logs = load_activity_logs()

    for log in logs:
        if log.timestamp.tzinfo != timezone.utc:
            raise ValueError(f"Log {log.log_id} timestamp must be UTC")

    return logs
