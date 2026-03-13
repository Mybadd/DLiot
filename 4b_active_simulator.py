import socket
import time
import threading
import sys

# WARNING: Only run this against 127.0.0.1 (localhost).
# Do not run this against external IPs without explicit permission.

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8080 # We'll just target a random local port

def udp_flood_attack(duration_seconds=5):
    print(f"[*] Starting UDP Flood (DoS) attack on {TARGET_IP} for {duration_seconds} seconds...")
    print("[*] (This is harmless local traffic to trigger the anomaly detector)")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 1024 bytes of junk data
    payload = b"X" * 1024 
    
    end_time = time.time() + duration_seconds
    packet_count = 0
    
    while time.time() < end_time:
        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
            packet_count += 1
        except Exception as e:
            print(f"[!] Error sending packet: {e}")
            break
            
    print(f"[+] Attack complete. Sent {packet_count} UDP packets rapidly.")

def simple_port_scan():
    print(f"[*] Starting basic Port Scan on {TARGET_IP} (Ports 1-100)...")
    
    open_ports = []
    # Scanning first 100 ports rapidly
    for port in range(1, 101):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.01) # Very fast timeout just to generate traffic spikes
        result = sock.connect_ex((TARGET_IP, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
        
    print(f"[+] Scan complete. Found {len(open_ports)} open ports.")
    print("[*] The live detector running in another window should have caught that massive spike in unique port connections!")

if __name__ == "__main__":
    print("-" * 50)
    print("Edge IDS - Active Simulator")
    print("-" * 50)
    print("1. Run UDP Flood (Simulates DoS Attack)")
    print("2. Run Port Scan (Simulates Reconnaissance)")
    print("3. Exit")
    
    choice = input("Select an attack to simulate locally: ")
    
    if choice == '1':
        udp_flood_attack()
    elif choice == '2':
        simple_port_scan()
    else:
        print("Exiting.")
