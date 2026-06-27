Student OS — Academic Co-Pilot (Final MVP Architecture)
Design Goal: Deliver a complete multi-agent academic assistant within 14 days using Google ADK + Gemini 2.5 Flash + Streamlit while demonstrating:
• Multi-Agent System
• Persistent Memory
• Proactive Behavior
• MCP Integration
• Security Layer
No additional features beyond MVP scope.

---

1. System Architecture
   High-Level Architecture
   ┌─────────────────────────┐
   │ Streamlit UI │
   └───────────┬─────────────┘
   │
   ▼
   ┌─────────────────────────┐
   │ Orchestrator Agent │
   │ (Google ADK) │
   └──────┬─────────┬────────┘
   │ │
   │ │
   ▼ ▼
   ┌───────────┐ ┌──────────────┐
   │ Academic │ │ Opportunity │
   │ Risk │ │ Scout Agent │
   │ Agent │ │ │
   └─────┬─────┘ └──────┬───────┘
   │ │
   │ │
   ▼ ▼
   ┌─────────────────────────┐
   │ MCP Server │
   │ Scholarship Search Tool │
   └───────────┬─────────────┘
   │
   ▼
   ┌─────────────────────────┐
   │ Long-Term JSON Memory │
   │ Student Profile Store │
   └─────────────────────────┘

---

2. Component Diagram
   +---------------------------------------------------+
   | Streamlit UI |
   +---------------------------------------------------+
   | |
   | Dashboard |
   | Weekly Briefing |
   | Risk Alerts |
   | Scholarships |
   | Agent Activity Log |
   | Session Chat |
   | |
   +---------------------+-----------------------------+
   |
   v

+---------------------------------------------------+
| Orchestrator Agent |
+---------------------------------------------------+
| |
| Intent Routing |
| Task Dispatching |
| Memory Loading |
| Session Context |
| Response Aggregation |
| |
+--------+----------------------+-------------------+
| |
v v

+------------------+ +---------------------------+
| Academic Risk | | Opportunity Scout Agent |
| Agent | | |
+------------------+ +---------------------------+
| GPA Monitoring | | Scholarship Matching |
| Credit Tracking | | Opportunity Ranking |
| Risk Detection | | MCP Search Execution |
| Alert Creation | | Weekly Opportunities |
+------------------+ +---------------------------+

         \                /
          \              /
           \            /
            v          v

+---------------------------------------------------+
| MCP Server |
+---------------------------------------------------+
| Scholarship Search Endpoint |
+---------------------------------------------------+

                      |
                      v

+---------------------------------------------------+
| JSON Storage |
+---------------------------------------------------+
| student_profile.json |
| session_memory.json |
| activity_log.json |
| alert_history.json |
+---------------------------------------------------+

---

3. Mermaid Architecture Diagram

---

4. Sequence Diagram
   Weekly Briefing Generation

---

5. Agent Communication Flow
   User-Initiated Flow
   User Query
   │
   ▼
   Orchestrator Agent
   │
   ├── Academic Question
   │ ▼
   │ Academic Risk Agent
   │
   ├── Scholarship Request
   │ ▼
   │ Opportunity Scout Agent
   │
   └── Combined Request
   ▼
   Both Agents

Agents Return Results
│
▼
Orchestrator
│
▼
Final Response

---

Proactive Flow
App Startup

      ▼

Orchestrator

      ▼

Load Student Profile

      ▼

Trigger Academic Risk Agent

      ▼

Risk Score Calculation

      ▼

If Risk > Threshold

      ▼

Generate Alert

      ▼

Save Alert History

      ▼

Display Dashboard Alert
This demonstrates proactive agent behavior without requiring background jobs.

---

6. Memory Flow
   Session Memory
   Purpose:
   • Current conversation
   • Temporary context
   Stored in:
   data/session_memory.json
   Example:
   {
   "session_id": "abc123",
   "recent_interactions": [
   {
   "role": "user",
   "message": "Find scholarships"
   }
   ]
   }

---

Long-Term Memory
Purpose:
• Persistent student profile
Stored in:
data/student_profile.json
Example:
{
"name": "John Doe",
"major": "Information Systems",
"gpa": 3.2,
"credits_completed": 48,
"target_graduation": "2028"
}

---

Memory Lifecycle
Startup
│
▼

Load Profile

│
▼

Load Session

│
▼

Agent Execution

│
▼

Update Memory

│
▼

Persist JSON

---

7. UI Flow
   Dashboard
   Dashboard
   │
   ├── Student Profile
   │
   ├── Weekly Briefing
   │
   ├── Risk Alerts
   │
   ├── Scholarship Matches
   │
   ├── Agent Activity Log
   │
   └── Session Chat

---

User Journey
Login

▼

Dashboard

▼

Student Profile Loaded

▼

Weekly Briefing Generated

▼

Risk Alert Check

▼

Scholarship Matches Loaded

▼

User Opens Chat

▼

Agent Interaction

▼

Memory Updated

---

8. File Structure
   student-os/

│
├── app.py
│
├── agents/
│ ├── orchestrator.py
│ ├── academic_risk_agent.py
│ └── opportunity_scout_agent.py
│
├── memory/
│ ├── profile_manager.py
│ ├── session_manager.py
│ └── memory_models.py
│
├── mcp/
│ ├── scholarship_server.py
│ └── scholarship_client.py
│
├── services/
│ ├── briefing_service.py
│ ├── alert_service.py
│ └── logging_service.py
│
├── security/
│ ├── input_validator.py
│ ├── sanitizer.py
│ └── access_control.py
│
├── data/
│ ├── student_profile.json
│ ├── activity_log.json
│ └── alert_history.json
│
├── ui/
│ ├── dashboard.py
│ ├── profile.py
│ ├── briefing.py
│ ├── alerts.py
│ ├── scholarships.py
│ └── activity_log.py
│
├── config/
│ └── settings.py
│
├── requirements.txt
│
└── README.md

---

9. Deployment Architecture
   MVP Deployment

---

Security Layer
Input Validation
Before reaching agents:
User Input
│
▼
Input Validator
│
▼
Sanitizer
│
▼
Orchestrator
Checks:
• Empty input
• Oversized prompts
• Invalid profile data
• JSON schema validation

---

Memory Protection
Agent
│
▼
Memory Manager
│
▼
Validated Write
│
▼
JSON Store
Prevents:
• Corrupted memory files
• Invalid profile updates
• Broken sessions

---

Final MVP Architecture Summary
Requirement Implementation
Multi-Agent Architecture Orchestrator + Academic Risk + Opportunity Scout
Session Memory session_memory.json
Long-Term Memory student_profile.json
Proactive Agent Behavior Risk scan at dashboard load
MCP Integration Scholarship Search MCP Server
Security Layer Validation + Sanitization + Controlled Memory Writes
Frontend Streamlit
LLM Gemini 2.5 Flash
Agent Framework Google ADK
Storage JSON Files
Deployment Single Streamlit + ADK instance
This architecture is intentionally minimal, judge-friendly, and realistic for a single developer delivering within 14 days, while still showcasing all required agentic-system concepts.
