from typing import List, Dict, Any


class ScholarshipMatchSkill:
    """
    Phase 5: Scholarship Ranking Engine
    - rule-based + weighted scoring
    - explainable output for MCP Agent
    """

    # =========================
    # PUBLIC API
    # =========================
    def rank(
        self,
        scholarships: List[Dict[str, Any]],
        student_profile: Dict[str, Any],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:

        results = []

        for s in scholarships:
            score, reasons = self._score(s, student_profile)

            if score > 0:
                results.append({
                    "scholarship_id": s["scholarship_id"],
                    "name": s["name"],
                    "provider": s["provider"],
                    "score": round(score, 4),
                    "reasons": reasons,
                    "award_amount": s["award_amount"],
                    "deadline": s["application_deadline"]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    # =========================
    # SCORING CORE
    # =========================
    def _score(self, s: Dict, student: Dict):

        score = 0.0
        reasons = []

        # -------------------
        # GPA (30%)
        # -------------------
        gpa = student.get("gpa", 0)
        if gpa >= s["minimum_gpa"]:
            g = 1.0
            reasons.append("GPA requirement satisfied")
        elif gpa >= s["minimum_gpa"] - 0.1:
            g = 0.7
            reasons.append("GPA slightly below threshold but acceptable")
        else:
            return 0.0, []

        score += g * 0.30

        # -------------------
        # MAJOR (25%)
        # -------------------
        major = student.get("major", "")
        if "All" in s["eligible_majors"] or major in s["eligible_majors"]:
            m = 1.0
            reasons.append("Major match")
        else:
            m = 0.0

        score += m * 0.25

        # -------------------
        # YEAR (15%)
        # -------------------
        year = student.get("year", "")
        if year in s["eligible_years"]:
            y = 1.0
            reasons.append("Year eligibility satisfied")
        else:
            y = 0.0

        score += y * 0.15

        # -------------------
        # CATEGORY / TAGS (20%)
        # -------------------
        interests = set(student.get("interests", []))
        tags = set(s.get("tags", []))

        overlap = len(interests.intersection(tags))

        if overlap >= 2:
            c = 1.0
            reasons.append("Strong interest alignment")
        elif overlap == 1:
            c = 0.5
            reasons.append("Partial interest alignment")
        else:
            c = 0.0

        score += c * 0.20

        # -------------------
        # LOCATION (10%)
        # -------------------
        loc = student.get("location", "USA")

        if "Global" in s["locations"] or loc in s["locations"]:
            l = 1.0
            reasons.append("Location eligible")
        else:
            l = 0.5  # soft penalty but not elimination

        score += l * 0.10

        return score, reasons
