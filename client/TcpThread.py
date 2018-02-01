from socket import *

class TcpThread:

    def __init__(self, port = 12001, remote_address=None):
        self.port = port
        self.connection = None
        self.remote_address = remote_address
        
        self.socket = socket(AF_INET, SOCK_STREAM)
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
        if (self.connection == None):
            data = self.socket.recv(1024)
        else:
            data = self.connection.recv(1024)
        
        return data

    def send(self, data):
        self.socket.send(data)
        
        
