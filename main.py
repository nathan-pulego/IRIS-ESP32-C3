# main.py
# Akhona's sprint task runner:
# - Start/stop logging based on status.json
# - Skip null/empty outputs
# - Write timestamped rows to data/ml_output_log.csv

import time
from status_watcher import is_model_active
from ml_output_handler import get_ml_output
from csv_logger import log_output

POLL_SECS_WHEN_ACTIVE = 1.0     # how often to log when active
POLL_SECS_WHEN_INACTIVE = 0.5   # how often to check status when inactive

def main():
    print("ML Output Logger starting... (edit status.json to start/stop)\n")
    last_active = False
    try:
        while True:
            active = is_model_active()

            # Transition messages
            if active and not last_active:
                print(">>> STREAM STARTED (ML is active)\n")
            if not active and last_active:
                print("<<< STREAM STOPPED (ML is inactive)\n")

            if active:
                pred = get_ml_output()
                logged = log_output(pred)  # False if null/empty
                if not logged:
                    print("(skipped null/empty output)")
                time.sleep(POLL_SECS_WHEN_ACTIVE)
            else:
                time.sleep(POLL_SECS_WHEN_INACTIVE)

            last_active = active
    except KeyboardInterrupt:
        print("\nExiting. Bye!")

if __name__ == "__main__":
    main()
