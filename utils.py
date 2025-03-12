# utils.py
import time

def wait(seconds: int):
    """Pauses the execution for given seconds."""
    print(f"[INFO] Waiting for {seconds} seconds...")
    time.sleep(seconds)