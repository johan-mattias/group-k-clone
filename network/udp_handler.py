from socket import *
from struct import *
import network.utils as utils

class UdpHandler:

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.port = utils.get_free_udp_port()
        self.socket.bind(('', self.port))
        
    def receive_player(self):
        data, address = self.socket.recvfrom(1024)

        return address, unpack_user_data(data)

    def receive_players(self):
        data, address = self.socket.recvfrom(1024)

        return address, unpack_server_data(data)
    
    def send_player(self, address, data):
        self.socket.sendto(pack_user_data(data), address)
    
    def send_players(self, address, data):
        self.socket.sendto(pack_server_data(data), address)
    
    def close(self):
        self.socket.close()


'''********************************
user_data_struct
********************************'''
user_data_struct = 'ihhq'
user_data_struct_names = ('player_id', 'xv', 'yv', 'client_time') 

def pack_user_data(data):
    print("Pack user data", data)
    return pack(user_data_struct, *data)
    
def unpack_user_data(binary_user_data):
    data = unpack(user_data_struct, binary_user_data)

    data_dict = {}
    for i in range(len(data)):
        data_dict[user_data_struct_names[i]] = data[i]

    return data_dict

'''********************************
server_data_struct
********************************'''

def pack_server_data(data):
    server_data_struct = 'H'
    data_tuple = (len(data),)
    i = 0

    for p in data:
        server_data_struct += "ihhq"
        data_tuple = data_tuple + p
        i = i + 1

    return pack(server_data_struct, *data_tuple)
    

def unpack_server_data(binary_server_data):
    number_of_players = unpack('H', binary_server_data[:2])[0]
    server_data_struct = 'H' + "ihhq"*number_of_players
    player_data = unpack(server_data_struct, binary_server_data)
    player_list = list()

    i = 1
    while i < len(player_data):
        player_list.append({'player_id': player_data[i], 'x': player_data[i+1], 'y': player_data[i+2], 'client_time': player_data[i+3]})
        i += 4

    return player_list
