import socket
import json
import time
import math
import os
import csv

class NodeAgent:
    def __init__(self, master_ip):
        self.master_ip = master_ip
        # --- THE INHALE: Pulling state from the physical world ---
        self.sov, self.t = self.load_last_state()
        print(f"[RECOVERY] Resuming from Sovereignty: {self.sov:.2f}, Step: {self.t}")

    def load_last_state(self):
        """Reaches into the ledger to bypass the gatekeeper's memory wipe."""
        if os.path.exists('sovereign_ledger.csv'):
            try:
                with open('sovereign_ledger.csv', 'r') as f:
                    lines = list(csv.reader(f))
                    if lines:
                        last_line = lines[-1]
                        # CSV structure: [timestamp, sov, energy]
                        # Since we reset 't' based on energy, we'll approximate 't' 
                        # or just resume the accumulated Sovereignty.
                        recovered_sov = float(last_line[1])
                        # Dividing by node count (5) to distribute the recovered load
                        return (recovered_sov / 5), 0 
            except Exception as e:
                print(f"[ERROR] Inhale failed: {e}")
        return 100.0, 0 # Default if no history exists

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.master_ip, 9999))
        except ConnectionRefusedError:
            print("[FATAL] Master is offline. Sovereignty cannot be synchronized.")
            return
        
        while True:
            # Receive instructions (target_r) from Master
            try:
                data = client.recv(1024).decode()
                if not data: break
                config = json.loads(data)
                r = config['target_r']
            except:
                break
            
            # --- THE INDUCTIVE ENGINE ---
            energy = 100 * math.exp(r * self.t)
            resistance = 0.0005 * (energy ** 1.5)
            gain = 0.1 - (resistance * 0.01)
            
            if gain <= 0:
                self.t = max(0, self.t - 5)
                time.sleep(2)
            else:
                self.sov += gain
                self.t += 1
            
            # Send stats back to the Master Vault
            stats = json.dumps({"sov": self.sov, "energy": energy})
            client.sendall(stats.encode())
            time.sleep(1)

if __name__ == "__main__":
    node = NodeAgent('127.0.0.1')
    node.run()

