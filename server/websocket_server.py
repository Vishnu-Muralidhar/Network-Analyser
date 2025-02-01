import asyncio
import websockets
import json
import pyshark
import threading

connected_clients = set()
clients_lock = asyncio.Lock()
capturing = False  # Global state to track packet capture
captured_data = []  # Store captured packets


class server_:
    async def handle_connection(self, websocket):
        """Handles a new WebSocket client connection."""
        async with clients_lock:
            connected_clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    # Handle control messages
                    if "action" in data:
                        response = await self.handle_action(data["action"], websocket)
                        await websocket.send(json.dumps({"status": "success", "response": response}))
                        continue

                except json.JSONDecodeError:
                    print(f"Received invalid JSON from {websocket.remote_address}")

        except websockets.exceptions.ConnectionClosedError:
            print(f"Client disconnected: {websocket.remote_address}")
        finally:
            async with clients_lock:
                connected_clients.discard(websocket)

    async def handle_action(self, action, websocket):
        """Handle client control actions like start, stop, and fetch data."""
        global capturing, captured_data

        if action == "start_capture":
            if not capturing:
                capturing = True
                threading.Thread(target=self.capture_packets, args=("wlp4s0",), daemon=True).start()
                return "Packet capture started."
            return "Packet capture is already running."

        elif action == "stop_capture":
            capturing = False  # Stop capturing
            response = json.dumps({"status": "capture_stopped", "data": captured_data})
            captured_data = []  # Clear stored packets
            return response  # Send captured data back to client

        elif action == "fetch_data":
            return json.dumps({"status": "data_fetched", "data": captured_data})

        return "Unknown action."

    def capture_packets(self, interface):
        """Capture packets continuously in a separate thread."""
        global capturing, captured_data
        capture = pyshark.LiveCapture(interface=interface)

        for packet in capture.sniff_continuously(packet_count=0):
            if not capturing:
                break  # Stop loop when capturing is disabled

            try:
                packet_data = {
                    "timestamp": str(packet.sniff_time),
                    "source": packet.ip.src,
                    "destination": packet.ip.dst,
                    "protocol": packet.transport_layer,
                    "length": int(packet.length),
                }
                captured_data.append(packet_data)  # Store packets
                print(packet_data)
                
                # Send packet data to all connected clients asynchronously
                asyncio.run(self.broadcast_packet(packet_data))

            except AttributeError:
                continue

    async def broadcast_packet(self, packet_data):
        """Send packet data to all connected clients."""
        async with clients_lock:
            for client in connected_clients:
                try:
                    await client.send(json.dumps(packet_data))
                except websockets.exceptions.ConnectionClosed:
                    connected_clients.discard(client)

    async def start_server(self):
        print("Starting WebSocket Server.......")
        async with websockets.serve(self.handle_connection, "localhost", 8765):
            try:
                await asyncio.Future()  # run forever
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    ws_server = server_()
    print("Starting server...")
    try:
        asyncio.run(ws_server.start_server())
    except Exception as e:
        print(f"Error: {e}")
