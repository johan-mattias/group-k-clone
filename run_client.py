from network import utils
from network.udp_handler import *
from network.tcp_handler import *
from snider_glider.game import *
from snider_glider.player import *
from snider_glider.utils import Action
import threading, queue, time

SERVER_MAIN_TCP_ADDRESS = ("antoncarlsson.se", 12000)

class NetworkHandler(threading.Thread):
    def __init__(self, game_window):
        threading.Thread.__init__(self)
        #commincation between thread object
        self.game_window = game_window
        #create handlers (sockets)
        self.tcp_handler = TcpHandler()
        self.udp_handler_listener = UdpHandler()
        self.udp_handler_sender = UdpHandler()

        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self)
        self.tcp_thread = TcpThread(self.tcp_handler, SERVER_MAIN_TCP_ADDRESS, self)

    def run(self):
        self.tcp_thread.start()
        #self.udp_thread_listener.start()
        #self.udp_thread_sender.start()


class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, server_address, parent):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.server_address = server_address
        self.udp_port = None
        self.player_id = None
        self.parent = parent

    def connect_to_server(self):
        self.tcp_handler.connect(self.server_address)
        data = self.tcp_handler.receive()
        new_port = data[1][0]
        self.udp_port = data[1][1]
        self.player_id = data[1][2]
        self.server_address = (self.server_address[0], new_port)
        
    def connect_to_new_tcp_socket(self):
        self.tcp_handler.close()
        self.tcp_handler = TcpHandler()
        self.tcp_handler.connect(self.server_address)

    def get_players(self):
        data = self.tcp_handler.receive()
        print (data)
        players = data[1]
        print(players)
        for player in players:
            print("adding", player, "own id:",self.player_id)
            self.parent.game_window.create_new_player(player.player_id,
                                                      player.user_id,
                                                      player.name,
                                                      player.player_id == self.player_id)
            
    def run(self):
        self.connect_to_server()
        self.connect_to_new_tcp_socket()
        self.get_players()
        #print(self.parent.game_window.players)


class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, parent):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.parent = parent

    def run(self):
        while True:
            #send
            #todo not static address
            player = self.comms.local_player
            if player != None:
                self.udp_handler.send_player(("antoncarlsson.se", 12000), (player.player_id, player.x_velocity, player.y_velocity, self.comms.time))
            #Sleep
            time.sleep(1/60)


class UdpThreadListener(threading.Thread):
    def __init__(self, udp_handler, parent):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.have_received_server_data = False
        self.parent = parent

    def run(self):
        while True:
            #TEMPORARY
            if not self.have_received_server_data:
                self.udp_handler.send_player(("antoncarlsson.se", 12000), (0,0,0,0))
                try:
                    self.udp_handler.socket.settimeout(0.1)
                    self.udp_handler.receive_players()
                    self.have_received_server_data = True
                except:
                    pass
                time.sleep(1/10)
            #TEMPORARY
            else:
                try:
                    address, data = self.udp_handler.receive_players()
                    self.comms.add_players(data)
                    #self.game_thread.update(data)
                except:
                    pass
            
            #sleep
            #time.sleep(1/60)        


def main():
    game_window = GameWindow(width=800, height=600)
    network_handler = NetworkHandler(game_window)
    
    network_handler.start()
    
    pyglet.clock.schedule_interval(game_window.update, 1 / 120.0)
    pyglet.app.run()

if __name__ == '__main__':
    main()
