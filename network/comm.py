import queue


class ClientComm:
    def __init__(self):
        # Game->Network
        self.local_player = None
        self.time = 0

        # Network->Game
        # UDP
        self.player_updates = list()

        # TCP
        self.modification_queue = queue.Queue()#(action, PlayerTO)

class ServerComm:
    def __init__(self):
        # Game->Network
        self.players = list()

        # Network->Game
        # UDP
        self.player_updates = queue.Queue()# (PlayerTO, client_time)

        # TCP
        self.modification_queue = queue.Queue()#(action, PlayerTO)


