from socket import *
import pyglet as py
import sys, time
from Player import Player
from ClientGUI import ClientGUI


class Game:
    def __init__(self, size, demo_player=False):
        self.STDMOVEMENTSPEED = (2, 0)
        self.WIDTH, self.HEIGHT = size


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
        self.demo_player.move(self.keys)




#Constants for use/interaction in/with pyglet library
SIZE = WIDTH, HEIGHT = 600, 400
TIC_RATE = 1/60

#Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255


#Initializing window, adding stuffs to event-handler and running app.
game = Game(SIZE, True)
py.clock.schedule_interval(game.game_loop, TIC_RATE)
game.run_game()



'''
clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(1)
message = str(w)+','+str(d)+','+str(s)+','+str(a)
message = message.encode()
addr = ("antoncarlsson.se", 12000)
clientSocket.sendto(message, addr)
try:
data, server = clientSocket.recvfrom(1024)
print (data)

except timeout:
print ('REQUEST TIMED OUT')

p.generateMovementSpeed(keys)
p.drawPlayer(DISPLAYSURFACE)
pygame.display.flip()
time.sleep(0.1/10)


clientSocket.close()
'''
