import time, socket

def unixtime():
    return int(time.time() * 1000)

def get_free_udp_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 12000
    bound = False

    while not bound:
        try:
            sock.bind(('', port))
            bound = True
        except:
            port = port + 1

    sock.close()
    return port

def get_free_tcp_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 12000
    bound = False

    while not bound:
        try:
            sock.bind(('', port))
            bound = True
        except:
            port = port + 1

    sock.close()
    return port            
    
