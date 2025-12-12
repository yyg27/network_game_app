import socket
import json
import struct

PROTOCOL_VERSION = 1
HEADER_SIZE = 4
ENCODING = 'utf-8'

CMD_JOIN = "JOIN"
CMD_WAIT = "WAIT"
CMD_START = "START"
CMD_MOVE = "MOVE"
CMD_RESULT = "RESULT"
CMD_ERROR = "ERROR"
CMD_EXIT = "EXIT"

MOVE_ROCK = "R"
MOVE_PAPER = "P"
MOVE_SCISSORS = "S"

RESULT_WIN = "WIN"
RESULT_LOSE = "LOSE"
RESULT_DRAW = "DRAW"

def send_message(sock, msg_type, payload=None):
    if payload is None:
        payload = {};

    #schema
    message_dict = {
        "ver": PROTOCOL_VERSION,
        "type": msg_type,
        "payload": payload
    }

    try:
        json_data = json.dumps(message_dict).encode(ENCODING);
        msg_length = len(json_data);
        
        header = struct.pack('>I', msg_length) ;
        sock.sendall(header + json_data);
        
    except Exception as e:
        print(f"ERROR sending message: {e}");

def receive_message(sock):
    try:
        header_data = _recv_all(sock, HEADER_SIZE);
        if not header_data:
            return None
            
        msg_length = struct.unpack('>I', header_data)[0];

        body_data = _recv_all(sock, msg_length);
        if not body_data:
            return None

        message_dict = json.loads(body_data.decode(ENCODING));
        return message_dict

    except Exception as e:
        print(f"Error receiving message: {e}");
        return None

def _recv_all(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data));
        if not packet:
            return None
        data += packet
    return data