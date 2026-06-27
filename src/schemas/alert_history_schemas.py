import json
from datetime import timezone
from typing import List

from src.models.alert import Alert

ALERT_PATH = "memory/alert_history.json"


def load_alerts() -> List[Alert]:
    with open(ALERT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Alert.model_validate(item) for item in data]


def validate_alerts():
    alerts = load_alerts()

    for alert in alerts:
        if alert.timestamp.tzinfo != timezone.utc:
            raise ValueError(f"Alert {alert.alert_id} must be UTC")

    return alerts
