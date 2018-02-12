import pyglet
from snider_glider.player import Player
from random import randint


class GameWindow(pyglet.window.Window):
    def __init__(self, width=800, height=600):
        pyglet.window.Window.__init__(self, width=width, height=height)
        self.other_players = []
        self.player = None
        #self.create_new_player(1, 1, "Anton", False)

        self.player_batch = pyglet.graphics.Batch()
        #self.create_new_player(2, 2, "Fredrik", True, self.player_batch)
        #self.create_new_player(3, 3, "Filip", True, self.player_batch)
        #self.create_new_player(4, 4, "Kasper", True, self.player_batch)
        self.player_images = []
        for i in range(1, 4):
            self.player_images.append(self.center_image(pyglet.resource.image('player' + str(i) + '.png')))

    def create_new_player(self, user_id, player_id, name, npc=True):
        batch = self.player_batch if npc else None
        player_image = self.player_images[player_id % 4 + 1]

        player = Player(user_id=user_id, player_id=player_id, name=name, npc=npc, img=player_image, x=0, y=0,
                        batch=batch)
        if npc:
            self.other_players.append(player)
        else:
            self.player = player
            self.push_handlers(self.player)
            self.push_handlers(self.player.key_handler)            

    @staticmethod
    def center_image(image):
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        return image

    def on_draw(self):
        self.clear()
        if self.player != None:
            self.player.draw()
        self.player_batch.draw()

    def update(self, dt):
        if self.player != None:
            self.player.update(dt)

        for p in self.other_players:
            x = p.x + randint(-10, 10) * 10 * dt
            y = p.y + randint(-10, 10) * 10 * dt
            p.update(dt, x, y)


if __name__ == '__main__':
    game_window = GameWindow(width=800, height=600)
    pyglet.clock.schedule_interval(game_window.update, 1 / 120.0)
    pyglet.app.run()
