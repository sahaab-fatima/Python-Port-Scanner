import socket
import threading
from datetime import datetime

# Global list to store results
open_ports = []

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            open_ports.append((port, service))
            print(f"[+] Port {port}: OPEN ({service})")
        s.close()
    except:
        pass

def start_scan():
    global open_ports
    print("\n" + "="*50)
    target = input("Enter Target IP (or type 'exit' to quit): ")
    
    if target.lower() == 'exit':
        return False # Program stop karne ke liye
    
    print(f"Scanning {target}...")
    open_ports = [] # Purani list khali karna
    
    threads = []
    for port in range(1, 501): # 1 to 500 ports
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("-" * 50)
    print(f"Scan Finished for {target}")
    print("="*50 + "\n")
    return True

# Main Execution Loop
print("=" * 50)
print("   CONTINUOUS PORT SCANNER - SEMESTER PROJECT")
print("=" * 50)

while True:
    should_continue = start_scan()
    if not should_continue:
        print("Exiting... Goodbye!")
        break