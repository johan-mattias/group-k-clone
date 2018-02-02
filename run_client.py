from network import utils, TcpHandler, UdpHandler
#from snider_glider import Game, ClientGUI, Player
import threading, queue

SERVER_TCP_ADDRESS = ("antoncarlsson.se", 12000)

class NetworkHandler(threading.Thread):
    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.tcp_handler = TcpHandler.TcpHandler(SERVER_TCP_ADDRESS)
        print("tcp", self.tcp_handler.port)
        self.udp_handler = UdpHandler.UdpHandler()
        self.udp_handler.socket.settimeout(1)
        print("udp", self.udp_handler.port)        
        self.data_queue = data_queue


    def run(self):
        print("initializing udp receiving")
        udp_port = self.udp_handler.port
        self.tcp_handler.connect()
        while True:
            #send
            self.udp_handler.send(("antoncarlsson.se", 12000), (utils.unixtime(), 1, 1))
            #receive
            try:
                address, data = self.udp_handler.receive()
                x_pos = data['xv']
                y_pos = data['yv']
                self.data_queue.put((x_pos, y_pos))
                print("X: " + str(x_pos) + " - Y:" + str(y_pos))
            except:
                print("didnt get")
                
def main():
    data_queue = queue.Queue(100)

    network_handler = NetworkHandler(data_queue)
    #game = Game.Game(2, "Game client", data_queue, demo_player=True)


    network_handler.start()
    #game.start()


if __name__ == '__main__':
    main()
