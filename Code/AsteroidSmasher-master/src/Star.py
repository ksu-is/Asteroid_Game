import random
import pygame
from pygame.math import Vector2
from pygame.rect import Rect

WHITE = (255, 255, 255)
SIZELIMS = (2, 5)


class Star:
    window = None
    windowsize = None
    starlist = []
    size = 0
    position = Vector2()
    speed = 15

    def __init__(self, window, windowsize, starlist):
        self.window = window
        self.size = random.randint(SIZELIMS[0], SIZELIMS[1])
        self.position = Vector2(random.randint(0, windowsize[0] - self.size), -self.size)
        self.windowsize = windowsize
        self.starlist = starlist

    def getrect(self):
        return Rect((self.position.x, self.position.y), (self.size, self.size))

    def draw(self):
        pygame.draw.rect(self.window, WHITE, self.getrect())

    def step(self):
        self.position.y += self.speed

        if self.position.y >= self.windowsize[1]:
            self.starlist.remove(self)

        self.draw()
