from network import utils, tcp_handler, udp_handler, comm
from snider_glider.player import PlayerTO
#from snider_glider.game import ClientGame

import threading, queue

SERVER_TCP_ADDRESS = ("antoncarlsson.se", 12000)

class NetworkHandler(threading.Thread):
    def __init__(self, communication_object):
        threading.Thread.__init__(self)
        self.tcp_handler = tcp_handler.TcpHandler(SERVER_TCP_ADDRESS)
        print("tcp", self.tcp_handler.port)
        self.udp_handler = udp_handler.UdpHandler()
        print("udp", self.udp_handler.port)        
        self.communication_object = communication_object


    def run(self):
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


def main():
    communication_object = comm.ClientComm()

    network_handler = NetworkHandler(communication_object)
    #game_thread = ClientGame(2, "Game client", communication_object, demo_player=True)
    #gui = game_thread.get_gui()


    #game_thread.start()
    network_handler.start()

    #gui.gl.glClearColor(1, 1, 1, 1)
    #gui.app.run()


if __name__ == '__main__':
    main()
