from socket import *
from struct import *
from ... import utils
import sys, time

class UdpHandler:

    def __init__(self):
        
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = utils.get_free_port()
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
    return pack(user_data_struct, *data)
    
def unpack_user_data(binary_user_data):
    data = unpack(user_data_struct, binary_user_data)

    data_dict = {}
    for i in range(len(data)):
        data_dict[user_data_struct_names[i]] = data[i]

    return data_dict
