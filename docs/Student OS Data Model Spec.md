Executive Summary
This specification defines the complete implementation-ready data contracts for Student OS while strictly preserving the locked architecture:
• 3 Agents
o Orchestrator Agent
o Academic Risk Agent
o Opportunity Scout Agent
• 3 Skills
o GPA Risk Assessment
o Scholarship Matching
o Weekly Briefing Generation
• 3 Persistent Memory Files
o student_profile.json
o activity_log.json
o alert_history.json
Design principles:
• Strict schema validation
• ISO 8601 timestamps
• Reject unknown fields
• Orchestrator-only write access
• Agent read-only access
• JSON persistence only
• No database
• No vector store
• No additional memory systems
The model layer and schema layer are designed to support Streamlit UI, Google ADK agents, skills, memory persistence, and security controls defined in the locked specification.

---

Data Model Overview
Memory File Purpose Owner Readers
student_profile.json Long-term student profile Orchestrator All Agents
activity_log.json Agent activity history Orchestrator All Agents
alert_history.json Alert persistence Orchestrator All Agents
Global Rules:
• additionalProperties = false
• ISO 8601 timestamps only
• UTF-8 strings
• Null values disallowed unless explicitly specified
• All writes pass validation layer
• Orchestrator is the only component allowed to persist changes

---

student_profile.json
Purpose
Persistent long-term academic profile containing identity, academic baseline, goals, and scholarship preferences.
Used by:
• Streamlit UI
• Orchestrator Agent
• Academic Risk Agent
• Opportunity Scout Agent
• GPA Risk Assessment Skill
• Scholarship Matching Skill
• Weekly Briefing Skill

---

JSON Schema
{
"type": "object",
"additionalProperties": false,
"required": [
"student_id",
"name",
"major",
"year",
"gpa",
"target_gpa",
"credits_completed",
"target_graduation",
"career_goal",
"study_hours_per_week",
"preferences",
"risk_baseline",
"created_at",
"updated_at"
],
"properties": {
"student_id": {
"type": "string",
"minLength": 3,
"maxLength": 50
},
"name": {
"type": "string",
"minLength": 1,
"maxLength": 100
},
"major": {
"type": "string",
"minLength": 2,
"maxLength": 100
},
"year": {
"type": "integer",
"minimum": 1,
"maximum": 8
},
"gpa": {
"type": "number",
"minimum": 0.0,
"maximum": 4.0
},
"target_gpa": {
"type": "number",
"minimum": 0.0,
"maximum": 4.0
},
"credits_completed": {
"type": "integer",
"minimum": 0,
"maximum": 300
},
"target_graduation": {
"type": "string"
},
"career_goal": {
"type": "string",
"maxLength": 200
},
"study_hours_per_week": {
"type": "integer",
"minimum": 0,
"maximum": 100
},
"preferences": {
"type": "object",
"additionalProperties": false,
"required": [
"scholarship_categories",
"preferred_locations"
],
"properties": {
"scholarship_categories": {
"type": "array",
"minItems": 1,
"items": {
"type": "string",
"enum": [
"merit",
"need_based",
"stem",
"international",
"leadership",
"research"
]
}
},
"preferred_locations": {
"type": "array",
"items": {
"type": "string"
}
}
}
},
"risk_baseline": {
"type": "string",
"enum": [
"LOW",
"MEDIUM",
"HIGH"
]
},
"created_at": {
"type": "string"
},
"updated_at": {
"type": "string"
}
}
}

---

Required Fields
• student_id
• name
• major
• year
• gpa
• target_gpa
• credits_completed
• target_graduation
• career_goal
• study_hours_per_week
• preferences
• risk_baseline
• created_at
• updated_at

---

Optional Fields
None.
Locked schema.

---

Validation Rules
GPA
• 0.0 ≤ GPA ≤ 4.0
• max 2 decimal places
Target GPA
• 0.0 ≤ Target GPA ≤ 4.0
• target_gpa ≥ gpa allowed but not required
Credits
• 0 ≤ credits_completed ≤ 300
Major
• 2–100 chars
• alphanumeric, spaces, hyphens
Scholarship Preferences
• category list cannot exceed 20 entries
• location list cannot exceed 20 entries
Timestamps
• ISO 8601 UTC
Example:
2026-06-24T18:30:00Z

---

Security Constraints
Field Read Write Classification Validation
student_id All Agents Orchestrator Sensitive Unique ID
name All Agents Orchestrator Sensitive Length
major All Agents Orchestrator Non-Sensitive Enum/Text
year All Agents Orchestrator Non-Sensitive Range
gpa All Agents Orchestrator Sensitive Range
target_gpa All Agents Orchestrator Sensitive Range
credits_completed All Agents Orchestrator Non-Sensitive Range
target_graduation All Agents Orchestrator Non-Sensitive Format
career_goal All Agents Orchestrator Non-Sensitive Length
study_hours_per_week All Agents Orchestrator Non-Sensitive Range
preferences All Agents Orchestrator Non-Sensitive Schema
risk_baseline All Agents Orchestrator Non-Sensitive Enum
created_at All Agents Orchestrator Non-Sensitive ISO 8601
updated_at All Agents Orchestrator Non-Sensitive ISO 8601

---

Example Record
{
"student_id": "STU001",
"name": "Jane Smith",
"major": "Computer Science",
"year": 2,
"gpa": 3.2,
"target_gpa": 3.6,
"credits_completed": 48,
"target_graduation": "2028-05",
"career_goal": "Data Analyst",
"study_hours_per_week": 15,
"preferences": {
"scholarship_categories": [
"STEM",
"Women in Technology"
],
"preferred_locations": [
"California",
"Remote"
]
},
"risk_baseline": "LOW",
"created_at": "2026-06-24T18:00:00Z",
"updated_at": "2026-06-24T18:00:00Z"
}

---

Python Dataclass
StudentProfile
├── student_id: str
├── name: str
├── major: str
├── year: int
├── gpa: float
├── target_gpa: float
├── credits_completed: int
├── target_graduation: str
├── career_goal: str
├── study_hours_per_week: int
├── preferences: ScholarshipPreferences
├── risk_baseline: str
├── created_at: str
└── updated_at: str

---

activity_log.json
Purpose
Persistent activity memory storing agent coordination evidence and explainability records.

---

JSON Schema
{
"type": "array",
"items": {
"type": "object",
"additionalProperties": false,
"required": [
"timestamp",
"agent",
"action",
"reason",
"result",
"status"
],
"properties": {
"timestamp": {
"type": "string"
},
"agent": {
"type": "string",
"enum": [
"OrchestratorAgent",
"AcademicRiskAgent",
"OpportunityScoutAgent"
]
},  
 "action": {
"type": "string"
},
"reason": {
"type": "string"
},
"result": {
"type": "string"
},
"status": {
"type": "string",
"enum": [
"SUCCESS",
"FAILED"
]
}
}
}
}

---

Required Fields
• timestamp
• agent
• action
• reason
• result
• status

---

Optional Fields
None.

---

Validation Rules
Agent Names
Allowed:
• OrchestratorAgent
• AcademicRiskAgent
• OpportunityScoutAgent
Action
1–200 chars
Result
1–1000 chars
Timestamp
ISO 8601 UTC

---

Security Constraints
Field Read Write Classification
timestamp All Agents Orchestrator Non-Sensitive
agent All Agents Orchestrator Non-Sensitive
action All Agents Orchestrator Non-Sensitive
reason All Agents Orchestrator Non-Sensitive
result All Agents Orchestrator Non-Sensitive
status All Agents Orchestrator Non-Sensitive

---

Example Record
[
{
"timestamp": "2026-06-24T18:15:00Z",
"agent": "AcademicRiskAgent",
"action": "Risk Assessment",
"reason": "Weekly evaluation",
"result": "MEDIUM RISK",
"status": "SUCCESS"
}
]

---

Python Dataclass
ActivityLogEntry
├── timestamp: str
├── agent: str
├── action: str
├── reason: str
├── result: str
└── status: str

---

alert_history.json
Purpose
Persistent risk and notification memory used by GPA Risk Assessment and Weekly Briefing skills.

---

JSON Schema
{
"type": "array",
"items": {
"type": "object",
"additionalProperties": false,
"required": [
"alert_id",
"timestamp",
"severity",
"message",
"source_agent",
"resolved"
],
"properties": {
"alert_id": {
"type": "string"
},
"timestamp": {
"type": "string"
},
"severity": {
"type": "string",
"enum": [
"LOW",
"MEDIUM",
"HIGH"
]
},
"message": {
"type": "string"
},
"source_agent": {
"type": "string"
},
"resolved": {
"type": "boolean"
}
}
}
}

---

Required Fields
• alert_id
• timestamp
• severity
• message
• source_agent
• resolved

---

Optional Fields
None.

---

Validation Rules
Alert Severity
Allowed:
• LOW
• MEDIUM
• HIGH
Source Agent
Allowed:
• OrchestratorAgent
• AcademicRiskAgent
Message
1–500 chars
Timestamp
ISO 8601 UTC

---

Security Constraints
Field Read Write Classification
alert_id All Agents Orchestrator Non-Sensitive
timestamp All Agents Orchestrator Non-Sensitive
severity All Agents Orchestrator Non-Sensitive
message All Agents Orchestrator Non-Sensitive
source_agent All Agents Orchestrator Non-Sensitive
resolved All Agents Orchestrator Non-Sensitive

---

Example Record
[
{
"alert_id": "ALT001",
"timestamp": "2026-06-24T18:30:00Z",
"severity": "MEDIUM",
"message": "Current GPA is below target GPA by more than 0.5 points.",
"source_agent": "AcademicRiskAgent",
"resolved": false
}
]

---

Python Dataclass
Alert
├── alert_id: str
├── timestamp: str
├── severity: str
├── message: str
├── source_agent: str
└── resolved: bool

---

Models Layer Specification
models/student_profile.py
Purpose
Typed representation of persistent student profile.
Responsibilities
• Define StudentProfile dataclass
• Define ScholarshipPreferences dataclass
• Support serialization/deserialization
• Support validation integration
Dataclass Definitions
ScholarshipPreferences
StudentProfile
Estimated LOC
40–70

---

models/activity_log.py
Purpose
Typed activity log representation.
Responsibilities
• Define ActivityLogEntry
• Support audit records
• Support serialization
Dataclass Definitions
ActivityLogEntry
Estimated LOC
20–40

---

models/alert.py
Purpose
Typed alert representation.
Responsibilities
• Define Alert
• Support risk persistence
• Support alert lifecycle
Dataclass Definitions
Alert
Estimated LOC
20–40

---

Schema Layer Specification
schemas/student_profile_schema.py
Purpose
Validation contract for student profile.
Responsibilities
• Validate GPA
• Validate credits
• Validate preferences
• Validate timestamps
• Reject unknown fields
Validation Scope
• Structure validation
• Range validation
• Enum validation
• ISO timestamp validation
Estimated LOC
80–120

---

schemas/activity_log_schema.py
Purpose
Validation contract for activity history.
Responsibilities
• Validate activity entries
• Validate agent names
• Validate timestamps
Validation Scope
• Agent enum validation
• String length validation
• ISO timestamp validation
Estimated LOC
50–80

---

schemas/alert_history_schema.py
Purpose
Validation contract for alerts.
Responsibilities
• Validate severity
• Validate source agent
• Validate timestamps
Validation Scope
• Enum validation
• Boolean validation
• ISO timestamp validation
Estimated LOC
50–80

---

Cross-Model Validation Matrix
Rule student_profile activity_log alert_history
ISO 8601 Timestamp ✓ ✓ ✓
Reject Unknown Fields ✓ ✓ ✓
Enum Validation ✓ ✓ ✓
String Length Validation ✓ ✓ ✓
Numeric Range Validation ✓ N/A N/A
Agent Validation N/A ✓ ✓
Security Ownership ✓ ✓ ✓
Serialization Safety ✓ ✓ ✓

---

Security Matrix
Resource Orchestrator Read Orchestrator Write Risk Agent Read Risk Agent Write Scout Agent Read Scout Agent Write
student_profile.json ✓ ✓ ✓ ✗ ✓ ✗
activity_log.json ✓ ✓ ✓ ✗ ✓ ✗
alert_history.json ✓ ✓ ✓ ✗ ✓ ✗
Enforcement Rules

1. All writes routed through Orchestrator.
2. Agents return proposed updates only.
3. Validation occurs before persistence.
4. Unknown fields rejected.
5. Failed validation blocks write operation.
6. Memory corruption attempts rejected.
7. Prompt injection output never persisted.

---

Final Architect Review
Strengths
• Fully aligned with locked specification.
• Strict schema enforcement.
• Strong ownership boundaries.
• Minimal implementation complexity.
• Clear agent-memory contracts.
• Supports explainability requirements.
• Supports security controls required by Kaggle evaluation.
Risks
• Single JSON file growth over time.
• Activity history may become large.
• No archival strategy defined.
• No file locking strategy specified for concurrent writes.
Missing Fields
No mandatory fields are missing relative to the locked specification.
The only addition beyond the minimal memory schema is:
• year
• created_at
• updated_at
• status
• alert_id
• source_agent
• resolved
These are implementation-support fields and do not alter architecture, memory count, agents, skills, or system scope.
Recommended Improvements
Within the locked architecture:

1. Add maximum activity log retention (e.g., last 500 entries).
2. Add maximum alert retention (e.g., last 200 alerts).
3. Enforce UTC timestamps everywhere.
4. Generate deterministic alert IDs.
5. Add schema version constant in validation layer (not memory schema).
6. Add atomic file-write strategy in memory_ops.py.
   These improvements remain fully compliant with the FINAL LOCK specification and do not introduce new components, agents, memory stores, databases, or features.
