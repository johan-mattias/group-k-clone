from snider_glider.player import PlayerTO
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
        self.modification_queue = queue.Queue()

    def set_local_player(self, player_to):
        self.local_player = player_to

    def add_players(self, data):
        players = list()
        for player in data:
            players.append(PlayerTO(player['player_id'],
                                    x = player['x'],
                                    y = player['y']))
            
        self.player_updates = players

class ServerComm:
    def __init__(self):
        # Game->Network
        self.players = list()

        # Network->Game
        # UDP
        self.player_updates = queue.Queue()# (PlayerTO, client_time)

        # TCP
        self.modification_queue = queue.Queue()# (action, PlayerTO)

    def add_player(self, data):
        self.player_updates.put((PlayerTO(data['player_id'],
                                          x_velocity = data['xv'],
                                          y_velocity = data['yv']),
                                 data['client_time']))
