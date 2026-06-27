import json
from datetime import timezone
from src.models.student_profile import StudentProfile


PROFILE_PATH = "memory/student_profile.json"


def load_student_profile() -> StudentProfile:
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return StudentProfile.model_validate(data)


def validate_student_profile():
    profile = load_student_profile()

    # enforce UTC check
    if profile.created_at.tzinfo != timezone.utc:
        raise ValueError("created_at must be UTC")

    if profile.updated_at.tzinfo != timezone.utc:
        raise ValueError("updated_at must be UTC")

    return profile
