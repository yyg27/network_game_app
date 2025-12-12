
#  Python Network Toolkit & R/P/S Game Suite

##  Project Overview

This project is a comprehensive network programming suite developed in Python. It combines essential network administration tools, web utilities, and a real-time multiplayer game engine into a single, user-friendly GUI Dashboard.

The application demonstrates core networking concepts including TCP/UDP sockets, Multi-threading, Subnet Scanning, Custom Protocols, and Client-Server Architecture.

----------

##  Project Structure

The project is organized into modular components for better maintainability:

```
PROJECT_ROOT/
│
├── main.py                  # Entry point (Main GUI Dashboard)
├── README.md                # Project Documentation
│
├── modules/                 # Network & Web Tools
│   ├── port_scanner.py      # TCP Port Scanner (Multi-threaded)
│   ├── device_scanner.py    # Network Discovery (ICMP/Ping)
│   ├── file_transfer.py     # TCP File Transfer (Client/Server)
│   ├── broadcast.py         # UDP Broadcast Chat (Port 6548)
│   ├── web_crawler.py       # Web Scraper & Downloader
│   └── wiki_fetcher.py      # Wikipedia API Fetcher
│
└── game/                    # Multiplayer Game Engine
    ├── protocol.py          # Custom Communication Protocol (JSON + Struct)
    ├── server.py            # Game Server (Multi-threaded)
    ├── client.py            # CLI Game Client (Console based)
    └── client_gui.py        # GUI Game Client (Tkinter based)

```

----------

##  Features & Module Details

### 1. Network Tools (Part A)

#### **UDP Broadcast Chat** (`broadcast.py`)

-   **Technology:** Uses `socket.SOCK_DGRAM` with `SO_BROADCAST`
-   **Port:** Operates on port 6548
-   **Functionality:** Allows serverless messaging to all devices on the subnet (255.255.255.255)
-   **Threading:** Implements a background listener thread to receive messages while the user types
-   **Commands:** Supports `/exit` to close the chat session cleanly

#### **Port Scanner** (`port_scanner.py`)

-   Scans a target IP for open TCP ports
-   Uses multi-threading (ThreadPoolExecutor) to scan hundreds of ports in seconds

#### **Device Scanner** (`device_scanner.py`)

-   Discovers active devices on a local subnet (e.g., 192.168.1.0/24)
-   Automatically detects the OS (Windows/Linux) to use the correct Ping command parameters (-n vs -c)

#### **File Transfer** (`file_transfer.py`)

-   A reliable TCP-based file transfer system
-   Server listens for connections while the Client sends files

### 2. Web Utilities

#### **Web Crawler** (`web_crawler.py`)

-   Connects to a URL, parses HTML using BeautifulSoup
-   Identifies and downloads specific assets (images, PDFs) to a local directory
-   Handles HTTP headers to mimic a real browser (User-Agent)

#### **Wiki Fetcher** (`wiki_fetcher.py`)

-   Queries the Wikipedia REST API to fetch summaries of user-requested topics

### 3. Multiplayer Game (Part B)

-   **Architecture:** Centralized TCP Server with multiple Clients
-   **Protocol:** Uses a custom application-layer protocol defined in `protocol.py`. Messages are serialized in JSON and prefixed with a Struct header (4 bytes) to ensure data integrity
-   **Gameplay:** Supports turn-based multiplayer gaming (Rock-Paper-Scissors)
-   **Modes:**
    -   **GUI:** User-friendly graphical interface using tkinter
    -   **CLI:** Command-line interface for terminal purists

----------

##  Installation & Requirements

**Python 3.x is required.**

Install external dependencies via terminal:

```bash
pip install requests beautifulsoup4

```
Or if you want to use a virtual environment:
```bash
python -m venv venv
pip install -r requirements.txt
```

> **Note:** `tkinter`, `socket`, `threading`, `sys`, `os`, `subprocess`, `platform`, `ipaddress` are standard Python libraries and do not need installation. Check requirements.txt just in case

----------

##  How to Run

### 1. Main Dashboard

The dashboard allows you to control all modules from one place.

```bash
python main.py

```

### 2. Running Components Manually (Optional)

#### **Broadcast Chat:**

```bash
python modules/broadcast.py

```

-   Select 1 to Send, 2 to Listen
-   Or use the integrated threaded mode in `main.py`

#### **Rock/Paper/Scissors Multiplayer Game:**

**Start Server:**

```bash
python game/server.py

```

**Start Client (CLI):**

```bash
python game/client.py

```

----------

##  Troubleshooting / FAQ

### "ModuleNotFoundError: No module named 'modules'"

-   Ensure that you are running `main.py` from the root directory of the project, not from inside the modules folder
-   Verify that empty `__init__.py` files exist in both `modules/` and `game/` directories

### "Permission Denied" (Broadcast/Server)

-   Your firewall might be blocking Python network activity. Allow Python through the firewall or test on localhost

### "Address already in use"

-   If you restart the server quickly, the port might still be occupied. Wait a few seconds or change the port in `game/protocol.py`


##  Author

Yusuf Yiğit Gültekin 
2023556458

----------
