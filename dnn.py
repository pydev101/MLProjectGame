import random, time

random.seed(time.time())


class Neuron:
    weights = []

    def __init__(self, numOfInputs, learningRate, activation):
        for n in range(0, numOfInputs):
            self.weights.append(random.random())
        self.bias = random.random()
        self.weightsOld = self.weights
        self.oldBias = self.bias
        self.learningRate = learningRate
        self.activation = activation

    def out(self, inputs):
        x = self.bias
        for n in range(0, len(inputs)):
            x += inputs[n] * self.weights[n]
        return self.activation(x)

    def train(self, reward):
        temp = self.weights
        for i in range(0, len(self.weights)):
            d = self.weights[i] - self.weightsOld[i]
            if d == 0:
                self.weights[i] = random.random()
            else:
                self.weights[i] = self.learningRate * reward / d
        self.weightsOld = temp

        tempBias = self.bias
        d = self.bias - self.oldBias
        if d == 0:
            self.bias = random.random()
        else:
            self.bias = self.learningRate * reward / d
        self.oldBias = tempBias


class Layer:
    neurons = []

    def __init__(self, numOfInputs, numOfNeurons, learningRate, activation):
        for _ in range(0, numOfNeurons):
            self.neurons.append(Neuron(numOfInputs, learningRate, activation))

    def out(self, input):
        output = []
        for n in self.neurons:
            output.append(n.out(input))
        return output

    def train(self, reward):
        for n in self.neurons:
            n.train(reward)


class DNN:
    layers = []
    temp = []

    def __init__(self, inputs, design, learningRate, activation):
        self.layers.append(Layer(inputs, design[0], learningRate, activation))
        for i in range(1, len(design)):
            self.layers.append(Layer(design[i - 1], design[i], learningRate, activation))

    def out(self, input):
        self.temp = input
        for l in self.layers:
            self.temp = l.out(self.temp)
        return self.temp

    def train(self, reward):
        for l in self.layers:
            l.train(reward)
