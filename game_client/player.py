import pyglet
from pyglet.window import key


class Player(pyglet.sprite.Sprite):
    def __init__(self, user_id, name, npc, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        self.user_id = user_id
        self.name = name
        self.npc = npc

        self.jumping = False
        self.velocity_x, self.velocity_y = 400.0, 30.0
        self.mass = 3
        self.key_handler = key.KeyStateHandler()

    def jump(self, dt):
        if self.velocity_y > 0:
            self.y += (0.5 * self.mass * (self.velocity_y ** 2)) * dt
        else:
            self.y += -(0.5 * self.mass * (self.velocity_y ** 2)) * dt

        self.velocity_y -= 2

    def update(self, dt, x=0, y=0):
        if self.npc:
            self.x = x
            self.y = y
        else:
            if self.key_handler[key.A]:
                self.x -= self.velocity_x * dt
            if self.key_handler[key.D]:
                self.x += self.velocity_x * dt
            if self.key_handler[key.SPACE] and not self.jumping:
                self.jumping = True

            if self.jumping:
                self.jump(dt)

        self.check_bounds()

    def check_bounds(self):
        min_x = self.image.width / 2
        min_y = self.image.height / 2
        max_x = 800 - self.image.width / 2
        max_y = 600 - self.image.height / 2

        if self.x < min_x:
            self.x = min_x
        if self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
            self.jumping = False
            self.velocity_y = 30.0
        if self.y > max_y:
            self.y = max_y
