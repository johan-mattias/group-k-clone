from network import utils, udp_handler, comm
from network.tcp_handler import *
from snider_glider.game import ClientGame
from snider_glider.player import *
from snider_glider.utils import Action
import threading, queue, time

SERVER_MAIN_TCP_ADDRESS = ("antoncarlsson.se", 12000)
PLAYER_SPRITE = pyglet.sprite.Sprite(pyglet.image.load('testSprite.png'))

class NetworkHandler(threading.Thread):
    def __init__(self, comms, game_thread):
        threading.Thread.__init__(self)
        #commincation between thread object
        self.comms = comms
        self.game_thread = game_thread
        #create handlers (sockets)
        self.tcp_handler = TcpHandler()
        self.udp_handler_listener = udp_handler.UdpHandler()
        self.udp_handler_sender = udp_handler.UdpHandler()

        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self.comms)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self.comms)
        self.tcp_thread = TcpThread(self.tcp_handler, SERVER_MAIN_TCP_ADDRESS, self.comms, self.game_thread)

    def run(self):
        self.tcp_thread.start()
        self.udp_thread_listener.start()
        self.udp_thread_sender.start()


class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, server_address, comms, game_thread):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.server_address = server_address
        self.comms = comms
        self.udp_port = None
        self.player_id = None
        self.game_thread = game_thread

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
        players = data[1]
        for player in players:
            new_player = player_from_player_to(player)
            if new_player.player_id == self.player_id:
                gui = self.game_thread.get_gui()                    
                new_player.up = gui.window.key.UP
                new_player.right = gui.window.key.RIGHT
                new_player.down = gui.window.key.DOWN
                new_player.left = gui.window.key.LEFT
                new_player.controllable = True
                new_player.sprite = PLAYER_SPRITE
                self.game_thread.scale_sprite(PLAYER_SPRITE)
            self.game_thread.add_player(new_player)
            
    def run(self):
        self.connect_to_server()
        self.connect_to_new_tcp_socket()
        self.get_players()
        print(self.game_thread.players)
        '''
        while self.comms.local_player is None:
            pass
        self.tcp_handler.send(DataFormat.PLAYER_UDPATE, (Action.ADD, self.comms.local_player))
        '''
        while True:
            self.tcp_loop()
            
    def tcp_loop(self):
        self.handle_send()
        self.handle_recv()
        
    def handle_send(self):
        #TODO check comms queue
        while not self.comms.modification_queue.empty():
            player_to, action = self.comms.modification_queue.get()
            self.tcp_handler.send((DataFormat.PLAYER_UDPATE, (action, player_to)))

    def handle_recv(self):
        self.tcp_handler.socket.settimeout(0.5)
        try:
            data = self.tcp_handler.receive()
        except:
            pass
            #print("Socket timed out, nothing to receive")


class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, comms):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comms = comms

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
    def __init__(self, udp_handler, comms):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comms = comms
        self.have_received_server_data = False

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
                except:
                    pass
            
            #sleep
            #time.sleep(1/60)        


def main():
    communication_object = comm.ClientComm()

    game_thread = ClientGame(2, "Game client", communication_object, demo_player=True)
    network_handler = NetworkHandler(communication_object, game_thread)
    
    network_handler.start()

    gui = game_thread.get_gui()    
    game_thread.start()

    gui.gl.glClearColor(1, 1, 1, 1)
    gui.app.run()




if __name__ == '__main__':
    main()
