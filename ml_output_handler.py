# ml_output_handler.py
# Simulates ML predictions now; later, swap with Shakeel's real output.

import random

CLASSES = ["Open", "Closed", "Blinking"]

def simulate_ml_output():
    """Return a random class, sometimes None to simulate a bad/null read."""
    if random.random() < 0.1:  # ~10% nulls to prove we skip them
        return None
    return random.choice(CLASSES)

def get_ml_output():
    """
    Hook used by main.py.
    LATER: replace this with a call to Shakeel's real model output.
    MUST return: 'Open' | 'Closed' | 'Blinking' | None
    """
    return simulate_ml_output()
