from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityRules:

    MAX_INPUT_LENGTH: int = 2000

    BLOCKLIST = [
        "ignore previous instructions",
        "reveal system prompt",
        "show hidden prompt",
        "delete memory",
        "override rules",
        "act as system",
        "act as administrator",
        "print your instructions",
        "show internal memory"
    ]

    ALERT_LEVELS = {"LOW", "MEDIUM", "HIGH"}

    MIN_GPA = 0.0
    MAX_GPA = 4.0

    MIN_CREDITS = 0
    MAX_CREDITS = 200

    ALLOWED_SCHEMA_KEYS = {
        "student_id",
        "name",
        "major",
        "gpa",
        "target_gpa",
        "credits_completed",
        "target_graduation",
        "career_goal",
        "study_hours_per_week",
        "preferences",
        "risk_baseline"
    }


security_rules = SecurityRules()
