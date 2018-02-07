import pyglet as py


class ClientGUI(py.window.Window):
    def __init__(self, size, game, entities=[]):
        self.WIDTH, self.HEIGHT = size
        self.entities = entities
        self.game = game
        super().__init__(self.WIDTH, self.HEIGHT)

    def on_draw(self):
        print("Should draw")
        self.clear()
        for entity in self.entities:
            entity.draw(self)

    def add_entity(self, ent):
        self.entities.append(ent)
