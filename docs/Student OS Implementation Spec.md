# Implementation_Spec.md

**Project:** Student OS — Academic Co-Pilot
**Version:** 1.0.0
**Status:** FINAL & LOCKABLE
**Audience:** Coding AI Agents (Claude Code, Gemini CLI, Cursor, Codex, Devin)

---

## EXECUTIVE SUMMARY

This document provides the exhaustive implementation contracts for every file in the Student OS repository as defined by the locked architecture. All components are strictly derived from the locked source specifications.

**DEFINED IN SOURCE SPECIFICATION — NOT REDEFINED HERE:**

- All data schemas (see Data_Model_Spec.md)
- All validation rules (see Security_Architecture.md)
- All skill scoring algorithms (see Skills_Architecture.md)
- All memory ownership rules (see Memory_Architecture.md)
- All agent responsibilities (see Agent_Specification.md)
- All ADK mappings (see ADK_Architecture.md)

---

## SECTION 1 — APPLICATION ENTRYPOINT (`app.py`)

### Purpose

Main Streamlit application. Renders UI, manages session state, and coordinates user interaction with the orchestration layer.

### Responsibilities

1. Initialize Streamlit session state.
2. Render all UI components (Profile, Dashboard, Alerts, Scholarships, Briefing, Activity Log).
3. Handle all user input events.
4. Invoke Orchestrator Agent for all requests.
5. Display results and handle UI-level exceptions.

### Inputs

- User requests via forms and chat interface.
- `st.session_state` containing `profile`, `activity_log`, `alert_history`.

### Outputs

- Rendered UI components.
- Updated `st.session_state`.
- User responses.

### Dependencies

- `streamlit`
- `agents.orchestrator.OrchestratorAgent`
- `utils.file_manager`
- `security.input_validator.InputValidator`
- `config.settings`

### Public Methods

- `main()`: Entry point invoked by Streamlit.
- `_render_sidebar()`: Renders profile form and activity log.
- `_render_main_panel()`: Renders dashboard, alerts, scholarships, briefing, chat.
- `_run_startup_scan()`: Initiates proactive briefing generation.

### Preconditions

- All memory files exist (may be empty).
- Configuration is loaded.

### Postconditions

- Session state contains all loaded memory.
- UI reflects the current state of the system.

### Failure Behavior

- On memory load failure: Display critical error, use empty defaults.
- On agent invocation failure: Display error message, log error.
- On validation failure: Display user-friendly warning.

### Acceptance Criteria

- [ ] App loads without errors with or without memory files.
- [ ] All UI sections render correctly.
- [ ] User can update profile via form.
- [ ] Startup scan generates weekly briefing automatically.
- [ ] Agent activity log shows recent agent actions.

---

## SECTION 2 — AGENT IMPLEMENTATION CONTRACTS

### 2.1 OrchestratorAgent (`agents/orchestrator.py`)

#### Purpose

Central coordinator. Manages memory loading/routing/updates and orchestrates all agent interactions.

#### Responsibilities

1. Load all memory files.
2. Route requests to specialized agents.
3. Invoke the Weekly Briefing skill.
4. Aggregate results.
5. Enforce the Orchestrator Write Gate.
6. Validate all memory updates.

#### Inputs

- User request string.
- Session state containing memory objects.

#### Outputs

- Structured AgentResponse dict.
- Proposed memory updates.

#### Dependencies

- `agents.academic_risk_agent.AcademicRiskAgent`
- `agents.opportunity_scout_agent.OpportunityScoutAgent`
- `skills.weekly_briefing.skill.WeeklyBriefingSkill`
- `services.context_builder.ContextBuilder`
- `utils.file_manager`
- `utils.logger`
- `security.input_validator.InputValidator`
- `security.memory_guard.MemoryGuard`

#### Public Methods

- `__init__(self, model_name: str = "gemini-2.5-flash")`
- `run(self, request: str, session_state: dict) -> FinalResponse`

#### Private Methods

- `_route_request(self, request: str) -> WorkflowType`
- `_invoke_academic_risk(self, context: dict) -> AgentResponse`
- `_invoke_opportunity_scout(self, context: dict) -> AgentResponse`
- `_update_memory(self, proposed_updates: list[MemoryUpdate]) -> bool`

#### Preconditions

- Request is validated by InputValidator.
- Session state contains valid profile.

#### Postconditions

- Returns FinalResponse with structured results.
- All memory updates are validated.
- Activities are logged.

#### Failure Behavior

- On invalid request: Return error response.
- On agent failure: Log error, continue with partial results.
- On memory update failure: Log error, do not block response.

#### Acceptance Criteria

- [ ] Routes to AcademicRiskAgent for risk queries.
- [ ] Routes to OpportunityScoutAgent for scholarship queries.
- [ ] Generates weekly briefing on startup.
- [ ] Only Orchestrator modifies memory files.

---

### 2.2 AcademicRiskAgent (`agents/academic_risk_agent.py`)

#### Purpose

Performs academic risk analysis using the GPA Risk Assessment skill.

#### Responsibilities

1. Load student profile and alert history.
2. Invoke GPARiskSkill.
3. Generate risk assessment.
4. Propose alert creation if needed.

#### Inputs

- Student profile dict.
- Alert history list.

#### Outputs

- AgentResponse containing RiskAssessment.

#### Dependencies

- `skills.gpa_risk.skill.GPARiskSkill`

#### Public Methods

- `__init__(self)`
- `assess_risk(self, profile: dict) -> AgentResponse`

#### Preconditions

- Profile contains `gpa`, `target_gpa`.

#### Postconditions

- Returns structured AgentResponse.

#### Security Constraints

- **READ:** `student_profile.json`, `activity_log.json`, `alert_history.json`
- **WRITE:** **FORBIDDEN**

#### Acceptance Criteria

- [ ] Correctly classifies risk as LOW/MEDIUM/HIGH.
- [ ] Generates appropriate recommendations.
- [ ] Proposes alert for HIGH risk.

---

### 2.3 OpportunityScoutAgent (`agents/opportunity_scout_agent.py`)

#### Purpose

Discovers and ranks scholarship opportunities.

#### Responsibilities

1. Load student profile.
2. Load scholarship dataset.
3. Invoke ScholarshipMatchingSkill.
4. Return ranked matches.

#### Inputs

- Student profile dict.

#### Outputs

- AgentResponse containing ScholarshipMatches.

#### Dependencies

- `skills.scholarship_matching.skill.ScholarshipMatchingSkill`

#### Public Methods

- `__init__(self)`
- `find_matches(self, profile: dict) -> AgentResponse`

#### Preconditions

- Profile contains `gpa`, `major`, `year`.
- Scholarship dataset is available.

#### Postconditions

- Returns structured AgentResponse with top matches.

#### Security Constraints

- **READ:** `student_profile.json`
- **WRITE:** **FORBIDDEN**

#### Acceptance Criteria

- [ ] Filters scholarships by GPA, major, year.
- [ ] Scores and ranks matches.
- [ ] Returns at least one match for valid profiles.

---

## SECTION 3 — SKILL IMPLEMENTATION CONTRACTS

### 3.1 GPARiskSkill (`skills/gpa_risk/skill.py`)

#### Purpose

Implements GPA risk assessment business logic.

#### Inputs

- Profile dict containing `gpa` and `target_gpa`.

#### Outputs

- `RiskAssessment` dict with `risk_score`, `risk_level`, `recommendations`.

#### Algorithm

**DEFINED IN SOURCE SPECIFICATION — NOT REDEFINED HERE**

#### Public Methods

- `run(self, profile: dict) -> RiskAssessment`

#### Acceptance Criteria

- [ ] HIGH: gpa < 2.5
- [ ] LOW: gpa >= 3.5
- [ ] MEDIUM: 2.5 <= gpa < 3.5

---

### 3.2 ScholarshipMatchingSkill (`skills/scholarship_matching/skill.py`)

#### Purpose

Performs hard filtering and soft scoring against scholarship dataset.

#### Inputs

- Profile dict containing `gpa`, `major`, `year`, `preferences`.

#### Outputs

- `ScholarshipMatches` dict containing ranked matches.

#### Algorithm

**DEFINED IN SOURCE SPECIFICATION — NOT REDEFINED HERE**

#### Public Methods

- `run(self, profile: dict) -> ScholarshipMatches`

#### Acceptance Criteria

- [ ] Hard filters: GPA, major, year.
- [ ] Soft scoring: GPA (40%), Major (30%), Year (20%), Tags (10%).
- [ ] Returns top 5 matches.
- [ ] Generates reasoning for each match.

---

### 3.3 WeeklyBriefingSkill (`skills/weekly_briefing/skill.py`)

#### Purpose

Composes a weekly academic briefing.

#### Inputs

- Profile dict.
- Activity log list.
- Alert history list.
- Scholarship matches list.

#### Outputs

- `WeeklyBriefing` dict with `priorities`, `risk_summary`, `opportunity_summary`.

#### Algorithm

**DEFINED IN SOURCE SPECIFICATION — NOT REDEFINED HERE**

#### Public Methods

- `run(self, profile: dict, activity_log: list, alert_history: list, scholarship_matches: list) -> WeeklyBriefing`

#### Acceptance Criteria

- [ ] Prioritizes risk alerts first.
- [ ] Prioritizes scholarship deadlines second.
- [ ] Generates academic recommendations third.

---

## SECTION 4 — MEMORY IMPLEMENTATION CONTRACTS (`utils/file_manager.py`)

### Purpose

Handles JSON file I/O with atomic writes and consistency verification.

### Inputs

- File path strings.
- Data to persist.

### Outputs

- Loaded data (dict/list) or None on failure.
- Boolean success/failure for writes.

### Dependencies

- `json`
- `pathlib`
- `shutil` (for atomic writes)

### Public Methods

- `load_json(file_path: str) -> Any`
- `save_json(file_path: str, data: Any) -> bool`
- `load_profile() -> dict`
- `save_profile(profile_data: dict) -> bool`
- `load_activity() -> list`
- `save_activity(activity_data: list) -> bool`
- `load_alerts() -> list`
- `save_alerts(alert_data: list) -> bool`

### Failure Behavior

- **File not found:** Return None, log WARNING.
- **Invalid JSON:** Log ERROR, return None.
- **Write failure:** Log ERROR, return False.

### Atomic Write Strategy

1. Write to `{file_path}.tmp`.
2. Verify `tmp` file is valid JSON.
3. Use `shutil.move(tmp_path, file_path)`.

### Acceptance Criteria

- [ ] Files load correctly when present.
- [ ] Missing files return None without errors.
- [ ] Writes are atomic and don't corrupt data.

---

## SECTION 5 — SECURITY IMPLEMENTATION CONTRACTS

### 5.1 InputValidator (`security/input_validator.py`)

#### Purpose

Validates all user inputs before agent execution.

#### Public Methods

- `validate_user_input(request: str) -> tuple[bool, str]`
  - Checks: Empty, max length (2000), prompt injection patterns.
- `validate_profile_update(update: dict) -> tuple[bool, list]`
  - Checks: GPA range, credits range, enum values.

#### Failure Behavior

- Returns `(False, "Error message")` for validation failures.

#### Acceptance Criteria

- [ ] Rejects empty input.
- [ ] Rejects prompt injection patterns.
- [ ] Rejects invalid GPA values.

---

### 5.2 OutputValidator (`security/output_validator.py`)

#### Purpose

Validates all agent responses.

#### Public Methods

- `validate_agent_response(response: dict) -> bool`
  - Checks: Required keys, status field, result structure.

#### Failure Behavior

- Logs ERROR, returns False.

#### Acceptance Criteria

- [ ] Validates all agent responses.
- [ ] Rejects malformed responses.

---

### 5.3 MemoryGuard (`security/memory_guard.py`)

#### Purpose

Enforces the Orchestrator Write Gate.

#### Public Methods

- `check_write_privilege(agent_name: str, file_name: str) -> bool`
  - Returns True only for OrchestratorAgent.
- `validate_memory_update(file_name: str, data: Any) -> bool`
  - Validates data against appropriate schema.

#### Failure Behavior

- Logs ERROR, returns False.

#### Acceptance Criteria

- [ ] Only Orchestrator can write.
- [ ] Validates updates against schemas.

---

## SECTION 6 — MODEL IMPLEMENTATION CONTRACTS

**DEFINED IN SOURCE SPECIFICATION — NOT REDEFINED HERE**

All models are defined in Data_Model_Spec.md and must be implemented as Python dataclasses or Pydantic models.

### Models Directory Structure

- `models/student_profile.py`: StudentProfile, ScholarshipPreferences
- `models/activity_log.py`: ActivityLogEntry
- `models/alert.py`: Alert

---

## SECTION 7 — CONFIGURATION CONTRACTS (`config/settings.py`)

### Purpose

Central configuration for the application.

### Constants

- `MEMORY_PATH`: `"memory/"`
- `PROFILE_PATH`: `"memory/student_profile.json"`
- `ACTIVITY_PATH`: `"memory/activity_log.json"`
- `ALERT_PATH`: `"memory/alert_history.json"`
- `DATASET_PATH`: `"data/scholarships.json"`
- `MAX_USER_INPUT_LENGTH`: `2000`
- `MAX_ACTIVITY_ENTRIES`: `500`
- `MAX_ALERT_ENTRIES`: `200`
- `MODEL_NAME`: `"gemini-2.5-flash"`

---

## SECTION 8 — LOGGING CONTRACTS (`utils/logger.py`)

### Purpose

Central logging for all components.

### Public Methods

- `log_event(component: str, action: str, result: str, status: str, metadata: dict = None) -> None`

### Log Structure

- `component`: Component name (e.g., "OrchestratorAgent").
- `action`: Action performed (e.g., "route_request").
- `result`: Result message.
- `status`: "SUCCESS" or "FAILED".
- `metadata`: Optional dict for additional context.
- `timestamp`: ISO 8601 UTC timestamp.

### Log Levels

- **ERROR**: Used for failures.
- **WARNING**: Used for recoverable issues.
- **INFO**: Used for normal operations.

---

## SECTION 9 — CONTRACT DEFINITIONS

### Request Contract

```json
{
  "request_id": "string",
  "type": "string", // "risk_assessment" | "scholarship_search" | "weekly_briefing" | "startup"
  "payload": {}
}
Agent Response Contract
json
{
  "status": "string", // "SUCCESS" | "FAILED"
  "agent": "string",
  "result": {},
  "proposed_update": null | MemoryUpdate
}
Final Response Contract
json
{
  "status": "string", // "SUCCESS" | "PARTIAL" | "FAILED"
  "message": "string",
  "results": {},
  "memory_updates": []
}
Memory Update Contract
json
{
  "target": "string", // "profile" | "activity" | "alert"
  "operation": "string", // "update" | "append"
  "data": {}
}
Error Contract
json
{
  "status": "ERROR",
  "code": "string",
  "message": "string",
  "source": "string"
}
SECTION 10 — SECURITY MATRICES
Read/Write Permission Matrix
File	Orchestrator	AcademicRisk	OpportunityScout
student_profile.json	READ/WRITE	READ	READ
activity_log.json	READ/WRITE	READ	READ
alert_history.json	READ/WRITE	READ	READ
Validation Matrix
File	Schema Validator	Invoked By
student_profile.json	InputValidator.validate_profile_update()	MemoryGuard
activity_log.json	OutputValidator.validate_agent_response()	MemoryGuard
alert_history.json	OutputValidator.validate_agent_response()	MemoryGuard

SECTION 11 — EXECUTION STATE FLOW
Flow: Risk Assessment
text
User Request → Orchestrator._route_request()
    → Orchestrator._invoke_academic_risk()
        → AcademicRiskAgent.assess_risk()
            → GPARiskSkill.run()
    → Orchestrator._update_memory()
        → MemoryGuard.validate_memory_update()
            → InputValidator.validate_profile_update()
        → file_manager.save_*()
    → Orchestrator._format_response()
Flow: Scholarship Search
text
User Request → Orchestrator._route_request()
    → Orchestrator._invoke_opportunity_scout()
        → OpportunityScoutAgent.find_matches()
            → ScholarshipMatchingSkill.run()
    → Orchestrator._format_response()
Flow: Weekly Briefing
text
Startup → Orchestrator._run_startup_scan()
    → Orchestrator._invoke_academic_risk()
    → Orchestrator._invoke_opportunity_scout()
    → WeeklyBriefingSkill.run()
        → GPARiskSkill.run()
        → ScholarshipMatchingSkill.run()
    → Orchestrator._format_response()

SECTION 12 — IMPLEMENTATION SEQUENCE
Phase 1: Foundation (Days 1-2)
Create repository structure.

Create config/settings.py.

Create models (dataclasses).

Phase 2: Memory Layer (Day 3)
Implement utils/file_manager.py.

Implement utils/logger.py.

Create empty JSON files.

Phase 3: Security Layer (Days 4-5)
Implement security/input_validator.py.

Implement security/output_validator.py.

Implement security/memory_guard.py.

Phase 4: Skills (Days 6-8)
Implement skills/gpa_risk/skill.py.

Implement skills/scholarship_matching/skill.py.

Implement skills/weekly_briefing/skill.py.

Phase 5: Agents (Days 9-11)
Implement agents/academic_risk_agent.py.

Implement agents/opportunity_scout_agent.py.

Implement agents/orchestrator.py.

Phase 6: UI (Days 12-13)
Implement app.py.

Implement all UI components.

Phase 7: Testing (Day 14)
Implement unit tests.

Implement integration tests.

Perform end-to-end testing.

SECTION 13 — DETERMINISM RULES
All agents must produce deterministic outputs for the same inputs.

Skill algorithms must not rely on random values.

UUID generation for request IDs should use uuid.uuid4().

Timestamps should use datetime.now(timezone.utc).isoformat().

Sorting must be deterministic (tie-break by ID).

File operations must be atomic.

QUALITY GATE CHECKLIST
No new files introduced.

No new agents introduced.

No new skills introduced.

No new memory components introduced.

No schemas modified.

No repository structure modified.

No ADK APIs invented.

No dependencies invented.

Every repository file has implementation contracts.

Every method has signatures and return types.

Every validation rule is explicit.

Every error path is defined.

All schema definitions reference Data_Model_Spec.md.

All algorithm definitions reference source specifications.

APPENDIX: FILE COMPLIANCE MATRIX
File	Purpose	Inputs	Outputs	Dependencies
app.py	UI Entrypoint	User requests, session state	UI, updates	orchestrator.py, file_manager.py
orchestrator.py	Coordinator	Requests, memory	Responses, updates	agents, skills, file_manager.py
academic_risk_agent.py	Risk Analysis	Profile	RiskAssessment	gpa_risk skill
opportunity_scout_agent.py	Scholarship Search	Profile	ScholarshipMatches	scholarship_matching skill
gpa_risk/skill.py	Risk Logic	Profile	RiskAssessment	None
scholarship_matching/skill.py	Matching Logic	Profile	ScholarshipMatches	scholarships.json
weekly_briefing/skill.py	Briefing Logic	Profile, logs, alerts, matches	WeeklyBriefing	gpa_risk, scholarship_matching
file_manager.py	Memory I/O	File paths, data	Data, success	json, pathlib, shutil
input_validator.py	Input Validation	User input, profile updates	Validation results	settings.py
output_validator.py	Output Validation	Agent responses	Validation results	None
memory_guard.py	Write Gate	Agent name, file name, data	Permission, validation	input_validator.py, output_validator.py
logger.py	Logging	Component, action, result, status	Log entry	datetime
settings.py	Configuration	Environment	Constants	os, dotenv
student_profile.py	Profile Model	N/A	StudentProfile dataclass	None
activity_log.py	Activity Model	N/A	ActivityLogEntry dataclass	None
alert.py	Alert Model	N/A	Alert dataclass	None
```
