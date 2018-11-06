import pygame
from pygame.math import Vector2


NUM_STEPS = 10


class Explosion:
    img = None
    window = None
    position = Vector2()
    curr_step = 0
    explosionlist = []

    def __init__(self, window, pos, elist):
        self.explosionlist = elist
        self.img = pygame.image.load('../res/explosion.png')
        self.position = Vector2(pos)
        self.window = window

    def draw(self):
        self.window.blit(self.img, self.position)

    def step(self):
        if not self.isexpired():
            self.draw()
            self.curr_step += 1
        else:
            self.explosionlist.remove(self)

    def isexpired(self):
        return self.curr_step > NUM_STEPS