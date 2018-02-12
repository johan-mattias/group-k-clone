import pyglet


class GameObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(GameObject, self).__init__(*args, **kwargs)

    def update(self, x, y):
        self.x = x
        self.y = y

