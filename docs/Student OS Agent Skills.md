Student OS — Agent Skills Architecture (Hackathon Edition)
Based on your locked architecture:
• Orchestrator Agent
• Academic Risk Agent
• Opportunity Scout Agent
and memory design:
• student_profile.json
• activity_log.json
• alert_history.json
the simplest skill architecture is:
Orchestrator
│
├── GPA Risk Assessment Skill
│
├── Scholarship Matching Skill
│
└── Weekly Briefing Generation Skill
The key principle:
Skills are reusable capabilities.
Agents do not contain business logic.
Agents call skills.
This demonstrates:
✅ Agent Skills
✅ Skill Reuse
✅ Multi-Agent Coordination
✅ Minimal implementation

---

1. GPA Risk Assessment Skill
   Purpose
   Evaluate whether a student is at risk academically.
   Produces:
   • risk score
   • risk level
   • intervention recommendations
   This is the core proactive capability of Student OS.

---

Inputs
{
"gpa": 3.1,
"target_gpa": 3.5,
"credits_completed": 48,
"recent_alerts": 2
}
Retrieved from:
student_profile.json
alert_history.json

---

Outputs
{
"risk_score": 0.74,
"risk_level": "HIGH",
"recommendations": [
"Meet advisor",
"Increase study hours",
"Reduce overload"
]
}

---

Trigger Conditions
Automatic
• GPA updated
• New semester grades entered
Agent-triggered
• User asks:
"Am I at risk?"

---

Example Skill.md

# GPA Risk Assessment Skill

## Purpose

Estimate academic risk level.

## Inputs

- GPA
- Target GPA
- Credits Completed
- Alert History

## Outputs

- Risk Score
- Risk Level
- Recommended Actions

## Rules

IF GPA < 2.5
→ HIGH

IF GPA < target_gpa - 0.5
→ MEDIUM

ELSE
→ LOW

---

Agents Using It
Primary
Academic Risk Agent
Secondary
Orchestrator Agent
Uses results for routing and triggering alerts.

---

2. Scholarship Matching Skill
   Purpose
   Find scholarship opportunities matching student profile.
   Supports the MVP "fast win" requirement described in the strategy document.

---

Inputs
{
"major": "Information Systems",
"gpa": 3.6,
"year": "Sophomore",
"preferences": [
"merit",
"international"
]
}
Retrieved from:
student_profile.json

---

Outputs
{
"matches": [
{
"name": "Merit Scholarship",
"score": 0.91,
"reason": "GPA qualifies"
}
]
}

---

Trigger Conditions
Automatic
Weekly scan
User Request
"Find scholarships"
Profile Update
• GPA changes
• Major changes

---

Example Skill.md

# Scholarship Matching Skill

## Purpose

Match scholarships to student profile.

## Inputs

- GPA
- Major
- Year
- Preferences

## Outputs

- Ranked Scholarships
- Match Score
- Eligibility Reason

## Rules

For each scholarship:

score =
eligibility_match

- preference_match

Return top 3.

---

Agents Using It
Primary
Opportunity Scout Agent
Secondary
Orchestrator Agent
Can invoke it during onboarding.

---

3. Weekly Briefing Generation Skill
   Purpose
   Generate a concise proactive summary.
   This demonstrates "system initiates value" rather than waiting for user prompts.

---

Inputs
{
"student_profile": {},
"recent_activity": [],
"recent_alerts": [],
"scholarship_matches": []
}
Sources:
student_profile.json
activity_log.json
alert_history.json

---

Outputs
{
"priorities": [
"Apply for Merit Scholarship",
"Monitor GPA trend",
"Prepare for midterm week"
],
"risk_summary": "Low",
"opportunity_summary": "2 scholarships found"
}

---

Trigger Conditions
Automatic
At Session Start (App Load)
The briefing is generated automatically whenever the student opens Student OS. This demonstrates proactive agent behavior without requiring a scheduler, cron job, or cloud worker.
Manual
User presses:
Generate Weekly Briefing

---

Example Skill.md

# Weekly Briefing Generation Skill

## Purpose

Create weekly student summary.

## Inputs

- Student Profile
- Recent Activity
- Recent Alerts
- Opportunities

## Outputs

- Top Priorities
- Risk Summary
- Opportunity Summary

## Rules

Priority Order:

1. High Risk Alerts
2. Scholarship Deadlines
3. Academic Recommendations

Return top 3 priorities.

---

Agents Using It
Primary
Orchestrator Agent
Reuses
GPA Risk Assessment Skill
Scholarship Matching Skill

---

Multi-Agent Coordination Flow
This is the smallest coordination architecture that still scores well.
Session Start
│
▼
Orchestrator
│
├──────────────► GPA Risk Skill
│
├──────────────► Scholarship Skill
│
▼
Weekly Briefing Skill
│
▼
Student

---

Skill Reuse Demonstration
Academic Risk Agent
Uses:

- GPA Risk Assessment Skill
  Opportunity Scout Agent
  Uses:
- Scholarship Matching Skill
  Orchestrator Agent
  Uses:
- GPA Risk Assessment Skill
- Scholarship Matching Skill
- Weekly Briefing Skill
  Reuse matrix:
  Skill Risk Agent Scout Agent Orchestrator
  GPA Risk Assessment ✓ ✓
  Scholarship Matching ✓ ✓
  Weekly Briefing ✓
  This is enough to demonstrate skill reuse to judges.

---

Recommended Folder Structure
student-os/

agents/
│
├── orchestrator.py
├── academic_risk_agent.py
└── opportunity_scout_agent.py

skills/
│
├── gpa_risk/
│ ├── skill.md
│ └── skill.py
│
├── scholarship_matching/
│ ├── skill.md
│ └── skill.py
│
└── weekly_briefing/
├── skill.md
└── skill.py

memory/
│
├── student_profile.json
├── activity_log.json
└── alert_history.json

---

Kaggle Judge Review (Ruthless Evaluation)
What Judges Want
The strategy document explicitly emphasizes:

1. Persistent student model
2. Multi-agent reasoning
3. Proactive actions
4. Explainable decisions
5. Twin update loop
   This architecture demonstrates all five.

---

Over-Engineering to Avoid
❌ Skill Registry
skill_registry.py
dynamic_loading.py
plugin_manager.py
Not needed for 3 skills.

---

❌ Tool Router Layer
Agent
↓
Router
↓
Dispatcher
↓
Skill
Adds complexity without scoring benefit.

---

❌ Individual Skill Databases
risk_db.json
scholarship_db.json
briefing_db.json
Use the existing 3 memory files only.

---

❌ Event Bus / PubSub
Kafka
Redis
RabbitMQ
Massive overkill for a solo developer.

---

❌ Separate Memory per Agent
risk_memory.json
scout_memory.json
Violates your clean shared-memory design.

---

Final Kaggle Judge Verdict
Score: 9.7 / 10
Why it scores highly:
• 3 agents only
• 3 skills only
• Clear skill reuse
• Clear multi-agent coordination
• Reuses existing JSON memory system
• Demonstrates proactive behavior through Session-Start Briefing
• Implementable by one developer in a 14-day hackathon
What prevents 10/10:
• Weekly Briefing is primarily a composition skill rather than a deeply autonomous agent capability.
• No external opportunity dataset integration yet (acceptable for MVP).
For a Kaggle AI Agents capstone, I would build exactly these 3 skills and no more. Any additional abstractions are more likely to reduce your score than increase it.
