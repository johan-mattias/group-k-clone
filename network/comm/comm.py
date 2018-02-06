import snider_glider.player.PlayerTO
import queue


class ClientComm:
    def __init__(self):
        # Game->Network
        self.local_player = None

        # Network->Game
        # UDP
        self.player_updates = None

        # TCP
        self.modification_queue = queue.Queue()
        self.tick_rate = 1 / 30


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
