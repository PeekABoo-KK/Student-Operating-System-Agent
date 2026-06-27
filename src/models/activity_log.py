from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone

@dataclass
class ActivityLogEntry:
    timestamp: str
    agent: str
    action: str
    reason: str
    result: Any
    status: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert ActivityLogEntry to a dictionary compatible with activity_log.json."""
        return {
            "timestamp": self.timestamp,
            "agent": self.agent,
            "action": self.action,
            "reason": self.reason,
            "result": self.result,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActivityLogEntry":
        """Create ActivityLogEntry from a dictionary."""
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        timestamp = data.get("timestamp") or now_iso

        return cls(
            timestamp=timestamp,
            agent=data["agent"],
            action=data["action"],
            reason=data["reason"],
            result=data["result"],
            status=data["status"]
        )
