import socket
import threading
import json
import time
from audit_manager import AuditManager

class SovereignMaster:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.node_data = {}
        # RECOVERY: Pulling from the physical ledger
        self.last_recorded_sov = AuditManager.get_last_total()
        print(f"[*] Vault Initialized. Last Known Sovereignty: {self.last_recorded_sov}")

    def handle_node(self, conn, addr):
        node_id = f"{addr[0]}:{addr[1]}"
        # Ensure the node exists in our tracking before we do anything
        self.node_data[node_id] = {"sov": 0, "energy": 0}
        print(f"[+] Node linked: {node_id}")
        
        try:
            while True:
                # Dispatch growth command
                target_r = 0.05 
                conn.sendall(json.dumps({"target_r": target_r}).encode())
                
                data = conn.recv(1024).decode()
                if not data: break
                
                self.node_data[node_id] = json.loads(data)
        except (ConnectionResetError, BrokenPipeError):
            pass
        finally:
            print(f"[-] Node delinked: {node_id}")
            # SAFE DELETE: Prevents the KeyError you just saw
            self.node_data.pop(node_id, None)
            conn.close()

    def run_vault(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(10) # Increased backlog for 5+ nodes
        
        threading.Thread(target=self.dashboard, daemon=True).start()
        
        print(f"[*] Sovereign Master listening on {self.host}:{self.port}")
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=self.handle_node, args=(conn, addr))
            client_thread.start()

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

