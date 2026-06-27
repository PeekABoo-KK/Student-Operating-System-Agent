ADK_Architecture.md
A. ADK Overview
Purpose of Google ADK
Google Agent Development Kit (ADK) is used as the execution framework for Student OS because it provides:
• Structured multi-agent orchestration
• Tool-based skill execution
• Session management
• Agent communication patterns
• Typed inputs and outputs
• Deterministic workflow execution
• Integration with Streamlit UI
• Clear separation between agents, tools, memory, and orchestration
Student OS does not use ADK for autonomous planning or dynamic agent creation.
ADK is used strictly as the execution layer for the locked architecture.

---

Student OS to ADK Mapping
Student OS Component ADK Component
Orchestrator Agent Root Agent
Academic Risk Agent Sub Agent
Opportunity Scout Agent Sub Agent
GPA Risk Assessment Tool
Scholarship Matching Tool
Weekly Briefing Generation Tool
student_profile.json Persistent Memory Source
activity_log.json Persistent Memory Source
alert_history.json Persistent Memory Source
Streamlit UI Frontend Client
ADK Session Runtime Session

---

Agent Execution Model
Student OS uses hierarchical orchestration.
Execution hierarchy:
User
↓
Orchestrator Agent
↓
Academic Risk Agent
↓
GPA Risk Assessment Tool

Orchestrator Agent
↓
Opportunity Scout Agent
↓
Scholarship Matching Tool

Orchestrator Agent
↓
Weekly Briefing Tool
Execution rules:

1. User requests enter through Orchestrator Agent.
2. Orchestrator validates input.
3. Orchestrator loads memory.
4. Orchestrator invokes specialized agent.
5. Specialized agent invokes assigned tool.
6. Tool returns structured output.
7. Orchestrator validates output.
8. Orchestrator updates memory if permitted.
9. Response returned to user.

---

Session Model
One user session maps to one ADK session.
Session contains:
Session State
├── request_id
├── user_request
├── loaded_profile
├── loaded_activity_log
├── loaded_alert_history
├── workflow_type
├── workflow_result
└── execution_metadata
Session state exists only during execution.
Persistent data remains in JSON memory files.

---

B. Agent Mapping
Orchestrator Agent
ADK Type
Root Agent
Purpose
Central coordinator for all Student OS workflows.
Responsibilities
• Receive requests
• Load memory
• Validate input
• Route execution
• Invoke specialized agents
• Generate weekly briefings
• Validate outputs
• Persist approved updates
Inputs
• User request
• Student profile
• Activity log
• Alert history
• Agent responses
Outputs
• User response
• Workflow results
• Memory update requests
Skills Used
• Weekly Briefing Generation
Memory Access
Read:
• student_profile.json
• activity_log.json
• alert_history.json
Write:
• student_profile.json
• activity_log.json
• alert_history.json
Security Boundaries
Allowed:
• Agent invocation
• Memory updates
• Activity logging
Forbidden:
• External storage creation
• Schema modification

---

Academic Risk Agent
ADK Type
Sub Agent
Purpose
Perform academic risk analysis.
Responsibilities
• GPA evaluation
• Risk scoring
• Risk classification
• Alert generation
Inputs
• Student profile
• Activity history
Outputs
• Risk assessment
• Academic alerts
Skills Used
• GPA Risk Assessment
Memory Access
Read:
• student_profile.json
• activity_log.json
Write:
• None
Security Boundaries
Allowed:
• Read memory
• Run GPA analysis
Forbidden:
• Memory modification
• Scholarship access

---

Opportunity Scout Agent
ADK Type
Sub Agent
Purpose
Perform scholarship discovery and matching.
Responsibilities
• Eligibility filtering
• Match scoring
• Ranking opportunities
Inputs
• Student profile
• Scholarship dataset
Outputs
• Scholarship matches
• Opportunity alerts
Skills Used
• Scholarship Matching
Memory Access
Read:
• student_profile.json
Write:
• None
Security Boundaries
Allowed:
• Read profile
• Read scholarship dataset
Forbidden:
• Memory updates
• GPA analysis

---

C. Skill Mapping

1. GPA Risk Assessment Skill
   ADK Component
   Tool
   Invocation Method
   AcademicRiskAgent → GPA_Risk_Assessment_Tool
   Inputs
   StudentProfile
   Outputs
   RiskAssessment
   Validation
   • GPA exists
   • GPA range valid
   • Profile schema valid
   Failure Handling
   • Return structured error
   • Log validation failure
   • Reject invalid output

---

2. Scholarship Matching Skill
   ADK Component
   Tool
   Invocation Method
   OpportunityScoutAgent → Scholarship_Matching_Tool
   Inputs
   StudentProfile
   ScholarshipDataset
   Outputs
   ScholarshipMatch[]
   Validation
   • Profile valid
   • Dataset valid
   • Required fields present
   Failure Handling
   • Return empty results
   • Log failure
   • Reject malformed output

---

3. Weekly Briefing Generation Skill
   ADK Component
   Tool
   Invocation Method
   OrchestratorAgent → Weekly_Briefing_Tool
   Inputs
   StudentProfile
   RiskAssessment
   ScholarshipMatches
   AlertHistory
   Outputs
   WeeklyBriefing
   Validation
   • All required objects present
   • Structured output validation
   Failure Handling
   • Return fallback briefing
   • Log generation failure

---

D. Session Architecture
Streamlit Session
Purpose:
Maintain UI interaction state.
Contains:
Current Page
Current Request
Current Results

---

ADK Session
Purpose:
Maintain workflow execution state.
Contains:
Session ID
Workflow Type
Loaded Memory
Agent Outputs
Execution Metadata

---

Session Lifecycle
Session Creation
User submits request
↓
Create ADK Session
↓
Load memory
↓
Initialize workflow

---

Session Update
Agent execution
↓
Store outputs
↓
Store execution metadata
↓
Update state

---

Session Termination
Workflow completed
↓
Persist approved updates
↓
Close session

---

E. Memory Integration
Memory Sources
student_profile.json
Contains:
StudentProfile
activity_log.json
Contains:
ActivityLog[]
alert_history.json
Contains:
Alert[]

---

Memory Loading Process
Orchestrator Start
↓
Load student_profile.json
↓
Load activity_log.json
↓
Load alert_history.json
↓
Validate schema
↓
Inject into session context

---

Memory Passing
Orchestrator passes only required data.
Examples:
Academic Risk Agent
receives:
profile
activity log

Opportunity Scout Agent
receives:
profile

---

Update Validation
Every update follows:
Schema Validation
↓
Security Validation
↓
Update Approval
↓
Persistence

---

Persistence
Only Orchestrator writes memory.
Process:
Validated Update
↓
Write JSON
↓
Verify Write
↓
Log Event

---

F. Workflow Execution

1.  GPA Risk Assessment
    sequenceDiagram
    participant User
    participant Orchestrator
    participant AcademicRisk
    participant GPA_Tool

        User->>Orchestrator: Risk Assessment Request

        Orchestrator->>Orchestrator: Load Memory

        Orchestrator->>AcademicRisk: Assess Risk

        AcademicRisk->>GPA_Tool: Run Analysis

        GPA_Tool-->>AcademicRisk: Risk Assessment

        AcademicRisk-->>Orchestrator: Assessment

        Orchestrator-->>User: Results

---

2.  Scholarship Matching
    sequenceDiagram
    participant User
    participant Orchestrator
    participant OpportunityScout
    participant MatchTool

        User->>Orchestrator: Scholarship Request

        Orchestrator->>Orchestrator: Load Memory

        Orchestrator->>OpportunityScout: Match Scholarships

        OpportunityScout->>MatchTool: Execute Matching

        MatchTool-->>OpportunityScout: Ranked Matches

        OpportunityScout-->>Orchestrator: Matches

        Orchestrator-->>User: Results

---

3.  Weekly Briefing Generation
    sequenceDiagram
    participant Scheduler
    participant Orchestrator
    participant AcademicRisk
    participant OpportunityScout
    participant BriefingTool

        Scheduler->>Orchestrator: Weekly Trigger

        Orchestrator->>AcademicRisk: Assess Risk
        AcademicRisk-->>Orchestrator: Risk Result

        Orchestrator->>OpportunityScout: Match Scholarships
        OpportunityScout-->>Orchestrator: Matches

        Orchestrator->>BriefingTool: Generate Briefing

        BriefingTool-->>Orchestrator: Briefing

        Orchestrator-->>Scheduler: Completed

---

G. Tool Registration
GPA_Risk_Assessment_Tool
Purpose
Calculate academic risk.
Inputs
StudentProfile
Outputs
RiskAssessment
Invocation Agent
Academic Risk Agent

---

Scholarship_Matching_Tool
Purpose
Match scholarships.
Inputs
StudentProfile
ScholarshipDataset
Outputs
ScholarshipMatch[]
Invocation Agent
Opportunity Scout Agent

---

Weekly_Briefing_Tool
Purpose
Generate weekly summary.
Inputs
StudentProfile
RiskAssessment
ScholarshipMatches
AlertHistory
Outputs
WeeklyBriefing
Invocation Agent
Orchestrator Agent

---

H. Error Handling
Validation Failures
Detection:
Schema validation failure
Action:
Reject request
Log error
Return structured response
Retry:
No retry

---

Memory Failures
Detection:
Missing file
Corrupted file
Action:
Abort workflow
Return error
Retry:
1 retry

---

Dataset Failures
Detection:
Invalid scholarship dataset
Action:
Return empty matches
Retry:
1 retry

---

Agent Failures
Detection:
Timeout
Invalid output
Exception
Action:
Reject output
Retry:
Single retry
Failure sequence:
Failure
↓
Retry Once
↓
Log Error
↓
Return Safe Response

---

I. Security Integration
Input Validation
Executed before workflow starts.
Checks:
Required fields
Data types
Value ranges
Schema compliance

---

Prompt Injection Checks
Applied to:
User requests
Agent outputs
Checks:
Unexpected instructions
Memory modification attempts
System override attempts

---

Structured Outputs
All agents return:
Typed Models
Validated Schemas
No free-form memory writes allowed.

---

Orchestrator Write Gate
Only Orchestrator can write memory.
Process:
Agent Output
↓
Validation
↓
Security Check
↓
Write Approval
↓
Persistence
Sub-agents cannot directly modify memory.

---

J. Implementation Mapping
Repository File ADK Component
agents/orchestrator.py Orchestrator Agent
agents/academic_risk.py Academic Risk Agent
agents/opportunity_scout.py Opportunity Scout Agent
skills/gpa_risk_assessment.py GPA Risk Assessment Tool
skills/scholarship_matching.py Scholarship Matching Tool
skills/weekly_briefing_generation.py Weekly Briefing Tool
memory/student_profile.json Student Profile Memory
memory/activity_log.json Activity Log Memory
memory/alert_history.json Alert History Memory
models/student_profile.py Student Profile Schema
models/activity_log.py Activity Log Schema
models/alert.py Alert Schema
models/risk_assessment.py Risk Assessment Schema
models/scholarship.py Scholarship Schema
models/scholarship_match.py Scholarship Match Schema
models/weekly_briefing.py Weekly Briefing Schema
security/input_validator.py Input Validation Layer
security/output_validator.py Output Validation Layer
security/memory_guard.py Orchestrator Write Gate
data/scholarships.json Scholarship Dataset
app.py Streamlit Entry Point
config/settings.py Runtime Configuration
utils/logger.py Logging Layer
utils/file_manager.py Memory Persistence Layer
