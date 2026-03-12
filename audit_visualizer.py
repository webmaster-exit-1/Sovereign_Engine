import pandas as pd
import matplotlib.pyplot as plt

def generate_report():
    try:
        # Load the Sovereign Audit data
        data = pd.read_csv('sovereign_ledger.csv', names=['Timestamp', 'Sovereignty', 'Energy'])
        
        plt.figure(figsize=(10, 6))
        
        # Plotting Energy vs Sovereignty
        plt.plot(data['Energy'], label='Kinetic Energy (Induction)', color='cyan')
        plt.plot(data['Sovereignty'], label='Total Sovereignty (Accumulation)', color='lime')
        
        plt.title('Sovereign Engine: Inductive Growth Analysis')
        plt.xlabel('Audit Cycles')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Save the result
        plt.savefig('sovereign_plot.png')
        print("--- REPORT GENERATED: sovereign_plot.png ---")
        
    except FileNotFoundError:
        print("[ERROR] No audit file found. Run swarm_final.py first.")

if __name__ == "__main__":
    generate_report()
