import socket
import threading
import json
import time
import os
from audit_manager import AuditManager

class SovereignMaster:
    def __init__(self, socket_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.runtime_dir = os.path.join(base_dir, '.runtime')
        self.socket_path = socket_path or os.path.join(self.runtime_dir, 'sovereign_master.sock')
        self.node_data = {}
        # RECOVERY: Pulling from the physical ledger
        self.last_recorded_sov = AuditManager.get_last_total()
        print(f"[*] Vault Initialized. Last Known Sovereignty: {self.last_recorded_sov}")

    def handle_node(self, conn):
        node_id = None
        reader = conn.makefile('r', encoding='utf-8', newline='\n')
        writer = conn.makefile('w', encoding='utf-8', newline='\n')

        try:
            handshake_line = reader.readline()
            if not handshake_line:
                return

            registration = json.loads(handshake_line)
            launch_index = int(registration['launch_index'])
            worker_pid = int(registration['worker_pid'])
            node_id = f"worker-{launch_index}:pid-{worker_pid}"

            # Ensure the node exists in our tracking before we do anything
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
                writer.write(json.dumps({"target_r": target_r}) + "\n")
                writer.flush()

                data = reader.readline()
                if not data:
                    break

                payload = json.loads(data)
                payload["launch_index"] = launch_index
                payload["worker_pid"] = worker_pid
                self.node_data[node_id] = payload
        except (ConnectionResetError, BrokenPipeError, json.JSONDecodeError, KeyError, ValueError, OSError):
            pass
        finally:
            if node_id:
                print(f"[-] Node delinked: {node_id}")
                # SAFE DELETE: Prevents the KeyError you just saw
                self.node_data.pop(node_id, None)
            try:
                reader.close()
                writer.close()
            except OSError:
                pass
            conn.close()

    def run_vault(self):
        os.makedirs(self.runtime_dir, exist_ok=True)
        os.chmod(self.runtime_dir, 0o700)
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)

        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        os.chmod(self.socket_path, 0o600)
        server.listen(5)

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
            if self.node_data:
                # Summing contributions + adding the Inhaled history
                current_session_sov = sum(d.get('sov', 0) for d in self.node_data.values())
                # If nodes are fresh, we add the recovery value to the session total
                total_sov = current_session_sov if current_session_sov > self.last_recorded_sov else (self.last_recorded_sov + current_session_sov)
                
                total_energy = sum(d.get('energy', 0) for d in self.node_data.values())
                
                # Physical Save
                AuditManager.save_state(total_sov, total_energy)
                
                print("\n" + "="*35)
                print(f" GLOBAL SOVEREIGNTY: {total_sov:.2f}")
                print(f" SYSTEM ENERGY:     {total_energy:.2f}")
                print(f" ACTIVE NODES:      {len(self.node_data)}")
                print("="*35)
            else:
                print(f"[IDLE] Searching Ledger... (Last: {self.last_recorded_sov})", end='\r')
            
            time.sleep(1)

if __name__ == "__main__":
    master = SovereignMaster()
    master.run_vault()
