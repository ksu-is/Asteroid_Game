import pygame, sys
from pygame.locals import *

def handleEvent(event, objectmanager):
    #handle quit event
    if(event.type == QUIT):
        pygame.quit()
        sys.exit()
    #handle keypresses by switching on and off velocity
    if(event.type == pygame.KEYDOWN):
        if(event.key == pygame.K_LEFT):
            objectmanager.player.velX = -1
        if(event.key == pygame.K_RIGHT):
            objectmanager.player.velX = 1
        if(event.key == pygame.K_SPACE):
            objectmanager.spawnBullet()
    #handle key ups by zeroing velocity, but only if direction has not changed
    if(event.type == pygame.KEYUP):
        if(event.key == pygame.K_LEFT):
            if(objectmanager.player.velX == -1):
                objectmanager.player.velX = 0
        if(event.key == pygame.K_RIGHT):
            if(objectmanager.player.velX == 1):
                objectmanager.player.velX = 0