import random
import sys
import math

import pygame
from pygame.constants import KEYDOWN, QUIT, K_w, K_s, K_a, K_d, KEYUP, K_SPACE, MOUSEBUTTONDOWN
from Asteroid import Asteroid
from Explosion import Explosion
from Player import Player
from Powerup import Powerup, POWERUP_SHIELD, POWERUP_POINTS
from Star import Star



# Color RGB values
#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = ( 60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (  0, 255, 0)
MEDGREEN = (  0, 150, 0)
DARKGREEN = (  0, 100, 0)
BLUE = (  0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (  0, 255, 255)
BLACK = (  0, 0, 0)

FPS = 30
BGCOLOR = BLACK
WINDOW_SIZE = (500, 500)

BUTTONWIDTH = 50
BUTTONHEIGHT = 25

PUP_SPAWN_RATE = (5000, 10000)

MAX_ASTEROIDS = 6
MAX_STARS = 500
SCORE_TEXT = 'Score: %d / %d'
LEVEL_TEXT = 'Level: %d'

#key codes
W = 119
A = 97
S = 115
D = 100
SPACE = 32

pygame.init()

RESULT_PLAY = 1
RESULT_QUIT = 2

fpsClock = pygame.time.Clock()
fontObj = pygame.font.Font('../res/freesansbold.ttf', 18)
asteroidhit = pygame.mixer.Sound('../res/asteroidhit.wav')
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Asteroid Smasher")

highscore = 0


def end_game():
    pygame.quit()
    sys.exit(0)


def getLvl(score):
    return min(math.floor(score / 10), 10)


def getSpawnRate(score):
    low = (math.floor((getLvl(score) + 1) * -0.04444) + 13) / 1000
    hi = (math.floor((getLvl(score) + 1) * -0.04444) + 13.25) / 1000

    return [int(low), int(hi)]


def play_game():
    global highscore
    asteroids = []
    starlist = []
    explosions = []
    puplist = []
    score = 0
    plr = Player(window, WINDOW_SIZE)
    last_spawn = pygame.time.get_ticks()
    last_pup_spawn = pygame.time.get_ticks()
    asteroid_reload = random.randint(*getSpawnRate(score))
    powerup_reload = random.randint(*PUP_SPAWN_RATE)

    #         w      s      a      d
    keys = [False, False, False, False]
    shooting = False

    while True:  # game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                key = event.key
                if key == K_w:
                    keys[0] = True
                elif key == K_s:
                    keys[1] = True
                elif key == K_a:
                    keys[2] = True
                elif key == K_d:
                    keys[3] = True
                elif key == K_SPACE:
                    shooting = True
            elif event.type == KEYUP:
                key = event.key
                if key == W:
                    keys[0] = False
                elif key == S:
                    keys[1] = False
                elif key == A:
                    keys[2] = False
                elif key == D:
                    keys[3] = False
                elif key == SPACE:
                    shooting = False


        # Clear the screen
        window.fill(BGCOLOR)

        # Generate stars.
        if len(starlist) < MAX_STARS:
            starlist.append(Star(window, WINDOW_SIZE, starlist))

        for star in starlist:
            star.step()

        if len(asteroids) < MAX_ASTEROIDS and last_spawn + asteroid_reload <= pygame.time.get_ticks():
            asteroids.append(Asteroid(asteroids, window, WINDOW_SIZE, getLvl(score)))
            last_spawn = pygame.time.get_ticks()
            asteroid_reload = random.randint(*getSpawnRate(score))

        if last_pup_spawn + powerup_reload <= pygame.time.get_ticks():
            if random.randint(1, 2) % 2 == 0:
                puplist.append(Powerup(window, WINDOW_SIZE, puplist))

            last_pup_spawn = pygame.time.get_ticks()
            powerup_reload = random.randint(*PUP_SPAWN_RATE)

        for explosion in explosions:
            explosion.step()

        for asteroid in asteroids:
            asteroid.step()

        for powerup in puplist:
            powerup.step()

        if shooting:
            plr.shoot()

        # Move the player & handle shooting
        plr.move(keys)
        plr.draw()

        for powerup in puplist:
            if plr.checkcollision(powerup):
                #powerup.applyeffect(plr)
                pygame.mixer.Sound('../res/powerup.wav').play()
                if powerup.ptype == POWERUP_SHIELD:
                    plr.takedmg(-1)
                elif powerup.ptype == POWERUP_POINTS:
                    score += random.randint(1, 10)
                powerup.destroy()

        for asteroid in asteroids:
            for bullet in plr.bullets:
                if asteroid.checkcollision(bullet):
                    asteroidhit.play()
                    bullet.destroy()
                    asteroid.destroy()
                    score += 1
                    explosions.append(Explosion(window, (asteroid.position.x, asteroid.position.y), explosions))

            if asteroid.checkcollision(plr):
                gameover = plr.takedmg(1)
                asteroid.destroy()

                if gameover:
                    plr.bullets.clear()
                    return score

        # Draw score
        highscore = max(score, highscore)

        textSfcObj = fontObj.render((SCORE_TEXT % (score, highscore)), True, WHITE)
        textRect = textSfcObj.get_rect()
        #textRect.center = (440, 25)
        textRect.center = (WINDOW_SIZE[0] - 85, 15)

        lvlSfc = fontObj.render(LEVEL_TEXT % getLvl(score), True, WHITE)
        lvlRect = lvlSfc.get_rect()
        lvlRect.center = (WINDOW_SIZE[0] - 50, 40)

        window.blit(textSfcObj, textRect)
        window.blit(lvlSfc, lvlRect)
        pygame.display.update()
        fpsClock.tick(FPS)


def game_over(score):
    pygame.mixer.Sound('../res/gameover.wav').play()

    bigFontObj = pygame.font.Font('../res/freesansbold.ttf', 45)
    while True:

        mousepos = (0, 0)
        clickchanged = False

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clickchanged = True
                    mousepos = tuple(pygame.mouse.get_pos())
            elif event.type == QUIT:
                return
        window.fill(DARKGREEN)

        titleSfc = bigFontObj.render("Game Over!", True, WHITE, DARKGREEN)
        titleRect = titleSfc.get_rect()
        titleRect.center = (WINDOW_SIZE[0] / 2, 100)

        scoreSfc = fontObj.render('You got a score of %d!' % score, True, WHITE, DARKGREEN)
        scoreRect = scoreSfc.get_rect()
        scoreRect.center = (WINDOW_SIZE[0] / 2, 135)

        subtitleSfc = fontObj.render('Do you want to play again?', True, WHITE, DARKGREEN)
        subtitleRect = subtitleSfc.get_rect()
        subtitleRect.center = (WINDOW_SIZE[0] / 2, 165)

        yesBtnSfc = bigFontObj.render(' Yes ', True, WHITE, MEDGREEN)
        yesBtnRect = yesBtnSfc.get_rect()
        yesBtnRect.center = (WINDOW_SIZE[0] / 4 + 25, 250)

        noBtnSfc = bigFontObj.render(' No ', True, WHITE, MEDGREEN)
        noBtnRect = noBtnSfc.get_rect()
        noBtnRect.center = (3 * WINDOW_SIZE[0] / 4 - 25, 250)

        if clickchanged:
            if yesBtnRect.collidepoint(mousepos):
                return True
            elif noBtnRect.collidepoint(mousepos):
                return False

        window.blit(noBtnSfc, noBtnRect)
        window.blit(yesBtnSfc, yesBtnRect)
        window.blit(titleSfc, titleRect)
        window.blit(scoreSfc, scoreRect)
        window.blit(subtitleSfc, subtitleRect)

        pygame.display.update()
        fpsClock.tick(FPS)


def intro_screen():
    bigFontObj = pygame.font.Font('../res/freesansbold.ttf', 45)
    rlyBigFontObj = pygame.font.Font('../res/freesansbold.ttf', 50)
    while True:

        mousepos = (0, 0)
        clickchanged = False

        for event in pygame.event.get():
            if event.type == QUIT:
                return RESULT_QUIT
            elif event.type == MOUSEBUTTONDOWN:
                clickchanged = True
                mousepos = tuple(pygame.mouse.get_pos())

        window.fill(DARKGREEN)

        titleSfc = rlyBigFontObj.render('Asteroid Smasher', True, WHITE)
        titleRect = titleSfc.get_rect()
        titleRect.center = (WINDOW_SIZE[0] / 2, 75)

        playBtn = bigFontObj.render('Play', True, WHITE, MEDGREEN)
        playBtnRect = playBtn.get_rect()
        playBtnRect.center = (WINDOW_SIZE[0] / 2, 250)

        quitBtn = bigFontObj.render('Quit', True, WHITE, MEDGREEN)
        quitBtnRect = quitBtn.get_rect()
        quitBtnRect.center = (WINDOW_SIZE[0] / 2, 350)

        if clickchanged:
            if playBtnRect.collidepoint(mousepos):
                return RESULT_PLAY
            elif quitBtnRect.collidepoint(mousepos):
                return RESULT_QUIT

        window.blit(titleSfc, titleRect)
        window.blit(playBtn, playBtnRect)
        window.blit(quitBtn, quitBtnRect)

        pygame.display.update()
        fpsClock.tick(FPS)

#noinspection PyArgumentList
def main():
    global highscore
    global f
    f = None

    try:
        f = open('../save.txt', 'r')
        highscore = int(f.read())
    except IOError: #If a file doesn't exist, create it.
        f = open('../save.txt', 'x')
        highscore = 0
        f.write('0')

    f.close()

    playAgain = True

    result = intro_screen()

    if result == RESULT_QUIT:
        playAgain = False

    while playAgain:
        score = play_game()
        if score is not None:
            playAgain = game_over(score)
        else:
            playAgain = False

    f = open('../save.txt', 'wb')
    f.write(bytes('%s' % str(highscore), 'UTF-8'))
    f.close()
    end_game()


if __name__ == '__main__':
    pygame.mixer.music.load('../res/music.mid')
    pygame.mixer.music.play(-1, 0)
    main()
