import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def generate_live_audit():
    print("--- SOVEREIGN VISUALIZER: OBSERVER MODE ACTIVE ---")
    while True:
        try:
            # 1. Load the latest data from the Vault
            if os.path.exists('sovereign_ledger.csv'):
                data = pd.read_csv('sovereign_ledger.csv', names=['timestamp', 'sov', 'energy'])
                
                # 2. Render the Induction Graph
                plt.figure(figsize=(10, 6))
                plt.plot(data['energy'], color='cyan', label='Kinetic Energy (Induction)')
                plt.plot(data['sov'], color='lime', label='Total Sovereignty (Accumulation)')
                
                plt.title('Sovereign Engine: Real-Time Inductive Growth')
                plt.xlabel('Audit Cycles')
                plt.ylabel('Value')
                plt.legend()
                plt.grid(True, linestyle='--', alpha=0.6)
                
                # 3. Overwrite the image for the Web-UI
                plt.savefig('sovereign_plot.png')
                plt.close()
                
                print(f"[OBSERVER] Snapshot updated: {time.strftime('%H:%M:%S')}")
            else:
                print("[WAIT] Waiting for ledger data...")
        
        except Exception as e:
            print(f"[ERROR] Visualizer glitch: {e}")
        
        # 4. Wait for the next induction cycle
        time.sleep(30)

if __name__ == "__main__":
    generate_live_audit()
