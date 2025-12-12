import socket
from concurrent.futures import ThreadPoolExecutor

TIMEOUT = 1.0
PROTOCOL = "tcp"

def get_service_name(port):
    try:
        return socket.getservbyport(port,PROTOCOL);
    except:
        return "Unknown"

#function to scan single port    
def scan_port(ip,port):
    try:
        #creating a tcp socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        s.settimeout(TIMEOUT);

        #connect_ex instead of connect for returning a number instead of a exception
        result = s.connect_ex((ip,port));
        s.close();
        if result == 0:
            service_name = get_service_name(port);
            return (port, "Open", service_name);
    except Exception:
        pass
    return None

def scan_all_ports(target_ip, start_port, end_port):
    print(f"Scanning {target_ip} within ports {start_port}--{end_port}");
    
    open_ports = [];

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [];
        for port in range(start_port, end_port + 1):
            futures.append(executor.submit(scan_port, target_ip, port));
        
        for future in futures:
            result = future.result();
            if result:
                open_ports.append(result);

    return open_ports


if __name__ == "__main__":
    target_ip = input("Target IP (default: 127.0.0.1): ") or "127.0.0.1";
    start_port = int(input("Start Port (default: 1): ") or 1);
    end_port = int(input("End Port (default: 1000): ") or 1000);

    results = scan_all_ports(target_ip, start_port, end_port);

    print(f"\nPORT\tSTATUS\tSERVICE ({PROTOCOL.upper()})");
    for port, status, service in results:
        print(f"{port}\t{status}\t{service}");

