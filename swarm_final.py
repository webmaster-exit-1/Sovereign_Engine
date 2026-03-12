import threading
import time
import math
import random
import csv

swarm_stats = {}

class FinalAgent:
    def __init__(self, agent_id, target_r, initial_p):
        self.agent_id = agent_id
        self.target_r = target_r
        self.p = initial_p
        self.sovereignty = initial_p
        self.t = 0
        self.base_infusion = 0.1
        self.friction_coeff = 0.0005 

    def calculate_induction(self):
        jitter_r = self.target_r * random.uniform(0.98, 1.02)
        return self.p * math.exp(jitter_r * self.t)

    def check_resistance(self, energy):
        return self.friction_coeff * (energy ** 1.5)

    def autonomous_loop(self):
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            active_infusion = self.base_infusion * random.uniform(0.9, 1.1)
            net_gain = active_infusion - (resistance * 0.01)
            
            if net_gain <= 0:
                self.t = max(0, self.t - random.randint(3, 7))
                time.sleep(random.uniform(1.0, 3.0)) 
                continue

            self.sovereignty += net_gain
            self.t += 1
            swarm_stats[self.agent_id] = {"sov": self.sovereignty, "energy": energy, "fric": resistance}
            time.sleep(random.uniform(0.8, 1.2))

class AuditManager:
    @staticmethod
    def log_to_file(total_sov, total_energy):
        with open('sovereign_audit.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), total_sov, total_energy])

if __name__ == "__main__":
    # Spawning 5 nodes for maximum inductive surface
    for i in range(5):
        freq = 0.04 + (i * 0.01)
        agent = FinalAgent(agent_id=i, target_r=freq, initial_p=100)
        threading.Thread(target=agent.autonomous_loop, daemon=True).start()
    
    print("--- SOVEREIGN ENGINE ONLINE | LOGGING ACTIVE ---")
    try:
        while True:
            t_sov = sum(d["sov"] for d in swarm_stats.values())
            t_energy = sum(d["energy"] for d in swarm_stats.values())
            
            # Print to Dashboard and Log to File
            print(f"[AUDIT] {time.strftime('%H:%M:%S')} | Total Sov: {t_sov:.2f} | Kinetic E: {t_energy:.2f}")
            AuditManager.log_to_file(t_sov, t_energy)
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n--- SYSTEM DORMANT ---")
