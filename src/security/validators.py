from datetime import datetime
from src.security.security_rules import security_rules


# ======================
# INPUT VALIDATION
# ======================
def validate_user_input(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be string")

    if len(text.strip()) == 0:
        raise ValueError("Empty input")

    if len(text) > security_rules.MAX_INPUT_LENGTH:
        raise ValueError("Input too long")

    lowered = text.lower()

    for bad in security_rules.BLOCKLIST:
        if bad in lowered:
            raise ValueError(f"Blocked: {bad}")

    return text.strip()


# ======================
# GPA VALIDATION
# ======================
def validate_gpa(gpa):
    if not isinstance(gpa, (int, float)):
        raise ValueError("GPA must be numeric")

    if not (security_rules.MIN_GPA <= gpa <= security_rules.MAX_GPA):
        raise ValueError("Invalid GPA range")

    return float(gpa)


# ======================
# CREDITS VALIDATION
# ======================
def validate_credits(credits):
    if not isinstance(credits, int):
        raise ValueError("Credits must be integer")

    if not (security_rules.MIN_CREDITS <= credits <= security_rules.MAX_CREDITS):
        raise ValueError("Invalid credits range")

    return credits


# ======================
# TIMESTAMP VALIDATION
# ======================
def validate_timestamp(ts: str) -> str:
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        raise ValueError("Invalid ISO 8601 timestamp")

    return ts


# ======================
# ALERT VALIDATION
# ======================
def validate_alert_level(level: str) -> str:
    if level not in security_rules.ALERT_LEVELS:
        raise ValueError("Invalid alert level")

    return level


# ======================
# OUTPUT VALIDATION (AGENT RESPONSE)
# ======================
def validate_agent_output(output: dict) -> dict:
    if not isinstance(output, dict):
        raise ValueError("Output must be dict")

    required = {"agent", "status", "result"}

    if not required.issubset(output.keys()):
        raise ValueError("Missing required output fields")

    return output
