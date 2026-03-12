import threading
import time
import math
import random

swarm_stats = {}

class GovernedAgent:
    def __init__(self, agent_id, target_r, initial_p):
        self.agent_id = agent_id
        self.target_r = target_r # This is now dynamic
        self.p = initial_p
        self.sovereignty = initial_p
        self.t = 0
        self.base_infusion = 0.1
        self.friction_coeff = 0.0005 

    def calculate_induction(self):
        return self.p * math.exp(self.target_r * self.t)

    def check_resistance(self, energy):
        return self.friction_coeff * (energy ** 1.5)

    def autonomous_loop(self):
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            net_gain = (self.base_infusion * random.uniform(0.9, 1.1)) - (resistance * 0.01)
            
            if net_gain <= 0:
                self.t = max(0, self.t - random.randint(3, 7))
                time.sleep(2)
                continue

            self.sovereignty += net_gain
            self.t += 1
            swarm_stats[self.agent_id] = {"sov": self.sovereignty, "energy": energy, "r": self.target_r}
            time.sleep(1)

class Orchestrator:
    def __init__(self, agent_count):
        self.agents = []
        for i in range(agent_count):
            freq = 0.04 + (i * 0.01)
            self.agents.append(GovernedAgent(i, freq, 100))

    def deploy(self):
        print("--- INITIATING GOVERNED SWARM ---")
        for agent in self.agents:
            threading.Thread(target=agent.autonomous_loop, daemon=True).start()
        
        try:
            while True:
                t_sov = sum(d["sov"] for d in swarm_stats.values())
                t_energy = sum(d["energy"] for d in swarm_stats.values())
                
                # --- GOVERNOR LOGIC ---
                if t_energy > 3500:
                    print(f"\n[GOVERNOR] High Kinetic Heat ({t_energy:.2f}). Throttling all nodes...")
                    for a in self.agents: a.target_r *= 0.95
                elif t_energy < 1500 and t_energy > 0:
                    print(f"\n[GOVERNOR] Field Stable. Increasing Inductive Pressure...")
                    for a in self.agents: a.target_r *= 1.05

                print(f"[DASHBOARD] {time.strftime('%H:%M:%S')} | Total Sov: {t_sov:.2f} | Kinetic E: {t_energy:.2f}")
                time.sleep(10) # 10s Governance Cycle
        except KeyboardInterrupt:
            print("\n--- SYSTEM DORMANT ---")

if __name__ == "__main__":
    swarm = Orchestrator(5)
    swarm.deploy()
