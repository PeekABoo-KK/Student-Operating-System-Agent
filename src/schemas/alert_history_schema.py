from datetime import datetime
from typing import Dict, Any, List, Tuple

def is_valid_iso8601(timestamp_str: str) -> bool:
    """Check if a string is a valid ISO 8601 timestamp."""
    if not isinstance(timestamp_str, str):
        return False
    try:
        datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def validate_single_alert(alert: Any) -> List[str]:
    """Validate a single alert entry dictionary."""
    errors = []
    if not isinstance(alert, dict):
        return ["Alert entry must be a dictionary"]

    required_fields = {"alert_id", "timestamp", "severity", "message", "source_agent", "resolved"}

    # 1. Reject unknown fields
    for key in alert.keys():
        if key not in required_fields:
            errors.append(f"Unknown field: {key}")

    # 2. Validate required fields presence
    for field in required_fields:
        if field not in alert:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    # 3. Validate types and bounds
    # alert_id
    alert_id = alert["alert_id"]
    if not isinstance(alert_id, str):
        errors.append("alert_id must be a string")

    # timestamp
    timestamp = alert["timestamp"]
    if not is_valid_iso8601(timestamp):
        errors.append(f"timestamp must be a valid ISO 8601 timestamp: {timestamp}")

    # severity
    severity = alert["severity"]
    allowed_severities = {"LOW", "MEDIUM", "HIGH"}
    if not isinstance(severity, str):
        errors.append("severity must be a string")
    elif severity not in allowed_severities:
        errors.append(f"severity must be one of {allowed_severities}")

    # message
    message = alert["message"]
    if not isinstance(message, str):
        errors.append("message must be a string")
    elif not (1 <= len(message) <= 500):
        errors.append("message length must be between 1 and 500 characters")

    # source_agent
    source_agent = alert["source_agent"]
    allowed_sources = {"OrchestratorAgent", "AcademicRiskAgent"}
    if not isinstance(source_agent, str):
        errors.append("source_agent must be a string")
    elif source_agent not in allowed_sources:
        errors.append(f"source_agent must be one of {allowed_sources}")

    # resolved
    resolved = alert["resolved"]
    if not isinstance(resolved, bool):
        errors.append("resolved must be a boolean")

    return errors

def validate(data: Any) -> Tuple[bool, List[str]]:
    """Validate alert history data (either a list of alerts or a single alert)."""
    errors = []
    if isinstance(data, list):
        for idx, alert in enumerate(data):
            alert_errors = validate_single_alert(alert)
            for err in alert_errors:
                errors.append(f"Alert {idx}: {err}")
    elif isinstance(data, dict):
        errors = validate_single_alert(data)
    else:
        errors.append("Alert history data must be a list of alerts or a single alert dictionary")

    return len(errors) == 0, errors
