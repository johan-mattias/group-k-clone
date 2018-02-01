from socket import *
from struct import *
import Utils
import sys, time

class UdpHandler:

    def __init__(self):
        
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = Utils.get_free_port()
        self.socket.bind(('', self.port))
        
    def receive(self):
        data, address = self.socket.recvfrom(1024)

        return address, unpack_user_data(data)

    def send(self, address, data):
        self.socket.sendto(pack_user_data(data), address)

    def close(self):
        self.socket.close()


'''********************************
user_data_struct
********************************'''
user_data_struct = 'qhh'
user_data_struct_names = ('clientTime', 'xv', 'yv') 

def pack_user_data(data):
    return pack(userDataStruct, *data)
    
def unpack_user_data(binaryUserData):
    data = unpack(userDataStruct, binaryUserData)

    data_dict = {}
    for i in range(len(data)):
        data_dict[userDataStructNames[i]] = data[i]

    return data_dict
