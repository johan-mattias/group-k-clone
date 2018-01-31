from socket import *

class TcpThread:

    def __init__(self, port = 12001):
        self.port = port
        self.connection = None
        self.remoteAddress = None
        
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', self.port))
        self.socket.listen(1)

    def acceptRemoteSocket(self):
        self.connection, self.remoteAddress = self.socket.accept()

        return self.remoteAddress

    def connectRemoteSocket(self, address):
        self.remoteAddress = address
        self.socket.connect(address)
        
    def receiveTcpPacket(self):
        data = self.connection.revc(1024)
        
        return data

    def sendTcpPacket(self, data):
        self.socket.send(data)
        
        
