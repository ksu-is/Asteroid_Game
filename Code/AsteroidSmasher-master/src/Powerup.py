import random
import pygame
from pygame.math import Vector2


DARKGREEN = (  0, 100, 0)

SPEED = 5
SIZE = (15, 15) # 15x15

POWERUP_SHIELD = 1
POWERUP_POINTS = 2

POWERUPS = {
    'shield': [pygame.image.load('../res/shield.png'), POWERUP_SHIELD],
    'points': [pygame.image.load('../res/coin.png'), POWERUP_POINTS]
}


class Powerup:
    window = None
    winSize = None
    img = None
    hitbox = None
    position = Vector2()
    pupList = []
    ptype = -1

    def __init__(self, window, windowsize, puplist):
        self.window = window
        self.winSize = windowsize
        self.pupList = puplist
        index = random.choice(list(POWERUPS.keys())) # pick a random powerup
        powerup = POWERUPS[index]
        self.img = powerup[0]
        self.ptype = powerup[1]
        self.position = Vector2(random.randint(0, windowsize[0] - SIZE[-0]), -SIZE[1])
        self.sethitbox()

    def draw(self):
        self.sethitbox()
        self.window.blit(self.img, self.position)

    def sethitbox(self):
        self.hitbox = self.img.get_rect(topleft=(self.position.x, self.position.y))

    def step(self):
        self.position.y += SPEED

        if self.position.y >= self.winSize[1] and self in self.pupList:
            self.pupList.remove(self)

        self.draw()

    def destroy(self):
        if self in self.pupList:
            self.pupList.remove(self)

            #def applyeffect(self, player):
            #    if self.ptype == POWERUP_SHIELD:
            #        player.takedmg(-1)
