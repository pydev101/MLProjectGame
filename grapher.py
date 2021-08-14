class Graph:
    def __init__(self, name):
        self.X = []
        self.Y = []
        self.name = name

    def add(self, x, y):
        self.X.append(x)
        self.Y.append(y)

    def save(self):
        with open(self.name + ".csv", "a") as f:
            for i in range(0, len(self.X)):
                f.write("{},{}\n".format(self.X[i], self.Y[i]))
        self.X = []
        self.Y = []

    def clear(self):
        with open(self.name + ".csv", "w") as f:
            f.write("")

    def read(self):
        self.X = []
        self.Y = []
        with open(self.name + ".csv", "r") as f:
            data = f.read()
        data = data.split("\n")
        for l in data:
            try:
                d = l.split(",")
                self.X.append(float(d[0]))
                self.Y.append(float(d[1]))
            except Exception as e:
                pass


SAMPLESIZE = 5
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    graph = Graph("test")
    graph.read()
    X = []
    Y = []
    for i in range(SAMPLESIZE, len(graph.X), SAMPLESIZE):
        X.append(i)
        Y.append((graph.Y[i] - graph.Y[i-SAMPLESIZE])/(graph.X[i] - graph.X[i-SAMPLESIZE]))
    plt.plot(X, Y)

    sum = 0
    for n in Y:
        sum += n
    print(sum)
    plt.show()
