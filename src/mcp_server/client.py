from server import server


class ScholarshipMCPClient:
    def __init__(self):
        self.server = server

    def get_recommendations(self, student_profile: dict):
        """
        Bridge from Agent → MCP server
        """

        query = {
            "gpa": student_profile.get("gpa"),
            "major": student_profile.get("major"),
            "year": student_profile.get("year")
        }

        results = self.server.search_scholarships(query)

        return self._format_response(results)

    def _format_response(self, results):
        formatted = []

        for r in results:
            s = r["scholarship"]

            formatted.append({
                "id": s["scholarship_id"],
                "name": s["name"],
                "provider": s["provider"],
                "score": r["score"],
                "award": s["award_amount"],
                "deadline": s["application_deadline"],
                "reason": self._explain(s)
            })

        return formatted

    def _explain(self, s):
        reasons = []

        if s["minimum_gpa"] <= 3.0:
            reasons.append("GPA requirement accessible")

        if "Computer Science" in s["eligible_majors"]:
            reasons.append("Matches CS field")

        if s["category"] == "stem":
            reasons.append("STEM alignment")

        return reasons
