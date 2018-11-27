#base gameobject class
class GameObject:
    #tags
    PLAYER = 1
    ASTEROID = 2
    BULLET = 3

    def __init__(self, position, speed, velocity, size, tag):
        self.position = position
        self.speed = speed
        self.velocity = velocity
        self.size = size
        self.tag = tag

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @x.setter
    def x(self, value):
        self.position = (value, self.position[1])

    @y.setter
    def y(self, value):
        self.position = (self.position[0], value)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def velX(self):
        return self.velocity[0]

    @property
    def velY(self):
        return self.velocity[1]

    @velX.setter
    def velX(self, value):
        self.velocity = (value, self.velocity[1])

    @velY.setter
    def velY(self, value):
        self.velocity = (self.velocity[0], value)

    @property
    def speedX(self):
        return self.speed[0]

    @property
    def speedY(self):
        return self.speed[1]

    def move(self):
        #update the position by velocity
        self.x += (self.velX * self.speedX)
        self.y += (self.velY * self.speedY)
        #self.updatePosition(self.x + self.velX, self.y + self.velY)
        #test for x bounds and adjust accordingly
        if(self.x < 0):
            self.x = 0
        if((self.x + self.width) > 1):
            self.x = (1 - self.width)
        #test for y bounds and adjust accordingly
        if(self.y < 0):
            self.y = 0
        if((self.y + self.height) > 1):
            self.y = (1 - self.height)

    def testCollision(self, gameObject):
        pos = gameObject.position
        size = gameObject.size
        #test for overlap in x axis
        if(self.x < (pos[0] + size[0]) and (self.x + self.width) > pos[0]):
            #test for overlap in y axis
            if(self.y < (pos[1] + size[1]) and (self.y + self.height) > pos[1]):
                return True
        return False

class Player(GameObject):
    # relod time of 2 seconds
    RELOADTIME = 120
    NUMLIVES = 3
    MAGCAPACITY = 500

    def __init__(self, position, speed, velocity, size):
        GameObject.__init__(self, position, speed, 
            velocity, size, GameObject.PLAYER)
        self.lives = self.NUMLIVES
        self.magazine = self.MAGCAPACITY
        self.reloading = False
        self.reloadTimer = 0

    def isAlive(self):
        if(self.lives <= 0):
            return False
        return True

    def loseLife(self):
        # check time limit to avoid getting hit twice straight away
        self.lives -= 1

    def fireBullet(self):
        if(self.magazine > 0):
            self.magazine -= 1;
            if(self.magazine == 0):
                self.reloading = True
            return True
        else:
            return False

    def update(self):
        self.move()
        self.reload()

    def reload(self):
        if(self.reloadTimer >= self.RELOADTIME):
            self.reloading = False
            self.reloadTimer = 0
            self.magazine = self.MAGCAPACITY
        if(self.reloading == True):
            self.reloadTimer += 0;


class Asteroid(GameObject):

    def __init__(self, position, speed, velocity, size):
        GameObject.__init__(self, position, speed, 
            velocity, size, GameObject.ASTEROID)

    def move(self):
        self.y += (self.velY * self.speedY)

    def outOfBounds(self):
        if(self.y > 1):
            return True
        return False

class Bullet(GameObject):

    def __init__(self, position, speed, velocity, size):
        GameObject.__init__(self, position, speed, 
            velocity, size, GameObject.BULLET)

    def move(self):
        self.y += (self.velY * self.speedY)

    def outOfBounds(self):
        if(self.y < 0):
            return True
        return False




