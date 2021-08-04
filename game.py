from math import floor
from random import randint, seed
from time import time

seed(time())


class Object:
    def __init__(self, x, y, width, length):
        self.x = x
        self.y = y
        self.width = width
        self.length = length


class Car(Object):
    def __init__(self, x, y, width, length, setAccel, frictionCoeff):
        super().__init__(x, y, width, length)
        self.Fc = frictionCoeff
        self.speed = 0
        self.setAccel = setAccel
        self.accel = 0

    def left(self):
        self.accel = -1 * self.setAccel

    def right(self):
        self.accel = self.setAccel

    def stop(self):
        self.accel = 0

    def update(self):
        self.speed += self.accel - self.Fc * self.speed
        self.x += self.speed


class Faller(Object):
    def __init__(self, x, y, width, length, speed):
        super().__init__(x, y, width, length)
        self.speed = speed

    def update(self):
        self.y += self.speed


def generateUnused(minI, maxI, used):
    i = randint(minI, maxI)
    if i in used:
        return generateUnused(minI, maxI, used)
    return i


class Game:
    # SIZE = WIDTH, HEIGHT = 320, 600
    SIZE = WIDTH, HEIGHT = 400, 600
    ROAD = 0.80
    ObjSize = 35
    GRASS_WIDTH = 0.5 * (1 - ROAD) * WIDTH
    ROAD_BOUNDS = (GRASS_WIDTH, WIDTH - GRASS_WIDTH)
    CELL_OPEN_PCT = 0.6
    MAX_CELLS = floor(ROAD * WIDTH / ObjSize)
    CELL_WIDTH = floor(ROAD * WIDTH / MAX_CELLS)
    MAX_ROW_CELLS = floor(CELL_OPEN_PCT * MAX_CELLS)

    score = 0
    spawn_speed = 5
    obstacles = []
    index = 0

    def __init__(self):
        CAR_WIDTH = 30
        CAR_HEIGHT = 30
        CAR_ACCEL = 1
        CAR_BRAKE = 0.1
        self.car = Car(0.5 * self.WIDTH - 0.5 * CAR_WIDTH, self.HEIGHT - 0.1 * self.HEIGHT,
                       CAR_WIDTH, CAR_HEIGHT, CAR_ACCEL, CAR_BRAKE)

    def spawnRow(self):
        cells = randint(1, self.MAX_ROW_CELLS)
        usedPos = []
        for _ in range(0, cells):
            i = generateUnused(0, self.MAX_CELLS-1, usedPos)
            usedPos.append(i)
            o = Faller(self.ROAD_BOUNDS[0] + i * self.CELL_WIDTH, 0, self.ObjSize, self.ObjSize, self.spawn_speed)
            self.obstacles.append(o)

    def update(self):
        self.car.update()
        removals = []
        global hit
        hit = False
        for o in self.obstacles:
            o.update()
            if o.y + o.length > self.car.y:
                if o.y > self.car.y + self.car.length:
                    if (self.car.x > self.ROAD_BOUNDS[0]) and (self.car.x + self.car.width < self.ROAD_BOUNDS[1]):
                        self.score += 3
                    removals.append(o)
                else:
                    if o.x < self.car.x + self.car.width:
                        if o.x + o.width > self.car.x:
                            hit = True
                            break
        if hit:
            self.obstacles = []
            self.score -= 50
        else:
            for o in removals:
                self.obstacles.remove(o)

        if (self.car.x < self.ROAD_BOUNDS[0]) or (self.car.x + self.car.width > self.ROAD_BOUNDS[1]):
            self.score -= 1

        if (self.car.x < 0) or (self.car.x + self.car.width > self.WIDTH):
            self.car.speed = 0
            self.car.accel = 0
            if self.car.x < 0:
                self.car.x = 0
            else:
                self.car.x = self.WIDTH - self.car.width

        self.index += 1
        # 60 frames per second, new row every 0.5 seconds to 1.5 seconds; controls allowed response time
        if self.index > randint(30, 90):
            self.spawnRow()
            self.index = 0
