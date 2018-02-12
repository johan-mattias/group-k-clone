import pickle
import pyglet

class Player:

    def __init__(self, player_id, user_id, name, keys, image):
        self.player_id = player_id
        self.user_id = user_id
        
        self.sprite_width = 50
        self.sprite_height = 50

        self.image = image
        self.sprite = image
        if image == 'testSprite.png':
            image = pyglet.image.load('testSprite.png')
            self.sprite = pyglet.sprite.Sprite(image) #seg fault
            self.scale_sprite(self.sprite)
            
        self.movementSpeed = (0, 0)
        self.vSpeed = 0
        self.x, self.y = (0, 0)

        self.name = name
        self.controllable = False
        if keys is not None:
            self.up = keys[0]
            self.right = keys[1]
            self.down = keys[2]
            self.left = keys[3]
            self.controllable = True
        self.move_rate = 1

    def scale_sprite(self, sprite):
        x_scale = self.sprite_width/sprite.width
        y_scale = self.sprite_height/sprite.height

        sprite.scale_x = x_scale
        sprite.scale_y = y_scale
        
    def generate_movement_speed(self, keys):
        m1 = (0, 0)
        m2 = (0, 0)
        m3 = (0, 0)
        m4 = (0, 0)

        if keys[self.up]:       m1 = (0, self.move_rate)
        if keys[self.right]:    m2 = (self.move_rate, 0)
        if keys[self.down]:     m3 = (0, -self.move_rate)
        if keys[self.left]:     m4 = (-self.move_rate, 0)

        self.movementSpeed = tuple(map(sum, zip(m1, m2, m3, m4)))

    def draw_player(self, window):
        self.sprite.position = self.get_position()
        self.sprite.draw()
    
    def draw(self, py):
        self.draw_player(py)

    def move(self, keys):
        self.generate_movement_speed(keys)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def to_transfer_object(self):
        return PlayerTO(self.player_id, self.user_id, x=self.x, y=self.y, x_velocity=self.movementSpeed[0], y_velocity=self.movementSpeed[1], name=self.name)

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "pid: " + str(self.player_id) + " name: " + str(self.name) +  " image: " + str(self.image)
    
class PlayerTO:
    def __init__(self, player_id, user_id=None, x=None, y=None, x_velocity=None, y_velocity=None, color=None, name=None, image = None):
        self.player_id = player_id
        self.user_id = user_id
        self.x = x
        self.y = y

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

        self.color = color
        self.name = name
        self.image = image

    def serialize(self):
        return pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "pid: " + str(self.player_id) + " x: " + str(self.x) + " y: " + str(self.y)

def player_from_player_to(p, image = None):
    if image == None:
        return Player(p.player_id, p.user_id, p.name, None, p.image)
    else:
        return Player(p.player_id, p.user_id, p.name, None, image)
    
