import pygame
from pygame.math import Vector2


IMGSIZE = (3, 7)
SPEED = 8


class Bullet:
    img = None
    window = None
    bulletlist = None
    hitbox = None
    position = Vector2()

    def __init__(self, bulletlist, window, pos):
        self.bulletlist = bulletlist
        self.window = window
        self.img = pygame.image.load('../res/bullet.png')
        self.position = Vector2(pos[0], pos[1])
        self.sethitbox()

    def sethitbox(self):
        self.hitbox = self.img.get_rect(topleft=(self.position.x, self.position.y))


    def draw(self):
        self.sethitbox()
        self.window.blit(self.img, self.position)

    def step(self):
        self.position.y -= SPEED

        # If we're off the screen, remove the bullet from the list
        if self.position.y <= -SPEED and self in self.bulletlist:
            self.bulletlist.remove(self)

        self.draw()

    def destroy(self):
        self.bulletlist.remove(self)


    @staticmethod
    def getsize():
        return IMGSIZE