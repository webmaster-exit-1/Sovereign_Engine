import csv
import os
from datetime import datetime

class AuditManager:
    FILE_NAME = 'sovereign_ledger.csv'

    @staticmethod
    def save_state(sovereignty, energy):
        """Writes the current state to the physical ledger."""
        file_exists = os.path.isfile(AuditManager.FILE_NAME)
        with open(AuditManager.FILE_NAME, 'a', newline='') as f:
            writer = csv.writer(f)
            # Log the timestamp, the total sovereignty, and the system energy
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                             round(sovereignty, 2), 
                             round(energy, 2)])

    @staticmethod
    def get_last_total():
        """Bypasses session memory to find the truth on the disk."""
        if not os.path.exists(AuditManager.FILE_NAME):
            return 100.0  # Baseline if ledger is deleted
        try:
            with open(AuditManager.FILE_NAME, 'r') as f:
                lines = list(csv.reader(f))
                if not lines:
                    return 100.0
                # Pull the Sovereignty value from the last recorded row
                return float(lines[-1][1])
        except Exception as e:
            print(f"[AUDIT ERROR] Could not read ledger: {e}")
            return 100.0
