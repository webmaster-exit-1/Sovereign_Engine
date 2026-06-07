import subprocess
import time
import sys
import os
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUNTIME_DIR = os.path.join(BASE_DIR, '.runtime')
SOCKET_PATH = os.path.join(RUNTIME_DIR, 'sovereign_master.sock')
TIMEOUT_BUDGET_SECONDS = 5.0
PROBE_INTERVAL_SECONDS = 0.25

def cleanup_runtime_socket():
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

def is_master_ready(socket_path):
    """Probes the AF_UNIX socket path to see if the Master has successfully bound."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(PROBE_INTERVAL_SECONDS)
        try:
            s.connect(socket_path)
            return True
        except OSError:
            return False

def ignite_engine():
    print("--- INITIATING SOVEREIGN AGENT PROTOCOL ---")

    # 1. SURGICAL CLEARANCE
    print(f"[CLEANUP] Preparing runtime socket at {SOCKET_PATH}...")
    os.makedirs(RUNTIME_DIR, exist_ok=True)
    os.chmod(RUNTIME_DIR, 0o700)
    cleanup_runtime_socket()

    # 2. DECOUPLED MASTER LAUNCH
    # Launching the Master and piping all output so we can see the Sovereignty recovery.
    print(f"[INIT] Seating Sovereign Master on {SOCKET_PATH}...")
    master_proc = subprocess.Popen(
        [sys.executable, "sovereign_master.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=BASE_DIR
    )

    # 3. SYNCHRONIZATION PROBE
    deadline = time.monotonic() + TIMEOUT_BUDGET_SECONDS

    while time.monotonic() < deadline:
        if is_master_ready(SOCKET_PATH):
            print("[READY] Master C2 is broadcasting over AF_UNIX.")
            break
        print("[WAIT] Master warming up...")
        time.sleep(PROBE_INTERVAL_SECONDS)
    else:
        print("[FATAL] Master failed to bind. Ensure sovereign_master.py exists.")
        master_proc.terminate()
        cleanup_runtime_socket()
        return

    # 4. SEQUENTIAL ARROW DEPLOYMENT
    node_count = 5
    print(f"[INIT] Deploying {node_count} Sovereign Nodes...")
    # Launch indices are intentionally 1-based for human-readable worker IDs.
    for i in range(1, node_count + 1):
        subprocess.Popen(
            [sys.executable, "sovereign_node.py", str(i)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=BASE_DIR
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
        cleanup_runtime_socket()
        print("[STATUS] Sovereign Engine Dormant.")

if __name__ == "__main__":
    ignite_engine()
