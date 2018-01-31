from socket import *

class TcpThread:

    def __init__(self, port = 12001):
        self.port = port
        self.connection = None
        self.remoteAddress = None
        
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', self.port))
        

    def accept(self):
        self.socket.listen(1)
        self.connection, self.remoteAddress = self.socket.accept()

        print(self.remoteAddress, "connected")
        return self.remoteAddress

    def connect(self, address):
        self.remoteAddress = address
        self.socket.connect(self.remoteAddress)
        
        print("Connected to", self.remoteAddress)
        
    def receive(self):
        data = self.socket.recv(1024)
        
        return data

    def send(self, data):
        self.socket.send(data)
        
        
