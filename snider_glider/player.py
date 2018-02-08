import pickle


class Player:

    def __init__(self, image, name, keys, player_id=92):
        self.player_id = player_id
        self.sprite = image
        self.movementSpeed = (0, 0)
        self.vSpeed = 0
        self.x, self.y = (0, 0)

        self.name = name

        self.up = keys[0]
        self.right = keys[1]
        self.down = keys[2]
        self.left = keys[3]
        self.move_rate = 4

    def generateMovementSpeed(self, keys):
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
        self.generateMovementSpeed(keys)
        self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.movementSpeed)))

    def set_position(self, pos):
        self.x, self.y = pos

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def to_transfer_object(self):
        return PlayerTO(self.player_id, self.x, self.y, username=self.name)


class PlayerTO:

    def __init__(self, player_id, x=0, y=0, x_velocity=0, y_velocity=0, color=(0, 0, 0), username="shame"):
        self.player_id = player_id
        self.x = x
        self.y = y

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

        self.color = color
        self.username = username

    def serialize(self):
        return pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)

    def get_position(self):
        return self.x, self.y


def player_from_player_to(player_to):
    new_player = Player(None, player_to.username, None)
    return new_player
