import socket
import threading
import protocol

def listen_for_messages(sock):
    while True:
        msg = protocol.receive_message(sock);
        if not msg:
            print("\nDisconnected from server.");
            break
        
        msg_type = msg["type"];
        payload = msg["payload"];

        if msg_type == protocol.CMD_WAIT:
            print(f"\n[SERVER] {payload.get('msg')}");
        
        elif msg_type == protocol.CMD_START:
            print(f"\n[GAME START] Opponent found: {payload.get('opponent')}");
            print("Make your move: (R)ock, (P)aper, (S)cissors");
        
        elif msg_type == protocol.CMD_RESULT:
            res = payload["result"];
            opp_move = payload["opponent_move"];
            
            print(f"\n[RESULT] You {res}!")
            print(f"Opponent played: {opp_move}")
            print("#" * 20)
            print("New round! Make your move (R/P/S):");

        elif msg_type == protocol.CMD_ERROR:
            print(f"\n[ERROR] {payload.get('msg')}");

def start_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    try:
        sock.connect((host, port));
    except Exception as e:
        print(f"Connection failed: {e}");
        return

    protocol.send_message(sock, protocol.CMD_JOIN);

    t = threading.Thread(target=listen_for_messages, args=(sock,), daemon=True);
    t.start();

    print(f"Connected to {host}:{port}. Sending JOIN...");

    while True:
        user_input = input() ;
        
        if user_input.lower() == "/exit":
            break

        if user_input.upper() in [protocol.MOVE_ROCK, protocol.MOVE_PAPER, protocol.MOVE_SCISSORS]:
            protocol.send_message(sock, protocol.CMD_MOVE, {"move": user_input.upper()});
            print("Move sent. Waiting for result...");
        else:
            print("Invalid move. Use R, P, or S.");

    sock.close();

if __name__ == "__main__":
    host = input("Target IP (default: 127.0.0.1): ") or "127.0.0.1";
    port = input("Port (default: 6677): ") or "6677";
    
    ##start_client(host, port);
    start_client(host, int(port));