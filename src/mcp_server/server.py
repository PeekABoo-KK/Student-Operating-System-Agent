import json
from pathlib import Path
from typing import List
from validators import validate_scholarship

DATA_PATH = Path(__file__).parent / "data" / "scholarships.json"


class ScholarshipMCPServer:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)

        valid = []
        for r in raw:
            ok, reason = validate_scholarship(r)
            if ok:
                valid.append(r)
            else:
                print(f"[REJECTED] {r.get('scholarship_id')} -> {reason}")

        print(f"[MCP SERVER] Loaded {len(valid)} valid scholarships")
        return valid

    # -------------------------
    # MCP TOOL: search
    # -------------------------
    def search_scholarships(self, query: dict):
        """
        query:
        {
          "gpa": float,
          "major": str,
          "year": str
        }
        """

        gpa = query.get("gpa", 0)
        major = query.get("major", "")
        year = query.get("year", "")

        results = []

        for s in self.data:

            # HARD FILTERS
            if gpa < s["minimum_gpa"]:
                continue

            if year and year not in s["eligible_years"]:
                continue

            if major and major not in s["eligible_majors"]:
                continue

            # SOFT SCORE (simple MVP scoring)
            score = 0.0

            # GPA score
            score += 0.3 if gpa >= s["minimum_gpa"] else 0

            # Major match
            score += 0.25 if major in s["eligible_majors"] else 0

            # Year match
            score += 0.15 if year in s["eligible_years"] else 0

            # Category boost
            if s["category"] == "stem" and major in ["Computer Science", "Data Science"]:
                score += 0.2

            results.append({
                "scholarship": s,
                "score": round(score, 3)
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:10]


# singleton
server = ScholarshipMCPServer()
