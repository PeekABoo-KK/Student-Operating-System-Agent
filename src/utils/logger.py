from datetime import datetime, timezone
from src.utils.file_manager import FileManager


class Logger:
    """
    Central activity logger.
    MUST be used by orchestrator only.
    Writes into memory/activity_log.json
    """

    ACTIVITY_PATH = "memory/activity_log.json"

    @staticmethod
    def _now():
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def log(action: str, status: str, metadata: dict = None):
        if metadata is None:
            metadata = {}

        log_entry = {
            "log_id": f"log_{int(datetime.now().timestamp()*1000)}",
            "timestamp": Logger._now(),
            "action": action,
            "status": status,
            "metadata": metadata
        }

        # load existing logs
        try:
            logs = FileManager.read_json(Logger.ACTIVITY_PATH)
        except FileNotFoundError:
            logs = []

        # append new log
        logs.append(log_entry)

        # retention rule (deterministic)
        logs = Logger._apply_retention(logs)

        FileManager.write_json_atomic(Logger.ACTIVITY_PATH, logs)

        return log_entry

    @staticmethod
    def _apply_retention(logs: list, max_items: int = 200):
        """
        Keep only last N logs to prevent memory bloat.
        Deterministic truncation (FIFO).
        """
        if len(logs) <= max_items:
            return logs

        return logs[-max_items:]
