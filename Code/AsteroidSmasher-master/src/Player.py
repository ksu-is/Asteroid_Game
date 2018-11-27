import math
import pygame
from pygame.math import Vector2
from Bullet import Bullet

IMGSIZE = (64, 64) #The asset is 64x64 pixels
SPEED = 3
RELOAD_TIME = 125 # 1/8 seconds
SHIELDPOS = (45, 15)
STARTING_SHIELDS = 3
SOUND_WAIT = 750
SHIELDS_PER_LINE = 10
DIST_PER_SHIELD = 20

WHITE = (255, 255, 255)


class Player:
    img = None
    window = None
    fontobj = None
    hitbox = None
    shootSound = None
    hitsound = None
    windowsize = (0, 0)
    position = Vector2()
    bullets = []
    lastshot = 0
    lastsound = 0
    num_shields = 0

    def __init__(self, window, windowsize):
        self.num_shields = STARTING_SHIELDS
        self.lastshot = pygame.time.get_ticks()
        self.lastsound
        self.window = window
        self.windowsize = windowsize
        self.img = pygame.image.load('../res/player.png')
        self.shield_img = pygame.image.load('../res/shield.png')
        self.fontobj = pygame.font.Font('../res/freesansbold.ttf', 18)
        self.shootSound = pygame.mixer.Sound('../res/shoot.wav')
        self.hitsound = pygame.mixer.Sound('../res/playerhit.wav')
        self.position = Vector2(windowsize[0] / 2 - IMGSIZE[0] / 2, windowsize[1] - IMGSIZE[1] - 50)
        self.sethitbox()


    #keys will be [w,s,a,d]
    def move(self, keys):
        movx = 0
        movy = 0

        if keys[0] and not keys[1]:
            movy = -SPEED
        elif not keys[0] and keys[1]:
            movy = SPEED

        if keys[2] and not keys[3]:
            movx = -SPEED
        elif not keys[2] and keys[3]:
            movx = SPEED

        # make sure we don't go off screen
        if (self.position.x >= SPEED and keys[2]) or (self.position.x <= self.windowsize[0] - IMGSIZE[0] - SPEED \
                                                          and keys[3]):
            self.position.x += movx

        if (self.position.y >= SPEED and keys[0]) or (self.position.y <= self.windowsize[1] - IMGSIZE[1] - SPEED \
                                                          and keys[1]):
            self.position.y += movy

        self.sethitbox()


    def sethitbox(self):
        self.hitbox = self.img.get_rect(topleft=(self.position.x, self.position.y))

    def draw(self):
        loc = (self.position.x, self.position.y)
        self.window.blit(self.img, loc)

        #Draw shields
        textSurface = self.fontobj.render("Shields: ", True, WHITE)
        textRect = textSurface.get_rect()
        textRect.center = SHIELDPOS
        self.window.blit(textSurface, textRect)

        for bullet in self.bullets:
            bullet.step()

        numIters = 0
        for i in range(max(0, self.num_shields)):
            self.window.blit(self.shield_img,
                             (90 + (numIters % SHIELDS_PER_LINE) * DIST_PER_SHIELD,
                              15 - 6 + math.floor(numIters / SHIELDS_PER_LINE) * DIST_PER_SHIELD))
            numIters += 1


    def takedmg(self, dmg):
        if self.num_shields > 0:
            self.hitsound.play()
        self.num_shields -= dmg
        return self.num_shields < 0  #return True if the player is dead.

    def shoot(self):
        if self.lastshot + RELOAD_TIME <= pygame.time.get_ticks():

            #because spamming this sound gets REALLY annoying (and sounds bad)
            if self.lastsound + 3 * RELOAD_TIME <= pygame.time.get_ticks():
                self.shootSound.play()
                self.lastsound = pygame.time.get_ticks()

            bpos = (self.position.x + IMGSIZE[0] / 2, self.position.y - 10)
            bullet = Bullet(self.bullets, self.window, bpos)
            self.bullets.append(bullet)
            self.lastshot = pygame.time.get_ticks()

    def checkcollision(self, other):
        return self.hitbox.colliderect(other.hitbox)

    @staticmethod
    def getsize():
        return IMGSIZE
