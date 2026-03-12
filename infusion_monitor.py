import time
import math

class SovereignAgent:
    def __init__(self, target_r, initial_p):
        self.target_r = target_r
        self.p = initial_p
        self.sovereignty = initial_p
        self.t = 0
        self.infusion_rate = 0.1
        self.friction_coeff = 0.0005 # Systemic Resistance Factor

    def calculate_induction(self):
        return self.p * math.exp(self.target_r * self.t)

    def check_resistance(self, energy):
        # Resistance scales quadratically with Energy (Thermal analogy)
        return self.friction_coeff * (energy ** 1.5)

    def autonomous_loop(self):
        print(f"--- PROTOCOL: RESISTANCE MANAGEMENT ACTIVE ---")
        while True:
            energy = self.calculate_induction()
            resistance = self.check_resistance(energy)
            
            # Net Infusion after Resistance
            net_gain = self.infusion_rate - (resistance * 0.01)
            
            if net_gain <= 0:
                print(f"[COLD BOOT] Resistance ({resistance:.2f}) peaked. Resetting Induction Field...")
                self.t = max(0, self.t - 5) # Draw back the 't' variable to cool the system
                time.sleep(2) # Dissipation period
                continue

            self.sovereignty += net_gain
            self.t += 1
            
            print(f"Step {self.t} | Net Sovereignty: {self.sovereignty:.2f} | Energy: {energy:.2f} | Friction: {resistance:.2f}")
            time.sleep(1)

agent = SovereignAgent(target_r=0.06, initial_p=100)
agent.autonomous_loop()
