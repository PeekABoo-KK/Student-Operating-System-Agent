import json
import random
from typing import List, Dict
from datetime import datetime

from mcp_server.security.security_pipeline import SecurityPipeline
from mcp_server.security.schema import ScholarshipSchema


# =========================
# LOAD VOCAB
# =========================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


majors = load_json("mcp_server/data/majors.json")["majors"]
tags_vocab = load_json("mcp_server/data/tags.json")["tags"]
categories = load_json("mcp_server/data/categories.json")["categories"]


# =========================
# GENERATOR CORE
# =========================

ADJECTIVES = [
    "Excellence", "Future", "Rising", "Global", "National",
    "Innovative", "Academic", "Leadership", "Premier", "Distinguished"
]

AWARD_TYPES = ["Scholarship", "Grant", "Fellowship", "Award"]

PROVIDERS = [
    "National STEM Foundation",
    "Future Leaders Foundation",
    "Academic Excellence Institute",
    "Global Education Council",
    "Tech Innovation Association"
]


def generate_id(i):
    return f"SCH-{i:06d}"


def generate_name():
    return f"{random.choice(ADJECTIVES)} {random.choice(['STEM','Academic','Leadership','Research','Community'])} {random.choice(AWARD_TYPES)}"


def generate_amount():
    tier = random.random()

    if tier < 0.15:
        return random.randrange(250, 1000, 250)
    elif tier < 0.45:
        return random.randrange(1000, 2500, 250)
    elif tier < 0.75:
        return random.randrange(2500, 5000, 250)
    elif tier < 0.93:
        return random.randrange(5000, 10000, 500)
    else:
        return random.randrange(10000, 50000, 1000)


def format_amount(a):
    return f"${a:,}"


def generate_gpa(category):
    if category == "merit":
        return round(random.uniform(3.0, 3.8), 1)
    if category == "need_based":
        return round(random.uniform(2.0, 3.0), 1)
    if category == "stem":
        return round(random.uniform(2.8, 3.5), 1)
    if category == "leadership":
        return round(random.uniform(2.5, 3.5), 1)
    return round(random.uniform(2.5, 3.5), 1)


def generate_years():
    patterns = [
        [1],
        [1,2],
        [2,3],
        [3,4],
        [4],
        [1,2,3,4]
    ]
    return random.choice(patterns)


def generate_deadline():
    return random.randint(1,12), random.randint(1,28)


def generate_tags(category, major_list):
    tags = [category]

    if "Computer Science" in major_list:
        tags.append("computer-science")
        tags.append("stem")

    if category == "need_based":
        tags.append("financial-aid")

    if category == "merit":
        tags.append("academic-excellence")

    return list(set(tags))[:6]


# =========================
# MAIN GENERATION
# =========================

def generate_dataset(n=300):
    pipeline = SecurityPipeline()

    dataset = []

    pipeline.snapshot([])

    for i in range(1, n + 1):

        category = random.choice([
            "merit", "need_based", "stem",
            "leadership", "community_service",
            "research", "diversity", "international"
        ])

        amount = generate_amount()
        min_gpa = generate_gpa(category)

        record = {
            "id": generate_id(i),
            "name": generate_name(),
            "provider": random.choice(PROVIDERS),
            "category": category,
            "amount": amount,
            "amount_display": format_amount(amount),
            "currency": "USD",
            "min_gpa": min_gpa,
            "max_gpa": 4.0,
            "eligible_years": generate_years(),
            "eligible_majors": random.sample(majors, k=3),
            "need_based": category == "need_based",
            "merit_only": category == "merit",
            "tags": [],
            "deadline_month": random.randint(1,12),
            "deadline_day": random.randint(1,28),
            "description": f"A scholarship supporting {category} students in academic achievement.",
            "renewable": random.random() < 0.3,
            "location": "national"
        }

        record["tags"] = generate_tags(category, record["eligible_majors"])

        # =========================
        # SECURITY CHECK (LIGHT)
        # =========================

        try:
            ScholarshipSchema(**record)
        except Exception as e:
            print(f"[SCHEMA FAIL] {record['id']}: {e}")
            continue

        dataset.append(record)

    return dataset


# =========================
# DEDUP + QA
# =========================

def deduplicate(data: List[Dict]):
    seen = set()
    unique = []

    for r in data:
        key = (r["name"].lower(), r["provider"], r["amount"], r["category"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)

    return unique


def qa_check(data: List[Dict]):
    category_count = {}

    for r in data:
        c = r["category"]
        category_count[c] = category_count.get(c, 0) + 1

    print("\nQA REPORT")
    print("================")
    print("Total:", len(data))
    print("Category distribution:", category_count)


# =========================
# OUTPUT WRITER
# =========================

def write_output(data):
    with open("mcp_server/data/scholarships.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    stats = {
        "version": "v1.0.0",
        "generated_at": datetime.utcnow().isoformat(),
        "total_records": len(data)
    }

    with open("mcp_server/data/scholarships.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


# =========================
# RUN
# =========================

if __name__ == "__main__":

    raw = generate_dataset(300)

    clean = deduplicate(raw)

    qa_check(clean)

    write_output(clean)

    print("\nDONE: scholarships.json generated")
