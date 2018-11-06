import random
import pygame
from pygame.math import Vector2


IMGSIZE = (64, 64)

FILENAME = '../res/asteroid%d.png'
SPEEDLIMS = (1, 5)

class Asteroid:
    window = None
    asteroidlist = None
    img = None
    hitbox = None
    speed = 0
    windowsize = (0, 0)
    position = Vector2()


    def __init__(self, asteroidlist, window, windowsize, lvl):
        posx = random.randint(0, windowsize[0] - IMGSIZE[0])
        posy = -IMGSIZE[1]
        self.speed = random.randint(SPEEDLIMS[0] + lvl, SPEEDLIMS[1] + lvl)
        self.position = Vector2(posx, posy)
        self.windowsize = windowsize
        self.img = pygame.image.load(FILENAME % random.randint(0, 3))
        self.asteroidlist = asteroidlist
        self.window = window
        self.sethitbox()

    def sethitbox(self):
        self.hitbox = self.img.get_rect(topleft=(self.position.x, self.position.y))

    def draw(self):
        self.sethitbox()
        self.window.blit(self.img, (self.position.x, self.position.y))

    def step(self):
        self.position.y += self.speed

        if self.position.y >= self.windowsize[1] and self in self.asteroidlist:
            self.asteroidlist.remove(self)

        self.draw()

    def checkcollision(self, other):
        return self.hitbox.colliderect(other.hitbox)

    def destroy(self):
        if self in self.asteroidlist:
            self.asteroidlist.remove(self)

    @staticmethod
    def getsize():
        return IMGSIZE