import UdpThread

while True:
    address, data = UdpThread.receiveUdpPacket()
    print(address, data)
