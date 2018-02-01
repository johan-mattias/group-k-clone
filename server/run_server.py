import UdpThread
import TcpThread
import math
import time

udp = UdpThread.UdpThread()
tcp = TcpThread.TcpThread()

print("waiting for TCP conn")
address = tcp.accept()
port = tcp.receive()
port = int(port.decode())

angle = 0

while True:
    x, y = math.cos(angle)*50 + 200, math.sin(angle)*50 + 200
    angle += math.pi/30
    udp.send((address[0], port), (int(time.time() * 1000), int(x), int(y)))
    time.sleep(1/60)
