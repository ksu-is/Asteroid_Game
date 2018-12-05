import random
from gameobject import Player, Asteroid, Bullet

#player
PLAYERSIZE = (0.1, 0.2)
PLAYERSTART = (0.5, 1)
PLAYERSPEED = (0.01, 0.01)

#asteroids
ASTEROIDSPEED = (0, 0.005)
ASTEROIDSIZE = (0.06, 0.1)
ASTEROIDVELOCITY = (0, 1)

#bullets
BULLETSPEED = (0, 0.01)
BULLETSIZE = (0.005, 0.01)
BULLETVELOCITY = (0, -1)

#asteroid
SPAWNINTERVAL = 30
ASTEROIDCAP = 3

#difficulty - 10s
TIMEDIFFICULTYINCREASE = 600

class ObjectManager:

    def __init__(self):
        self.asteroids = list()
        self.bullets = list()
        self.player = Player(PLAYERSTART, PLAYERSPEED, (0, 0), PLAYERSIZE)
        #self.gameObjects.append(self.player)
        self.ticksSinceAsteroidSpawn = 0
        self.ticksSinceDifficultyIncrease = 0

    @property
    def gameObjects(self):
        gameObjects = self.asteroids + self.bullets
        gameObjects.append(self.player)
        return gameObjects

    def update(self):
        self.updatePlayer()
        self.updateBullets()
        self.updateAsteroids()
        self.performCollisionDetection()
        self.checkToIncreaseDifficulty()
        
    def updateAsteroids(self):
        self.checkToSpawnAsteroid()
        for asteroid in self.asteroids:
            asteroid.move()
            if(asteroid.outOfBounds() == True):
                self.asteroids.remove(asteroid)

    def updateBullets(self):
        for bullet in self.bullets:
            bullet.move()
            if(bullet.outOfBounds() == True):
                self.bullets.remove(bullet)

    def updatePlayer(self):
        self.player.update()

    def performCollisionDetection(self):
        for asteroid in self.asteroids:
            # check collison with player
            if(self.player.testCollision(asteroid)):
                self.player.loseLife()
                self.asteroids.remove(asteroid)
            # check collision with bullets
            for bullet in self.bullets:
                if(bullet.testCollision(asteroid)):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)

    def checkToSpawnAsteroid(self):
        self.ticksSinceAsteroidSpawn += 1
        if(len(self.asteroids) < ASTEROIDCAP):
            if(self.ticksSinceAsteroidSpawn > SPAWNINTERVAL):
                self.spawnAsteroid()
                self.ticksSinceAsteroidSpawn = 0

    def spawnAsteroid(self):
        x = random.random()
        asteroid = Asteroid((x, 0), ASTEROIDSPEED, ASTEROIDVELOCITY,
            ASTEROIDSIZE)
        self.asteroids.append(asteroid)

    def checkToIncreaseDifficulty(self):
        self.ticksSinceDifficultyIncrease += 1
        if(self.ticksSinceDifficultyIncrease > TIMEDIFFICULTYINCREASE):
            global ASTEROIDCAP
            global SPAWNINTERVAL
            global ASTEROIDSPEED
            ASTEROIDSPEED = (0, (ASTEROIDSPEED[1] + 0.0005))
            ASTEROIDCAP += 1
            SPAWNINTERVAL -= 1
            self.ticksSinceDifficultyIncrease = 0

    def spawnBullet(self):
        if(self.player.fireBullet() == True):
            position = ((self.player.x + (self.player.width/2)),
                (self.player.y - self.player.height))
            bullet = Bullet(position, BULLETSPEED, BULLETVELOCITY, BULLETSIZE)
            self.bullets.append(bullet)

    def gameOver(self):
        if(self.player.isAlive() == False):
            return True
        return False

