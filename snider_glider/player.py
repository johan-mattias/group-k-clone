class Player:

    def __init__(self, image, name, keys):
        self.sprite = image
        self.movementSpeed = (0, 0)
        self.vSpeed = 0
        self.position = (0, 0)
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


    def drawPlayer(self, window):
        self.sprite.position = self.position
        self.sprite.draw()
    
    def draw(self, py):
        self.drawPlayer(py)

    def move(self, keys):
        self.generateMovementSpeed(keys)
        self.position = tuple(map(sum, zip(self.position, self.movementSpeed)))

    def set_position(self, pos):
        self.position = pos



