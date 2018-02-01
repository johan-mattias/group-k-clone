import network.UdpHandler, network.TcpHandler, utils
import math, time

tcp = TcpHandler.TcpHandler()
udp = UdpHandler.UdpHandler()

print("waiting for TCP conn")
address = tcp.accept()
port = tcp.receive()
port = int(port.decode())

angle = 0

while True:
    x, y = math.cos(angle)*50 + 200, math.sin(angle)*50 + 200
    angle += math.pi/30
    udp.send((address[0], port), (utils.unixtime(), int(x), int(y)))
    time.sleep(1/60)
