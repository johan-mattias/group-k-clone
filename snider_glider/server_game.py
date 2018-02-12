import threading
import time
from snider_glider.utils import Action
from snider_glider.player import *


class ServerGame(threading.Thread):
    def __init__(self, thread_id, comm, tick_rate, game_size):
        self.action_mapping = {
            Action.ADD: self.add_player,
            Action.REMOVE: self.remove_player
        }

        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.comm = comm
        self.players = list()

        self.TICK_RATE = tick_rate
        self.WIDTH, self.HEIGHT = game_size

    def run(self):
        while 1:
            self.game_loop()

    def game_loop(self):
        self.modify_players()
        self.update_players()
        self.set_player_updates()
        time.sleep(self.TICK_RATE)
        

    def modify_players(self):
        while not self.comm.modification_queue.empty():
            #print("Should now add a player to the game")
            action, player_to = self.comm.modification_queue.get()
            self.modify_player(player_to, action)

    def modify_player(self, player_to, action):
        #print ("Is in modify player function with: ", action)
        self.action_mapping[action](player_to)

    def remove_player(self, player_to):
        self.players.remove(self.players[player_to.player_id])

    def add_player(self):
        new_id = len(self.players)
        new_player = Player(new_id, 92, "McFace", None, None)
        self.players.append(new_player)
        return new_id

    def update_players(self):
        '''
        #Gettings player_to objects from comm object
        updates = []
        while not self.comm.player_updates.empty():
            updates.append(self.comm.player_updates.get())
            
        #Updating each player that was found in comm object
        for player_to in updates:
            self.update_player(self.players[player_to[0].player_id], player_to[0])
         '''
        for player in self.players:
            self.update_player(player)


    def update(self, data):
        self.players[data['player_id']].movementSpeed = (data['xv'], data['yv'])
    
    def update_player(self, player):
        dx = player.movementSpeed[0]
        dy = player.movementSpeed[1]

        player.x = player.x + dx
        player.y = player.y + dy
        
    def set_player_updates(self):
        players_to_push = []
        for player in self.players:
            players_to_push.append(player.to_transfer_object())
        self.comm.players = players_to_push
        
