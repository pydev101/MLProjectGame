from game import *
from dnn import DNN
from math import exp

LEARNINGRATE = 1


def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))


game = Game()
dnn = DNN(1+game.MAX_CELLS, [3, 3, 3], 1, sigmoid)

action = [game.car.left, game.car.right, game.car.stop]
