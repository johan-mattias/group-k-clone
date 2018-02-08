from network import utils, udp_handler, comm
from network.tcp_handler import *
from snider_glider.player import PlayerTO
from snider_glider.game import ClientGame

import threading, queue

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


        '''
        print("initializing udp receiving")
        udp_port = self.udp_handler.port
        self.tcp_handler.connect()
        data = self.tcp_handler.receive()
        print("NEW PORT:", data[1])
        while True:
            #send
            print("send")
            self.udp_handler.send(("antoncarlsson.se", 12000), (utils.unixtime(), 1, 1))
            #receive
            print("recv")
            try:
                self.udp_handler.socket.settimeout(1)
                address, data = self.udp_handler.receive()
                x_pos = data['xv']
                y_pos = data['yv']
                #self.data_queue.put((x_pos, y_pos))
                print("Rec     ====    X: " + str(x_pos) + " - Y:" + str(y_pos))
            except:
                print("didnt get")
            print("X: " + str(self.communication_object.local_player.x) + " - Y: " + str(self.communication_object.local_player.y))
            '''

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
        self.server_address = (server_address[0], new_port)
        #TODO close
        self.tcp_handler.connect(self.server_address)
        while True:
            self.tcp_loop()
            
    def tcp_loop(self):
        self.handle_send()
        self.handle_recv()
        
    def handle_send(self):
        #TODO check comms queue        
        pass

    def handle_recv(self):
        self.tcp_handler.socket.settimeout(0.5)
        try:
            data = self.tcp_handler.receive()
        
class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, comms, address_list):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comms = comms
        self.address_list = address_list

    def run(self):
        angle = 0
        while True:
            #calculate position
            x, y = math.cos(angle)*50 + 200, math.sin(angle)*50 + 200
            angle += math.pi/30

            #send
            for address in self.address_list:
                if(address[1] != None):
                    self.udp_handler.send((address), (utils.unixtime(), int(x), int(y)))
                    
            #Sleep
            time.sleep(1/60)
                
    def add_accepted_ip(self, address):
        self.address_list.append(address)

class UdpThreadListener(threading.Thread):
    def __init__(self, udp_handler, comms, address_list):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comms = comms
        self.address_list = address_list

    def run(self):
        while True:
            #receive
            address, data = self.udp_handler.receive()
            print(data)

            #TEMPORARY
            for addr in self.address_list:
                if address[0] == addr[0]:
                    addr = address
                    break
            #TEMPORARY
            
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
