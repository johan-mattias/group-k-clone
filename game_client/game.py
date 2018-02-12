import pyglet
from player import Player
from gameobject import GameObject
from random import randint


class GameWindow(pyglet.window.Window):
    def __init__(self, width=800, height=600):
        pyglet.window.Window.__init__(self, width=width, height=height)

        self.player = Player(user_id=1, name="Anton", npc=False, img=self.center_image(pyglet.resource.image('player.png')), x=0, y=0, batch=None)
        self.push_handlers(self.player)
        self.push_handlers(self.player.key_handler)

        self.player_batch = pyglet.graphics.Batch()
        player2 = Player(user_id=2, name="Fredrik", npc=True, img=self.center_image(pyglet.resource.image('player2.png')), x=300, y=400, batch=self.player_batch)
        player3 = Player(user_id=3, name="Filip", npc=True, img=self.center_image(pyglet.resource.image('player3.png')), x=400, y=300, batch=self.player_batch)
        player4 = Player(user_id=4, name="Kasper", npc=True, img=self.center_image(pyglet.resource.image('player4.png')), x=500, y=500, batch=self.player_batch)
        self.other_players = [player2, player3, player4]

    @staticmethod
    def center_image(image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        return image

    def on_draw(self):
        game_window.clear()
        self.player.draw()
        self.player_batch.draw()

    def update(self, dt):
        self.player.update(dt)

        for p in self.other_players:
            x = p.x + randint(-10, 10) * 10 * dt
            y = p.y + randint(-10, 10) * 10 * dt
            p.update(dt, x, y)


if __name__ == '__main__':
    game_window = GameWindow(width=800, height=600)
    pyglet.clock.schedule_interval(game_window.update, 1 / 120.0)
    pyglet.app.run()
