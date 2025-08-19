# csv_logger.py
# Writes ML outputs to CSV/TXT, skipping null/empty values.

from pathlib import Path
import csv
import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent
CSV_PATH = PROJECT_ROOT / "data" / "ml_output_log.csv"
TXT_PATH = PROJECT_ROOT / "data" / "ml_output_log.txt"

def _ensure_files():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "EyeState"])

def log_output(eye_state: Optional[str]) -> bool:
    """Return True if a row was logged, False if skipped (null/empty)."""
    if eye_state is None:
        return False
    eye_state = str(eye_state).strip()
    if not eye_state:
        return False

    _ensure_files()
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with CSV_PATH.open("a", newline="") as f:
        csv.writer(f).writerow([ts, eye_state])

    with TXT_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts}, {eye_state}\n")

    print(f"LOGGED → {ts}, {eye_state}")
    return True
