import pyglet


class GameObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(GameObject, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
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
        if self.y > max_y:
            self.y = max_y
