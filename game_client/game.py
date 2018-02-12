import pyglet
from player import Player
from gameobject import GameObject
from random import randint

game_window = pyglet.window.Window(800, 600)

# player_batch = pyglet.graphics.Batch()

player_image = pyglet.resource.image('player.png')
# player = pyglet.sprite.Sprite(player_image, x=400, y=300, batch=player_batch)
# players = [player]


def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


center_image(player_image)
player = Player(user_id=1, name="Anton", npc=False, img=player_image, x=0, y=0, batch=None)
game_window.push_handlers(player)
game_window.push_handlers(player.key_handler)

player_batch = pyglet.graphics.Batch()
player2 = Player(user_id=2, name="Fredrik", npc=True, img=pyglet.resource.image('player2.png'), x=300, y=400, batch=player_batch)
player3 = Player(user_id=3, name="Filip", npc=True, img=pyglet.resource.image('player3.png'), x=400, y=300, batch=player_batch)
player4 = Player(user_id=4, name="Kasper", npc=True, img=pyglet.resource.image('player4.png'), x=500, y=500, batch=player_batch)
other_players = [player2, player3, player4]


@game_window.event
def on_draw():
    game_window.clear()
    player.draw()
    player_batch.draw()


def update(dt):
    player.update(dt)

    for p in other_players:
        x = p.x + randint(-10, 10) * 10 * dt
        y = p.y + randint(-10, 10) * 10 * dt
        p.update(dt, x, y)


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 120.0)
    pyglet.app.run()
