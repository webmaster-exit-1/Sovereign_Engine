import subprocess
import time
import sys
import os
import socket
from ipc_contract import (
    BASE_DIR,
    RUNTIME_DIR,
    SOCKET_PATH,
    MAX_WORKERS,
    READINESS_TIMEOUT,
    READINESS_PROBE_INTERVAL,
)

def cleanup_runtime_socket(abort_if_active=True):
    if not os.path.exists(SOCKET_PATH):
        return True

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe_sock:
        probe_sock.settimeout(READINESS_PROBE_INTERVAL)
        try:
            probe_sock.connect(SOCKET_PATH)
            if abort_if_active:
                print(f"[FATAL] Active engine detected on {SOCKET_PATH}. Aborting execution.")
            return False
        except (ConnectionRefusedError, FileNotFoundError, OSError):
            try:
                os.unlink(SOCKET_PATH)
                print(f"[INFO] Cleared stale socket file: {SOCKET_PATH}")
            except FileNotFoundError:
                pass
            return True

def is_master_ready(socket_path):
    """Probes the AF_UNIX socket path to see if the Master has successfully bound."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(READINESS_PROBE_INTERVAL)
        try:
            s.connect(socket_path)
            return True
        except OSError:
            return False

def ignite_engine():
    print("--- INITIATING SOVEREIGN AGENT PROTOCOL ---")
    if os.name != "posix":
        print("[FATAL] activate_engine.py requires POSIX/Linux AF_UNIX support.")
        return

    # 1. SURGICAL CLEARANCE
    print(f"[CLEANUP] Preparing runtime socket at {SOCKET_PATH}...")
    os.makedirs(RUNTIME_DIR, exist_ok=True)
    os.chmod(RUNTIME_DIR, 0o700)
    if not cleanup_runtime_socket():
        return

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
    deadline = time.monotonic() + READINESS_TIMEOUT

    while time.monotonic() < deadline:
        if is_master_ready(SOCKET_PATH):
            print("[READY] Master C2 is broadcasting over AF_UNIX.")
            break
        print("[WAIT] Master warming up...")
        time.sleep(READINESS_PROBE_INTERVAL)
    else:
        print("[FATAL] Master failed to bind. Ensure sovereign_master.py exists.")
        master_proc.terminate()
        cleanup_runtime_socket(abort_if_active=False)
        return

    # 4. SEQUENTIAL ARROW DEPLOYMENT
    node_count = MAX_WORKERS
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
        cleanup_runtime_socket(abort_if_active=False)
        print("[STATUS] Sovereign Engine Dormant.")

if __name__ == "__main__":
    ignite_engine()
