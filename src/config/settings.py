import os
from pathlib import Path

# Base workspace directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Persistent memory directories and files (Strictly 3 memory files)
MEMORY_PATH = "memory/"
PROFILE_PATH = "memory/student_profile.json"
ACTIVITY_PATH = "memory/activity_log.json"
ALERT_PATH = "memory/alert_history.json"

# Scholarship dataset path (as specified by Implementation_Stages.md Phase 1/5)
DATASET_PATH = "src/mcp_server/data/scholarships.json"

# Security constraints
MAX_USER_INPUT_LENGTH = 2000
MAX_ACTIVITY_ENTRIES = 500
MAX_ALERT_ENTRIES = 200

# LLM Engine Configuration
MODEL_NAME = "gemini-3.5-flash"

# Resolve absolute paths helpers
def get_absolute_path(relative_path: str) -> str:
    """Helper function to resolve a relative path to absolute workspace path."""
    return str(BASE_DIR / relative_path)
