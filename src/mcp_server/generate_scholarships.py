import json
import random
from pathlib import Path
from datetime import datetime

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

MAJORS_PATH = DATA_DIR / "majors.json"
TAGS_PATH = DATA_DIR / "tags.json"
CATEGORIES_PATH = DATA_DIR / "categories.json"

SCHOLARSHIPS_PATH = DATA_DIR / "scholarships.json"
STATS_PATH = DATA_DIR / "dataset_stats.json"

# ==========================================================
# LOAD VOCABULARIES
# ==========================================================


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


MAJORS = load_json(MAJORS_PATH)["majors"]
TAGS = load_json(TAGS_PATH)["tags"]
CATEGORIES = load_json(CATEGORIES_PATH)["categories"]

# ==========================================================
# CONSTANTS
# ==========================================================

ADJECTIVES = [
    "Excellence",
    "Future",
    "Global",
    "Premier",
    "Rising",
    "Distinguished",
    "Outstanding",
    "Innovative",
    "Leadership",
    "Academic"
]

FIELDS = [
    "STEM",
    "Technology",
    "Research",
    "Leadership",
    "Business",
    "Engineering",
    "Community",
    "Science",
    "Innovation"
]

AWARD_TYPES = [
    "Scholarship",
    "Award",
    "Grant",
    "Fellowship"
]

PROVIDERS = [
    "National STEM Foundation",
    "Future Leaders Foundation",
    "Academic Excellence Institute",
    "Global Education Council",
    "Technology Advancement Association",
    "Innovation Scholarship Trust",
    "Premier Academic Society",
    "Research Excellence Council"
]

LOCATIONS = [
    "national",
    "regional",
    "state",
    "institutional",
    "international"
]

# ==========================================================
# HELPERS
# ==========================================================


def generate_id(index: int) -> str:
    return f"SCH-{index:06d}"


def generate_name() -> str:
    return (
        f"{random.choice(ADJECTIVES)} "
        f"{random.choice(FIELDS)} "
        f"{random.choice(AWARD_TYPES)}"
    )


def generate_amount() -> int:

    tier = random.random()

    if tier < 0.15:
        return random.randrange(250, 1000, 250)

    if tier < 0.45:
        return random.randrange(1000, 2500, 250)

    if tier < 0.75:
        return random.randrange(2500, 5000, 250)

    if tier < 0.93:
        return random.randrange(5000, 10000, 500)

    return random.randrange(10000, 50000, 1000)


def amount_display(amount: int) -> str:
    return f"${amount:,}"


def generate_min_gpa(category: str) -> float:

    ranges = {
        "merit": (3.0, 3.8),
        "need_based": (2.0, 3.0),
        "stem": (2.8, 3.5),
        "leadership": (2.5, 3.5),
        "research": (3.0, 3.7),
        "community_service": (2.5, 3.2),
        "diversity": (2.0, 3.5),
        "international": (2.8, 3.5),
    }

    low, high = ranges.get(category, (2.5, 3.5))

    return round(random.uniform(low, high), 1)


def generate_years():

    patterns = [
        [1],
        [1, 2],
        [2, 3],
        [3, 4],
        [4],
        [2, 3, 4],
        [1, 2, 3, 4]
    ]

    return random.choice(patterns)


def generate_tags(category, majors):

    result = {category}

    if "Computer Science" in majors:
        result.update([
            "computer-science",
            "stem",
            "technology"
        ])

    if "Data Science" in majors:
        result.update([
            "data-science",
            "stem"
        ])

    if category == "need_based":
        result.update([
            "need-based",
            "financial-aid"
        ])

    if category == "merit":
        result.update([
            "academic-excellence",
            "merit"
        ])

    if category == "research":
        result.update([
            "research",
            "undergraduate-research"
        ])

    valid_tags = [t for t in result if t in TAGS]

    return valid_tags[:6]


# ==========================================================
# RECORD GENERATION
# ==========================================================


def generate_record(index):

    category = random.choice(CATEGORIES)

    amount = generate_amount()

    majors = random.sample(
        MAJORS,
        k=min(3, len(MAJORS))
    )

    record = {
        "id": generate_id(index),
        "name": generate_name(),
        "provider": random.choice(PROVIDERS),
        "category": category,
        "amount": amount,
        "amount_display": amount_display(amount),
        "currency": "USD",
        "min_gpa": generate_min_gpa(category),
        "max_gpa": 4.0,
        "eligible_years": generate_years(),
        "eligible_majors": majors,
        "need_based": category == "need_based",
        "merit_only": category == "merit",
        "tags": [],
        "deadline_month": random.randint(1, 12),
        "deadline_day": random.randint(1, 28),
        "description": (
            f"A scholarship supporting students "
            f"in {category.replace('_', ' ')} programs."
        ),
        "renewable": random.choice([True, False]),
        "location": random.choice(LOCATIONS)
    }

    record["tags"] = generate_tags(
        category,
        record["eligible_majors"]
    )

    return record


# ==========================================================
# DATASET GENERATION
# ==========================================================


def generate_dataset(total=300):

    dataset = []

    for i in range(1, total + 1):
        dataset.append(generate_record(i))

    return dataset


# ==========================================================
# DEDUPLICATION
# ==========================================================


def deduplicate(records):

    seen = set()
    clean = []

    for record in records:

        key = (
            record["name"].lower(),
            record["provider"]
        )

        if key in seen:
            continue

        seen.add(key)
        clean.append(record)

    return clean


# ==========================================================
# STATS
# ==========================================================


def build_stats(records):

    categories = {}

    for r in records:

        c = r["category"]

        categories[c] = (
            categories.get(c, 0) + 1
        )

    return {
        "version": "1.0.0",
        "generated_at": datetime.utcnow().isoformat(),
        "total_records": len(records),
        "category_distribution": categories
    }


# ==========================================================
# WRITE FILES
# ==========================================================


def write_dataset(records):

    with open(
        SCHOLARSHIPS_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            records,
            f,
            indent=2,
            ensure_ascii=False
        )


def write_stats(stats):

    with open(
        STATS_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            stats,
            f,
            indent=2,
            ensure_ascii=False
        )


# ==========================================================
# MAIN
# ==========================================================


def main():

    raw_records = generate_dataset(300)

    clean_records = deduplicate(raw_records)

    stats = build_stats(clean_records)

    write_dataset(clean_records)

    write_stats(stats)

    print(
        f"Generated {len(clean_records)} scholarships"
    )

    print(
        f"Saved to {SCHOLARSHIPS_PATH}"
    )


if __name__ == "__main__":
    main()
