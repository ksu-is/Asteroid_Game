#!/usr/bin/env python3

import pygame, display, controls
from pygame.locals import *
from objectmanager import ObjectManager
#from gameobject import GameObject, Player

FPS = 60

# initialisation
fpsClock = pygame.time.Clock()
pygame.init() 
objectmanager = ObjectManager()
window = display.initialise((None, None))
gameOver = False

# game loop
while(gameOver == False):
    #test for quit event
    for event in pygame.event.get():
        controls.handleEvent(event, objectmanager)
    #update the gameobjects
    objectmanager.update()
    #update graphics
    display.update(window, objectmanager.gameObjects)
    gameOver = objectmanager.gameOver()
    fpsClock.tick(FPS)