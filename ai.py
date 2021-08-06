from game import *
from dnn import DNN
from numpy import exp
import animation
import time
import random
import grapher

LEARNINGRATE = 0.1
LEARNFRAMES = 600
EPSILION = 0.0


def sigmoid(x):
    try:
        return 1.0 / (1.0 + exp(-x))
    except Exception as e:
        print(x)
        exit()


game = Game()
graph = grapher.Graph("test")
dnn = DNN(3 + game.MAX_CELLS, [6, 8, 3], 1, sigmoid)

action = [game.car.left, game.car.right, game.car.stop]

oldScore = game.score
oldSum = 0

running = True
i = 0
t = time.time()
runsum = 0
oldX = game.car.x

while running:
    inputs = []
    for _ in range(0, game.MAX_CELLS):
        inputs.append(0)
    if len(game.rows) > 0:
        for o in game.rows[0]:
            inputs[floor((o.x - game.GRASS_WIDTH) / game.CELL_WIDTH)] = 1
        inputs.append(game.rows[0][0].y / game.HEIGHT)
    inputs.append(game.car.x / game.WIDTH)
    inputs.append((game.car.x - oldX) / game.WIDTH)
    oldX = game.car.x

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

        if avgChangeOfScore <= oldSum / LEARNFRAMES:
            dnn.train(avgChangeOfScore)
        oldSum = runsum
        runsum = 0

    if i % 300000 == 0:
        graph.save()
        t = time.time()
    if (time.time() - t) < 5:
        animation.animate(game)

    i = i + 1
