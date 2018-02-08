from snider_glider.player import PlayerTO
import queue


class ClientComm:
    def __init__(self):
        # Game->Network
        self.local_player = None

        # Network->Game
        # UDP
        self.player_updates = list()

        # TCP
        self.modification_queue = queue.Queue()
        self.tick_rate = 1 / 30

    def set_local_player(self, player_to):
        self.local_player = player_to

class ServerComm:
    def __init__(self):
        # Game->Network
        self.players = list()

        # Network->Game
        # UDP
        self.player_updates = queue.Queue()# (PlayerTO, client_time)

        # TCP
        self.modification_queue = queue.Queue()# (PlayerTO, action)
        self.tick_rate = 1/30
