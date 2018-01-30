

class Player:

    def __init__(self, image, name, keys, pygame, size):
        self.sprite = image
        self.spriteRect = self.sprite.get_rect()
        self.movementSpeed = [0, 0]
        self.vSpeed = [0, 0]
        self.position = [0, 0]
        self.name = name

        self.up = keys[0]
        self.right = keys[1]
        self.down = keys[2]
        self.left = keys[3]

        self.pygame = pygame
        self.width, self.height = size

    def generateMovementSpeed(self, keys):
        
        mv1 = [0, 0]
        mv2 = [0, 0]
        mv3 = [0, 0]
        mv4 = [0, 0]
    
        if keys[self.down]:  mv1 = [0, 3]
        if not (self.spriteRect.bottom < self.height):
            if keys[self.up]:    mv2 = [0, -20]
        if keys[self.right]: mv3 = [3, 0]
        if keys[self.left]:  mv4 = [-3, 0]
    
        move = [mv1[i] + mv2[i] + mv3[i] + mv4[i] for i in range(2)]
        move[1] = move[1] + self.movementSpeed[1] + 1
        bD = self.spriteRect.bottom + move[1] - self.height
        lD = self.spriteRect.left + move[0]
        tD = self.spriteRect.top + move[1]
        rD = self.spriteRect.right + move[0] - self.width
    
        if bD > 0:
            move[1] = move[1] - bD
        if lD < 0:
            move[0] = move[0] - lD
        if tD < 0:
            move[1] = move[1] - tD
        if rD > 0:
            move[0] = move[0] - rD
        
        if move[1] > 6: move[1] = 10

        self.movementSpeed = move
        self.spriteRect = self.spriteRect.move(move)

    def drawPlayer(self, screen):
        screen.blit(self.sprite, self.spriteRect)
