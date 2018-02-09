import threading

from snider_glider.utils import Action
from snider_glider.player import player_from_player_to


class ServerGame(threading.Thread):
    def __init__(self, thread_id, comm, tick_rate, game_size):
        self.action_mapping = {
            Action.ADD: self.add_player,
            Action.REMOVE: self.remove_player
        }

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.comm = comm
        self.players ={}

        self.TICK_RATE = tick_rate
        self.WIDTH, self.HEIGHT = game_size

    def run(self):
        while 1:
            self.game_loop()

    def game_loop(self):
        self.modify_players()
        self.handle_player_updates()
        self.set_player_updates()

    def modify_players(self):
        while not self.comm.modification_queue.empty():
            print("Should now add a player to the game")
            action, player_to = self.comm.modification_queue.get()
            self.modify_player(player_to, action)

    def modify_player(self, player_to, action):
        print ("Is in modify player function with: ", action)
        self.action_mapping[action](player_to)

    def remove_player(self, player_to):
        i = 0
        while i < len(self.players):
            if self.players[i].player_id == player_to.player_id:
                break
            else:
                i += 1
        try:
            del self.players[i]
        except KeyError:
            print("Player is not in the game!!")

    def add_player(self, player_to):
        print("player to add with id: ", player_to.player_id)
        new_player = player_from_player_to(player_to)
        self.players[new_player.player_id] = new_player

    def handle_player_updates(self):
        updates = []
        while not self.comm.player_updates.empty():
            updates.append(self.comm.player_updates.get())
        for player_to, client_time in updates:
            if player_to.player_id in self.players:
                self.handle_player_update(player_to, client_time)

    def handle_player_update(self, player_to, client_time):
        dx = player_to.x_velocity
        dy = player_to.y_velocity

        current_x, current_y = self.players[player_to.player_id].position
        new_x = current_x + dx
        new_y = current_y + dy

        self.players[player_to.player_id].position = (new_x, new_y)

        
    def set_player_updates(self):
        players_to_push = []
        for p_id, player in self.players.items():
            players_to_push.append(player.to_transfer_object())
        self.comm.players = players_to_push
