from network import utils, udp_handler, comm
from network.tcp_handler import *
from snider_glider.game import ClientGame
from snider_glider.utils import Action
import threading, queue, time

SERVER_MAIN_TCP_ADDRESS = ("antoncarlsson.se", 12000)

class NetworkHandler(threading.Thread):
    def __init__(self, comms):
        threading.Thread.__init__(self)
        #commincation between thread object
        self.comms = comms
        #create handlers (sockets)
        self.tcp_handler = TcpHandler()
        self.udp_handler_listener = udp_handler.UdpHandler()
        self.udp_handler_sender = udp_handler.UdpHandler()


    def run(self):
        #create threads
        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self.comms)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self.comms)        
        self.tcp_thread = TcpThread(self.tcp_handler, SERVER_MAIN_TCP_ADDRESS, self.comms)
        #start threads
        self.tcp_thread.start()
        self.udp_thread_listener.start()
        self.udp_thread_sender.start()


class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, server_address, comms):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.server_address = server_address
        self.comms = comms

    def run(self):
        self.tcp_handler.connect(self.server_address)
        data = self.tcp_handler.receive()
        new_port = data[1]
        self.server_address = (self.server_address[0], new_port)
        self.tcp_handler.close()
        self.tcp_handler = TcpHandler()
        self.tcp_handler.connect(self.server_address)
        while self.comms.local_player is None:
            pass
        self.tcp_handler.send(DataFormat.PLAYER_UDPATE, (Action.ADD, self.comms.local_player))
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
        except socket.timeout:
            print("Socket timed out, nothing to receive")


class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, comms):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comms = comms

    def run(self):
        while True:
            #send
            self.udp_handler.send(("antoncarlsson.se", 12000), (utils.unixtime(), 1, 1))  
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
            if not self.have_received_server_data:
                self.udp_handler.send(("antoncarlsson.se", 12000), (0,0,0))
                try:
                    self.udp_handler.socket.settimeout(0.1)
                    self.udp_handler.receive()
                    self.have_received_server_data = True
                except:
                    print("havent gotten anything")
            address, data = self.udp_handler.receive()
            x_pos = data['xv']
            y_pos = data['yv']
            print(" X:", x_pos, " - Y:", y_pos)
            
            #sleep
            time.sleep(1/60)        


def main():
    communication_object = comm.ClientComm()

    network_handler = NetworkHandler(communication_object)
    game_thread = ClientGame(2, "Game client", communication_object, demo_player=True)
    gui = game_thread.get_gui()


    game_thread.start()
    network_handler.start()

    gui.gl.glClearColor(1, 1, 1, 1)
    gui.app.run()


if __name__ == '__main__':
    main()
