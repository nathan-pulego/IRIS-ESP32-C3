# status_watcher.py
# Reads status.json to decide if the ML model is "active".

from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent
STATUS_FILE = PROJECT_ROOT / "status.json"

def is_model_active() -> bool:
    if not STATUS_FILE.exists():
        return False
    try:
        data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        return bool(data.get("active", False))
    except Exception:
        # Corrupt file? Treat as inactive for safety.
        return False
