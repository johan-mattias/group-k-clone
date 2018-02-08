from socket import *
import network.utils as utils
from enum import Enum

class DataFormat(Enum):
    TOKEN = 0
    PLAYER_UDPATE = 1
    PORT = 2
    PORTS = 3


class TcpHandler:

    def __init__(self, remote_address=None):
        self.connection = None
        self.remote_address = remote_address

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.port = utils.get_free_tcp_port()
        print("free port", self.port)
        self.socket.bind(('', self.port))

    def accept(self):
        self.socket.listen(1)
        self.connection, self.remote_address = self.socket.accept()
        
        print(self.remote_address, "connected")
        return self.remote_address

    def connect(self, address = None):
        if address != None:
            self.remote_address = address

        self.socket.connect(self.remote_address)
        print("Connected to", self.remote_address)
        
    def receive(self):
        if self.connection is None:
            data = self.socket.recv(1024)
        else:
            data = self.connection.recv(1024)
        
        return utils.deserialize_obj(data)

    def send(self, data_format, data):
        sendData = utils.serialize_obj((data_format, data))
        
        if self.connection is None:
            self.socket.send(sendData)
        else:
            self.connection.send(sendData)

    def close_connection(self):
        if self.connection != None:
            self.connection.close()
            
    def shutdown(self):
        self.socket.shutdown(SHUT_RDWR)
        
    def close(self):
        self.socket.close()
