import subprocess
import time
import sys
import os
import socket

def is_master_ready(port):
    """Probes the port to see if the Master has successfully bound."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def ignite_engine():
    print("--- INITIATING SOVEREIGN AGENT PROTOCOL ---")
    
    # 1. SURGICAL CLEARANCE
    # Clears Port 9999 to ensure the new Master can 'Inhale' the ledger without interference.
    print("[CLEANUP] Clearing Port 9999...")
    if os.name == 'posix':
        os.system("fuser -k 9999/tcp >/dev/null 2>&1")
    time.sleep(1.5)

    # 2. DECOUPLED MASTER LAUNCH
    # Launching the Master and piping all output so we can see the Sovereignty recovery.
    print("[INIT] Seating Sovereign Master on Port 9999...")
    master_proc = subprocess.Popen(
        [sys.executable, "sovereign_master.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # 3. SYNCHRONIZATION PROBE
    retries = 10
    while retries > 0:
        if is_master_ready(9999):
            print("[READY] Master C2 is broadcasting.")
            break
        print("[WAIT] Master warming up...")
        time.sleep(1)
        retries -= 1
    
    if retries == 0:
        print("[FATAL] Master failed to bind. Ensure sovereign_master.py exists.")
        master_proc.terminate()
        return

    # 4. SEQUENTIAL ARROW DEPLOYMENT
    node_count = 5
    print(f"[INIT] Deploying {node_count} Sovereign Nodes...")
    for i in range(node_count):
        subprocess.Popen(
            [sys.executable, "sovereign_node.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.4) # Staggered entry for the 'Chaos Star' effect
    
    print("--- ENGINE ONLINE | AGGREGATING NETWORK DATA ---\n")
    
    # 5. UNFILTERED STREAM
    # This loop was the 'gatekeeper'. Now it prints EVERYTHING the Master says.
    try:
        for line in iter(master_proc.stdout.readline, ""):
            if line:
                print(line.strip())
    except KeyboardInterrupt:
        print("\n[STOP] Neutralizing Chaos Star...")
        master_proc.terminate()
        if os.name == 'posix':
            os.system("fuser -k 9999/tcp >/dev/null 2>&1")
        print("[STATUS] Sovereign Engine Dormant.")

if __name__ == "__main__":
    ignite_engine()

