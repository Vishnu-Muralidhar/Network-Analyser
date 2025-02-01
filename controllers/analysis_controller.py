import pyshark
import json
import websockets

async def analyze_packets(interface, websocket_url):
    capture = pyshark.LiveCapture(interface=interface)
    for packet in capture.sniff_continuously(packet_count=0):
        try:
            data = {
                "timestamp": str(packet.sniff_time),
                "source": packet.ip.src,
                "destination": packet.ip.dst,
                "protocol": packet.transport_layer,
                "length": int(packet.length),
            }
            async with websockets.connect(websocket_url) as websocket:
                await websocket.send(json.dumps(data))
        except AttributeError:
            continue
