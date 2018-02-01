import UdpThread

thread = UdpThread.UdpThread()

while True:
    address, data = thread.receiveUdpPacket()
    print(address, data)
