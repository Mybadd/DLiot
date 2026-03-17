import pandas as pd
import numpy as np
import time
import os
import config

def generate_packet(attack_mode=False):
    """Creates a synthetic IoT packet calibrated to CICIOT23 training data"""
    if attack_mode:
        # 🚨 ATTACK PROFILE (Aggressive: High rate, low IAT, TCP Flags)
        packet = {
            "flow_duration": np.random.uniform(0.001, 0.05),
            "Header_Length": np.random.randint(1000, 5000),
            "Rate": np.random.uniform(5000, 10000),
            "Srate": np.random.uniform(5000, 10000),
            "Drate": 0,
            "IAT": np.random.uniform(0, 0.0001),
            "Protocol Type": 6.0,   # TCP
            "fin_flag_number": 0,
            "syn_flag_number": 1    # SYN Flood
        }
    else:
        # ✅ BENIGN PROFILE (Calibrated to look 'Normal' to the Autoencoder)
        # We use Protocol 6 (TCP) and much lower rates to stay under the threshold.
        packet = {
            "flow_duration": np.random.uniform(0.1, 1.0),
            "Header_Length": np.random.randint(50, 150),
            "Rate": np.random.uniform(1, 10),
            "Srate": np.random.uniform(1, 10),
            "Drate": 0,
            "IAT": np.random.uniform(0.05, 0.2),
            "Protocol Type": 6.0,   # Matches the majority of BenignTraffic
            "fin_flag_number": 0,
            "syn_flag_number": 0
        }
    return pd.DataFrame([packet])

def start_active_demo():
    print("="*50)
    print("🔥  ACTIVE ATTACK SIMULATOR (CALIBRATED)")
    print("="*50)
    print("[*] Options: [1] Normal Traffic  [2] Launch DDoS Attack  [Q] Quit")
    
    try:
        while True:
            choice = input("\n[Demo Control] > ").lower()
            
            if choice == '1':
                print("[*] Generating Normal User Traffic...")
                for _ in range(5):
                    packet = generate_packet(attack_mode=False)
                    packet.to_csv("live_stream.csv", index=False)
                    time.sleep(1)
                    
            elif choice == '2':
                print("🚨 LAUNCHING DDoS ATTACK BURST!")
                for i in range(20):
                    packet = generate_packet(attack_mode=True)
                    packet.to_csv("live_stream.csv", index=False)
                    print(f"  -> Flooding packet {i+1}...")
                    time.sleep(0.1)
                    
            elif choice == 'q':
                break
            else:
                print("[!] Invalid choice.")
                
    except KeyboardInterrupt:
        print("\n[!] Simulator stopped.")

if __name__ == "__main__":
    start_active_demo()