from network import TcpHandler, UdpHandler
#from snider_glider import Game, ClientGUI, Player
import threading, queue

SERVER_TCP_ADDRESS = ("antoncarlsson.se", 12000)

class NetworkHandler(threading.Thread):
    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.tcp_handler = TcpHandler.TcpHandler(SERVER_TCP_ADDRESS)        
        self.udp_handler = UdpHandler.UdpHandler()
        self.data_queue = data_queue


    def run(self):
        print("initializing udp receiving")
        udp_port = self.udp_handler.port
        self.tcp_handler.connect()
        self.tcp_handler.send(str(udp_port).encode())
        while 1:
            address, data = self.udp_handler.receive()
            x_pos = data['xv']
            y_pos = data['yv']
            self.data_queue.put((x_pos, y_pos))
            print("X: " + str(x_pos) + " - Y:" + str(y_pos))


def main():
    data_queue = queue.Queue(100)

    network_handler = NetworkHandler(data_queue)
    #game = Game.Game(2, "Game client", data_queue, demo_player=True)


    network_handler.start()
    #game.start()


if __name__ == '__main__':
    main()
