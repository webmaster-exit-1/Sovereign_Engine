import os
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()
SYSTEM_ID = os.getenv("SYSTEM_ID", "DEFAULT_ID")

def initialize_memory():
    """
    Ensures core ledger files exist locally with proper headers.
    If a file was corrupted by a 404 sync, delete it manually 
    and this function will recreate it clean.
    """
    files_to_check = {
        "the_archive.csv": "timestamp,event_type,content,importance_score\n",
        "sovereign_ledger.csv": "entry_id,goal_id,status,last_update\n",
        "sovereign_audit.csv": "timestamp,action,module,result\n"
    }
    
    for filename, headers in files_to_check.items():
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(headers)
            print(f"Initialized new memory stream: {filename}")
        else:
            # Check for 404 poisoning (HTML content in a CSV)
            with open(filename, "r") as f:
                first_line = f.readline()
                if "<html" in first_line.lower() or "<!doctype" in first_line.lower():
                    print(f"WARNING: {filename} appears corrupted by 404 sync. Re-initializing.")
                    with open(filename, "w") as wf:
                        wf.write(headers)

def start_engine():
    """
    Replaces the old sync_system. 
    Runs the engine in Local-First Sovereign mode.
    """
    print(f"System ID: {SYSTEM_ID}")
    print("Sovereign Mode: ONLINE (Local-Only). External sync bypassed.")

if __name__ == "__main__":
    # 1. Ensure memory structures are intact
    initialize_memory()
    
    # 2. Start the local engine
    start_engine()
