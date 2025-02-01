import argparse
import asyncio
import json
import websockets

class WebSocketClient:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.websocket = None

    async def connect(self):
        """Connect to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.ws_url)
            print(f"Connected to WebSocket server at {self.ws_url}")
        except Exception as e:
            print(f"Failed to connect to WebSocket server: {e}")
            raise

    async def send_message(self, message):
        """Send a message to the WebSocket server."""
        if self.websocket:
            await self.websocket.send(message)
        else:
            raise ConnectionError("WebSocket connection is not established.")

    async def receive_message(self):
        """Receive a message from the WebSocket server."""
        if self.websocket:
            return await self.websocket.recv()
        else:
            raise ConnectionError("WebSocket connection is not established.")

    async def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed.")

class CLIClient:
    def __init__(self, ws_url):
        self.ws_client = WebSocketClient(ws_url)

    async def handle_command(self, command):
        """
        Handle CLI commands and communicate with the WebSocket server.
        """
        if command == "--start":
            await self.ws_client.send_message(json.dumps({"action": "start_capture"}))
            response = await self.ws_client.receive_message()
            print(f"Response: {response}")

        elif command == "--fetch":
            await self.ws_client.send_message(json.dumps({"action": "fetch_data"}))
            response = await self.ws_client.receive_message()
            print(f"Response: {response}")

        elif command == "--stop":
            await self.ws_client.send_message(json.dumps({"action": "stop_capture"}))
            response = await self.ws_client.receive_message()
            print(f"Response: {response}")

        elif command == "--exit":
            print("Exiting...")
            await self.ws_client.close()
            exit(0)

        else:
            print("Unknown command. Use --start, --fetch, --stop, or --exit.")

    async def run(self):
        """
        Main loop for listening to user input and executing commands.
        """
        try:
            await self.ws_client.connect()
            print("CLI is ready. Enter commands: --start, --fetch, --stop, --exit")

            while True:
                try:
                    user_input = input(">> ").strip()
                    await self.handle_command(user_input)
                except KeyboardInterrupt:
                    print("\nExiting gracefully...")
                    await self.ws_client.close()
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Failed to run CLI: {e}")


if __name__ == "__main__":
    async def main():
        parser = argparse.ArgumentParser(description="Interactive CLI for network analysis.")
        parser.add_argument(
            "--ws-url", type=str, default="ws://localhost:8765", help="WebSocket server URL"
        )
        args = parser.parse_args()

        cli_client = CLIClient(ws_url=args.ws_url)
        await cli_client.run()

    asyncio.run(main())