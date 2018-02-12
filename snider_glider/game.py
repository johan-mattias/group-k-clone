import pyglet as py
import threading, time
import network.utils as net_utils
from snider_glider.player import Player
from snider_glider.client_gui import ClientGUI


class ClientGame(threading.Thread):

    def __init__(self,thread_id, thread_name, comms, size=(600, 400),tick_rate=1/100, demo_player=False):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.comms = comms

        self.STDMOVEMENTSPEED = (2, 0)
        self.WIDTH, self.HEIGHT = size
        self.TICK_RATE = tick_rate

        self.sprite_width = 50
        self.sprite_height = 50

        self.players = list()

        self.WINDOW = ClientGUI(size, self)
        self.keys = py.window.key.KeyStateHandler()
        self.WINDOW.push_handlers(self.keys)
        '''
        if demo_player:
            demo_player_image = py.image.load('testSprite.png')
            demo_player_sprite = py.sprite.Sprite(demo_player_image)
            self.scale_sprite(demo_player_sprite)
            self.demo_player = Player(demo_player_sprite, 'McFace', (py.window.key.UP, py.window.key.RIGHT, py.window.key.DOWN, py.window.key.LEFT))
            self.players[self.demo_player.player_id] = self.demo_player
            self.WINDOW.add_entity(self.demo_player)
        '''
        py.clock.schedule_interval(self.game_loop, self.TICK_RATE)        

    def update(self):
        id = data['player_id']
        self.players[id].x = data['x']
        self.players[id].y = data['y']        

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
            #time.sleep(self.TIC_RATE)

    def update_player_positions(self):
        '''
        for player_to in self.comms.player_updates:
            self.players[player_to.player_id].set_position(player_to.x, player_to.y)
        '''
        pass

    def handle_player_inputs(self):
        for player in self.players:
            if player.controllable:
                player.move(self.keys)
                self.comms.set_local_player(player.to_transfer_object())
                self.comms.time = net_utils.unixtime()
                break

    def add_player(self, player):
        self.players.append(player)
        self.WINDOW.add_entity(player)        
        
    def get_gui(self):
        return py
