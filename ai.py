from game import *
from dnn import DNN
from numpy import exp
import animation
import time
import random
import grapher
import math

LEARNINGSCALE = 0.0001
LEARNFRAMES = 1000
EPSILION = 0.0


def linear(x):
    return x


def sigmoid(x):
    try:
        return 1.0 / (1.0 + exp(-x))
    except Exception as e:
        print(x)
        exit()


game = Game()
graph = grapher.Graph("test")

action = [game.car.left, game.car.right, game.car.stop]
dnn = DNN(2 + game.MAX_CELLS, [3, 18, 9, len(action)], linear)

oldScore = game.score
oldSum = 0

running = True
i = 0
t = time.time()
runsum = 0

while running:
    inputs = []
    for _ in range(0, game.MAX_CELLS):
        inputs.append(0)
    if len(game.rows) > 0:
        for o in game.rows[0]:
            inputs[floor((o.x - game.GRASS_WIDTH) / game.CELL_WIDTH)] = 1
        inputs.append(game.rows[0][0].y / game.HEIGHT)
    else:
        inputs.append(0)
    pos = floor((game.car.x - game.GRASS_WIDTH) / game.CELL_WIDTH) / game.MAX_CELLS
    inputs.append(pos)

    if len(inputs) != 2 + game.MAX_CELLS:
        print("BAD INPUT")
        break

    table = dnn.out(inputs)
    if random.random() < EPSILION:
        action[random.randint(0, 2)]()
    else:
        action[table.index(max(table))]()

    failCondition = game.update()
    delta = game.score - oldScore
    if game.score < -999999:
        game.score = 0
    oldScore = game.score

    runsum += delta
    if i % LEARNFRAMES == 0:
        avgChangeOfScore = runsum / LEARNFRAMES
        graph.add(i, avgChangeOfScore)

        '''
        if avgChangeOfScore <= LEARNINGSCALE:
            avgChangeOfScore = LEARNINGSCALE
        dnn.train(LEARNINGSCALE / avgChangeOfScore)
        '''
        if avgChangeOfScore <= 0:
            rate = 1
        else:
            rate = 0.001**(0.5*avgChangeOfScore)
        dnn.train(rate)

        oldSum = runsum
        runsum = 0

    if i % 300000 == 0:
        graph.save()
        t = time.time()
        print("Saved", floor(i / LEARNFRAMES))
    if (time.time() - t) < 0:
        animation.animate(game)

    i = i + 1
