import socket
import time
import sys

def check_port(host, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0

def wait_for_services():
    services = [("Backend", 8000), ("Frontend", 3001)]
    start_time = time.time()
    max_wait = 60 # seconds
    
    print("Waiting for services...")
    while time.time() - start_time < max_wait:
        all_up = True
        for name, port in services:
            if check_port("localhost", port):
                print(f"[OK] {name} is listening on port {port}")
            else:
                print(f"[..] {name} is NOT listening on port {port}")
                all_up = False
        
        if all_up:
            print("All services are UP!")
            sys.exit(0)
        
        time.sleep(2)
        print("---")
    
    print("Timeout waiting for services.")
    sys.exit(1)

if __name__ == "__main__":
    wait_for_services()
