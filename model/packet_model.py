from typing import List

class Packet:
    def __init__(self, timestamp:str, source: str, destination: str, protocol: str, length : int):
        self.timestamp = timestamp
        self.source =source
        self.destination = destination
        self.protocol = protocol
        self.length = length
    
    def to_dict(self):
        return{
            "timestamp":self.timestamp,
            "source":self.source,
            "destination":self.destination,
            "protocol":self.protocol,
            "length":self.length
        }
