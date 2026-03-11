import os
import requests
from dotenv import load_dotenv

load_dotenv()
SYSTEM_ID = os.getenv("SYSTEM_ID", "DEFAULT_ID")
BASE_URL = f"https://g.co/gemini/share/{SYSTEM_ID}/files"

def initialize_memory():
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

# Call it at the start of your script
initialize_memory()

def sync_system():
    files = ["Sovereign_engine.html", "the_archive.csv", "processor.py"]
    for file in files:
        print(f"Syncing {file}...")
        r = requests.get(f"{BASE_URL}/{file}")
        with open(file, 'wb') as f:
            f.write(r.content)
    print("Sovereign System: ONLINE and SYNCED.")

if __name__ == "__main__":
    sync_system()
