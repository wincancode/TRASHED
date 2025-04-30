import socket
from tokenize import String
import uuid


class User:
    def __init__(self,name):
        self.name = name
        self.ip = self.get_ip_address()
        self.generate_uuid = self.generate_uuid()

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception as e:
            return f"u  nable to get IP: {e}"
        
    def generate_uuid(self):
        return str(uuid.uuid4())
        

