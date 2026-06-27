from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime, timezone

@dataclass
class ScholarshipPreferences:
    scholarship_categories: List[str]
    preferred_locations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert ScholarshipPreferences to a dictionary."""
        return {
            "scholarship_categories": self.scholarship_categories,
            "preferred_locations": self.preferred_locations
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScholarshipPreferences":
        """Create ScholarshipPreferences from a dictionary."""
        return cls(
            scholarship_categories=data.get("scholarship_categories", []),
            preferred_locations=data.get("preferred_locations", [])
        )

@dataclass
class StudentProfile:
    student_id: str
    name: str
    major: str
    year: int
    gpa: float
    target_gpa: float
    credits_completed: int
    target_graduation: str
    career_goal: str
    study_hours_per_week: int
    preferences: ScholarshipPreferences
    risk_baseline: str
    created_at: str
    updated_at: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert StudentProfile to a dictionary compatible with student_profile.json."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "major": self.major,
            "year": self.year,
            "gpa": self.gpa,
            "target_gpa": self.target_gpa,
            "credits_completed": self.credits_completed,
            "target_graduation": self.target_graduation,
            "career_goal": self.career_goal,
            "study_hours_per_week": self.study_hours_per_week,
            "preferences": self.preferences.to_dict(),
            "risk_baseline": self.risk_baseline,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StudentProfile":
        """Create StudentProfile from a dictionary."""
        pref_data = data.get("preferences", {})
        if isinstance(pref_data, ScholarshipPreferences):
            preferences = pref_data
        else:
            preferences = ScholarshipPreferences.from_dict(pref_data)

        # Enforce defaults for datetime string fields if missing
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        created_at = data.get("created_at") or now_iso
        updated_at = data.get("updated_at") or now_iso

        return cls(
            student_id=data["student_id"],
            name=data["name"],
            major=data["major"],
            year=int(data["year"]),
            gpa=float(data["gpa"]),
            target_gpa=float(data["target_gpa"]),
            credits_completed=int(data["credits_completed"]),
            target_graduation=data["target_graduation"],
            career_goal=data.get("career_goal", ""),
            study_hours_per_week=int(data["study_hours_per_week"]),
            preferences=preferences,
            risk_baseline=data.get("risk_baseline", "LOW"),
            created_at=created_at,
            updated_at=updated_at
        )
