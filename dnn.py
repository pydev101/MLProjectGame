import random, time

random.seed(time.time())


class Neuron:
    def __init__(self, numOfInputs, activation):
        self.weights = []
        for n in range(0, numOfInputs):
            self.weights.append(random.random())
        self.bias = random.random()
        self.weightsOld = self.weights
        self.oldBias = self.bias
        self.activation = activation

    def out(self, inputs):
        x = self.bias
        for n in range(0, len(inputs)):
            x += inputs[n] * self.weights[n]
        return self.activation(x)

    def train(self, rate):
        change = random.random()
        if round(random.random()) == 0:
            change = -change

        temp = self.weights
        for i in range(0, len(self.weights)):
            d = self.weights[i] - self.weightsOld[i]
            if d == 0:
                self.weights[i] = random.random()
            else:
                self.weights[i] = rate * change / d
        self.weightsOld = temp

        tempBias = self.bias
        d = self.bias - self.oldBias
        if d == 0:
            self.bias = random.random()
        else:
            self.bias = rate * change / d
        self.oldBias = tempBias


class Layer:
    def __init__(self, numOfInputs, numOfNeurons, activation):
        self.neurons = []
        for _ in range(0, numOfNeurons):
            self.neurons.append(Neuron(numOfInputs, activation))

    def out(self, input):
        output = []
        for n in self.neurons:
            output.append(n.out(input))
        return output

    def train(self, rate):
        for n in self.neurons:
            n.train(rate)


class DNN:
    def __init__(self, inputs, design, activation):
        self.layers = []
        self.temp = []
        self.layers.append(Layer(inputs, design[0], activation))
        for i in range(1, len(design)):
            self.layers.append(Layer(design[i - 1], design[i], activation))

    def out(self, input):
        self.temp = input
        for l in self.layers:
            self.temp = l.out(self.temp)
        return self.temp

    def train(self, rate):
        for l in self.layers:
            l.train(rate)
