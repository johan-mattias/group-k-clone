import pyglet as py
import threading, time
from snider_glider.player import Player, player_from_player_to
from snider_glider.client_gui import ClientGUI
from enum import Enum


class Action(Enum):
    ADD = 0
    REMOVE = 1
    MODIFY = 2


class ClientGame(threading.Thread):

    def __init__(self,thread_id, thread_name, comm, size=(600, 400),tic_rate=1/60, demo_player=False):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.comm = comm

        self.STDMOVEMENTSPEED = (2, 0)
        self.WIDTH, self.HEIGHT = size
        self.TIC_RATE = tic_rate

        self.sprite_width = 50
        self.sprite_height = 50

        self.players = dict()

        self.WINDOW = ClientGUI(size, self)
        self.keys = py.window.key.KeyStateHandler()
        self.WINDOW.push_handlers(self.keys)

        if demo_player:
            demo_player_image = py.image.load('testSprite.png')
            demo_player_sprite = py.sprite.Sprite(demo_player_image)
            self.scale_sprite(demo_player_sprite)
            self.demo_player = Player(demo_player_sprite, 'McFace', (py.window.key.UP, py.window.key.RIGHT, py.window.key.DOWN, py.window.key.LEFT))
            self.players[self.demo_player.player_id] = self.demo_player
            self.WINDOW.add_entity(self.demo_player)

        py.clock.schedule_interval(self.game_loop, self.TIC_RATE)

    def run_game(self):
        py.app.run()

    def scale_sprite(self, sprite):
        x_scale = self.sprite_width/sprite.width
        y_scale = self.sprite_height/sprite.height

        sprite.scale_x = x_scale
        sprite.scale_y = y_scale

    def game_loop(self, dt):
        #print("Running game_loop")
        self.update_player_positions()
        self.handle_player_inputs()

    def run(self):
        while 1:
            self.game_loop(1)
            time.sleep(self.TIC_RATE)

    def update_player_positions(self):
        for player_to in self.comm.player_updates:
            self.players[player_to.player_id].set_position(player_to.get_position())

    def handle_player_inputs(self):
        try:
            self.demo_player.move(self.keys)
        except KeyError:
            print("No demo-player ya n00b")
        self.comm.set_local_player(self.demo_player.to_transfer_object())

    def get_gui(self):
        return py


class ServerGame(threading.Thread):
    def __init__(self, thread_id, comm, tick_rate, game_size):
        self.action_mapping = {
            Action.ADD: self.add_player,
            Action.REMOVE: self.remove_player
        }

        threading.Thread__init__(self)
        self.thread_id = thread_id
        self.comm = comm
        self.players ={}

        self.TICK_RATE = tick_rate
        self.WIDTH, self.HEIGHT = game_size

    def run(self):
        self.players = list()
        while 1:
            self.game_loop()

    def game_loop(self):
        self.modify_players()
        self.handle_player_updates()
        self.set_player_updates()

    def modify_players(self):
        while not self.comm.modification_queue.empty():
            player_to, action = self.comm.modification_queue.get()
            self.modify_player(player_to, action)

    def modify_player(self, player_to, action):
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
        new_player = player_from_player_to(player_to)
        self.players[new_player.player_id] = new_player

    def handle_player_updates(self):
        updates = []
        while not self.comm.player_updates.empty():
            updates.append(self.comm.player_updates.get())
        for player_to, client_time in updates:
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
        for player in self.players:
            players_to_push.append(player.to_transfer_object())

        self.comm.players = players_to_push

