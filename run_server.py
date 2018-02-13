from snider_glider.server_game import ServerGame
from snider_glider.utils import Action
from network import utils
from network.tcp_handler import *
from network.udp_handler import *
import math, time, threading


class NetworkHandler(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        #game object
        self.game = game
        #create handlers (sockets)
        self.main_tcp_handler = TcpHandler() #Should be port 12000
        self.udp_handler_listener = UdpHandler()
        self.udp_handler_sender = UdpHandler()

        self.address_list = list() #The list udp uses to send and receive data.

        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self.address_list, self)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self.address_list, self)
        self.main_tcp_thread = MainTcpThread(self.main_tcp_handler, self.address_list, self)

        print("TCP on port:", self.main_tcp_handler.port) #debug
        print("UDP listener on port:", self.udp_handler_listener.port) #debug
        print("UDP sender on port:", self.udp_handler_sender.port) #debug

    def run(self):
        #start threads
        self.main_tcp_thread.start()
        self.udp_thread_listener.start()
        self.udp_thread_sender.start()


class MainTcpThread(threading.Thread):
    def __init__(self, tcp_handler, address_list, parent):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.address_list = address_list
        self.parent = parent
        self.children = list()

    def run(self):
        while True:
            remote_ip = self.accept_new_connection() #accept new connection
            new_tcp_thread = self.create_new_tcp_thread(remote_ip) #create new tcp thread
            #TODO Check auth
            #TODO Match auth to user_id and name, set those on row below
            new_player_id = self.parent.game.add_player(user_id=42, name="Mr. Borg") #create new player
            self.send_new_player_to_other_clients(new_player_id)#woop woop
            self.address_list.append((remote_ip, None)) #add new ip to address list
            self.send_info_to_client(new_tcp_thread, new_player_id) #send info about ports and player_id to client
            self.children.append(new_tcp_thread) #add new tcp thread to children list            
            self.tcp_handler.close_connection() #close connection to make room for a new

    def send_new_player_to_other_clients(self, player_id):
        player = self.parent.game.players[player_id]
        for child in self.children:
            child.send_add_player(player)
            
    def accept_new_connection(self):
        remote_address = self.tcp_handler.accept()
        return remote_address[0]

    def create_new_tcp_thread(self, remote_ip):
        new_tcp_handler = TcpHandler()
        new_tcp_thread = TcpThread(new_tcp_handler, remote_ip, self)
        new_tcp_thread.start()        
        return new_tcp_thread

    def send_info_to_client(self, tcp_thread, player_id):
        tcp_port = tcp_thread.tcp_handler.port
        udp_port = self.parent.udp_thread_listener.udp_handler.port
        self.tcp_handler.send(DataFormat.PORTS_AND_PLAYER_ID, (tcp_port, udp_port, player_id))
        

class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, remote_ip, parent):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.remote_ip = remote_ip
        self.parent = parent

    def run(self):
        remote_address = self.tcp_handler.accept()
        if(remote_address[0] == self.remote_ip): #TODO handle more harshly
            print("Correct expected address")
        else:
            print("Wrong excpeted address")
            print("Expected:", self.remote_ip)
            print("Got:", remote_address[0])
            
        self.send_players()
        
        while True:
            self.receive()


    def receive(self):
        time.sleep(1)
    
    def send_players(self):
        try:
            player_list = list(self.parent.parent.game.players)
            self.tcp_handler.send(DataFormat.PLAYERS, player_list)
        except:
            pass

    def send_add_player(self, player):
        try:
            print("SENDING", player)
            self.tcp_handler.send(DataFormat.PLAYER_UPDATE,
                                  (Action.ADD, player))
        except:
            pass
                              
            
        


class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, address_list, parent):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.address_list = address_list
        self.parent = parent        
    
    def run(self):
        while True:
            binary_data = self.make_packet_to_send()
            
            for address in self.address_list:
                if address[1] != None:
                    self.udp_handler.send_binary_data(address, binary_data)
                    
            time.sleep(1/60)
            
    def make_packet_to_send(self):
        player_list = list(self.parent.game.players)
        
        players = list()
        for player in player_list:
            players.append((player.player_id, player.x, player.y, utils.unixtime()))

        binary_data = pack_server_data(players)

        return binary_data                


class UdpThreadListener(threading.Thread):
    def __init__(self, udp_handler, address_list, parent):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.address_list = address_list
        self.parent = parent

    def update_address(self, address):
        print(address)
        for i in range(len(self.address_list)):
            if self.address_list[i][0] == address[0] and self.address_list[i][1] == None:
                self.address_list[i] = address
                break
        print(self.address_list)
        
            

    def run(self):
        while True:
            address, data = self.udp_handler.receive_player()
            if data['client_time'] == 0:
                self.update_address(address)
            else:
                id = data['player_id']
                try:
                    self.parent.game.players[id].x = data['x']
                    self.parent.game.players[id].y = data['y']
                except:
                    pass


def main():                       
    game = ServerGame()
    network = NetworkHandler(game)

    network.start()


if __name__ == '__main__':
    main()

