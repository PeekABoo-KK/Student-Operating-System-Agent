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

def validate_single_entry(entry: Any) -> List[str]:
    """Validate a single activity log entry dictionary."""
    errors = []
    if not isinstance(entry, dict):
        return ["Activity log entry must be a dictionary"]

    required_fields = {"timestamp", "agent", "action", "reason", "result", "status"}

    # 1. Reject unknown fields
    for key in entry.keys():
        if key not in required_fields:
            errors.append(f"Unknown field: {key}")

    # 2. Validate required fields presence
    for field in required_fields:
        if field not in entry:
            errors.append(f"Missing required field: {field}")

    if errors:
        return errors

    # 3. Validate types and bounds
    # timestamp
    timestamp = entry["timestamp"]
    if not is_valid_iso8601(timestamp):
        errors.append(f"timestamp must be a valid ISO 8601 timestamp: {timestamp}")

    # agent
    agent = entry["agent"]
    allowed_agents = {"OrchestratorAgent", "AcademicRiskAgent", "OpportunityScoutAgent"}
    if not isinstance(agent, str):
        errors.append("agent must be a string")
    elif agent not in allowed_agents:
        errors.append(f"agent must be one of {allowed_agents}")

    # action
    action = entry["action"]
    if not isinstance(action, str):
        errors.append("action must be a string")
    elif not (1 <= len(action) <= 200):
        errors.append("action length must be between 1 and 200 characters")

    # reason
    reason = entry["reason"]
    if not isinstance(reason, str):
        errors.append("reason must be a string")

    # result
    result = entry["result"]
    if not isinstance(result, str):
        errors.append("result must be a string")
    elif not (1 <= len(result) <= 1000):
        errors.append("result length must be between 1 and 1000 characters")

    # status
    status = entry["status"]
    allowed_statuses = {"SUCCESS", "FAILED", "PARTIAL", "TIMEOUT", "VALIDATION_ERROR", "ROUTING_ERROR",}
    if not isinstance(status, str):
        errors.append("status must be a string")
    elif status not in allowed_statuses:
        errors.append(f"status must be one of {allowed_statuses}")

    return errors

def validate(data: Any) -> Tuple[bool, List[str]]:
    """Validate activity log data (either a list of entries or a single entry)."""
    errors = []
    if isinstance(data, list):
        for idx, entry in enumerate(data):
            entry_errors = validate_single_entry(entry)
            for err in entry_errors:
                errors.append(f"Entry {idx}: {err}")
    elif isinstance(data, dict):
        errors = validate_single_entry(data)
    else:
        errors.append("Activity log data must be a list of entries or a single entry dictionary")

    return len(errors) == 0, errors
