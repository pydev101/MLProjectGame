class Graph:
    def __init__(self, name):
        self.X = []
        self.Y = []
        self.name = name

    def add(self, x, y):
        self.X.append(x)
        self.Y.append(y)

    def save(self):
        with open(self.name + ".csv", "w") as f:
            for i in range(0, len(self.X)):
                f.write("{},{}\n".format(self.X[i], self.Y[i]))

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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    graph = Graph("test")
    graph.read()
    plt.plot(graph.X, graph.Y)
    plt.show()
