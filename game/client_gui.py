import tkinter as tk
from tkinter import messagebox
import socket
import threading
import protocol

class RPSClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Online")
        self.root.geometry("400x500")
        
        self.sock = None
        self.running = False

        self.setup_login_ui()

    def setup_login_ui(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=60)

        tk.Label(self.login_frame, text="Server IP Address:").pack()
        self.entry_ip = tk.Entry(self.login_frame)
        self.entry_ip.insert(0, "127.0.0.1")
        self.entry_ip.pack(pady=5)

        tk.Label(self.login_frame, text="Port:").pack()
        self.entry_port = tk.Entry(self.login_frame)
        self.entry_port.insert(0, "6677")
        self.entry_port.pack(pady=5)

        tk.Button(self.login_frame, text="CONNECT", bg="green", fg="white", width=15, command=self.connect_to_server).pack(pady=20)

    def setup_game_ui(self):
        self.login_frame.destroy()
        
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill=tk.BOTH, expand=True)

        self.lbl_status = tk.Label(self.game_frame, text="Connecting...", font=("Arial", 12), fg="orange")
        self.lbl_status.pack(pady=20)

        self.lbl_result = tk.Label(self.game_frame, text="", font=("Arial", 14, "bold"), fg="blue")
        self.lbl_result.pack(pady=10)

        self.btn_frame = tk.Frame(self.game_frame)
        self.btn_frame.pack(pady=30)

        self.btn_rock = tk.Button(self.btn_frame, text="ROCK", width=10, height=3, command=lambda: self.send_move("R"))
        self.btn_rock.grid(row=0, column=0, padx=5)

        self.btn_paper = tk.Button(self.btn_frame, text="PAPER", width=10, height=3, command=lambda: self.send_move("P"))
        self.btn_paper.grid(row=0, column=1, padx=5)

        self.btn_scissors = tk.Button(self.btn_frame, text="SCISSORS", width=10, height=3, command=lambda: self.send_move("S"))
        self.btn_scissors.grid(row=0, column=2, padx=5)

        self.toggle_buttons(False)

    def connect_to_server(self):
        host = self.entry_ip.get()
        try:
            port = int(self.entry_port.get())
        except ValueError:
            messagebox.showerror("Error", "Port must be a number!")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            
            protocol.send_message(self.sock, protocol.CMD_JOIN)
            
            self.running = True
            self.setup_game_ui()
            
            t = threading.Thread(target=self.listen_server, daemon=True)
            t.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed:\n{e}")

    def listen_server(self):
        while self.running:
            msg = protocol.receive_message(self.sock)
            if not msg:
                self.root.after(0, self.on_disconnect)
                break
            self.root.after(0, self.handle_message, msg)

    def handle_message(self, msg):
        m_type = msg["type"]
        payload = msg["payload"]

        if m_type == protocol.CMD_WAIT:
            self.lbl_status.config(text=payload.get("msg"), fg="orange")
            self.lbl_result.config(text="")
        
        elif m_type == protocol.CMD_START:
            self.lbl_status.config(text="GAME STARTED!", fg="green")
            self.lbl_result.config(text="Make your move", fg="black")
            self.toggle_buttons(True)
        
        elif m_type == protocol.CMD_RESULT:
            res = payload["result"]
            opp = payload["opponent_move"]
            
            tr_move = {"R": "Rock", "P": "Paper", "S": "Scissors"}
            opp_text = tr_move.get(opp, opp)

            txt = f"RESULT: {res}\nOpponent: {opp_text}"
            color = "green" if res == "WIN" else "red" if res == "LOSE" else "grey"
            
            self.lbl_result.config(text=txt, fg=color)
            self.lbl_status.config(text="Waiting for new round...", fg="blue")
            self.toggle_buttons(True)

        elif m_type == protocol.CMD_ERROR:
            messagebox.showerror("Server Error", payload.get("msg"))

    def send_move(self, move):
        protocol.send_message(self.sock, protocol.CMD_MOVE, {"move": move})
        self.lbl_status.config(text="Move sent, waiting...", fg="grey")
        self.toggle_buttons(False)

    def toggle_buttons(self, state):
        st = tk.NORMAL if state else tk.DISABLED
        self.btn_rock.config(state=st)
        self.btn_paper.config(state=st)
        self.btn_scissors.config(state=st)

    def on_disconnect(self):
        if self.running:
            messagebox.showerror("Error", "Disconnected from server.")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSClientGUI(root)
    root.mainloop()