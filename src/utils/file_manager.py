import json
import os
import tempfile
from datetime import datetime, timezone


class FileManager:
    """
    Atomic JSON file manager for Student OS memory system.
    Ensures safe read/write without corruption.
    """

    @staticmethod
    def read_json(path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def write_json_atomic(path: str, data):
        """
        Atomic write using temp file + replace.
        Prevents partial writes / corruption.
        """

        dir_name = os.path.dirname(path)
        os.makedirs(dir_name, exist_ok=True)

        timestamp = datetime.now(timezone.utc).isoformat()

        # attach write metadata (debug-safe, not persisted in schema validation)
        if isinstance(data, dict):
            data["_last_written_at"] = timestamp

        with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name, encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2, ensure_ascii=False)
            temp_name = tmp.name

        os.replace(temp_name, path)
