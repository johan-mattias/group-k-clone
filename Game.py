from socket import *
import pygame, sys, time
from Player import Player

clientSocket = socket(AF_INET, SOCK_DGRAM)

pygame.init()

SIZE = WIDTH, HEIGHT = 600, 400
speed = [2, 2]
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DISPLAYSURFACE = pygame.display.set_mode(SIZE)

pKeys = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]
p = Player(pygame.transform.scale(pygame.image.load("testSprite.png"), (50, 50)), "Dickbutt", pKeys, pygame, SIZE)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    DISPLAYSURFACE.fill(WHITE)
    keys = pygame.key.get_pressed()
    
    w = 0
    d = 0
    s = 0
    a = 0
    if keys[pygame.K_w]: w = 1
    if keys[pygame.K_d]: d = 1
    if keys[pygame.K_s]: s = 1
    if keys[pygame.K_a]: a = 1

    clientSocket.settimeout(1)

    message = str(w)+','+str(d)+','+str(s)+','+str(a)
    message = message.encode()
    addr = ("antoncarlsson.se", 12000)
    clientSocket.sendto(message, addr)
    try:
        data, server = clientSocket.recvfrom(1024)
        print (data)
        
    except timeout:
        print ('REQUEST TIMED OUT')
    
    p.generateMovementSpeed(keys)
    p.drawPlayer(DISPLAYSURFACE)
    pygame.display.flip()
    time.sleep(0.1/10)

clientSocket.close()