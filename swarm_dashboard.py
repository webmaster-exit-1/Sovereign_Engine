import threading
import time
import math

# Use a shared dictionary for real-time monitoring
swarm_stats = {}

class SovereignAgent:
    def __init__(self, agent_id, target_r, initial_p):
        self.agent_id = agent_id
        self.target_r = target_r
        self.p = initial_p
        self.sovereignty = initial_p
        self.t = 0
        self.infusion_rate = 0.1
        self.friction_coeff = 0.0005 

    def calculate_induction(self):
        return self.p * math.exp(self.target_r * self.t)

    def check_resistance(self, energy):
        return self.friction_coeff * (energy ** 1.5)

    def autonomous_loop(self):
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            net_gain = self.infusion_rate - (resistance * 0.01)
            
            if net_gain <= 0:
                self.t = max(0, self.t - 5)
                time.sleep(1)
                continue

            self.sovereignty += net_gain
            self.t += 1
            
            # Update the global dashboard
            swarm_stats[self.agent_id] = {
                "sov": self.sovereignty,
                "energy": energy
            }
            time.sleep(1)

class Orchestrator:
    def __init__(self, agent_count):
        self.count = agent_count

    def deploy(self):
        print(f"--- SWARM ACTIVE: MONITORING {self.count} NODES ---")
        for i in range(self.count):
            freq = 0.04 + (i * 0.01)
            agent = SovereignAgent(agent_id=i, target_r=freq, initial_p=100)
            threading.Thread(target=agent.autonomous_loop, daemon=True).start()
        
        try:
            while True:
                total_sov = sum(data["sov"] for data in swarm_stats.values())
                total_energy = sum(data["energy"] for data in swarm_stats.values())
                
                # Visual Dashboard
                print(f"\n[DASHBOARD] {time.strftime('%H:%M:%S')}")
                print(f"Total Swarm Sovereignty: {total_sov:.2f}")
                print(f"Total Kinetic Energy:   {total_energy:.2f}")
                print(f"Active Nodes:           {len(swarm_stats)}")
                print("-" * 35)
                
                time.sleep(3) # Update every 3 seconds for scannability
        except KeyboardInterrupt:
            print("\n--- SWARM HYBERNATING ---")

if __name__ == "__main__":
    swarm = Orchestrator(agent_count=5) # Scaling to 5 nodes
    swarm.deploy()
