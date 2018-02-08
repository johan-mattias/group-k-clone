from network import utils, tcp_handler, udp_handler, comm
import math, time, threading

class NetworkHandler(threading.Thread):
    def __init__(self, comm):
        threading.Thread.__init__(self)
        #create commincation between thread object
        self.comm = comm 
        #create handlers (sockets)
        self.main_tcp_handler = tcp_handler.TcpHandler() #Should be port 12000
        self.udp_handler_listener = udp_handler.UdpHandler()
        self.udp_handler_sender = udp_handler.UdpHandler()

        print("TCP on port:", self.main_tcp_handler.port) #debug
        print("UDP listener on port:", self.udp_handler_listener.port) #debug
        print("UDP sender on port:", self.udp_handler_sender.port) #debug        

    def run(self):
        #create threads
        address_list = list() #The list udp uses to send and receive data.
        self.udp_thread_listener = UdpThreadListener(self.udp_handler_listener, self.comm, address_list)
        self.udp_thread_sender = UdpThreadSender(self.udp_handler_sender, self.comm, address_list)        
        self.main_tcp_thread = MainTcpThread(self.main_tcp_handler, self.udp_thread, self.comm)
        #start threads
        self.main_tcp_thread.start()
        self.udp_thread_listener.start()
        self.udp_thread_sender.start()        
        
class MainTcpThread(threading.Thread):
    def __init__(self, tcp_handler, udp_thread, comm):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.udp_thread = udp_thread
        self.comm = comm

    def run(self):
        while True:
            remote_address = self.tcp_handler.accept()
            new_tcp_handler = tcp_handler.TcpHandler()
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
    def __init__(self, tcp_handler, remote_ip, comm):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler
        self.remote_ip = remote_ip
        self.comm = comm

    def run(self):
        remote_address = self.tcp_handler.accept()
        #TODO if(remote_address[0] != remote_ip): handle
        print("Connection from", remote_address[0], "accepted")
        print("Expected from", self.remote_ip)
        

class UdpThreadSender(threading.Thread):
    def __init__(self, udp_handler, comm, address_list):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comm = comm
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
    def __init__(self, udp_handler, comm, address_list):
        threading.Thread.__init__(self)
        self.udp_handler = udp_handler
        self.comm = comm
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
    #Todo: Create comm object and give it to both network threads and GameThread when created.
    comm = comm.ServerComm()
    
    network = NetworkHandler(comm)
    network.start()



if __name__ == '__main__':
    main()

