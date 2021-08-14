from game import *
from dnn import DNN, loadDNN
from numpy import exp
import animation
import time
import grapher
import argparse

# LEARNINGSCALE = 0.0001
LEARNFRAMES = 1000
ANIMATE = False

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--frames", help="Frames used to calculate learning average")
parser.add_argument("-a", "--animate", help="Show Animation")
args = parser.parse_args()
if args.frames:
    LEARNFRAMES = int(args.frames)
if args.animate:
    ANIMATE = bool(args.animate)


def linear(x):
    return x


def sigmoid(x):
    try:
        return 1.0 / (1.0 + exp(-x))
    except Exception as e:
        print(x)


game = Game()
graph = grapher.Graph("test")

action = [game.car.left, game.car.right, game.car.stop]

loadOld = True
if loadOld:
    dnn, globalsum, i = loadDNN()
else:
    globalsum = 0
    dnn = DNN(2 + game.MAX_CELLS, [3, 18, 9, len(action)], linear)
    graph.clear()
    i = 0

oldScore = game.score
oldSum = 0

running = True
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

    if len(inputs) != dnn.expectedInputs:
        print("BAD INPUT")
        break

    table = dnn.out(inputs)
    action[table.index(max(table))]()

    failCondition = game.update()
    delta = game.score - oldScore
    if game.score < -999999:
        game.score = 0
    oldScore = game.score

    runsum += delta
    if i % LEARNFRAMES == 0:
        avgChangeOfScore = runsum / LEARNFRAMES
        globalsum = avgChangeOfScore
        graph.add(i, avgChangeOfScore)

        '''
        if avgChangeOfScore <= LEARNINGSCALE:
            avgChangeOfScore = LEARNINGSCALE
        dnn.train(LEARNINGSCALE / avgChangeOfScore)
        '''
        if avgChangeOfScore <= 0:
            rate = 1
        else:
            rate = 0.001 ** (0.5 * avgChangeOfScore)
        dnn.train(rate)

        oldSum = runsum
        runsum = 0

    if i % 300000 == 0:
        graph.save()
        dnn.save(globalsum, i)
        t = time.time()
        print("Saved", floor(i / LEARNFRAMES), globalsum)

    if ANIMATE:
        animation.animate(game)

    i = i + 1
