import pygame
from objectmanager import PLAYERSIZE, ASTEROIDSIZE, BULLETSIZE
from gameobject import GameObject

#default screen size
WINWIDTH = 800
WINHEIGHT = 600

#colours
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#misc
CAPTION = 'Spaceship Asteroids'
SPRITEDIR = './Images/'

#images
SPRITEMAP = {}

#initialise the display by creating the surface and loading the sprites into
#a map
def initialise(screenSize):
    if(screenSize != None):
        displaySurface = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    else:
        displaySurface = pygame.display.set_mode((screenSize[0], screenSize[1]))
    pygame.display.set_caption(CAPTION)
    loadSprite('SpaceShip.png', GameObject.PLAYER, PLAYERSIZE)
    loadSprite('Asteroid.png', GameObject.ASTEROID, ASTEROIDSIZE)
    loadSprite('Bullet.png', GameObject.BULLET, BULLETSIZE)
    return displaySurface

def update(window, gameObjects):
    #draw graphics
    window.fill(BLACK)
    for gameObject in gameObjects:
        window.blit(SPRITEMAP[gameObject.tag], 
            logicToPixels(gameObject.position))
    #update graphics to screen
    pygame.display.update()

#load a sprite into the sprite map
def loadSprite(spriteName, key, logicSize):
    sprite = pygame.image.load((SPRITEDIR + spriteName)).convert()
    if(logicSize != None):
        sprite = pygame.transform.smoothscale(sprite, logicToPixels(logicSize))
    SPRITEMAP[key] = sprite

#convert logic co-ordinates to graphics co-ordinates
def logicToPixels(logic):
    pixels = (int(logic[0]*WINWIDTH), int(logic[1]*WINHEIGHT))
    return pixels 