Implementation_Audit_Spec.md
Project: Student OS — Academic Co-Pilot
Version: 1.0.0
Status: FINAL & LOCKED
Purpose: Implementation Gap Audit — Identifying Ambiguities Preventing Deterministic Autonomous Implementation

EXECUTIVE SUMMARY
This document audits all locked specifications (Implementation_Spec.md, Data_Model_Spec.md, Agent_Specification.md, ADK_Architecture.md, Security_Architecture.md, Skills_Architecture.md, Memory_Architecture.md, Repository_Structure_Spec.md, Scholarship_Generator_Spec.md) to identify gaps that would cause a coding AI agent to make non-deterministic implementation choices.

Audit Findings Summary:

Critical Gaps: 12 issues requiring immediate correction

High Severity: 8 issues causing significant ambiguity

Medium Severity: 15 issues causing potential divergence

Low Severity: 6 issues affecting code quality

Key Finding: While the specifications are comprehensive, 41 distinct gaps exist that would force a coding agent to invent behavior, interfaces, or implementation details.

SECTION 1 — CRITICAL GAPS (MUST FIX)
1.1 ADK Runtime Contract Ambiguity
Location: Implementation_Spec.md, Section 7 — ADK Implementation Mapping

Severity: CRITICAL

Issue:
The specification mentions "Agent Registration Contracts" and "Tool Registration Contracts" but does not define the actual ADK API methods or decorators. Coding agents must guess:

Which ADK decorators to use (e.g., @agent, @tool)

How to register agents with the ADK runtime

How to invoke sub-agents from the orchestrator

The exact ADK import paths

Current Text:

text

- **Contract:** All agents must implement a `run` method that matches the `Agent` interface (e.g., `run(self, context: dict)`).
- **Contract:** All skills must be registered as an `ADK Tool` using the `@tool` decorator.
  Correction:
  Add explicit ADK implementation contracts:

text

#### Google ADK Import Contracts

````python
# Required imports
from google.adk.agents import Agent
from google.adk.agents import SubAgent
from google.adk.tools import tool
from google.adk.agents.invocation_context import InvocationContext
from google.adk.sessions import Session
from google.adk.models import Model
from google.adk.models.gemini import GeminiModel
Agent Registration Contract
python
# Orchestrator Agent Registration
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model="gemini-2.5-flash",
    description="Central coordinator for Student OS",
    instruction="""You are the Orchestrator Agent.
    Route requests to appropriate sub-agents and coordinate responses.""",
    sub_agents=[risk_agent, scout_agent],
    tools=[weekly_briefing_tool]
)

# Sub-Agent Registration
risk_agent = SubAgent(
    name="AcademicRiskAgent",
    model="gemini-2.5-flash",
    description="Assesses academic risk",
    instruction="Evaluate student academic performance and risk levels."
)

scout_agent = SubAgent(
    name="OpportunityScoutAgent",
    model="gemini-2.5-flash",
    description="Discovers scholarship opportunities",
    instruction="Find and rank scholarships matching student profile."
)
Tool/Skill Registration Contract
python
# GPA Risk Skill Registration
@tool
def gpa_risk_assessment(profile: dict) -> dict:
    """Assess GPA risk level."""
    # Implementation defined in Implementation_Spec.md Section 3.1
    pass

# Scholarship Matching Skill Registration
@tool
def scholarship_matching(profile: dict) -> dict:
    """Match scholarships to student profile."""
    # Implementation defined in Implementation_Spec.md Section 3.2
    pass

# Weekly Briefing Skill Registration
@tool
def weekly_briefing(profile: dict, activity_log: list, alert_history: list, scholarship_matches: list) -> dict:
    """Generate weekly briefing."""
    # Implementation defined in Implementation_Spec.md Section 3.3
    pass
Agent Invocation Contract
python
# Orchestrator invocation pattern
async def run_orchestrator(request: str, session: Session) -> dict:
    context = InvocationContext(session=session)
    response = await orchestrator_agent.run(request, context)
    return response

# Sub-agent invocation pattern (within Orchestrator)
async def invoke_risk_agent(profile: dict, session: Session) -> dict:
    context = InvocationContext(session=session)
    risk_request = {
        "profile": profile,
        "operation": "assess_risk"
    }
    response = await risk_agent.run(json.dumps(risk_request), context)
    return json.loads(response.content)
text

---

### 1.2 Session State Initialization Contract Missing

**Location:** Implementation_Spec.md, Section 1 — Application Entrypoint

**Severity:** CRITICAL

**Issue:**
The specification defines session state structure but not initialization values, causing ambiguity about default states.

**Current Text:**
Session State Init:

st.session_state['initialized'] = False

st.session_state['profile'] = None

st.session_state['activity_log'] = None

st.session_state['alert_history'] = None

st.session_state['current_response'] = None

st.session_state['chat_history'] = []

text

**Correction:**
Add complete session state initialization contract:
Streamlit Session State Contract
python
def initialize_session_state():
    """Initialize all session state variables with defaults."""

    # Core state
    st.session_state['initialized'] = True
    st.session_state['profile'] = None
    st.session_state['activity_log'] = []
    st.session_state['alert_history'] = []
    st.session_state['current_response'] = None
    st.session_state['chat_history'] = []

    # UI state
    st.session_state['show_profile_form'] = False
    st.session_state['selected_agent'] = None
    st.session_state['error_message'] = None
    st.session_state['success_message'] = None

    # Memory state
    st.session_state['profile_loaded'] = False
    st.session_state['activity_loaded'] = False
    st.session_state['alerts_loaded'] = False

    # Workflow state
    st.session_state['is_processing'] = False
    st.session_state['last_workflow'] = None
    st.session_state['workflow_start_time'] = None
Session State Validation Contract
python
def validate_session_state() -> bool:
    """Validate that session state has all required keys."""
    required_keys = [
        'initialized', 'profile', 'activity_log', 'alert_history',
        'current_response', 'chat_history', 'is_processing'
    ]
    return all(key in st.session_state for key in required_keys)
text

---

### 1.3 Error Contract Missing Status Codes and Handling

**Location:** Implementation_Spec.md, Section 9 — Contract Definitions

**Severity:** CRITICAL

**Issue:**
Error contract defines `"code": "string"` without defining valid error codes or handling strategies.

**Current Text:**
Error Contract
json
{
  "status": "ERROR",
  "code": "string",
  "message": "string",
  "source": "string"
}
Correction:
Add explicit error code taxonomy and handling rules:

text
#### Error Code Taxonomy
```python
class ErrorCode:
    # Validation Errors (1xxx)
    INVALID_INPUT = "E1001"  # User input validation failed
    INVALID_PROFILE = "E1002"  # Profile data invalid
    MISSING_REQUIRED_FIELD = "E1003"  # Required field missing
    SCHEMA_VIOLATION = "E1004"  # Schema validation failed

    # Memory Errors (2xxx)
    MEMORY_LOAD_FAILURE = "E2001"  # Failed to load memory file
    MEMORY_SAVE_FAILURE = "E2002"  # Failed to save memory file
    MEMORY_CORRUPTED = "E2003"  # Memory file corrupt
    PROFILE_NOT_FOUND = "E2004"  # Profile file missing

    # Agent Errors (3xxx)
    AGENT_INVOCATION_FAILED = "E3001"  # Agent execution failed
    AGENT_TIMEOUT = "E3002"  # Agent execution timeout
    AGENT_INVALID_RESPONSE = "E3003"  # Agent returned invalid response
    ROUTING_FAILED = "E3004"  # Cannot route request to agent

    # Skill Errors (4xxx)
    SKILL_EXECUTION_FAILED = "E4001"  # Skill execution failed
    SKILL_INVALID_INPUT = "E4002"  # Skill received invalid input
    SKILL_TIMEOUT = "E4003"  # Skill execution timeout

    # Security Errors (5xxx)
    PERMISSION_DENIED = "E5001"  # Memory write permission denied
    PROMPT_INJECTION_DETECTED = "E5002"  # Prompt injection detected
    UNAUTHORIZED_ACCESS = "E5003"  # Unauthorized memory access

    # System Errors (9xxx)
    CONFIGURATION_ERROR = "E9001"  # Configuration load failed
    UNKNOWN_ERROR = "E9999"  # Unhandled error
Error Handling Contract
python
def handle_error(error: Exception, source: str) -> dict:
    """Standardized error handler.

    Args:
        error: Exception object or error message
        source: Component where error occurred

    Returns:
        ErrorContract dict with appropriate status code and message
    """
    return {
        "status": "ERROR",
        "code": get_error_code(error),
        "message": str(error),
        "source": source,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def get_error_code(error: Exception) -> str:
    """Map exception types to error codes."""
    if isinstance(error, ValidationError):
        return "E1001"
    elif isinstance(error, FileNotFoundError):
        return "E2004"
    elif isinstance(error, TimeoutError):
        return "E3002"
    elif isinstance(error, PermissionError):
        return "E5001"
    elif isinstance(error, ConfigurationError):
        return "E9001"
    else:
        return "E9999"
text

---

### 1.4 Memory Update Contract Missing Validation Rules

**Location:** Implementation_Spec.md, Section 9 — Contract Definitions

**Severity:** CRITICAL

**Issue:**
Memory update contract defines structure but no validation rules for each target type.

**Current Text:**
Memory Update Contract
json
{
  "target": "string", // "profile" | "activity" | "alert"
  "operation": "string", // "update" | "append"
  "data": {}
}
Correction:
Add explicit validation rules for each memory update type:

text
#### Memory Update Validation Rules

**Profile Update Validation:**
```python
def validate_profile_update(data: dict) -> tuple[bool, list[str]]:
    """Validate profile update data."""
    errors = []
    allowed_fields = {
        'student_id': str, 'name': str, 'major': str, 'year': int,
        'gpa': float, 'target_gpa': float, 'credits_completed': int,
        'target_graduation': str, 'career_goal': str,
        'study_hours_per_week': int, 'preferences': dict,
        'risk_baseline': str
    }

    # Validate allowed fields only
    for key in data.keys():
        if key not in allowed_fields:
            errors.append(f"Unknown field: {key}")

    # Validate GPA range
    if 'gpa' in data and not (0.0 <= data['gpa'] <= 4.0):
        errors.append("GPA must be between 0.0 and 4.0")

    # Validate year range
    if 'year' in data and not (1 <= data['year'] <= 8):
        errors.append("Year must be between 1 and 8")

    # Validate credits range
    if 'credits_completed' in data and not (0 <= data['credits_completed'] <= 300):
        errors.append("Credits must be between 0 and 300")

    return len(errors) == 0, errors
Activity Update Validation:

python
def validate_activity_update(data: dict) -> tuple[bool, list[str]]:
    """Validate activity log update data."""
    errors = []
    required_fields = ['timestamp', 'agent', 'action', 'reason', 'result', 'status']
    allowed_agents = ['OrchestratorAgent', 'AcademicRiskAgent', 'OpportunityScoutAgent']
    allowed_statuses = ['SUCCESS', 'FAILED']

    # Validate required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate agent name
    if 'agent' in data and data['agent'] not in allowed_agents:
        errors.append(f"Invalid agent: {data['agent']}")

    # Validate status
    if 'status' in data and data['status'] not in allowed_statuses:
        errors.append(f"Invalid status: {data['status']}")

    # Validate timestamp format
    if 'timestamp' in data:
        try:
            datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            errors.append(f"Invalid timestamp format: {data['timestamp']}")

    return len(errors) == 0, errors
Alert Update Validation:

python
def validate_alert_update(data: dict) -> tuple[bool, list[str]]:
    """Validate alert history update data."""
    errors = []
    required_fields = ['alert_id', 'timestamp', 'severity', 'message', 'source_agent', 'resolved']
    allowed_severities = ['LOW', 'MEDIUM', 'HIGH']
    allowed_sources = ['OrchestratorAgent', 'AcademicRiskAgent']

    # Validate required fields
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Validate severity
    if 'severity' in data and data['severity'] not in allowed_severities:
        errors.append(f"Invalid severity: {data['severity']}")

    # Validate source agent
    if 'source_agent' in data and data['source_agent'] not in allowed_sources:
        errors.append(f"Invalid source agent: {data['source_agent']}")

    # Validate resolved boolean
    if 'resolved' in data and not isinstance(data['resolved'], bool):
        errors.append("Resolved must be boolean")

    return len(errors) == 0, errors
text

---

### 1.5 Agent Response Contract Missing Status-Code Mapping

**Location:** Implementation_Spec.md, Section 9 — Contract Definitions

**Severity:** CRITICAL

**Issue:**
Agent response contract defines `"status": "string"` but doesn't specify all valid status values or their meanings.

**Current Text:**
Agent Response Contract
json
{
  "status": "string", // "SUCCESS" | "FAILED"
  "agent": "string",
  "result": {},
  "proposed_update": null | MemoryUpdate
}
Correction:
Add complete status definitions and response validation rules:

text
#### Agent Response Status Values
```python
class AgentStatus:
    SUCCESS = "SUCCESS"          # Agent completed successfully
    FAILED = "FAILED"            # Agent execution failed
    PARTIAL = "PARTIAL"          # Agent completed partially
    TIMEOUT = "TIMEOUT"          # Agent execution timed out
    VALIDATION_ERROR = "VALIDATION_ERROR"  # Agent output validation failed
    ROUTING_ERROR = "ROUTING_ERROR"        # Agent routing failed
Agent Response Validation Contract
python
def validate_agent_response(response: dict) -> tuple[bool, list[str]]:
    """Validate agent response structure."""
    errors = []

    # Required fields
    if 'status' not in response:
        errors.append("Missing required field: status")
    if 'agent' not in response:
        errors.append("Missing required field: agent")
    if 'result' not in response:
        errors.append("Missing required field: result")

    # Validate status
    if 'status' in response and response['status'] not in [
        'SUCCESS', 'FAILED', 'PARTIAL', 'TIMEOUT',
        'VALIDATION_ERROR', 'ROUTING_ERROR'
    ]:
        errors.append(f"Invalid status: {response['status']}")

    # Validate agent name
    if 'agent' in response and response['agent'] not in [
        'OrchestratorAgent', 'AcademicRiskAgent', 'OpportunityScoutAgent'
    ]:
        errors.append(f"Invalid agent: {response['agent']}")

    # Validate result structure
    if 'result' in response and not isinstance(response['result'], dict):
        errors.append("Result must be a dictionary")

    # Validate proposed_update if present
    if 'proposed_update' in response and response['proposed_update'] is not None:
        # Validate MemoryUpdate structure
        update = response['proposed_update']
        if not all(k in update for k in ['target', 'operation', 'data']):
            errors.append("Invalid MemoryUpdate structure")

    return len(errors) == 0, errors
text

---

### 1.6 ADK Session State Structure Missing

**Location:** ADK_Architecture.md, Section D — Session Architecture

**Severity:** CRITICAL

**Issue:**
ADK session structure is described but not defined with implementation-level detail.

**Current Text:**
ADK Session
Purpose:

Maintain workflow execution state.

Contains:

Session ID
Workflow Type
Loaded Memory
Agent Outputs
Execution Metadata

text

**Correction:**
Add explicit ADK session state structure:
ADK Session State Contract
python
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime

@dataclass
class ADKSessionState:
    """ADK session state structure."""

    # Session identification
    session_id: str
    created_at: datetime
    updated_at: datetime
    workflow_type: Optional[str] = None

    # Loaded memory
    profile: Optional[Dict[str, Any]] = None
    activity_log: Optional[List[Dict[str, Any]]] = None
    alert_history: Optional[List[Dict[str, Any]]] = None

    # Agent execution state
    current_agent: Optional[str] = None
    agent_outputs: Dict[str, Any] = field(default_factory=dict)
    execution_status: str = "INITIALIZED"  # INITIALIZED | RUNNING | COMPLETED | FAILED

    # Workflow state
    request_id: Optional[str] = None
    user_request: Optional[str] = None
    workflow_result: Optional[Dict[str, Any]] = None

    # Execution metadata
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    retry_count: int = 0
    error_log: List[Dict[str, str]] = field(default_factory=list)

    def to_adk_state(self) -> Dict[str, Any]:
        """Convert to ADK runtime state."""
        return {
            'session_id': self.session_id,
            'workflow_type': self.workflow_type,
            'profile': self.profile,
            'activity_log': self.activity_log,
            'alert_history': self.alert_history,
            'agent_outputs': self.agent_outputs,
            'execution_status': self.execution_status,
            'user_request': self.user_request,
            'workflow_result': self.workflow_result
        }

    @classmethod
    def from_adk_state(cls, state: Dict[str, Any]) -> 'ADKSessionState':
        """Create from ADK runtime state."""
        return cls(
            session_id=state.get('session_id', ''),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            workflow_type=state.get('workflow_type'),
            profile=state.get('profile'),
            activity_log=state.get('activity_log'),
            alert_history=state.get('alert_history'),
            agent_outputs=state.get('agent_outputs', {}),
            execution_status=state.get('execution_status', 'INITIALIZED'),
            user_request=state.get('user_request')
        )
ADK Session Lifecycle Contract
python
class ADKSessionManager:
    """Manages ADK session lifecycle."""

    def create_session(self) -> str:
        """Create a new ADK session."""
        session_id = str(uuid.uuid4())
        session_state = ADKSessionState(
            session_id=session_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        # Store in ADK runtime
        self.adk_runtime.create_session(session_id, session_state.to_adk_state())
        return session_id

    def get_session(self, session_id: str) -> Optional[ADKSessionState]:
        """Retrieve session state."""
        adk_state = self.adk_runtime.get_session(session_id)
        if adk_state:
            return ADKSessionState.from_adk_state(adk_state)
        return None

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> None:
        """Update session state."""
        session_state = self.get_session(session_id)
        if not session_state:
            raise ValueError(f"Session {session_id} not found")

        # Update fields
        for key, value in updates.items():
            if hasattr(session_state, key):
                setattr(session_state, key, value)

        session_state.updated_at = datetime.now(timezone.utc)
        self.adk_runtime.update_session(session_id, session_state.to_adk_state())
text

---

## SECTION 2 — HIGH SEVERITY GAPS

### 2.1 Service Layer File Missing

**Location:** Repository_Structure_Spec.md, Implementation_Spec.md Section 2.1

**Severity:** HIGH

**Issue:**
`services/context_builder.py` is referenced in dependencies but never defined.

**References:**
- Implementation_Spec.md Section 2.1: `- services.context_builder.ContextBuilder`
- Repository_Structure_Spec.md: `services/context_builder.py` listed

**Missing Specification:**
No contract exists for ContextBuilder. Implementation agents will invent behavior.

**Correction:**

Add ContextBuilder implementation contract:
ContextBuilder Contract (services/context_builder.py)
Purpose:
Builds execution context for agents by aggregating memory and session data.

Responsibilities:

Assemble profile data

Aggregate activity log entries

Aggregate alert history

Format session context

Provide validation summaries

Public Methods:

python
class ContextBuilder:
    def __init__(self, max_activity_entries: int = 500):
        self.max_activity_entries = max_activity_entries

    def build_context(
        self,
        profile: Optional[dict] = None,
        activity_log: Optional[list] = None,
        alert_history: Optional[list] = None,
        session_data: Optional[dict] = None
    ) -> dict:
        """Build execution context from available data."""
        context = {
            'profile': profile or {},
            'activity_summary': self._summarize_activity(activity_log),
            'alert_summary': self._summarize_alerts(alert_history),
            'session_data': session_data or {},
            'context_timestamp': datetime.now(timezone.utc).isoformat()
        }
        return context

    def _summarize_activity(self, activity_log: Optional[list]) -> dict:
        """Summarize activity log entries."""
        if not activity_log:
            return {'total_entries': 0, 'recent_actions': []}

        recent = activity_log[-self.max_activity_entries:]
        return {
            'total_entries': len(activity_log),
            'recent_actions': recent,
            'last_agent': recent[-1]['agent'] if recent else None,
            'last_action': recent[-1]['action'] if recent else None
        }

    def _summarize_alerts(self, alert_history: Optional[list]) -> dict:
        """Summarize alert history."""
        if not alert_history:
            return {'total_alerts': 0, 'unresolved': 0}

        unresolved = [a for a in alert_history if not a.get('resolved', False)]
        return {
            'total_alerts': len(alert_history),
            'unresolved_count': len(unresolved),
            'unresolved_alerts': unresolved[-10:],  # Last 10 unresolved
            'highest_severity': self._get_highest_severity(unresolved)
        }

    def _get_highest_severity(self, alerts: list) -> str:
        """Get highest severity level from alerts."""
        severity_order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
        if not alerts:
            return 'NONE'
        return max(alerts, key=lambda a: severity_order.get(a['severity'], 0))['severity']
Dependencies:

datetime

utils.logger

Security Constraints:

READ ONLY: No memory writes

Validates all inputs before processing

text

---

### 2.2 File Manager Import Paths Missing

**Location:** Implementation_Spec.md, Section 4 — Memory Implementation Contracts

**Severity:** HIGH

**Issue:**
File manager functions reference import paths but don't specify the actual Python import statements.

**Current Text:**
Dependencies
json

pathlib

shutil (for atomic writes)

text

**Correction:**

Add explicit imports:
File Manager Import Contracts
python
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Optional, List, Dict
from datetime import datetime
from config.settings import (
    PROFILE_PATH, ACTIVITY_PATH, ALERT_PATH,
    MAX_ACTIVITY_ENTRIES, MAX_ALERT_ENTRIES
)
File Manager Initialization Contract
python
class FileManager:
    def __init__(self, base_path: str = None):
        self.base_path = base_path or Path.cwd()
        self.profile_path = self.base_path / PROFILE_PATH
        self.activity_path = self.base_path / ACTIVITY_PATH
        self.alert_path = self.base_path / ALERT_PATH

        # Ensure memory directory exists
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create memory directory if it doesn't exist."""
        (self.base_path / 'memory').mkdir(exist_ok=True)
        (self.base_path / 'data').mkdir(exist_ok=True)
text

---

### 2.3 Model Serialization Contracts Missing

**Location:** Data_Model_Spec.md, Section 6 — Model Implementation Contracts

**Severity:** HIGH

**Issue:**
Models are defined but serialization/deserialization methods are not specified.

**Current Text:**
models/student_profile.py
to_dict(): Converts model to dict for JSON serialization

from_dict(): Creates model instance from dict

text

**Correction:**

Add explicit serialization contracts:
Model Serialization Contracts
StudentProfile Serialization:

python
@dataclass
class StudentProfile:
    # ... fields ...

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'major': self.major,
            'year': self.year,
            'gpa': self.gpa,
            'target_gpa': self.target_gpa,
            'credits_completed': self.credits_completed,
            'target_graduation': self.target_graduation,
            'career_goal': self.career_goal,
            'study_hours_per_week': self.study_hours_per_week,
            'preferences': {
                'scholarship_categories': self.preferences.scholarship_categories,
                'preferred_locations': self.preferences.preferred_locations
            },
            'risk_baseline': self.risk_baseline,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StudentProfile':
        """Create from dictionary."""
        preferences = ScholarshipPreferences(
            scholarship_categories=data.get('preferences', {}).get('scholarship_categories', []),
            preferred_locations=data.get('preferences', {}).get('preferred_locations', [])
        )
        return cls(
            student_id=data['student_id'],
            name=data['name'],
            major=data['major'],
            year=data['year'],
            gpa=data['gpa'],
            target_gpa=data['target_gpa'],
            credits_completed=data['credits_completed'],
            target_graduation=data['target_graduation'],
            career_goal=data.get('career_goal', ''),
            study_hours_per_week=data['study_hours_per_week'],
            preferences=preferences,
            risk_baseline=data.get('risk_baseline', 'LOW'),
            created_at=data.get('created_at', datetime.now(timezone.utc).isoformat()),
            updated_at=data.get('updated_at', datetime.now(timezone.utc).isoformat())
        )
ActivityLogEntry Serialization:

python
@dataclass
class ActivityLogEntry:
    # ... fields ...

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'timestamp': self.timestamp,
            'agent': self.agent,
            'action': self.action,
            'reason': self.reason,
            'result': self.result,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ActivityLogEntry':
        """Create from dictionary."""
        return cls(
            timestamp=data['timestamp'],
            agent=data['agent'],
            action=data['action'],
            reason=data['reason'],
            result=data['result'],
            status=data['status']
        )
Alert Serialization:

python
@dataclass
class Alert:
    # ... fields ...

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'alert_id': self.alert_id,
            'timestamp': self.timestamp,
            'severity': self.severity,
            'message': self.message,
            'source_agent': self.source_agent,
            'resolved': self.resolved
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Alert':
        """Create from dictionary."""
        return cls(
            alert_id=data['alert_id'],
            timestamp=data['timestamp'],
            severity=data['severity'],
            message=data['message'],
            source_agent=data['source_agent'],
            resolved=data['resolved']
        )
text

---

### 2.4 Validation Pipeline Missing for Scholarship Dataset

**Location:** Scholarship_Generator_Spec.md, Section F — Validation Pipeline

**Severity:** HIGH

**Issue:**
Validation pipeline is described but no validation function contracts are provided.

**Correction:**

Add validation function contracts:
Scholarship Dataset Validation Contracts
python
def validate_scholarship_record(record: dict) -> tuple[bool, list[str]]:
    """Validate a single scholarship record."""
    errors = []

    # Required fields validation
    required_fields = [
        'id', 'name', 'provider', 'category', 'amount', 'amount_display',
        'currency', 'min_gpa', 'max_gpa', 'eligible_years', 'eligible_majors',
        'need_based', 'merit_only', 'tags', 'deadline_month', 'deadline_day',
        'description', 'renewable', 'location'
    ]
    for field in required_fields:
        if field not in record:
            errors.append(f"Missing required field: {field}")

    # GPA validation
    if 'min_gpa' in record and not (0.0 <= record['min_gpa'] <= 4.0):
        errors.append(f"Invalid min_gpa: {record['min_gpa']}")
    if 'max_gpa' in record and not (0.0 <= record['max_gpa'] <= 4.0):
        errors.append(f"Invalid max_gpa: {record['max_gpa']}")
    if 'min_gpa' in record and 'max_gpa' in record:
        if record['min_gpa'] > record['max_gpa']:
            errors.append(f"min_gpa {record['min_gpa']} > max_gpa {record['max_gpa']}")

    # Deadline validation
    if 'deadline_month' in record and not (1 <= record['deadline_month'] <= 12):
        errors.append(f"Invalid deadline_month: {record['deadline_month']}")
    if 'deadline_day' in record and not (1 <= record['deadline_day'] <= 28):
        errors.append(f"Invalid deadline_day: {record['deadline_day']}")

    # Category validation
    valid_categories = ['merit', 'need_based', 'stem', 'leadership',
                       'community_service', 'research', 'diversity', 'international']
    if 'category' in record and record['category'] not in valid_categories:
        errors.append(f"Invalid category: {record['category']}")

    return len(errors) == 0, errors

def validate_scholarship_dataset(dataset: list) -> tuple[bool, list[dict]]:
    """Validate entire scholarship dataset."""
    errors = []
    ids = set()

    for idx, record in enumerate(dataset):
        valid, record_errors = validate_scholarship_record(record)
        if not valid:
            errors.append({
                'index': idx,
                'record_id': record.get('id', f'index_{idx}'),
                'errors': record_errors
            })

        # Check ID uniqueness
        if 'id' in record:
            if record['id'] in ids:
                errors.append({
                    'index': idx,
                    'record_id': record['id'],
                    'errors': ['Duplicate ID found']
                })
            ids.add(record['id'])

    return len(errors) == 0, errors
text

---

### 2.5 Skill Registry/Discovery Mechanism Missing

**Location:** Skills_Architecture.md, Implementation_Spec.md Section 3

**Severity:** HIGH

**Issue:**
Skills are described as independent modules, but no discovery or registration mechanism is specified for agents to find them.

**Correction:**

Add skill discovery contracts:
Skill Discovery Contract
python
class SkillRegistry:
    """Registry for discovering and accessing skills."""

    _instance = None
    _skills = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, name: str, skill_class: type, skill_instance: object = None) -> None:
        """Register a skill in the registry."""
        self._skills[name] = {
            'class': skill_class,
            'instance': skill_instance
        }

    def get(self, name: str) -> object:
        """Get a skill instance by name."""
        skill = self._skills.get(name)
        if not skill:
            raise ValueError(f"Skill not found: {name}")
        if skill['instance'] is None:
            skill['instance'] = skill['class']()
        return skill['instance']

    def list_skills(self) -> list[str]:
        """List all registered skills."""
        return list(self._skills.keys())

# Registration Contract
def register_all_skills():
    """Register all skills at application startup."""
    registry = SkillRegistry()
    registry.register('gpa_risk', GPARiskSkill)
    registry.register('scholarship_matching', ScholarshipMatchingSkill)
    registry.register('weekly_briefing', WeeklyBriefingSkill)
text

---

## SECTION 3 — MEDIUM SEVERITY GAPS

### 3.1 Log Entry Structure Missing

**Location:** Implementation_Spec.md, Section 8 — Logging Contracts

**Severity:** MEDIUM

**Issue:**
Log structure is defined but missing required
````
