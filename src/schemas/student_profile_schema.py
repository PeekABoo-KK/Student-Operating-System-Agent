import re
from datetime import datetime
from typing import Dict, Any, List, Tuple

def is_valid_iso8601(timestamp_str: str) -> bool:
    """Check if a string is a valid ISO 8601 timestamp."""
    if not isinstance(timestamp_str, str):
        return False
    try:
        # replace 'Z' with timezone offset for fromisoformat compatibility in python versions
        datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def validate(data: Any) -> Tuple[bool, List[str]]:
    """Validate student profile dictionary against schema rules."""
    errors = []
    if not isinstance(data, dict):
        return False, ["Profile data must be a dictionary"]

    required_fields = {
        "student_id", "name", "major", "year", "gpa", "target_gpa",
        "credits_completed", "target_graduation", "career_goal",
        "study_hours_per_week", "preferences", "risk_baseline",
        "created_at", "updated_at"
    }

    # 1. Reject unknown fields
    for key in data.keys():
        if key not in required_fields:
            errors.append(f"Unknown field: {key}")

    # 2. Validate required fields presence
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # 3. Validate types and bounds
    # student_id
    student_id = data["student_id"]
    if not isinstance(student_id, str):
        errors.append("student_id must be a string")
    elif not (3 <= len(student_id) <= 50):
        errors.append("student_id length must be between 3 and 50 characters")

    # name
    name = data["name"]
    if not isinstance(name, str):
        errors.append("name must be a string")
    elif not (1 <= len(name) <= 100):
        errors.append("name length must be between 1 and 100 characters")

    # major
    major = data["major"]
    if not isinstance(major, str):
        errors.append("major must be a string")
    elif not (2 <= len(major) <= 100):
        errors.append("major length must be between 2 and 100 characters")
    else:
        if not re.match(r"^[a-zA-Z0-9\s\-]+$", major):
            errors.append("major must only contain alphanumeric characters, spaces, and hyphens")

    # year
    year = data["year"]
    if not isinstance(year, int) or isinstance(year, bool):
        errors.append("year must be an integer")
    elif not (1 <= year <= 8):
        errors.append("year must be between 1 and 8")

    # gpa
    gpa = data["gpa"]
    if not isinstance(gpa, (int, float)) or isinstance(gpa, bool):
        errors.append("gpa must be a number")
    elif not (0.0 <= gpa <= 4.0):
        errors.append("gpa must be between 0.0 and 4.0")

    # target_gpa
    target_gpa = data["target_gpa"]
    if not isinstance(target_gpa, (int, float)) or isinstance(target_gpa, bool):
        errors.append("target_gpa must be a number")
    elif not (0.0 <= target_gpa <= 4.0):
        errors.append("target_gpa must be between 0.0 and 4.0")

    # credits_completed
    credits = data["credits_completed"]
    if not isinstance(credits, int) or isinstance(credits, bool):
        errors.append("credits_completed must be an integer")
    elif not (0 <= credits <= 300):
        errors.append("credits_completed must be between 0 and 300")

    # target_graduation
    target_graduation = data["target_graduation"]
    if not isinstance(target_graduation, str):
        errors.append("target_graduation must be a string")

    # career_goal
    career_goal = data["career_goal"]
    if not isinstance(career_goal, str):
        errors.append("career_goal must be a string")
    elif len(career_goal) > 200:
        errors.append("career_goal length cannot exceed 200 characters")

    # study_hours_per_week
    study_hours = data["study_hours_per_week"]
    if not isinstance(study_hours, int) or isinstance(study_hours, bool):
        errors.append("study_hours_per_week must be an integer")
    elif not (0 <= study_hours <= 100):
        errors.append("study_hours_per_week must be between 0 and 100")

    # risk_baseline
    risk_baseline = data["risk_baseline"]
    if not isinstance(risk_baseline, str):
        errors.append("risk_baseline must be a string")
    elif risk_baseline not in {"LOW", "MEDIUM", "HIGH"}:
        errors.append("risk_baseline must be one of LOW, MEDIUM, HIGH")

    # created_at
    created_at = data["created_at"]
    if not is_valid_iso8601(created_at):
        errors.append(f"created_at must be a valid ISO 8601 timestamp: {created_at}")

    # updated_at
    updated_at = data["updated_at"]
    if not is_valid_iso8601(updated_at):
        errors.append(f"updated_at must be a valid ISO 8601 timestamp: {updated_at}")

    # preferences
    preferences = data["preferences"]
    if not isinstance(preferences, dict):
        errors.append("preferences must be a dictionary")
    else:
        pref_required = {"scholarship_categories", "preferred_locations"}
        for k in preferences.keys():
            if k not in pref_required:
                errors.append(f"Unknown key in preferences: {k}")
        for k in pref_required:
            if k not in preferences:
                errors.append(f"Missing key in preferences: {k}")

        if not errors:
            categories = preferences["scholarship_categories"]
            locations = preferences["preferred_locations"]

            if not isinstance(categories, list):
                errors.append("scholarship_categories must be a list")
            else:
                allowed_cats = {
                    "merit", "need_based", "stem", "international", "leadership", "research", "diversity", "community_service",
                    "STEM", "Women in Technology", "Women in STEM", "Women in Tech"
                }
                for cat in categories:
                    if not isinstance(cat, str):
                        errors.append("scholarship_categories items must be strings")
                        break
                    # allow case-insensitive match or exact match
                    if cat not in allowed_cats and cat.lower() not in allowed_cats:
                        errors.append(f"Invalid scholarship category: {cat}")

            if not isinstance(locations, list):
                errors.append("preferred_locations must be a list")
            else:
                for loc in locations:
                    if not isinstance(loc, str):
                        errors.append("preferred_locations items must be strings")
                        break

    return len(errors) == 0, errors
