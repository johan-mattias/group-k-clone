from snider_glider.game import ServerGame
from network import utils, udp_handler, comm
from network.tcp_handler import *
import math, time, threading

class NetworkHandler(threading.Thread):
    def __init__(self, comms):
        threading.Thread.__init__(self)
        #commincation between thread object
        self.comms = comms 
        #create handlers (sockets)
        self.main_tcp_handler = TcpHandler() #Should be port 12000
        self.udp_handler_listener = udp_handler.UdpHandler()
        self.udp_handler_sender = udp_handler.UdpHandler()

        self.address_list = list() #The list udp uses to send and receive data.

        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self.comms, self.address_list)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self.comms, self.address_list)
        self.main_tcp_thread = MainTcpThread(self.main_tcp_handler, self.udp_thread_listener, self.comms)

        print("TCP on port:", self.main_tcp_handler.port) #debug
        print("UDP listener on port:", self.udp_handler_listener.port) #debug
        print("UDP sender on port:", self.udp_handler_sender.port) #debug        

    def run(self):
        #start threads
        self.main_tcp_thread.start()
        self.udp_thread_listener.start()
        self.udp_thread_sender.start()


class MainTcpThread(threading.Thread):
    def __init__(self, tcp_handler, udp_thread, comms):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.udp_thread = udp_thread
        self.comms = comms

    def run(self):
        while True:
            remote_address = self.tcp_handler.accept()
            new_tcp_handler = TcpHandler()
            new_tcp_thread = TcpThread(new_tcp_handler, remote_address[0], self.comms)
            new_port = new_tcp_thread.tcp_handler.port
            new_tcp_thread.start()
            #TODO check auth
            self.udp_thread.add_accepted_ip((remote_address[0], None))
            self.tcp_handler.send(DataFormat.PORT, new_port)
            self.tcp_handler.close_connection()


class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, remote_ip, comms):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.remote_ip = remote_ip
        self.comms = comms

    def run(self):
        remote_address = self.tcp_handler.accept()
        #TODO if(remote_address[0] != remote_ip): handle
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
        except socket.timeout:
            print("Socket timed out")
        

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
                if address[1] != None:
                    self.udp_handler.send((address), (utils.unixtime(), int(x), int(y)))
                    
            #Sleep
            time.sleep(1/60)
                



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

            #TEMPORARY
            #todo make nicer
            if data['clientTime'] == 0:
                print(data)
                for addr in self.address_list:
                    if address[0] == addr[0]:                    
                        addr = address
                        break    
            #TEMPORARY

            print(data)
            
            #sleep
            time.sleep(1/60)

    def add_accepted_ip(self, address):
        self.address_list.append(address)            

def main():

    comms = comm.ServerComm()

    network = NetworkHandler(comms)
    game_tread = ServerGame(9, comms, 1/30, (800, 600))

    network.start()
    game_tread.start()


if __name__ == '__main__':
    main()

