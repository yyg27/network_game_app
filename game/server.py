import socket
import threading
import protocol

clients = [];
client_moves = {};
game_lock = threading.Lock();

def determine_winner(move1, move2):
    if move1 == move2:
        return protocol.RESULT_DRAW
    
    if (move1 == protocol.MOVE_ROCK and move2 == protocol.MOVE_SCISSORS) or \
       (move1 == protocol.MOVE_PAPER and move2 == protocol.MOVE_ROCK) or \
       (move1 == protocol.MOVE_SCISSORS and move2 == protocol.MOVE_PAPER):
        return protocol.RESULT_WIN
    
    return protocol.RESULT_LOSE

def broadcast_result(winner_idx):
    c1 = clients[0];
    c2 = clients[1];
    
    m1 = client_moves[c1];
    m2 = client_moves[c2];

    res1 = protocol.RESULT_DRAW
    res2 = protocol.RESULT_DRAW

    if winner_idx == 0:
        res1 = protocol.RESULT_WIN
        res2 = protocol.RESULT_LOSE
    elif winner_idx == 1:
        res1 = protocol.RESULT_LOSE
        res2 = protocol.RESULT_WIN

    payload1 = {"result": res1, "opponent_move": m2};
    payload2 = {"result": res2, "opponent_move": m1};

    protocol.send_message(c1, protocol.CMD_RESULT, payload1);
    protocol.send_message(c2, protocol.CMD_RESULT, payload2);

    client_moves.clear();

def handle_client(sock, addr):
    print(f"New connection: {addr}");
    
    try:
        msg = protocol.receive_message(sock);
        if not msg or msg["type"] != protocol.CMD_JOIN:
            return

        with game_lock:
            if len(clients) >= 2:
                protocol.send_message(sock, protocol.CMD_ERROR, {"msg": "Room full"});
                sock.close();
                return
            clients.append(sock);

        if len(clients) == 1:
            protocol.send_message(sock, protocol.CMD_WAIT, {"msg": "Waiting for opponent..."});
        else:
            protocol.send_message(clients[0], protocol.CMD_START, {"opponent": "Player 2"});
            protocol.send_message(clients[1], protocol.CMD_START, {"opponent": "Player 1"});

        while True:
            msg = protocol.receive_message(sock)
            if not msg:
                break
            
            if msg["type"] == protocol.CMD_MOVE:
                move = msg["payload"]["move"];
                
                with game_lock:
                    client_moves[sock] = move;
                    
                    if len(client_moves) == 2:
                        c1_move = client_moves[clients[0]];
                        c2_move = client_moves[clients[1]];
                        
                        res = determine_winner(c1_move, c2_move);
                        
                        w_idx = -1
                        if res == protocol.RESULT_WIN:
                            w_idx = 0
                        elif res == protocol.RESULT_LOSE:
                            w_idx = 1
                            
                        broadcast_result(w_idx);

    except Exception as e:
        print(f"Error: {e}")
    finally:
        with game_lock:
            if sock in clients:
                clients.remove(sock);
                sock.close()
        print(f"Disconnected: {addr}");

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    server.bind((host, port));
    server.listen(2);
    print(f"Server listening on {host}:{port}");

    while True:
        client_sock, addr = server.accept();
        t = threading.Thread(target=handle_client, args=(client_sock, addr));
        t.start();

if __name__ == "__main__":
    host = "0.0.0.0";
    port = int(input("Start Port (default: 6677): ") or 6677);
    start_server(host, port);