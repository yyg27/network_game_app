import socket
import os

def send_file(filename, target_ip, target_port):
    try:
        if not os.path.exists(filename):
            print(f"ERROR: {filename} not found!!!");
            return False;
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        print(f"Connecting to {target_ip}:{target_port}..");
        s.connect((target_ip,target_port));
        print("Connected");

        s.send(os.path.basename(filename).encode());

        s.recv(1024);

        with open(filename,"rb") as f:
            data = f.read();
            s.sendall(data);

        s.close();
        print(f"File sent: {filename}");
        return True;

    except Exception as e:
        print(f"\nERROR sending file: {e}");
        return False;
    

def start_server(server_ip, server_port ,save_directory ="received"):

    if not os.path.exists(save_directory):
        os.makedirs(save_directory);

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    s.bind((server_ip,server_port));
    s.listen(1);

    print(f"Server is listening on {server_ip}:{server_port}...");

    client_socket , address = s.accept();
    print(f"Connection from {address}");

    filename = client_socket.recv(1024).decode();
    print(f"Receiving file: {filename}...");

    client_socket.send(b"---");

    file_path = os.path.join(save_directory, filename);
    
    with open(file_path, "wb") as f:
        while True:
            data = client_socket.recv(4096);
            if not data:
                break;
            f.write(data);

    client_socket.close();
    s.close();
    print(f"File saved to {file_path}");


if __name__ == "__main__":
    choice = input("Select Mode: (1) Send File / (2) Receive File: ");

    if choice == "1":
        filename = input("Filename to send: ");
        target_ip = input("Target IP: ");
        target_port = int(input("Target Port: "));
        send_file(filename, target_ip, target_port);
    
    elif choice == "2":
        server_ip = input("Server IP (0.0.0.0): ") or "0.0.0.0";
        server_port = int(input("Server Port (5566): ") or "5566");
        save_dir = input("Save directory (received): ") or "received";
        start_server(server_ip, server_port, save_dir);
    
    else:
        print("Invalid choice!!!");