import json
from fastapi import FastAPI
from utils.memory_guard import MemoryGuard
from utils.io_validator import IOValidator
from validators.scholarship_validator import ScholarshipValidator

app = FastAPI()

memory = MemoryGuard()

# LOAD DATASET
with open("mcp_server/data/scholarships.json", "r", encoding="utf-8") as f:
    RAW_DATA = json.load(f)

DATASET = ScholarshipValidator.validate_dataset(RAW_DATA)


# =========================
# MCP TOOL: SEARCH
# =========================
@app.post("/search_scholarships")
def search_scholarships(profile: dict):

    IOValidator.validate_student_profile(profile)

    gpa = profile["gpa"]
    major = profile["major"]
    year = profile["year"]

    results = []

    for s in DATASET:

        # HARD FILTER
        if gpa < s["minimum_gpa"]:
            continue

        if year not in s["eligible_years"]:
            continue

        if major not in s["eligible_majors"] and "All" not in s["eligible_majors"]:
            continue

        results.append(s)

    memory.log_event({
        "event": "search",
        "input": profile,
        "results_count": len(results)
    })

    return {"results": results}


# =========================
# MCP TOOL: GET TOP K
# =========================
@app.post("/rank_scholarships")
def rank_scholarships(payload: dict):

    scholarships = payload["scholarships"]

    def score(s):
        return (
            s["minimum_gpa"] * -1 +
            len(s["categories"]) +
            len(s["tags"])
        )

    ranked = sorted(scholarships, key=score, reverse=True)

    return {
        "top_k": ranked[:10]
    }
