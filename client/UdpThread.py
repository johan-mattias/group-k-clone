from socket import *
import pygame, sys, time
import UdpData

class UdpThread:

    def __init__(self, port = 12000):
        self.port = port
        
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', self.port))
        
    def receiveUdpPacket(self):
        data, address = self.socket.recvfrom(1024)

        return address, UdpData.unpackUserData(data)

    def sendUdpPacket(self, address, data):
        self.socket.sendto(UdpData.packUserData(data), address)
        
