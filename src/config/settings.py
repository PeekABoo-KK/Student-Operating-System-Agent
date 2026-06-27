"""Locked configuration for the Student OS Agent foundation layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final


DEFAULT_MODEL: Final[str] = "gemini-3.5-flash"

AGENT_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "SUCCESS",
        "FAILED",
        "PARTIAL",
        "TIMEOUT",
        "VALIDATION_ERROR",
        "ROUTING_ERROR",
    }
)

SCHOLARSHIP_SCORING_WEIGHTS: Final[dict[str, float]] = {
    "GPA": 0.4,
    "MAJOR": 0.3,
    "YEAR": 0.2,
    "TAG": 0.1,
}


@dataclass(frozen=True)
class Settings:
    """Immutable application settings for locked Phase 1 foundation."""

    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    default_model: str = DEFAULT_MODEL
    scholarship_scoring_weights: dict[str, float] = field(
        default_factory=lambda: dict(SCHOLARSHIP_SCORING_WEIGHTS)
    )
    agent_statuses: frozenset[str] = AGENT_STATUSES

    @property
    def memory_dir(self) -> Path:
        return self.project_root / "memory"

    @property
    def student_profile_path(self) -> Path:
        return self.memory_dir / "student_profile.json"

    @property
    def activity_log_path(self) -> Path:
        return self.memory_dir / "activity_log.json"

    @property
    def alert_history_path(self) -> Path:
        return self.memory_dir / "alert_history.json"

    @property
    def locked_memory_paths(self) -> tuple[Path, Path, Path]:
        return (
            self.student_profile_path,
            self.activity_log_path,
            self.alert_history_path,
        )


SETTINGS: Final[Settings] = Settings()
