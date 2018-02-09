import pickle


class Player:

    def __init__(self, image, name, keys, player_id=92):
        self.player_id = player_id
        self.sprite = image
        self.movementSpeed = (0, 0)
        self.vSpeed = 0
        self.x, self.y = (0, 0)

        self.name = name
        if keys is not None:
            self.up = keys[0]
            self.right = keys[1]
            self.down = keys[2]
            self.left = keys[3]
        self.move_rate = 4

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
        return PlayerTO(self.player_id, self.x, self.y, username=self.name)


class PlayerTO:

    def __init__(self, player_id, x=None, y=None, x_velocity=None, y_velocity=None, color=None, username=None):
        self.player_id = player_id
        self.x = x
        self.y = y

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

        self.color = color
        self.username = username

    def serialize(self):
        return pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)


def player_from_player_to(player_to):
    new_player = Player(None, player_to.username, None, player_id=player_to.player_id)
    return new_player
    
