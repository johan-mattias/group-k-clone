import pyglet as py
import threading
from Player import Player
from ClientGUI import ClientGUI


class Game(threading.Thread):

    def __init__(self,thread_id, thread_name, data_queue, size=(600, 400),tic_rate=1/60, demo_player=False):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.data_queue = data_queue

        self.STDMOVEMENTSPEED = (2, 0)
        self.WIDTH, self.HEIGHT = size
        self.TIC_RATE = tic_rate

        self.sprite_width = 50
        self.sprite_height = 50

        self.players = []

        self.WINDOW = ClientGUI(size, self)
        py.gl.glClearColor(1, 1, 1, 1)
        self.keys = py.window.key.KeyStateHandler()
        self.WINDOW.push_handlers(self.keys)

        if demo_player:
            demo_player_image = py.image.load('testSprite.png')
            demo_player_sprite = py.sprite.Sprite(demo_player_image)
            self.scale_sprite(demo_player_sprite)
            self.demo_player = Player(demo_player_sprite, 'McFace', (py.window.key.UP, py.window.key.RIGHT, py.window.key.DOWN, py.window.key.LEFT))
            self.WINDOW.add_entity(self.demo_player)

    def run_game(self):
        py.app.run()

    def scale_sprite(self, sprite):
        x_scale = self.sprite_width/sprite.width
        y_scale = self.sprite_height/sprite.height

        sprite.scale_x = x_scale
        sprite.scale_y = y_scale

    def game_loop(self, dt):
        self.demo_player.set_position(self.data_queue.get())
        self.demo_player.move(self.keys)

    def run(self):
        py.clock.schedule_interval(self.game_loop, self.TIC_RATE)
        self.run_game()

    #Colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255

