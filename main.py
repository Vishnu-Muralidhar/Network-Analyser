import os
from multiprocessing import Process
from server.websocket_server import server_
from api_gateway.routes import setup_routes
import asyncio

class entrypoint:
    def __init__(self):
        self.api_server = setup_routes()
        self.server = server_()

    def start_server_linux(self):
        try:
            # Start the API server in a separate process
            p2 = Process(target=self.run_api_server)
            p2.start()

            # Start the WebSocket server in a separate process
            p3 = Process(target=self.run_websocket_server)
            p3.start()

            # Wait for the processes to finish (optional)
            p2.join()
            p3.join()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            p2.terminate()
            p3.terminate()

    def run_api_server(self):
        """Synchronous wrapper to run the API server."""
        self.api_server.run_server()

    def run_websocket_server(self):
        """Synchronous wrapper to run the WebSocket server."""
        asyncio.run(self.server.start_server())

if __name__ == "__main__":
    entrypoint().start_server_linux()