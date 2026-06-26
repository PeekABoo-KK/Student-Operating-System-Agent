# Scholarship_Generator_Spec.md

**Project:** Student OS — Academic Co-Pilot  
**Document:** Scholarship Dataset Generation Specification  
**Version:** 1.0.0  
**Status:** FINAL & LOCKED  
**Consumer:** `mcp_server/server.py` → `Opportunity Scout Agent` → `scholarship_match_skill.py`  
**Output File:** `mcp_server/data/scholarships.json`

---

## Table of Contents

| # | Section | Description |
|---|---------|-------------|
| A | Dataset Purpose | Why this dataset exists and what it must not do |
| B | Dataset Architecture | Generation pipeline diagram |
| C | Controlled Vocabularies | Canonical value sets for all categorical fields |
| D | Scholarship Generation Rules | How each field is produced |
| E | Synthetic Dataset Distribution | Target proportions by category |
| F | Validation Pipeline | Schema, field, and vocabulary checks |
| G | Deduplication Rules | Exact and near-duplicate detection |
| H | Quality Assurance Framework | Completeness, consistency, distribution checks |
| I | Dataset Statistics | Required metrics at release |
| J | Dataset Versioning | Version format and update policy |
| K | Scout Agent Compatibility | How dataset supports agent operations |
| L | Generation Workflow | End-to-end generation process |
| M | Failure Handling | Per-failure-type detection and response |
| N | Implementation Mapping | Repository file mapping |
| O | Final Architect Review | Strengths, risks, tradeoffs, scalability |

---

## A. Dataset Purpose

### Purpose

`scholarships.json` is the static reference dataset that powers the Opportunity Scout Agent's scholarship discovery capability. It is the only data source the MCP tool `search_scholarships()` queries. The dataset must be rich enough to return meaningful, differentiated matches for any realistic student profile the system encounters during a live demo or judging session.

### Consumers

| Consumer | How It Uses the Dataset | Access Pattern |
|----------|------------------------|----------------|
| `mcp_server/server.py` | Loads entire dataset at subprocess startup into memory | Load-once at startup |
| `search_scholarships()` MCP tool | Filters in-memory records against query parameters (gpa, major, year, need_based) | Filter on every call |
| `scholarship_match_skill.py` | Receives filtered subset, applies scoring and ranking | Receives filtered list |
| `OpportunityScoutAgent` | Receives top-3 ranked matches with reasoning | Receives ranked result |
| `briefing_skill.py` | Uses scholarship names and deadlines in weekly briefing | Receives match summary |

### Scope

- Synthetic scholarship records designed to match realistic US university scholarship programs
- Covers GPA ranges 2.0–4.0, years 1–4 (freshman through senior), 20+ majors, need-based and merit categories
- Scalable from 80 records (MVP) to 10,000 records (production) without schema changes
- Self-contained: no external API calls, no database, no internet access required

### Non-Goals

The following are explicitly out of scope for this dataset and specification:

- Real scholarship data from live sources (no web scraping, no API feeds)
- Graduate-level scholarships (year = 5+ is excluded in MVP)
- International student-specific scholarships (location = "international" is a tag only)
- Resume, portfolio, or essay content generation
- Scholarship application tracking or submission
- Any runtime database — `scholarships.json` is read-only static data

---

## B. Dataset Architecture

### Pipeline

```
┌─────────────────────────────────────┐
│       Scholarship Generator         │
│                                     │
│  • Read controlled vocabularies     │
│  • Apply generation rules           │
│  • Apply distribution targets       │
│  • Produce raw records              │
└────────────────┬────────────────────┘
                 │  raw_scholarships[]
                 ▼
┌─────────────────────────────────────┐
│        Validation Pipeline          │
│                                     │
│  • Schema validation (Pydantic)     │
│  • Field validation (ranges, types) │
│  • Vocabulary validation            │
│  • Deadline validation              │
│  • Award amount validation          │
└────────────────┬────────────────────┘
                 │  valid_scholarships[]
                 ▼
┌─────────────────────────────────────┐
│        Deduplication Pass           │
│                                     │
│  • Exact duplicate detection        │
│  • Near-duplicate detection         │
│  • Provider duplication limits      │
└────────────────┬────────────────────┘
                 │  deduplicated_scholarships[]
                 ▼
┌─────────────────────────────────────┐
│       Quality Assurance             │
│                                     │
│  • Completeness checks              │
│  • Consistency checks               │
│  • Distribution checks              │
│  • Data integrity checks            │
│  • Random sampling review           │
└────────────────┬────────────────────┘
                 │  qa_approved_scholarships[]
                 ▼
┌─────────────────────────────────────┐
│        scholarships.json            │
│                                     │
│  mcp_server/data/scholarships.json  │
│  Versioned release artifact         │
└─────────────────────────────────────┘
```

### Component Responsibilities

| Component | Input | Output | Failure Behavior |
|-----------|-------|--------|-----------------|
| Scholarship Generator | Vocabularies + rules | Raw records array | Abort on vocabulary load failure |
| Validation Pipeline | Raw records | Valid records | Reject invalid, log, continue |
| Deduplication Pass | Valid records | Deduplicated records | Remove duplicate, log, continue |
| Quality Assurance | Deduplicated records | QA-approved records | Flag distribution failures, halt release |
| scholarships.json | QA-approved records | Final JSON file | Overwrite only on full QA pass |

### Record Schema (Locked)

Every scholarship record in `scholarships.json` must conform to this schema. **No additional fields may be added without a version bump.**

```json
{
  "id": "SCH-000001",
  "name": "STEM Excellence Scholarship",
  "provider": "National STEM Foundation",
  "category": "stem",
  "amount": 2500,
  "amount_display": "$2,500",
  "currency": "USD",
  "min_gpa": 3.0,
  "max_gpa": 4.0,
  "eligible_years": [2, 3, 4],
  "eligible_majors": ["Computer Science", "Software Engineering", "Data Science"],
  "need_based": false,
  "merit_only": true,
  "tags": ["stem", "technology", "merit"],
  "deadline_month": 3,
  "deadline_day": 15,
  "description": "Awarded to undergraduate students demonstrating excellence in STEM disciplines.",
  "renewable": false,
  "location": "national"
}
```

### Field Type Constraints

| Field | Type | Constraints |
|-------|------|------------|
| `id` | string | Format: `SCH-NNNNNN`. Unique. Auto-generated. |
| `name` | string | 10–120 chars. No HTML. No duplicates. |
| `provider` | string | 5–100 chars. Max 5 scholarships per provider. |
| `category` | string | Must be from Category vocabulary. Exactly one. |
| `amount` | integer | 250–50,000. In USD. |
| `amount_display` | string | Formatted: `$N,NNN`. Must match `amount`. |
| `currency` | string | Always `"USD"` in MVP. |
| `min_gpa` | float | 0.0–4.0. Must be ≤ `max_gpa`. |
| `max_gpa` | float | 0.0–4.0. Must be ≥ `min_gpa`. Typically 4.0. |
| `eligible_years` | array[int] | Subset of [1, 2, 3, 4]. Non-empty. |
| `eligible_majors` | array[string] | Each from Major vocabulary. Non-empty. Min 1 item. |
| `need_based` | boolean | Required. |
| `merit_only` | boolean | Required. Cannot both be `false`. |
| `tags` | array[string] | 2–6 tags. Each from Tag vocabulary. |
| `deadline_month` | integer | 1–12. |
| `deadline_day` | integer | 1–28 (safe for all months). |
| `description` | string | 20–300 chars. |
| `renewable` | boolean | Required. |
| `location` | string | From Location vocabulary. |

---

## C. Controlled Vocabularies

### C.1 Scholarship Categories

One category per scholarship. Categories are mutually exclusive at the record level (a scholarship has exactly one primary category). Tags may add secondary context.

| Category | Definition | Expected % of Dataset |
|----------|-----------|----------------------|
| `merit` | Academic excellence, GPA-based awards | 20% |
| `need_based` | Financial need demonstrated | 20% |
| `stem` | Science, Technology, Engineering, Mathematics | 18% |
| `leadership` | Student government, community leadership | 12% |
| `community_service` | Volunteer, nonprofit, civic engagement | 10% |
| `research` | Undergraduate research, lab participation | 8% |
| `diversity` | Underrepresented groups in academia | 7% |
| `international` | Study abroad, global engagement, international students | 5% |

**Governance rules:**
- Only these 8 values are accepted. Any other value fails vocabulary validation.
- Percentage distributions are targets with ±3% tolerance.
- No category may fall below 3% of total records.
- No category may exceed 25% of total records.

### C.2 Eligible Academic Years

| Value | Label | Notes |
|-------|-------|-------|
| `1` | Freshman | First year of undergraduate study |
| `2` | Sophomore | Second year |
| `3` | Junior | Third year |
| `4` | Senior | Fourth year / final undergraduate year |

**Governance rules:**
- Only integer values 1, 2, 3, 4 are accepted.
- Graduate year (5+) is out of scope for MVP.
- Every scholarship must specify at least one eligible year.
- At least 15% of scholarships must include year 1 (freshman-eligible).
- At least 20% of scholarships must be open to all years (eligible_years = [1, 2, 3, 4]).

### C.3 Locations

Location describes the geographic scope of the scholarship, not the student's location.

| Value | Description |
|-------|-------------|
| `national` | Available to students at any US university |
| `regional` | Available within a geographic US region |
| `state` | State-specific scholarship |
| `institutional` | University-specific (simulated) |
| `international` | Available for study abroad or international students |

**Location strategy:**
- 50% of records: `national` — ensures broad matching for demo profiles
- 25% of records: `state` — increases realistic specificity
- 15% of records: `institutional` — simulates university-based awards
- 7% of records: `regional` — northeast, southeast, midwest, west, southwest
- 3% of records: `international` — for profiles with international preferences

**Governance rules:**
- Location does not affect MCP filtering in MVP (search_scholarships does not filter by location).
- Location is returned in the result and used in eligibility reasoning text generated by Gemini.
- The `regional` value must be accompanied by a `region` tag (e.g., `northeast`, `midwest`).

### C.4 Tags

Tags provide secondary classification for display and future filtering. Each scholarship must have 2–6 tags.

**Required tag governance rules:**
- All tags must come from the canonical tag vocabulary below.
- Tags must be lowercase, hyphen-separated (e.g., `first-generation`, not `First Generation`).
- The primary category must always appear as a tag (e.g., category = `stem` → tag `stem` required).
- No tag may appear more than 4 times in a single record's tag list.
- Maximum 6 tags per record.

**Canonical tag vocabulary:**

| Tag Group | Tags |
|-----------|------|
| Academic | `merit`, `gpa`, `academic-excellence`, `honors`, `dean-list` |
| Financial | `need-based`, `financial-aid`, `low-income`, `first-generation` |
| Field | `stem`, `technology`, `engineering`, `computer-science`, `data-science`, `mathematics`, `physics`, `biology`, `chemistry` |
| Business | `business`, `finance`, `economics`, `entrepreneurship`, `management` |
| Liberal Arts | `humanities`, `arts`, `communication`, `psychology`, `sociology`, `education` |
| Health | `health-sciences`, `nursing`, `pre-med`, `public-health`, `pharmacy` |
| Service | `community-service`, `volunteer`, `nonprofit`, `civic` |
| Leadership | `leadership`, `student-government`, `extracurricular` |
| Research | `research`, `undergraduate-research`, `lab`, `publication` |
| Diversity | `diversity`, `underrepresented`, `women-in-stem`, `minority` |
| Geographic | `national`, `state`, `regional`, `northeast`, `midwest`, `southeast`, `west`, `southwest`, `international` |
| Renewal | `renewable`, `one-time` |

**Tag normalization rules:**
- Input tags are lowercased before storage.
- Spaces replaced with hyphens.
- Tags not in the canonical vocabulary are rejected during validation.
- Duplicate tags within a record are deduplicated silently.

**Tag expansion rules (auto-applied during generation):**
- `computer-science` → also add `stem` and `technology`
- `nursing` or `pre-med` → also add `health-sciences`
- `first-generation` → also add `need-based`
- `undergraduate-research` → also add `research`
- `women-in-stem` → also add `diversity` and `stem`

### C.5 Majors

The canonical major taxonomy. Every value in `eligible_majors` must come from this list.

**Technology & Computing:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Computer Science | CS | Yes |
| Software Engineering | SE | Yes |
| Data Science | DS | Yes |
| Information Systems | IS | Yes |
| Information Technology | IT | Yes |
| Cybersecurity | CYS | Yes |
| Artificial Intelligence | AI | Yes |
| Computer Engineering | CE | Yes |

**Engineering:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Electrical Engineering | EE | Yes |
| Mechanical Engineering | ME | Yes |
| Civil Engineering | CivE | Yes |
| Chemical Engineering | ChE | Yes |
| Biomedical Engineering | BME | Yes |
| Industrial Engineering | IE | Yes |

**Natural Sciences:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Mathematics | MATH | Yes |
| Statistics | STAT | Yes |
| Physics | PHYS | Yes |
| Biology | BIO | Yes |
| Chemistry | CHEM | Yes |
| Environmental Science | ENV | Yes |

**Business:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Business Administration | BUS | No |
| Finance | FIN | No |
| Accounting | ACCT | No |
| Marketing | MKT | No |
| Economics | ECON | No |
| Entrepreneurship | ENT | No |
| Management Information Systems | MIS | Partial |

**Health Sciences:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Nursing | NUR | Yes |
| Public Health | PH | Yes |
| Pre-Medicine | PREMED | Yes |
| Pharmacy | PHARM | Yes |
| Health Administration | HA | No |

**Liberal Arts & Social Sciences:**

| Major | Abbreviation | STEM |
|-------|-------------|------|
| Psychology | PSYC | No |
| Sociology | SOC | No |
| Communication | COMM | No |
| Education | EDU | No |
| Political Science | POLS | No |
| English | ENG | No |
| History | HIST | No |

**Governance rules:**
- Every `eligible_majors` entry must match exactly one of the above major names.
- Abbreviations are not stored in the dataset — use full major names.
- `eligible_majors: ["All"]` is not permitted. Specify actual majors or use a broad set covering 10+ majors for universal scholarships.
- For universal scholarships (not major-specific), list all 30+ majors explicitly.
- Majors are case-sensitive: `"Computer Science"` not `"computer science"`.

**Major coverage requirements:**
- Computer Science must appear in at least 15% of all scholarship records.
- Data Science must appear in at least 10%.
- Business Administration must appear in at least 10%.
- Every major in the taxonomy must appear in at least 2 scholarship records per 100 total records.

---

## D. Scholarship Generation Rules

### D.1 ID Generation

```
Format:    SCH-NNNNNN
Padding:   6 digits, zero-padded
Start:     SCH-000001
Sequence:  Auto-increment, never reuse
Example:   SCH-000001, SCH-000002, ..., SCH-010000
```

**Rules:**
- IDs are assigned sequentially during generation.
- IDs are never recycled, even after deduplication removes records.
- Final dataset IDs will not be sequential if records are removed during deduplication — this is acceptable.
- ID uniqueness is validated as part of schema validation.

### D.2 Name Generation

**Pattern:** `[Adjective] [Scope/Field] [Award Type]`

**Components:**

| Component | Examples |
|-----------|---------|
| Adjective | Excellence, Achievement, Merit, Leadership, Future, Rising, Distinguished, Outstanding, Premier, Innovative |
| Scope/Field | STEM, Academic, Technology, Research, Community, Diversity, Engineering, Business, Science, Leadership, Computer Science, Data Science |
| Award Type | Scholarship, Award, Fellowship, Grant, Prize |

**Examples:**
- `STEM Excellence Scholarship`
- `Future Technology Award`
- `Distinguished Academic Fellowship`
- `Community Leadership Grant`
- `Rising Diversity Scholarship`

**Rules:**
- Name must be 10–120 characters.
- No name may be an exact duplicate of another name in the dataset.
- Name must not contain provider name (names and providers are independently generated).
- No HTML, no special characters beyond commas and hyphens.
- Near-duplicate names (Levenshtein distance ≤ 5) are flagged for review.

### D.3 Provider Generation

**Pattern:** `[Organization Type] + [Descriptor]`

| Organization Type | Examples |
|------------------|---------|
| Foundation | National STEM Foundation, Future Leaders Foundation, Academic Excellence Foundation |
| Association | American Engineering Association, Technology Professionals Association |
| Corporation | TechCorp Education Initiative, InnovateCo Scholarship Fund |
| University | State University Alumni Fund, Regional University Endowment |
| Society | Society of Data Scientists, National Honor Society |
| Institute | Institute for Academic Achievement, Leadership Institute |
| Council | National Academic Council, STEM Education Council |

**Rules:**
- Maximum 5 scholarships per provider across the entire dataset.
- Provider names must be 5–100 characters.
- Provider names must sound realistic but must not match actual real-world organizations exactly (synthetic only).
- A minimum of 20 unique providers per 100 scholarship records.

### D.4 Award Amount Generation

**Distribution targets:**

| Tier | Amount Range | % of Dataset | Typical Category |
|------|-------------|-------------|-----------------|
| Micro | $250 – $999 | 15% | community_service, diversity |
| Small | $1,000 – $2,499 | 30% | merit, leadership |
| Medium | $2,500 – $4,999 | 30% | stem, research, need_based |
| Large | $5,000 – $9,999 | 18% | stem, need_based, merit |
| Major | $10,000 – $50,000 | 7% | need_based, research, merit |

**Rules:**
- `amount` is always an integer (no cents).
- `amount_display` must exactly match `amount` formatted as `$N,NNN` or `$NN,NNN`.
- Amounts must be round numbers: multiples of $250 for amounts under $5,000; multiples of $500 for $5,000–$9,999; multiples of $1,000 for $10,000+.
- Need-based scholarships may have higher average amounts than merit scholarships.

### D.5 Deadline Generation

Deadlines represent the annual application deadline. They are stored as `deadline_month` (1–12) and `deadline_day` (1–28).

**Distribution targets:**

| Season | Months | % of Dataset | Rationale |
|--------|--------|-------------|-----------|
| Early Spring | January–February | 25% | Common scholarship cycle |
| Spring | March–April | 35% | Peak application season |
| Summer | May–June | 15% | Summer program deadlines |
| Fall | September–October | 15% | Fall cycle scholarships |
| Winter | November–December | 10% | Early application scholarships |

**Rules:**
- `deadline_day` is capped at 28 to avoid month-length validation issues (February compatibility).
- Deadlines are recurring annual dates — no year component stored.
- At least 30% of scholarships must have deadlines in March or April (spring peak).
- No more than 40% of scholarships may share the same `deadline_month`.

### D.6 Eligibility Generation

**GPA thresholds by category:**

| Category | min_gpa Range | Notes |
|----------|-------------|-------|
| merit | 3.0 – 3.8 | High GPA required |
| stem | 2.8 – 3.5 | Technical focus, moderate GPA |
| research | 3.0 – 3.7 | Research aptitude implied |
| leadership | 2.5 – 3.5 | Leadership over academics |
| need_based | 2.0 – 3.0 | Financial need primary; GPA secondary |
| community_service | 2.5 – 3.2 | Service over academics |
| diversity | 2.0 – 3.5 | Wide range to maximize access |
| international | 2.8 – 3.5 | Moderate academic requirement |

**Rules:**
- `min_gpa` must be ≤ `max_gpa`.
- `max_gpa` is always 4.0 (no upper cap exclusions in MVP).
- GPA thresholds must use values with one decimal place (e.g., 3.0, 3.2, 3.5 — not 3.14).
- At least 20% of scholarships must have `min_gpa` ≤ 2.5 (accessible to at-risk students — critical for demo coverage).
- No more than 30% of scholarships may have `min_gpa` ≥ 3.5.

**Year eligibility distribution:**

| Year Pattern | Description | Target % |
|-------------|-------------|---------|
| `[1, 2, 3, 4]` | Open to all years | 20% |
| `[1]` | Freshman only | 8% |
| `[1, 2]` | Early undergraduate | 10% |
| `[2, 3]` | Mid undergraduate | 15% |
| `[3, 4]` | Upper undergraduate | 20% |
| `[4]` | Senior only | 10% |
| `[2, 3, 4]` | Sophomore through senior | 17% |

### D.7 Tag Generation

**Auto-generation process:**

```
1. Start with category as first tag
2. Add 1-3 field-specific tags based on eligible_majors
3. Add financial tags (need-based / merit-only) based on flags
4. Add location tag
5. Apply expansion rules (see Section C.4)
6. Deduplicate tags
7. Trim to max 6 tags
```

**Minimum tag requirements per category:**

| Category | Required Tags |
|----------|-------------|
| stem | `stem` + at least one of: `technology`, `engineering`, `computer-science`, `data-science` |
| need_based | `need-based` + `financial-aid` |
| merit | `merit` + `academic-excellence` |
| research | `research` + `undergraduate-research` |
| leadership | `leadership` |
| community_service | `community-service` + `volunteer` |
| diversity | `diversity` + `underrepresented` |
| international | `international` |

---

## E. Synthetic Dataset Distribution

### E.1 Category Distribution

| Category | 80 Records (MVP) | 300 Records | 500 Records | 1,000 Records | 10,000 Records |
|----------|-----------------|-------------|-------------|---------------|----------------|
| merit | 16 (20%) | 60 (20%) | 100 (20%) | 200 (20%) | 2,000 (20%) |
| need_based | 16 (20%) | 60 (20%) | 100 (20%) | 200 (20%) | 2,000 (20%) |
| stem | 14 (18%) | 54 (18%) | 90 (18%) | 180 (18%) | 1,800 (18%) |
| leadership | 10 (12%) | 36 (12%) | 60 (12%) | 120 (12%) | 1,200 (12%) |
| community_service | 8 (10%) | 30 (10%) | 50 (10%) | 100 (10%) | 1,000 (10%) |
| research | 6 (8%) | 24 (8%) | 40 (8%) | 80 (8%) | 800 (8%) |
| diversity | 6 (7%) | 21 (7%) | 35 (7%) | 70 (7%) | 700 (7%) |
| international | 4 (5%) | 15 (5%) | 25 (5%) | 50 (5%) | 500 (5%) |

**Tolerance:** ±3% for datasets ≥ 300 records. ±5% for 80-record MVP dataset.

### E.2 GPA Threshold Distribution

| min_gpa Range | Target % | Notes |
|---------------|---------|-------|
| 2.0 – 2.4 | 10% | At-risk students — critical for demo risk alert matching |
| 2.5 – 2.9 | 20% | Below-average students |
| 3.0 – 3.2 | 30% | Average students |
| 3.3 – 3.5 | 25% | Good students |
| 3.6 – 3.9 | 15% | High achievers |

### E.3 Year Distribution (by record, not scholarship)

| Year Pattern | Target % |
|-------------|---------|
| Includes year 1 (freshman) | ≥ 25% |
| Includes year 2 (sophomore) | ≥ 45% |
| Includes year 3 (junior) | ≥ 50% |
| Includes year 4 (senior) | ≥ 40% |
| Open to all 4 years | ≥ 20% |

### E.4 Amount Distribution

| Amount Tier | Target % |
|------------|---------|
| Micro ($250 – $999) | 15% |
| Small ($1,000 – $2,499) | 30% |
| Medium ($2,500 – $4,999) | 30% |
| Large ($5,000 – $9,999) | 18% |
| Major ($10,000 – $50,000) | 7% |

### E.5 Renewal Distribution

| Renewable | Target % |
|-----------|---------|
| `true` | 30% |
| `false` | 70% |

---

## F. Validation Pipeline

### F.1 Schema Validation

Every record is validated against the locked schema using Pydantic v2 before any further processing.

| Check | Pass Criteria | Fail Action |
|-------|-------------|------------|
| All required fields present | All 18 fields present | Reject record, log missing fields |
| Field types correct | Types match schema definitions | Reject record, log type error |
| No extra fields | Only schema fields present | Reject record, log unexpected field |
| JSON parseable | Valid JSON structure | Reject record, log parse error |

### F.2 Field Validation

| Field | Validation Rule | Pass | Fail Action |
|-------|----------------|------|------------|
| `id` | Matches `SCH-\d{6}` regex | Pass | Reject |
| `id` | Unique across dataset | Pass | Reject duplicate, log |
| `name` | 10–120 chars | Pass | Reject |
| `name` | No HTML tags | Pass | Strip and re-validate |
| `provider` | 5–100 chars | Pass | Reject |
| `amount` | Integer 250–50,000 | Pass | Reject |
| `amount_display` | Matches formatted `amount` | Pass | Auto-correct or reject |
| `min_gpa` | Float 0.0–4.0, 1 decimal place | Pass | Reject |
| `max_gpa` | Float 0.0–4.0, ≥ min_gpa | Pass | Reject |
| `eligible_years` | Non-empty, values in [1,2,3,4] | Pass | Reject |
| `eligible_majors` | Non-empty, all from Major vocabulary | Pass | Reject |
| `tags` | 2–6 items, all from Tag vocabulary | Pass | Reject |
| `deadline_month` | Integer 1–12 | Pass | Reject |
| `deadline_day` | Integer 1–28 | Pass | Reject |
| `description` | 20–300 chars | Pass | Reject |
| `need_based` | Boolean | Pass | Reject |
| `merit_only` | Boolean | Pass | Reject |
| `need_based` OR `merit_only` = true | At least one true | Pass | Reject (ambiguous record) |
| `renewable` | Boolean | Pass | Reject |
| `location` | From Location vocabulary | Pass | Reject |

### F.3 Vocabulary Validation

| Vocabulary | Checked Against | Failure Action |
|-----------|----------------|---------------|
| `category` | Section C.1 canonical list | Reject record |
| `eligible_years` values | [1, 2, 3, 4] only | Reject record |
| `eligible_majors` values | Section C.5 canonical list | Reject record |
| `tags` values | Section C.4 canonical tag vocabulary | Reject record |
| `location` | Section C.3 canonical list | Reject record |
| `currency` | `"USD"` only (MVP) | Reject record |

### F.4 Deadline Validation

| Check | Rule | Action on Failure |
|-------|------|------------------|
| Month range | 1 ≤ deadline_month ≤ 12 | Reject |
| Day range | 1 ≤ deadline_day ≤ 28 | Reject |
| Combined validity | (month, day) forms a valid calendar date | Reject |
| Distribution check | No month > 40% of total | Flag for distribution review |

### F.5 Award Validation

| Check | Rule | Action on Failure |
|-------|------|------------------|
| Amount range | 250 ≤ amount ≤ 50,000 | Reject |
| Amount roundness | Divisible by 250 (< $5K) or 500 ($5K–$9,999) or 1000 ($10K+) | Flag, auto-correct to nearest valid |
| Display match | amount_display == f"${amount:,}" | Auto-correct amount_display |

### F.6 Eligibility Validation

| Check | Rule | Action on Failure |
|-------|------|------------------|
| GPA logic | min_gpa ≤ max_gpa | Reject |
| GPA range | Both values in [0.0, 4.0] | Reject |
| Year list | Non-empty list | Reject |
| Major list | Non-empty list, all canonical | Reject |
| Consistency | need_based=true with min_gpa ≤ 3.0 | Warn (not reject) |

### F.7 Validation Summary Report

After running the validation pipeline, generate a report with:

```
Validation Summary
==================
Total records processed:     N
Records passed validation:   N (N%)
Records rejected:            N (N%)

Rejection Reasons:
  Schema failures:           N
  Field validation failures: N
  Vocabulary failures:       N
  Deadline failures:         N
  Award failures:            N
  Eligibility failures:      N
  Duplicate IDs:             N
```

---

## G. Deduplication Rules

### G.1 Exact Duplicate Detection

A record is an exact duplicate if all of the following fields match another record:

- `name` (case-insensitive)
- `provider`
- `amount`
- `category`

**Action:** Keep the record with the lower ID (earlier in generation order). Reject and log the duplicate.

### G.2 Near-Duplicate Detection

A record is a near-duplicate if:

- `name` Levenshtein distance ≤ 5 from any other record's name **AND**
- `provider` is identical to another record **AND**
- `amount` is identical to another record

**Action:** Flag for human review. Do not auto-reject. Log the pair. In automated generation, treat as reject and regenerate with different name components.

### G.3 Provider Duplication Rules

| Rule | Limit | Action on Violation |
|------|-------|-------------------|
| Max scholarships per provider | 5 per 100 records | Reject additional records from that provider |
| Min unique providers | 20 per 100 records | Regenerate until met |
| Same provider + same category | Max 2 per 100 records | Reject additional |

### G.4 Name Similarity Rules

| Similarity Condition | Detection Method | Action |
|---------------------|-----------------|--------|
| Identical name | Exact string match (case-insensitive) | Reject |
| Near-identical name | Levenshtein distance ≤ 5 | Flag for review |
| Same 3+ word sequence | N-gram comparison | Flag for review |

---

## H. Quality Assurance Framework

### H.1 Completeness Checks

| Check | Requirement | Target |
|-------|------------|--------|
| All required fields populated | 100% of records | No missing fields permitted |
| Description non-empty and meaningful | 100% of records | Min 20 chars |
| Tags populated | 100% of records | Min 2 tags per record |
| Major coverage | Every canonical major appears in dataset | ≥ 2 records per major per 100 total records |

### H.2 Consistency Checks

| Check | Rule |
|-------|------|
| Category-tag alignment | Category must appear as a tag |
| Amount-display alignment | amount_display must exactly match amount |
| need_based flag with GPA | need_based=true records should trend toward lower min_gpa |
| STEM category with STEM majors | stem category records must list ≥ 1 STEM major |
| merit_only with higher GPA | merit_only=true records should trend toward higher min_gpa |

### H.3 Distribution Checks

Run after deduplication. Compare actual distribution to targets in Section E.

| Distribution | Target | Tolerance | Action on Failure |
|-------------|--------|-----------|------------------|
| Category distribution | Section E.1 | ±3% (±5% for MVP) | Regenerate deficit categories |
| GPA threshold distribution | Section E.2 | ±5% | Regenerate to fill gaps |
| Year distribution | Section E.3 | ±5% | Regenerate to fill gaps |
| Amount distribution | Section E.4 | ±5% | Regenerate to fill gaps |
| Provider diversity | ≥ 20 unique providers per 100 records | Hard minimum | Fail QA |

### H.4 Data Integrity Checks

| Check | Method |
|-------|--------|
| ID uniqueness | Assert no two records share an ID |
| Name uniqueness | Assert no two records share a name (case-insensitive) |
| JSON structure validity | Re-parse entire file after generation |
| File encoding | Assert UTF-8, no BOM |
| Schema compliance | Re-run Pydantic validation on final file |

### H.5 Random Sampling Review

For datasets ≥ 300 records: manually inspect a random sample of 10 records before release.

Checklist per sampled record:
- [ ] Name sounds like a realistic scholarship name
- [ ] Provider sounds like a realistic organization
- [ ] Description is coherent and matches category
- [ ] Amount is plausible for the category
- [ ] GPA threshold is plausible for the category
- [ ] Eligible majors are appropriate for category
- [ ] Tags accurately reflect the scholarship content

**Pass criteria:** All 7 checklist items pass for all 10 sampled records. If any record fails ≥ 2 items, fail QA and review generation rules.

---

## I. Dataset Statistics

The following statistics must be computed and stored in `mcp_server/data/dataset_stats.json` alongside `scholarships.json` at each release.

```json
{
  "version": "v1.0.0",
  "generated_at": "2025-01-15T00:00:00Z",
  "total_records": 300,
  "category_counts": {
    "merit": 60,
    "need_based": 60,
    "stem": 54,
    "leadership": 36,
    "community_service": 30,
    "research": 24,
    "diversity": 21,
    "international": 15
  },
  "major_coverage": {
    "Computer Science": 48,
    "Data Science": 35,
    "Business Administration": 40
  },
  "location_coverage": {
    "national": 150,
    "state": 75,
    "institutional": 45,
    "regional": 21,
    "international": 9
  },
  "award_distribution": {
    "min": 250,
    "max": 25000,
    "mean": 3200,
    "median": 2500,
    "micro_count": 45,
    "small_count": 90,
    "medium_count": 90,
    "large_count": 54,
    "major_count": 21
  },
  "deadline_distribution": {
    "jan": 18, "feb": 22, "mar": 45, "apr": 60,
    "may": 25, "jun": 20, "jul": 0, "aug": 0,
    "sep": 30, "oct": 25, "nov": 30, "dec": 25
  },
  "gpa_threshold_distribution": {
    "2.0_2.4": 30,
    "2.5_2.9": 60,
    "3.0_3.2": 90,
    "3.3_3.5": 75,
    "3.6_3.9": 45
  },
  "renewable_count": 90,
  "need_based_count": 90,
  "merit_only_count": 150,
  "unique_providers": 68,
  "validation_passed": 300,
  "validation_rejected": 12,
  "deduplication_removed": 3
}
```

---

## J. Dataset Versioning

### J.1 Version Format

```
vMAJOR.MINOR.PATCH

Examples:
  v1.0.0  — Initial MVP release (80 records)
  v1.1.0  — Expanded to 300 records, no schema changes
  v1.2.0  — Added new providers and majors
  v2.0.0  — Schema change (requires MCP server update)
```

| Version Segment | When to Increment |
|----------------|------------------|
| MAJOR | Schema changes (new required fields, removed fields, type changes) |
| MINOR | Record count changes, vocabulary additions, distribution adjustments |
| PATCH | Bug fixes (corrected amounts, fixed validation errors, deduplicated records) |

### J.2 Update Policy

| Update Type | Policy |
|------------|--------|
| Adding records | MINOR version bump. No schema changes. No code changes required. |
| Modifying existing records | PATCH version bump if fixing errors. MINOR if changing values. |
| Adding vocabulary terms | MINOR version bump. Update vocabulary files. |
| Removing vocabulary terms | MAJOR version bump. Audit affected records first. |
| Schema field additions | MAJOR version bump. Requires MCP server update. |

### J.3 Change Log Policy

Every version must include a `CHANGELOG.md` entry:

```markdown
## v1.1.0 — 2025-01-20

### Added
- Expanded dataset from 80 to 300 records
- Added 15 new providers
- Added `Cybersecurity` major to vocabulary

### Changed
- Adjusted merit category distribution from 22% to 20%

### Fixed
- Corrected amount_display for 3 records where value did not match amount

### Records
- Total: 300
- Added: 223
- Modified: 3
- Removed: 0
```

### J.4 Backward Compatibility Rules

| Rule |
|------|
| `scholarships.json` schema is backward-compatible within the same MAJOR version |
| `mcp_server/server.py` does not need updates for MINOR and PATCH version bumps |
| `scholarship_match_skill.py` does not need updates for MINOR and PATCH version bumps |
| Vocabulary files (`majors.json`, `tags.json`, `categories.json`) can be expanded in MINOR versions |
| MAJOR version bumps require full regression test of the MCP tool and skill |

---

## K. Scout Agent Compatibility

### K.1 Eligibility Filtering

The MCP tool `search_scholarships(gpa, major, year, need_based)` applies these filters against the dataset:

| Parameter | Filter Logic |
|-----------|-------------|
| `gpa` | Return records where `min_gpa ≤ gpa ≤ max_gpa`. If `gpa=None`, skip GPA filter. |
| `major` | Return records where `major in eligible_majors`. If `major=None`, skip major filter. |
| `year` | Return records where `year in eligible_years`. If `year=None`, skip year filter. |
| `need_based` | If `need_based=True`, filter to `need_based=True` records only. If `False` or `None`, return all. |

**Dataset coverage requirement:** For any valid student profile (GPA 2.0–4.0, year 1–4, any canonical major), the MCP filter must return at least 3 records. The dataset distribution is designed to guarantee this.

**Demo profile compatibility:** The two demo profiles defined in the Implementation Blueprint must each return ≥ 3 scholarship matches:

| Demo Profile | Expected Minimum Matches |
|-------------|------------------------|
| Aisha: GPA 2.9, Pre-med, Year 2, need_based=true | ≥ 5 matches |
| Safe profile: GPA 3.9, CS, Year 2, need_based=false | ≥ 8 matches |

### K.2 Match Scoring

The `scholarship_match_skill.py` applies this scoring formula to filtered results:

```
score = 0.0
if student.gpa >= scholarship.min_gpa:          score += 0.40
if student.year in scholarship.eligible_years:  score += 0.30
if student.major in scholarship.eligible_majors: score += 0.20
if preferences.need_based == scholarship.need_based: score += 0.10
```

**Dataset design for scoring:** Records are designed so that different profiles produce meaningfully differentiated scores. A student with a 3.8 GPA, CS major, year 2, not need-based should receive different top-3 matches than a student with 2.8 GPA, Nursing, year 1, need-based.

### K.3 Explainability

Gemini generates an eligibility reasoning string per match. The dataset fields that feed into reasoning are:

| Field | Used in Reasoning? | Example Reasoning Fragment |
|-------|-------------------|--------------------------|
| `name` | Yes | "The STEM Excellence Scholarship..." |
| `min_gpa` | Yes | "Your GPA of 3.4 meets the 3.0 minimum." |
| `category` | Yes | "This need-based award matches your financial preference." |
| `eligible_years` | Yes | "Sophomore students are eligible." |
| `eligible_majors` | Yes | "Computer Science is an eligible major." |
| `amount_display` | Yes | "Award value is $2,500." |
| `description` | Yes | Used as context for reasoning |
| `deadline_month` | Yes | "Deadline is March 15th." |
| `renewable` | Yes | "This award is renewable annually." |

**Specification requirement:** Every record's `description` field must be a complete sentence that Gemini can incorporate into reasoning without hallucinating facts. Vague descriptions like "A great scholarship" are invalid.

### K.4 Weekly Briefings

The `briefing_skill.py` uses scholarship match results to populate the Opportunity Summary section of the weekly briefing. Requirements:

- At least 1 scholarship match must have a deadline within the next 60 days (calculated as current month relative to `deadline_month`)
- Match `name` and `amount_display` must be concise enough to fit in a briefing bullet point
- Match `deadline_month` must be stored as an integer for date arithmetic

---

## L. Generation Workflow

### L.1 End-to-End Workflow

```
Step 1: Load Controlled Vocabularies
         ↓
         Load: categories, years, locations, tags, majors
         Validate: all vocabulary files present and parseable
         Fail fast: missing vocabulary = abort generation

Step 2: Calculate Target Counts
         ↓
         Input: desired total_records (80 | 300 | 500 | 1000 | 10000)
         Compute: per-category targets using Section E.1 distribution
         Compute: per-GPA-tier targets using Section E.2 distribution
         Output: generation_plan dict

Step 3: Generate Raw Records
         ↓
         For each category in generation_plan:
           For each target record in category:
             Generate ID (auto-increment)
             Generate name (adjective + scope + award type)
             Generate provider (type + descriptor)
             Generate amount (tier-based)
             Generate GPA thresholds (category-based ranges)
             Generate eligible_years (distribution-based)
             Generate eligible_majors (category-appropriate)
             Generate tags (auto-generate from category + majors)
             Generate deadline (distribution-based)
             Generate description (template-based)
             Set need_based, merit_only, renewable, location
           End for
         End for
         Output: raw_records[]

Step 4: Validate Records
         ↓
         Run: Schema Validation (Section F.1)
         Run: Field Validation (Section F.2)
         Run: Vocabulary Validation (Section F.3)
         Run: Deadline Validation (Section F.4)
         Run: Award Validation (Section F.5)
         Run: Eligibility Validation (Section F.6)
         Output: valid_records[], rejected_records[]
         Log: validation_summary_report

Step 5: Deduplicate Records
         ↓
         Run: Exact Duplicate Detection (Section G.1)
         Run: Near-Duplicate Detection (Section G.2)
         Run: Provider Duplication Check (Section G.3)
         Output: deduplicated_records[]
         Log: deduplication_report

Step 6: Quality Assurance
         ↓
         Run: Completeness Checks (Section H.1)
         Run: Consistency Checks (Section H.2)
         Run: Distribution Checks (Section H.3)
         Run: Data Integrity Checks (Section H.4)
         Run: Random Sampling Review (Section H.5)
         Decision: PASS → proceed to Step 7
                   FAIL → regenerate deficit categories → restart from Step 3

Step 7: Compute Dataset Statistics
         ↓
         Compute all metrics defined in Section I
         Write: mcp_server/data/dataset_stats.json

Step 8: Version Release
         ↓
         Assign version number per Section J.1
         Write: mcp_server/data/scholarships.json
         Update: CHANGELOG.md
         Commit: version tag to repository
         Output: RELEASE_COMPLETE
```

### L.2 Regeneration Policy

If QA fails (Step 6), the regeneration strategy is targeted, not full rebuild:

1. Identify which categories are under-represented.
2. Generate additional records for only those categories.
3. Re-run Steps 4–6 on the new records only.
4. Merge into existing valid set.
5. Re-run distribution checks on full merged set.
6. If ≥ 3 regeneration cycles fail, escalate to manual review of generation rules.

---

## M. Failure Handling

| Failure Type | Detection | Response | Logging |
|-------------|-----------|----------|---------|
| Invalid scholarship record (schema) | Pydantic ValidationError | Reject record. Do not include in output. | Log: `REJECTED [SCH-ID] reason: schema_failure field=X` |
| Missing required field | Field presence check | Reject record. | Log: `REJECTED [SCH-ID] reason: missing_field field=X` |
| Invalid GPA (min > max) | Eligibility validation | Reject record. | Log: `REJECTED [SCH-ID] reason: invalid_gpa min=X max=Y` |
| Invalid deadline (day > 28) | Deadline validation | Reject record. | Log: `REJECTED [SCH-ID] reason: invalid_deadline day=X` |
| Duplicate record (exact) | Duplicate detection | Remove later record (higher ID). Keep earlier. | Log: `DUPLICATE REMOVED [SCH-ID] conflicts_with=[SCH-ID]` |
| Near-duplicate record | Near-duplicate detection | Flag for review. Reject in automated mode. | Log: `NEAR_DUPLICATE FLAGGED [SCH-ID] similar_to=[SCH-ID] distance=N` |
| Vocabulary violation | Vocabulary check | Reject record. | Log: `REJECTED [SCH-ID] reason: vocab_violation field=X value=Y` |
| Provider limit exceeded | Provider deduplication check | Reject additional records from that provider. | Log: `REJECTED [SCH-ID] reason: provider_limit provider=X count=N` |
| Distribution failure | QA distribution check | Regenerate deficit categories. | Log: `QA_FAIL category=X actual=N% target=N% delta=N%` |
| JSON file unreadable on MCP startup | Try/except in server.py | Log error. MCP tool returns empty list. Scout Agent returns status='empty'. | Log: `CRITICAL mcp_server scholarships.json unreadable: {error}` |
| Empty filtered result | MCP tool returns [] | Scout Agent returns ScholarshipMatchResult(status='empty'). UI shows 'No matching scholarships'. | Orchestrator logs: `WARN scout_empty_result profile=...` |

---

## N. Implementation Mapping

### N.1 Repository Files

| File | Purpose | Contents |
|------|---------|---------|
| `mcp_server/data/scholarships.json` | Primary scholarship dataset | Array of scholarship records (schema in Section B) |
| `mcp_server/data/dataset_stats.json` | Dataset statistics and metadata | Stats structure from Section I |
| `mcp_server/data/majors.json` | Canonical major vocabulary | Array of major name strings |
| `mcp_server/data/tags.json` | Canonical tag vocabulary | Array of tag strings |
| `mcp_server/data/categories.json` | Canonical category vocabulary | Array of category strings with metadata |

### N.2 File Formats

**`majors.json`:**
```json
{
  "version": "v1.0.0",
  "majors": [
    "Computer Science",
    "Software Engineering",
    "Data Science",
    "Information Systems",
    "Business Administration"
  ]
}
```

**`tags.json`:**
```json
{
  "version": "v1.0.0",
  "tags": [
    "merit", "gpa", "academic-excellence",
    "need-based", "financial-aid",
    "stem", "technology", "engineering"
  ]
}
```

**`categories.json`:**
```json
{
  "version": "v1.0.0",
  "categories": [
    {"value": "merit", "label": "Merit-Based", "target_pct": 0.20},
    {"value": "need_based", "label": "Need-Based", "target_pct": 0.20},
    {"value": "stem", "label": "STEM", "target_pct": 0.18}
  ]
}
```

### N.3 MCP Server Integration

The `mcp_server/server.py` loads vocabulary files at startup alongside `scholarships.json`. No changes to the MCP server's tool interface are required by this specification. The `search_scholarships(gpa, major, year, need_based)` tool signature is unchanged.

**Load sequence in server.py:**
```python
# At startup — load once, serve many calls
scholarships = load_json("mcp_server/data/scholarships.json")
# Vocabulary files are for generation only — not loaded at runtime
```

### N.4 Generator Script Location

The scholarship generation script is a **development-time tool only** — not part of the runtime system:

```
student_os/
└── scripts/                    ← development tools, not in runtime path
    └── generate_scholarships.py  ← runs once to produce scholarships.json
```

`generate_scholarships.py` is not imported by any runtime component. It is run manually by the developer to produce `scholarships.json`, which is then committed to the repository. The generation script does not need to be present in the deployed system.

---

## O. Final Architect Review

### O.1 Strengths

| Strength | Detail |
|---------|--------|
| Zero runtime dependencies | Dataset is static JSON — no database, no API, no internet required. MCP server loads it once at startup. Perfectly compatible with locked architecture. |
| Scout Agent coverage guarantee | Distribution targets are designed to ensure any valid student profile returns ≥ 3 matches. The 20% low-GPA coverage (min_gpa ≤ 2.5) is critical for the demo risk alert scenario. |
| Explainability-first design | Every field has a defined role in Gemini reasoning generation. No field exists only for decoration — each maps to a reasoning fragment. |
| Vocabulary governance | Controlled vocabularies prevent data drift between dataset versions and maintain compatibility with the scholarship_match_skill scoring logic. |
| Scale-without-change architecture | The same schema, MCP tool interface, and skill scoring formula works identically for 80 or 10,000 records. No code changes required to scale the dataset. |
| Demo resilience | Two explicitly modeled demo profiles ensure the system never returns empty results during a judging session. |

### O.2 Risks

| Risk | Severity | Mitigation |
|------|---------|-----------|
| Generation script bugs produce systematically biased dataset | Medium | Distribution checks in QA catch systematic bias before release |
| New student major not in canonical vocabulary returns 0 matches | Medium | Universal scholarships (eligible_majors = all 30+ majors) provide fallback coverage |
| Scholarship names sound repetitive in large datasets | Low | Name component combinatorics provide 10 × 12 × 5 = 600 unique base names — sufficient for 300 records, requires more components for 1,000+ |
| GPA threshold clustering near 3.0 reduces discrimination | Low | Distribution rules explicitly prevent > 30% of records at any single min_gpa value |
| Dataset grows stale (scholarships with past deadlines feel unrealistic) | Low | Deadlines are stored as month/day only — no year component. Always current. |
| Large dataset (10,000 records) slows MCP server memory load | Low | 10,000 records × ~1 KB/record ≈ 10 MB in memory. Acceptable for local subprocess. |

### O.3 Tradeoffs

| Decision | Tradeoff Made | Rationale |
|---------|--------------|-----------|
| Static JSON vs. database | Chose static JSON | Aligned with locked architecture. No database permitted. Simpler. Sufficient for demo scale. |
| Single category per record vs. multi-category | Chose single category | Simplifies filtering logic. Tags provide secondary classification. MCP tool filters on primary category only if needed. |
| month/day deadline vs. full date | Chose month/day only | Deadlines recur annually. No year means the dataset never goes "stale." Simplifies deadline arithmetic in briefing skill. |
| Synthetic vs. real scholarship data | Chose synthetic | No legal/IP concerns. Controlled vocabulary. Predictable coverage. Guaranteed demo coverage. |
| 80 records (MVP) vs. 300+ | 80 records for MVP | Sufficient for demo. Covers all major/year/GPA combinations needed for demo profiles. Day 3 build constraint. |

### O.4 Scalability Analysis

| Dataset Size | Records | JSON File Size | MCP Load Time | Generation Time | QA Time |
|-------------|---------|--------------|--------------|----------------|---------|
| MVP | 80 | ~80 KB | < 50ms | 10–30 minutes | Manual |
| Small | 300 | ~300 KB | < 100ms | 1–2 hours | Semi-automated |
| Medium | 500 | ~500 KB | < 150ms | 2–4 hours | Automated |
| Large | 1,000 | ~1 MB | < 200ms | 4–8 hours | Automated |
| Production | 10,000 | ~10 MB | < 500ms | 8–24 hours | Automated + sampling |

**Key finding:** The architecture scales to 10,000 records without code changes. The only scaling concern is MCP server startup memory load (~10 MB), which remains well within acceptable limits for a local subprocess. No schema changes, no interface changes, no skill changes required at any scale.

**Recommendation for Kaggle submission:** Build to 300 records. This provides:
- Full GPA tier coverage with no gaps
- All 30+ majors represented multiple times
- Sufficient provider diversity (≥ 60 unique providers)
- Differentiated results across all realistic student profiles
- Manageable generation and QA time within Day 3 of the build schedule

---

*Document version: 1.0.0 | Status: FINAL & LOCKED | Compatible with: Student OS Final Specification v1.0*
