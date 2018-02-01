import TcpThread, UdpThread, Game, ClientGUI, Player, threading, queue


exitFlag = 0


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
        self.tcp_handler.connect()
        self.tcp_handler.send(b'12000')
        while 1:
            address, data = self.udp_handler.receiveUdpPacket()
            x_pos = data['xv']
            y_pos = data['yv']
            self.data_queue.put((x_pos, y_pos))
            print("X: " + str(x_pos) + " - Y:" + str(y_pos))


REMOTE_URL = "antoncarlsson.se"
REMOTE_UDP_PORT = 12000
REMOTE_TCP_PORT = 12001
LOCAL_TCP_PORT = 12012


def main():
    udp_handler = UdpThread.UdpThread(REMOTE_UDP_PORT)
    tcp_handler = TcpThread.TcpThread(LOCAL_TCP_PORT, (REMOTE_URL, REMOTE_TCP_PORT))

    data_queue = queue.Queue(100)

    network_handler = NetworkHandler(1, "Network", udp_handler, tcp_handler, data_queue)
    game = Game.Game(2, "Game client", data_queue, demo_player=True)


    network_handler.start()
    game.start()


if __name__ == '__main__':
    main()
