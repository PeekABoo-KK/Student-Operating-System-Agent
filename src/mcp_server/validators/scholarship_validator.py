import json
from datetime import datetime

ALLOWED_CATEGORIES = {
    "merit", "need_based", "stem", "leadership",
    "research", "international", "diversity", "community_service"
}

class ScholarshipValidator:

    @staticmethod
    def validate_record(s: dict):

        required_fields = [
            "scholarship_id",
            "name",
            "provider",
            "description",
            "categories",
            "eligible_majors",
            "minimum_gpa",
            "eligible_years",
            "locations",
            "award_amount",
            "application_deadline",
            "tags",
            "eligibility_rules"
        ]

        for f in required_fields:
            if f not in s:
                raise ValueError(f"Missing field: {f}")

        # GPA validation
        if not (0.0 <= s["minimum_gpa"] <= 4.0):
            raise ValueError("Invalid GPA")

        # Category validation
        for c in s["categories"]:
            if c not in ALLOWED_CATEGORIES:
                raise ValueError(f"Invalid category: {c}")

        # Deadline validation
        deadline = datetime.fromisoformat(s["application_deadline"])
        if deadline < datetime.now():
            raise ValueError("Expired scholarship")

        # Award validation
        if s["award_amount"]["min"] > s["award_amount"]["max"]:
            raise ValueError("Invalid award range")

        return True

    @staticmethod
    def validate_dataset(dataset: list):
        valid = []
        for item in dataset:
            try:
                ScholarshipValidator.validate_record(item)
                valid.append(item)
            except Exception:
                continue
        return valid
