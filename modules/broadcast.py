import socket
import threading
import time

BROADCAST_IP = "255.255.255.255";
PORT = 6548;

def send_broadcast(message):
    try:
        #udp socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        #permission to broadcast
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1);

        print(f"Sending broadcast: {message}");
        s.sendto(message.encode("utf-8"),(BROADCAST_IP, PORT));

        s.close();

    except Exception as e:
        print(f"ERROR: Failed to send broadcast: {e}");

def listen_broadcast():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1);
    
        s.bind(("",PORT));
        print(f"Listening on port {PORT}");
    
        while True:
            data, address = s.recvfrom(1024);
            message = data.decode();
            timestamp = time.strftime("%H:%M:%S")
            print(f"\n[{timestamp}][BROADCAST] from {address}: {message}");
    
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Stopping...");
    except Exception as e:
        print(f"Listener Error: {e}");

if __name__ == "__main__":
    
    print("Type your message and hit Enter (Type '/exit' to quit): ");
    listener_thread = threading.Thread(target=listen_broadcast, daemon=True);
    listener_thread.start();

    while True:
        msg = input("");
        if msg:
           if msg == "/exit":
            break
           send_broadcast(msg);