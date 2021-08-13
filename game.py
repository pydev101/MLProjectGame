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
        # self.accel = -1 * self.setAccel
        self.speed = -self.setAccel

    def right(self):
        # self.accel = self.setAccel
        self.speed = self.setAccel

    def stop(self):
        # self.accel = 0
        self.speed = 0

    def update(self):
        # self.speed += self.accel - self.Fc * self.speed
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
    FRAMERATE = 60
    MINSEC = 0.7
    MAXSEC = 1.5

    score = 1000
    spawn_speed = 5
    rows = []
    index = 0

    def __init__(self):
        CAR_WIDTH = 30
        CAR_HEIGHT = 30
        # CAR_ACCEL = 1
        CAR_SPEED = 5
        CAR_BRAKE = 0.1
        self.car = Car(0.5 * self.WIDTH - 0.5 * CAR_WIDTH, self.HEIGHT - 0.1 * self.HEIGHT,
                       CAR_WIDTH, CAR_HEIGHT, CAR_SPEED, CAR_BRAKE)

    def spawnRow(self):
        cells = randint(1, self.MAX_ROW_CELLS)
        usedPos = []
        testRow = []
        for _ in range(0, cells):
            i = generateUnused(0, self.MAX_CELLS-1, usedPos)
            usedPos.append(i)
            o = Faller(self.ROAD_BOUNDS[0] + i * self.CELL_WIDTH, 0, self.ObjSize, self.ObjSize, self.spawn_speed)
            testRow.append(o)
        self.rows.append(testRow)

    def update(self):
        self.car.update()

        # Update all obsticles, up score if past car, down score if hit car, update rows
        for r in self.rows:
            for o in r:
                o.update()
        if len(self.rows) > 0:
            r = self.rows[0]
            oi = r[0]
            if oi.y + oi.length > self.car.y:
                if oi.y > self.car.y + self.car.length:
                    # Past Car
                    if (self.car.x >= self.ROAD_BOUNDS[0]) and (self.car.x + self.car.width <= self.ROAD_BOUNDS[1]):
                        self.score += 3*len(r)
                    self.rows.pop(0)
                else:
                    # Potiental hit
                    for o in r:
                        if o.x < self.car.x + self.car.width:
                            if o.x + o.width > self.car.x:
                                # HIT
                                self.score -= 10
                                self.rows = []
                                break

        if (self.car.x < self.ROAD_BOUNDS[0]) or (self.car.x + self.car.width > self.ROAD_BOUNDS[1]):
            self.score -= 1
        '''
            self.car.speed = 0
            self.car.accel = 0
            if self.car.x < self.ROAD_BOUNDS[0]:
                self.car.x = self.ROAD_BOUNDS[0]
            else:
                self.car.x = self.WIDTH - self.GRASS_WIDTH - self.car.width
        '''

        if (self.car.x < 0) or (self.car.x + self.car.width > self.WIDTH):
            self.car.speed = 0
            self.car.accel = 0
            if self.car.x < 0:
                self.car.x = 0
            else:
                self.car.x = self.WIDTH - self.car.width

        self.index += 1
        # 60 frames per second, new row every 0.5 seconds to 1.5 seconds; controls allowed response time
        if self.index > randint(floor(self.MINSEC*self.FRAMERATE), floor(self.MINSEC*self.FRAMERATE)):
            self.spawnRow()
            self.index = 0

        if self.score < 1:
            # self.score = 0
            return -1
        if self.score > 1999:
            return 1
        return 0
