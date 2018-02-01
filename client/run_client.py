import TcpHandler, UdpHandler, Game, ClientGUI, Player,
import threading, queue

class NetworkHandler(threading.Thread):
    def __init__(self, threadID, name, udp_handler, tcp_handler, data_queue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.udp_handler = udp_handler
        self.tcp_handler = tcp_handler
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


SERVER_TCP_ADDRESS = ("antoncarlsson.se", 12000)


def main():
    udp_handler = UdpHandler.UdpHandler()
    tcp_handler = TcpHandler.TcpHandler(SERVER_TCP_ADDRESS)

    data_queue = queue.Queue(100)

    network_handler = NetworkHandler(1, "Network", udp_handler, tcp_handler, data_queue)
    game = Game.Game(2, "Game client", data_queue, demo_player=True)


    network_handler.start()
    game.start()


if __name__ == '__main__':
    main()
