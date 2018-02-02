import time, socket

def unixtime():
    return int(time.time() * 1000)

def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 12000
    bound = False

    while not bound:
        try:
            sock.bind(('', port))
            bound = True
        except OSError:
            port = port + 1

    sock.close()
    sock = None
    return port
            
    
