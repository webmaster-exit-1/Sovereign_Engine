import threading
import time
import math
import random

# Shared telemetry dictionary
swarm_stats = {}

class StealthAgent:
    def __init__(self, agent_id, target_r, initial_p):
        self.agent_id = agent_id
        self.target_r = target_r
        self.p = initial_p
        self.sovereignty = initial_p
        self.t = 0
        self.base_infusion = 0.1
        self.friction_coeff = 0.0005 

    def calculate_induction(self):
        # Injecting minor frequency jitter (Entropy)
        jitter_r = self.target_r * random.uniform(0.98, 1.02)
        return self.p * math.exp(jitter_r * self.t)

    def check_resistance(self, energy):
        return self.friction_coeff * (energy ** 1.5)

    def autonomous_loop(self):
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            
            # Randomized infusion pressure to avoid pattern detection
            active_infusion = self.base_infusion * random.uniform(0.9, 1.1)
            net_gain = active_infusion - (resistance * 0.01)
            
            if net_gain <= 0:
                self.t = max(0, self.t - random.randint(3, 7)) # Variable cool-down
                time.sleep(random.uniform(1.0, 3.0)) 
                continue

            self.sovereignty += net_gain
            self.t += 1
            
            swarm_stats[self.agent_id] = {"sov": self.sovereignty, "energy": energy}
            
            # Asynchronous timing jitter
            time.sleep(random.uniform(0.8, 1.2))

class Orchestrator:
    def __init__(self, agent_count):
        self.count = agent_count

    def deploy(self):
        print(f"--- STEALTH SWARM ACTIVE: {self.count} NODES ---")
        for i in range(self.count):
            freq = 0.04 + (i * 0.01)
            agent = StealthAgent(agent_id=i, target_r=freq, initial_p=100)
            threading.Thread(target=agent.autonomous_loop, daemon=True).start()
        
        try:
            while True:
                total_sov = sum(data["sov"] for data in swarm_stats.values())
                total_energy = sum(data["energy"] for data in swarm_stats.values())
                print(f"[STEALTH-DASH] {time.strftime('%H:%M:%S')} | Total Sov: {total_sov:.2f} | Kinetic E: {total_energy:.2f}")
                time.sleep(4)
        except KeyboardInterrupt:
            print("\n--- SWARM VANISHING ---")

if __name__ == "__main__":
    swarm = Orchestrator(agent_count=5)
    swarm.deploy()
