Based on the locked specification, I would prepare the repository as if a junior engineer will implement it in 14 days with minimal ambiguity.
The design below strictly follows the specification:
• 3 Agents only
• 3 Skills only
• 3 Memory Files only
• Streamlit
• Gemini 2.5 Flash
• Google ADK
• JSON Persistence
• Security Layer
• No databases
• No vector stores
• No additional features
Source: Student OS Final Specification.

---

1. Complete Repository Tree
   student-os/

app.py

agents/
│
├── orchestrator.py
├── academic_risk_agent.py
└── opportunity_scout_agent.py

skills/
│
├── gpa_risk/
│
├── scholarship_matching/
│
└── weekly_briefing/

memory/
│
├── student_profile.json
├── activity_log.json
└── alert_history.json

models/
│
├── student_profile.py
├── activity_log.py
└── alert.py

schemas/
│
├── student_profile_schema.py
├── activity_log_schema.py
└── alert_history_schema.py

security/
│
├── validators.py
├── prompt_guard.py
└── security_rules.py

services/
│
└── context_builder.py

utils/
│
├── memory_ops.py
└── logger.py

configs/
│
├── app_config.py
├── model_config.py
└── agent_settings.py

data/
│
└── scholarships/
scholarships.json

tests/
│
├── test_memory.py
├── test_security.py
├── test_agents.py
└── test_skills.py

---

2. File Specifications

---

app.py
Purpose
Main Streamlit application.
Responsibilities
• Render UI
• Load session state
• Collect profile input
• Send requests to Orchestrator
• Display:
o Risk Alerts
o Scholarship Matches
o Weekly Briefing
o Activity Log
Inputs
User Form Data
st.session_state
Outputs
UI Components
Agent Responses
Dependencies
streamlit
orchestrator.py
memory_ops.py
validators.py
Estimated LOC
200-250

---

AGENTS

---

agents/orchestrator.py
Purpose
Central controller of Student OS.
Responsibilities
• Load memory
• Build context
• Route requests
• Call agents
• Call skills
• Generate briefing
• Enforce write gate
• Update memory
Inputs
User Request
Session Context
Profile Data
Outputs
Structured JSON Response
Memory Updates
Dependencies
Google ADK
memory_ops.py
logger.py

academic_risk_agent.py
opportunity_scout_agent.py

validators.py
prompt_guard.py

weekly_briefing.skill
Estimated LOC
250-350

---

agents/academic_risk_agent.py
Purpose
Academic performance analysis.
Responsibilities
• Analyze GPA
• Calculate risk
• Generate recommendations
• Return structured output
Inputs
student_profile
alert_history
Outputs
{
risk_score,
risk_level,
recommendations
}
Dependencies
Google ADK
gpa_risk.skill
Estimated LOC
120-180

---

agents/opportunity_scout_agent.py
Purpose
Scholarship discovery.
Responsibilities
• Scan scholarship dataset
• Rank scholarships
• Explain matches
Inputs
student_profile
scholarships.json
Outputs
{
matches,
scores,
reasoning
}
Dependencies
Google ADK
scholarship_matching.skill
Estimated LOC
120-180

---

SKILLS

---

skills/gpa_risk/skill.py
Purpose
Business logic for GPA risk assessment.
Responsibilities
Apply locked rules:
if gpa < 2.5:
HIGH

elif gpa < target_gpa - 0.5:
MEDIUM

else:
LOW
Inputs
gpa
target_gpa
credits_completed
alert_history
Outputs
risk_score
risk_level
recommendations
Dependencies
None
Estimated LOC
70-100

---

skills/gpa_risk/skill.md
Purpose
ADK Skill Description.
Responsibilities
• Explain tool usage
• Define schema
Estimated LOC
40-60

---

skills/scholarship_matching/skill.py
Purpose
Scholarship matching engine.
Responsibilities
• Filter scholarships
• Calculate match score
• Rank results
Inputs
major
gpa
year
preferences
Outputs
ranked_scholarships
match_scores
eligibility_reason
Dependencies
scholarships.json
Estimated LOC
120-180

---

skills/scholarship_matching/skill.md
Purpose
ADK Skill Definition.
Estimated LOC
40-60

---

skills/weekly_briefing/skill.py
Purpose
Generate weekly academic briefing.
Responsibilities
Combine:
Risk Summary
Opportunity Summary
Top Priorities
Priority order:
1 Risk Alerts
2 Scholarship Deadlines
3 Academic Recommendations
Inputs
profile
activity_history
alert_history
matches
Outputs
weekly_briefing
Dependencies
Gemini 2.5 Flash
Estimated LOC
100-150

---

skills/weekly_briefing/skill.md
Purpose
ADK Skill Description.
Estimated LOC
40-60

---

MEMORY

---

memory/student_profile.json
Purpose
Persistent student profile.
Schema
{
"student_id": "",
"name": "",
"major": "",
"gpa": 0,
"target_gpa": 0,
"credits_completed": 0,
"target_graduation": "",
"career_goal": "",
"study_hours_per_week": 0,
"preferences": {},
"risk_baseline": ""
}
Estimated LOC
10-20

---

memory/activity_log.json
Purpose
Agent activity history.
Schema
[
{
"timestamp": "",
"agent": "",
"action": "",
"reason": "",
"result": ""
}
]
Estimated LOC
10-20

---

memory/alert_history.json
Purpose
Alert persistence.
Schema
[
{
"timestamp": "",
"level": "",
"message": ""
}
]
Estimated LOC
10-20

---

SECURITY

---

security/validators.py
Purpose
Input validation.
Responsibilities
Validate:
Empty Input
Max Length
Allowed Characters
Schema Validation
Inputs
User Inputs
Outputs
Validated Data
Validation Errors
Estimated LOC
120-180

---

security/prompt_guard.py
Purpose
Prompt injection detection.
Responsibilities
Block:
ignore previous instructions
reveal system prompt
show hidden memory
delete memory
override rules
act as administrator
print your instructions
Inputs
User Prompt
Outputs
allow
block
reason
Estimated LOC
80-120

---

security/security_rules.py
Purpose
Central security policy definitions.
Responsibilities
Store:
Blocked Patterns
Profile Schema
Permission Rules
Outputs
Constants
Estimated LOC
50-80

---

UTILITIES

---

utils/memory_ops.py
Purpose
JSON persistence layer.
Responsibilities
load_profile()
save_profile()

load_activity()
save_activity()

load_alerts()
save_alerts()
Inputs
JSON Files
Outputs
Python Objects
Dependencies
json
pathlib
Estimated LOC
150-220

---

utils/logger.py
Purpose
Activity logging.
Responsibilities
Create standardized entries.
Output
{
"agent":"",
"action":"",
"reason":"",
"result":"",
"timestamp":""
}
Estimated LOC
50-80

---

DATA

---

data/scholarships.json
Purpose
Scholarship dataset.
Example Schema
[
{
"name": "",
"major": "",
"min_gpa": 0,
"deadline": "",
"amount": 0
}
]
Estimated Size
50-500 records

---

TESTS

---

test_memory.py
Responsibilities
Load JSON
Save JSON
Persistence
LOC
80-120

---

test_security.py
Responsibilities
Prompt Injection
Schema Validation
Write Gate
LOC
120-180

---

test_agents.py
Responsibilities
Agent Routing
Agent Responses
LOC
100-150

---

test_skills.py
Responsibilities
Risk Skill
Scholarship Skill
Briefing Skill
LOC
120-180

---

3. Dependency Flow
   app.py
   │
   ▼
   Orchestrator Agent
   │
   ├───────────────► Academic Risk Agent
   │ │
   │ ▼
   │ GPA Risk Skill
   │
   ├───────────────► Opportunity Scout Agent
   │ │
   │ ▼
   │ Scholarship Matching Skill
   │
   ▼
   Weekly Briefing Skill
   │
   ▼
   Memory Layer
   │
   ├── student_profile.json
   ├── activity_log.json
   └── alert_history.json

Security Layer
│
├── validators.py
├── prompt_guard.py
└── security_rules.py

---

4. Build Order (Recommended)
   Step 1 — Foundation
   requirements.txt
   memory_ops.py
   student_profile.json
   activity_log.json
   alert_history.json
   app.py skeleton
   Step 2 — Security
   security_rules.py
   validators.py
   prompt_guard.py
   Step 3 — Skills
   gpa_risk skill
   scholarship_matching skill
   weekly_briefing skill
   Step 4 — Agents
   academic_risk_agent.py
   opportunity_scout_agent.py
   orchestrator.py
   Step 5 — UI
   Profile Form
   Risk Dashboard
   Scholarship Panel
   Weekly Briefing
   Activity Log
   Step 6 — Testing
   test_memory.py
   test_security.py
   test_skills.py
   test_agents.py
   Step 7 — Finalization
   README.md
   .env template
   Demo Data
   Kaggle Submission Package
   Estimated final codebase size: ~2,500–3,500 LOC, which is appropriate for a solo developer building the locked Student OS MVP within the 14-day implementation plan defined in the specification.
