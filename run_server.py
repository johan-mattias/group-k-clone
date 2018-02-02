from network import utils, TcpHandler, UdpHandler
import math, time, threading

class NetworkHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.main_tcp_handler = TcpHandler.TcpHandler()#Should be port 12000
        print(self.main_tcp_handler.port)
        self.udp_handler_listener = UdpHandler.UdpHandler()
        self.udp_handler_sender = UdpHandler.UdpHandler()

    def run(self):
        self.udp_thread = UdpThread(self.udp_handler_listener)
        self.main_tcp_thread = MainTcpThread(self.main_tcp_handler, self.udp_thread)
        self.main_tcp_thread.start()
        self.udp_thread.start()
        
class MainTcpThread(threading.Thread):
    def __init__(self, tcp_handler, udp_thread):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.udp_thread = udp_thread

    def run(self):
        while True:
            remote_address = self.tcp_handler.accept()
            new_tcp_handler = TcpHandler.TcpHandler()
            new_tcp_thread = TcpThread(new_tcp_handler, remote_address[0])
            new_port = new_tcp_thread.tcp_handler.port
            new_tcp_thread.start()
            #TODO
            #check auth
            self.udp_thread.add_accepted_ip((remote_address[0], None))
            #Send new_port to client
            #close connection
            #accept new connection

class TcpThread(threading.Thread):
    def __init__(self, tcp_handler, remote_ip):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.remote_ip = remote_ip

    def run(self):
        remote_address = self.tcp_handler.accept()
        #TODO if(remote_address[0] != remote_ip): handle
        print("Connection from", remote_address[0], "accepted")
        print("Expected from", self.remote_ip)
        
class UdpThread(threading.Thread):
    def __init__(self, udp_handler):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.address_list = list()
        self.ip_without_port = list()

    def run(self):
        while True:
            #receive
            address, data = self.udp_handler.receive()
            self.add_port(address)
            print(data)
            #send
            x, y = math.cos(angle)*50 + 200, math.sin(angle)*50 + 200
            angle += math.pi/30
            for address in self.address_list:
                if(address[1] != None):
                    self.udp_handler.send((address), (utils.unixtime(), int(x), int(y)))
            time.sleep(1/60)
                
    def add_accepted_ip(self, address):
        self.address_list.append(address)
        self.ip_without_port.append(address[0])

    def add_port(self, address):
        for ip in self.ip_without_port:
            if(address[0] == ip):
                for i in len(self.address_list):
                    if (address[0] == self.address_list[i][0]):
                        self.address_list[i][1] = address[1]
                        self.ip_without_port.remove(ip)
                        return

network = NetworkHandler()
network.start()


