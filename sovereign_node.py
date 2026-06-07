import socket
import json
import time
import math
import os
import csv
import sys

class NodeAgent:
    def __init__(self, launch_index, socket_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.launch_index = launch_index
        self.socket_path = socket_path or os.path.join(base_dir, '.runtime', 'sovereign_master.sock')
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
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(self.socket_path)
        except (ConnectionRefusedError, FileNotFoundError, OSError):
            print("[FATAL] Master is offline. Sovereignty cannot be synchronized.")
            return

        reader = client.makefile('r', encoding='utf-8', newline='\n')
        writer = client.makefile('w', encoding='utf-8', newline='\n')

        registration = {
            "launch_index": self.launch_index,
            "worker_pid": os.getpid()
        }
        writer.write(json.dumps(registration) + "\n")
        writer.flush()

        try:
            while True:
                # Receive instructions (target_r) from Master
                try:
                    data = reader.readline()
                    if not data:
                        break
                    config = json.loads(data)
                    r = config['target_r']
                except (json.JSONDecodeError, KeyError, OSError):
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
                writer.write(stats + "\n")
                writer.flush()
                time.sleep(1)
        finally:
            reader.close()
            writer.close()
            client.close()

if __name__ == "__main__":
    try:
        launch_index = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    except ValueError:
        print("[FATAL] launch_index must be a valid integer. Usage: python sovereign_node.py <launch_index>")
        raise SystemExit(1)
    node = NodeAgent(launch_index)
    node.run()
