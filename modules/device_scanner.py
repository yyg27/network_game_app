import platform
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

#function to ping single device
def ping_device(ip):
    #which os?
    winlux = "-n" if platform.system().lower() == "windows" else "-c";
    command = ["ping", winlux, "1", str(ip)];

    try:
        #ping and only return ip
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);
        
        #0 means active
        if response == 0:
            return str(ip);
    except Exception:
        pass


def scan_network(subnet):
    print(f"Scanning network: {subnet}");

    active_devices = [];

    try:
        ##create ip list
        network = ipaddress.ip_network(subnet, strict=False);
        hosts = list(network.hosts());
    except ValueError:
        print("Invalid Subnet Format!");
        return [];

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [];
        for ip in hosts:
            futures.append(executor.submit(ping_device, ip));
        
        for future in futures:
            result = future.result();
            if result:
                active_devices.append(result);
    
    return active_devices;

if __name__ == "__main__":
    target_subnet = input("Enter Subnet (default: 192.168.1.0/24): ") or "192.168.1.0/24";

    results = scan_network(target_subnet);

    print(f"\nACTIVE DEVICES FOUND ({len(results)})");
    for ip in results:
        print(f"{ip}");