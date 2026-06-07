import socket
import threading
import json
import time
import os
from audit_manager import AuditManager
from ipc_contract import (
    RUNTIME_DIR,
    SOCKET_PATH,
    JSON_FRAME_DELIMITER,
    SOCKET_BACKLOG,
)

class SovereignMaster:
    def __init__(self, socket_path=None):
        self.runtime_dir = RUNTIME_DIR
        self.socket_path = socket_path or SOCKET_PATH
        self.node_data = {}
        self.node_data_lock = threading.Lock()
        # RECOVERY: Pulling from the physical ledger
        self.last_recorded_sov = AuditManager.get_last_total()
        print(f"[*] Vault Initialized. Last Known Sovereignty: {self.last_recorded_sov}")

    def handle_node(self, conn):
        node_id = None
        reader = conn.makefile('r', encoding='utf-8', newline=JSON_FRAME_DELIMITER)
        writer = conn.makefile('w', encoding='utf-8', newline=JSON_FRAME_DELIMITER)

        try:
            handshake_line = reader.readline()
            if not handshake_line:
                return

            registration = json.loads(handshake_line)
            launch_index = int(registration['launch_index'])
            worker_pid = int(registration['worker_pid'])
            node_id = f"worker-{launch_index}:pid-{worker_pid}"

            # Ensure the node exists in our tracking before we do anything
            with self.node_data_lock:
                self.node_data[node_id] = {
                    "sov": 0,
                    "energy": 0,
                    "launch_index": launch_index,
                    "worker_pid": worker_pid
                }
            print(f"[+] Node linked: {node_id}")

            while True:
                # Dispatch growth command
                target_r = 0.05
                writer.write(json.dumps({"target_r": target_r}) + JSON_FRAME_DELIMITER)
                writer.flush()

                data = reader.readline()
                if not data:
                    break

                payload = json.loads(data)
                payload["launch_index"] = launch_index
                payload["worker_pid"] = worker_pid
                with self.node_data_lock:
                    self.node_data[node_id] = payload
        except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError, KeyError, ValueError, OSError):
            pass
        finally:
            if node_id:
                print(f"[-] Node delinked: {node_id}")
                # SAFE DELETE: Prevents the KeyError you just saw
                with self.node_data_lock:
                    self.node_data.pop(node_id, None)
            try:
                reader.close()
                writer.close()
            except OSError:
                pass
            conn.close()

    def run_vault(self):
        if os.name != "posix":
            print("[FATAL] Sovereign Master requires POSIX/Linux AF_UNIX support.")
            return

        os.makedirs(self.runtime_dir, exist_ok=True)
        os.chmod(self.runtime_dir, 0o700)
        if os.path.exists(self.socket_path):
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe_sock:
                probe_sock.settimeout(0.25)
                try:
                    probe_sock.connect(self.socket_path)
                    print("[FATAL] Another orchestrator instance is actively running on this socket path.")
                    return
                except (ConnectionRefusedError, FileNotFoundError, OSError):
                    try:
                        os.unlink(self.socket_path)
                    except FileNotFoundError:
                        pass

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        original_umask = os.umask(0o177)
        try:
            server.bind(self.socket_path)
            os.chmod(self.socket_path, 0o600)
        finally:
            os.umask(original_umask)
        server.listen(SOCKET_BACKLOG)

        threading.Thread(target=self.dashboard, daemon=True).start()

        print(f"[*] Sovereign Master listening on {self.socket_path}")
        try:
            while True:
                conn, _ = server.accept()
                client_thread = threading.Thread(target=self.handle_node, args=(conn,))
                client_thread.start()
        finally:
            server.close()
            if os.path.exists(self.socket_path):
                os.unlink(self.socket_path)

    def dashboard(self):
        while True:
            with self.node_data_lock:
                node_snapshot = list(self.node_data.items())

            if node_snapshot:
                # Summing contributions + adding the Inhaled history
                current_session_sov = sum(d.get('sov', 0) for _, d in node_snapshot)
                # If nodes are fresh, we add the recovery value to the session total
                total_sov = current_session_sov if current_session_sov > self.last_recorded_sov else (self.last_recorded_sov + current_session_sov)
                
                total_energy = sum(d.get('energy', 0) for _, d in node_snapshot)
                
                # Physical Save
                AuditManager.save_state(total_sov, total_energy)
                
                print("\n" + "="*35)
                print(f" GLOBAL SOVEREIGNTY: {total_sov:.2f}")
                print(f" SYSTEM ENERGY:     {total_energy:.2f}")
                print(f" ACTIVE NODES:      {len(node_snapshot)}")
                print("="*35)
            else:
                print(f"[IDLE] Searching Ledger... (Last: {self.last_recorded_sov})", end='\r')
            
            time.sleep(1)

if __name__ == "__main__":
    master = SovereignMaster()
    master.run_vault()
