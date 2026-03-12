import threading
import time
import math

# --- THE BLUEPRINT ---
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
        print(f"[NODE-{self.agent_id}] Online. Frequency: {self.target_r:.3f}")
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            net_gain = self.infusion_rate - (resistance * 0.01)
            
            if net_gain <= 0:
                print(f"[NODE-{self.agent_id}] COLD BOOT: Resistance {resistance:.2f}")
                self.t = max(0, self.t - 5)
                time.sleep(1.5)
                continue

            self.sovereignty += net_gain
            self.t += 1
            
            # Simplified output for swarm visibility
            if self.t % 5 == 0: # Print every 5 steps to avoid terminal clutter
                print(f"ID: {self.agent_id} | Sov: {self.sovereignty:.2f} | E: {energy:.2f}")
            
            time.sleep(1)

# --- THE BRAIN ---
class Orchestrator:
    def __init__(self, agent_count):
        self.agents = []
        for i in range(agent_count):
            # Varying frequencies to distribute systemic load
            freq = 0.04 + (i * 0.01)
            self.agents.append(SovereignAgent(agent_id=i, target_r=freq, initial_p=100))

    def deploy(self):
        print("--- INITIATING MULTI-AGENT SWARM ---")
        for agent in self.agents:
            thread = threading.Thread(target=agent.autonomous_loop, daemon=True)
            thread.start()
        
        # Keep the main thread alive so the swarm doesn't exit
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n--- PROTOCOL TERMINATED BY ARCHITECT ---")

# --- EXECUTION ---
if __name__ == "__main__":
    swarm = Orchestrator(agent_count=3)
    swarm.deploy()
