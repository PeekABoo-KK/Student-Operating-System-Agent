from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime, timezone

@dataclass
class Alert:
    alert_id: str
    timestamp: str
    severity: str
    message: str
    source_agent: str
    resolved: bool

    def to_dict(self) -> Dict[str, Any]:
        """Convert Alert to a dictionary compatible with alert_history.json."""
        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "source_agent": self.source_agent,
            "resolved": self.resolved
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Alert":
        """Create Alert from a dictionary."""
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        timestamp = data.get("timestamp") or now_iso
        resolved = data.get("resolved")
        if resolved is None:
            resolved = False
        else:
            resolved = bool(resolved)

        return cls(
            alert_id=data["alert_id"],
            timestamp=timestamp,
            severity=data["severity"],
            message=data["message"],
            source_agent=data["source_agent"],
            resolved=resolved
        )
