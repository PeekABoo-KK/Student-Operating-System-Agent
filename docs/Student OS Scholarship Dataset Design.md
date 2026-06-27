Executive Summary
The Scholarship Dataset (scholarships.json) is a core data foundation for the Opportunity Scout Agent in Student OS. It standardizes global scholarship opportunities into a structured, machine-readable format that enables:
• High-precision eligibility filtering
• Multi-factor ranking and scoring
• Explainable recommendation generation
• Weekly personalized opportunity briefings
The dataset is designed to scale from 300–500 records initially to 10,000+ records without schema changes, using normalized categorical fields, flexible tagging, and extensible eligibility rules.

---

Dataset Design Overview

1. Purpose of the Dataset
   The dataset exists to:
   • Aggregate scholarships from multiple domains (merit, need-based, STEM, leadership, etc.)
   • Normalize eligibility criteria into structured attributes
   • Enable AI-driven matching between student profiles and opportunities
   • Support explainability (“why this scholarship matches you”)
   • Power ranking, filtering, and briefing generation

---

2. How the Opportunity Scout Agent Uses It
   The Scout Agent uses this dataset as its primary retrieval index:
1. Receives student profile (GPA, major, year, location, interests)
1. Filters scholarships using hard constraints (eligibility rules)
1. Scores remaining candidates using weighted relevance model
1. Ranks scholarships by total score
1. Generates explanations using matched attributes

---

3. Matching Logic (High-Level)
   Matching is a hybrid of:
   • Rule-based filtering (hard constraints)
   o GPA minimum
   o Eligible major
   o Year eligibility
   o Location restrictions
   o Deadline validity
   • Soft scoring (ranking signals)
   o Category alignment (STEM, leadership, etc.)
   o Award relevance
   o Preference overlap (tags)

---

Scholarship Record Schema
Each scholarship record must follow this structure:
Core Fields
scholarship_id
• Type: string
• Required: Yes
• Validation: Unique, immutable ID (e.g., SCH-000123)

---

name
• Type: string
• Required: Yes
• Validation: 5–200 characters

---

provider
• Type: string
• Required: Yes
• Validation: Organization/university/company name

---

description
• Type: string
• Required: Yes
• Validation: 50–1000 characters

---

categories
• Type: array[string]
• Required: Yes
• Validation: Must be from controlled taxonomy:
o merit
o need_based
o stem
o leadership
o research
o international
o diversity
o community_service

---

eligible_majors
• Type: array[string]
• Required: Yes
• Validation: Standardized major names (e.g., “Computer Science”, “Information Systems”, “Business”)

---

minimum_gpa
• Type: number
• Required: Yes
• Validation: 0.0 – 4.0 scale

---

eligible_years
• Type: array[string]
• Required: Yes
• Validation:
o freshman
o sophomore
o junior
o senior
o graduate

---

locations
• Type: array[string]
• Required: Yes
• Validation: Country or region codes (“USA”, “Global”, “EU”)

---

award_amount
• Type: object
• Required: Yes
• Structure:
o min: number
o max: number
o currency: string (USD default)

---

application_deadline
• Type: string (ISO 8601 date)
• Required: Yes
• Validation: Must be future date at ingestion time

---

tags
• Type: array[string]
• Required: Yes
• Validation: Free-form but controlled vocabulary encouraged:
o first_gen
o women_in_stem
o low_income
o international_students
o leadership_track

---

eligibility_rules
• Type: array[string]
• Required: Yes
• Validation: Human + machine readable rule statements
Example:
• "GPA >= 3.5"
• "Must be enrolled full-time"
• "STEM majors only"

---

Design Principle
All fields are:
• Flat or lightly nested (no deep hierarchies)
• Filterable without joins
• Scalable to 10,000+ records
• Compatible with scoring + explainability

---

JSON Schema
scholarships.json Schema (Conceptual)
{
"type": "array",
"items": {
"type": "object",

    "required": [
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
      "status",
      "source_url",
      "last_updated",
      "tags",
      "eligibility_rules"
    ],

    "properties": {

      "scholarship_id": {
        "type": "string"
      },

      "name": {
        "type": "string",
        "minLength": 5,
        "maxLength": 200
      },

      "provider": {
        "type": "string"
      },

      "description": {
        "type": "string",
        "minLength": 50,
        "maxLength": 1000
      },

      "categories": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [
            "merit",
            "need_based",
            "stem",
            "leadership",
            "research",
            "international",
            "diversity",
            "community_service"
          ]
        }
      },

      "eligible_majors": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },

      "minimum_gpa": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 4.0
      },

      "eligible_years": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [
            "freshman",
            "sophomore",
            "junior",
            "senior",
            "graduate"
          ]
        }
      },

      "locations": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },

      "award_amount": {
        "type": "object",

        "required": [
          "min",
          "max",
          "currency"
        ],

        "properties": {
          "min": {
            "type": "number"
          },

          "max": {
            "type": "number"
          },

          "currency": {
            "type": "string"
          }
        }
      },

      "application_deadline": {
        "type": "string",
        "format": "date"
      },

      "status": {
        "type": "string",
        "enum": [
          "active",
          "closed",
          "expired"
        ]
      },

      "source_url": {
        "type": "string",
        "format": "uri"
      },

      "last_updated": {
        "type": "string",
        "format": "date"
      },

      "tags": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },

      "eligibility_rules": {
        "type": "array",
        "items": {
          "type": "string"
        }
      }
    },

    "additionalProperties": false

}
}

---

Example Scholarship Records

1. Merit Scholarship (General Excellence)
   • scholarship_id: SCH-000001
   • name: Global Academic Excellence Award
   • provider: International Education Foundation
   • categories: ["merit"]
   • minimum_gpa: 3.8
   • eligible_majors: ["All"]
   • award_amount: $2,000–$10,000
   • tags: ["high_achievers"]

---

2. STEM Scholarship
   • SCH-000002
   • Tech Future Leaders Scholarship
   • categories: ["stem", "leadership"]
   • eligible_majors: ["Computer Science", "Engineering"]
   • minimum_gpa: 3.5
   • award: $5,000–$15,000
   • tags: ["women_in_stem"]

---

3. Need-Based Scholarship
   • SCH-000003
   • Access Education Grant
   • categories: ["need_based"]
   • minimum_gpa: 2.8
   • tags: ["low_income"]
   • eligibility_rules: "Household income below threshold"

---

4. International Student Scholarship
   • SCH-000004
   • Global Bridge Scholarship
   • categories: ["international"]
   • locations: ["USA"]
   • eligible_majors: ["All"]
   • tags: ["visa_students"]

---

5. Leadership Award
   • SCH-000005
   • Emerging Leaders Fellowship
   • categories: ["leadership"]
   • minimum_gpa: 3.2
   • tags: ["community_service"]

---

6. Research Grant
   • SCH-000006
   • Undergraduate Research Innovation Fund
   • categories: ["research", "stem"]
   • eligible_majors: ["Science", "Engineering"]
   • minimum_gpa: 3.4

---

7. Diversity Scholarship
   • SCH-000007
   • Equity in Education Award
   • categories: ["diversity", "need_based"]
   • tags: ["first_gen"]

---

8. Community Service Scholarship
   • SCH-000008
   • Civic Impact Scholarship
   • categories: ["community_service"]
   • eligibility_rules: "Minimum 100 volunteer hours"

---

9. Women in Tech Scholarship
   • SCH-000009
   • Women in Technology Advancement Award
   • categories: ["stem", "diversity"]
   • tags: ["women_in_stem"]

---

10. Transfer Student Scholarship
    • SCH-000010
    • Transfer Achievement Award
    • categories: ["merit"]
    • eligible_years: ["junior", "senior"]
    • minimum_gpa: 3.3

---

Matching Logic

1. Eligibility Filtering (Hard Constraints)
   A scholarship is removed if:
   • Student GPA < minimum_gpa
   • Student major not in eligible_majors (unless "All")
   • Student year not in eligible_years
   • Student location not in allowed locations
   • Deadline has passed

---

2. Soft Matching Signals
   Used for ranking:
   • Category overlap score
   • Tag alignment score
   • Award relevance (higher awards slightly boosted for competitiveness match)
   • Preference boosting (e.g., STEM interest)

---

3. Explainability Layer
   Each match must generate:
   "Matched because:"
   • GPA requirement satisfied (3.6 ≥ 3.5)
   • Major matches Computer Science
   • Category aligns with STEM preference
   • Location eligibility satisfied (USA)

---

Scoring Framework
Final Score Formula (0.0 – 1.0)
Components:
• GPA Match: 30%
• Major Match: 25%
• Year Match: 15%
• Category Match: 20%
• Location Match: 10%

---

Scoring Rules
GPA Match
• ≥ requirement → 1.0
• -0.1 below → 0.7
• else → 0

---

Major Match
• Exact match → 1.0
• Related field → 0.6
• No match → 0

---

Category Match
• Full overlap → 1.0
• Partial → 0.5
• none → 0

---

Scout Agent Retrieval Flow
Student Profile
↓
Hard Filter (eligibility_rules)
↓
Candidate Pool Reduction
↓
Feature Scoring (GPA / Major / Year / Category / Location)
↓
Weighted Aggregation Score (0–1)
↓
Ranking (descending)
↓
Top-K Selection (e.g., 10–20)
↓
Explainability Generator
↓
Weekly Briefing Output

---

Validation Rules
GPA Validation
• Must be between 0.0–4.0
• Reject null values

---

Deadline Validation
• Must be valid ISO date
• Must be future date at ingestion

---

Category Validation
• Must match controlled taxonomy list
• Reject unknown categories

---

Major Validation
• Must match canonical major dictionary

---

Award Amount Validation
• min ≤ max
• currency must be valid ISO code (default USD)

---

Future Expansion Strategy
The schema is intentionally designed to support expansion without modification:

1. Add New Opportunity Types
   • internships
   • fellowships
   • grants
   Handled by adding:
   • opportunity_type (optional future field, not required)

---

2. Extend Categories
   No schema changes required:
   • just append new category strings

---

3. Add External Integrations
   • external_source_id
   • provider_api

---

4. Improve Scoring
   Additional signals can be added without breaking schema:
   • engagement score
   • acceptance rate
   • competition level

---

5. Multi-Region Scaling
   • locations already supports multi-value arrays
   • future: region grouping layer optional

---

Final Architect Review
Strengths
• Clean, flat, scalable schema (10k+ ready)
• Strong eligibility + scoring separation
• Explainability built into structure
• Flexible tagging system
• No tight coupling to agents or logic
• Supports multi-domain expansion (scholarships → internships → grants)

---

Risks
• Tag inconsistency over time without governance
• Major taxonomy drift (requires controlled dictionary)
• Eligibility_rules may become semi-unstructured if not standardized
• Scoring bias if weights are not tuned with real data

---

Recommended Improvements
• Introduce controlled vocabularies for:
o majors
o categories
o tags
• Add optional:
o acceptance_rate (for realism in ranking)
• Add deduplication strategy for cross-provider scholarships
• Build validation pipeline at ingestion stage
• Introduce versioning field for schema evolution tracking

---

If you want, next step I can design:
• real 500-record synthetic dataset generator blueprint
• or SQL + API layer for Scout Agent retrieval
• or ranking explanation prompt system for LLM explanations
