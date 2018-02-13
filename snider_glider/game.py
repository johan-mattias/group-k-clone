import pyglet
from snider_glider.player import Player
from snider_glider.utils import Action
from random import randint


class GameWindow(pyglet.window.Window):
    def __init__(self, shared_communication, width=800, height=600):
        pyglet.window.Window.__init__(self, width=width, height=height)
        self.shared_communication = shared_communication
        
        self.other_players = []
        self.player = None
        #self.create_new_player(1, 1, "Anton", False)

        self.player_batch = pyglet.graphics.Batch()
        #self.create_new_player(2, 2, "Fredrik", True, self.player_batch)
        #self.create_new_player(3, 3, "Filip", True, self.player_batch)
        #self.create_new_player(4, 4, "Kasper", True, self.player_batch)
        self.player_images = []
        for i in range(1, 5):
            self.player_images.append(self.center_image(pyglet.resource.image('snider_glider/player' + str(i) + '.png')))

        self.name_batch = pyglet.graphics.Batch()

    def create_new_player(self, user_id, player_id, name, npc=True):
        batch = self.player_batch if npc else None
        player_image = self.player_images[player_id % 4]

        label = pyglet.text.Label(name, font_name='Roboto', font_size=12, x=0, y=-20,
                                  anchor_x='center', anchor_y='center', batch=self.name_batch)

        player = Player(user_id=user_id, player_id=player_id, name=name, npc=npc,
                        label=label, img=player_image, x=0, y=0, batch=batch)
        
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
        self.name_batch.draw()

    def update(self, dt):
        if self.player != None:
            self.player.update(dt)

    def check_modification_queue(self):
        while not self.shared_communication.modification_queue.empty():
            action, player = self.shared_communication.modification_queue.get()
            
            if action == Action.ADD:
                self.create_new_player(*player)
                
    def game_loop(self, dt):
        self.check_modification_queue()
        self.update(dt)


if __name__ == '__main__':
    game_window = GameWindow(width=800, height=600)
    pyglet.clock.schedule_interval(game_window.update, 1 / 60.0)
    pyglet.app.run()
