# Network Analyzer

## Overview
Network Analyzer is a WebSocket-based packet capturing tool that allows real-time monitoring of network traffic. It captures packets using **PyShark** and provides a WebSocket interface for clients to control the capture process and receive live packet data.

## Features
- Real-time packet capture via WebSockets
- Start, stop, and fetch captured data remotely
- Supports multiple WebSocket clients
- Uses **PyShark** for deep packet inspection

## Requirements
Ensure you have the following installed:
- Python 3.12+
- Wireshark (tshark)
- Virtual environment (optional but recommended)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Network-Analyser
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure **tshark** is installed and accessible:
   ```bash
   sudo apt install tshark  # Debian/Ubuntu
   brew install wireshark   # macOS
   ```

## Usage
1. Run the WebSocket server:
   ```bash
   sudo python main.py
   ```

2. Connect a WebSocket client to `ws://localhost:8765`.

3. Use the following JSON messages to control the capture:
   - Start capturing:
     ```json
     { "action": "start_capture" }
     ```
   - Stop capturing:
     ```json
     { "action": "stop_capture" }
     ```
   - Fetch captured data:
     ```json
     { "action": "fetch_data" }
     ```

## Troubleshooting
- **Permission Issues:** Run with `sudo` if required to access network interfaces.
- **Interface Not Found:** Ensure you specify the correct network interface (e.g., `wlp4s0` instead of `wlan0`).
  ```bash
  ip link show  # List available interfaces
  ```
- **PyShark Errors:** Verify **tshark** is installed and accessible:
  ```bash
  tshark -v
  ```

## License
This project is licensed under the MIT License.

## Author
**Vishnu MK**

