import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'game'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules import port_scanner
    from modules import device_scanner
    from modules import file_transfer
    from modules import web_crawler
    from modules import wiki_fetcher
    from modules import broadcast
except ImportError as e:
    print(f"ERROR: Could not load modules: {e}");
    sys.exit();

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear');

def print_banner():
    print("="*40);
    print("   PYTHON NETWORK & GAME TOOLKIT (CLI)");
    print("="*40);

def menu():
    while True:
        clear_screen();
        print_banner();
        print("1. Port Scanner (TCP)");
        print("2. Device Scanner (Network Discovery)");
        print("3. Web Crawler (Download Files)");
        print("4. Wiki Fetcher (Search Topic)");
        print("5. Broadcast Chat (UDP)");
        print("6. File Transfer (TCP)");
        print("7. GAME (Rock Paper Scissors)");
        print("0. Exit");
        print("-" * 40);
        
        choice = input("Select > ");

        if choice == "1":
            run_port_scanner();
        elif choice == "2":
            run_device_scanner();
        elif choice == "3":
            run_web_crawler();
        elif choice == "4":
            run_wiki_fetcher();
        elif choice == "5":
            run_broadcast();
        elif choice == "6":
            run_file_transfer();
        elif choice == "7":
            run_game_menu()
        elif choice == "0":
            print("Exiting...");
            sys.exit()
        else:
            input("Invalid selection. Press Enter to continue...");

def run_port_scanner():
    clear_screen();
    print("### PORT SCANNER ###");
    ip = input("Target IP (Default: 127.0.0.1): ") or "127.0.0.1";
    start = input("Start Port (Default: 1): ") or "1";
    end = input("End Port (Default: 1000): ") or "1000";
    
    print(f"\nScanning {ip} ({start}-{end})...");
    results = port_scanner.scan_all_ports(ip, int(start), int(end));
    
    print(f"\n[Result] {len(results)} open ports found:");
    for p in results:
        print(p)
    input("\nPress Enter to return...");

def run_device_scanner():
    clear_screen();
    print("### DEVICE SCANNER ###");
    subnet = input("Enter Subnet (default: 192.168.1.0/24): ") or "192.168.1.0/24";
    
    print(f"\nScanning {subnet}...");
    results = device_scanner.scan_network(subnet);
    
    print(f"\n[Result] {len(results)} active devices:");
    for d in results:
        print(d);
    input("\nPress Enter to return...");

def run_web_crawler():
    clear_screen();
    print("### WEB CRAWLER ###");
    url = input("Enter Target URL: ") or "https://en.wikipedia.org/wiki/Never_Gonna_Give_You_Up";
    if not url: return
    ext = input("Enter desired file extension to download: ").strip() or "png";
    
    try:
        web_crawler.start_crawler(url, ext);
    except AttributeError:
        web_crawler.crawler(url,ext);
    
    input("\nDone. Press Enter to return...");

def run_wiki_fetcher():
    clear_screen();
    print("### WIKI FETCHER ###");
    topic = input("Would you kindly enter a topic: ");
    if topic:
        wiki_fetcher.get_wiki(topic)
    else:
        print("Please enter a topic.");
    input("\nPress Enter to return...")

def run_broadcast():
    clear_screen()
    print("### UDP BROADCAST CHAT ###");
    print("1. Send Message")
    print("2. Listen (Continuous)")
    
    sub = input("Select > ")
    if sub == "1":
        msg = input("Message: ")
        broadcast.send_broadcast(msg)
        input("Sent. Press Enter...")
    elif sub == "2":
        print("Listening... (Press CTRL+C to stop)")
        try:
            broadcast.listen_broadcast()
        except KeyboardInterrupt:
            pass

def run_file_transfer():
    clear_screen()
    print("### FILE TRANSFER ###")
    
    choice = input("Select Mode: (1) Send File / (2) Receive File: ");

    if choice == "1":
        filename = input("Filename to send: ");
        target_ip = input("Target IP: ");
        target_port = int(input("Target Port: "));
        file_transfer.send_file(filename, target_ip, target_port);
    
    elif choice == "2":
        server_ip = input("Server IP (0.0.0.0): ") or "0.0.0.0";
        server_port = int(input("Server Port (5566): ") or "5566");
        save_dir = input("Save directory (received): ") or "received";
        file_transfer.start_server(server_ip, server_port, save_dir);
    
    else:
        print("Invalid choice!!!");
            
    input("\nPress Enter to return...");

def run_game_menu():
    while True:
        clear_screen();
        print("### GAME MENU ###")
        print("1. Start Server (Host)");
        print("2. Start Client (Player)");
        print("0. Back");
        
        sub = input("Select > ");
        
        if sub == "1":
            print("Starting Server... (CTRL+C to stop)");
            try:
                os.system(f"{sys.executable} game/server.py");
            except KeyboardInterrupt:
                pass
        elif sub == "2":
            print("Starting Client...");
            try:
                os.system(f"{sys.executable} game/client.py");
            except KeyboardInterrupt:
                pass
        elif sub == "0":
            break

if __name__ == "__main__":
    try:
        menu();
    except KeyboardInterrupt:
        print("\nExited.");