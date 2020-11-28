class RRT:
    def __init__(self, config):
        self.xlim = config["graph"]["xlim"]
        self.ylim = config["graph"]["ylim"]
        self.start = config["rrt"]["start"]
        self.end = config["rrt"]["end"]
        self.iters = config["rrt"]["iters"]
        self.delta = config["rrt"]["delta"]

        self.obstacles = []
        for obstacle in config["graph"]["obstacles"]:
            self.obstacles.append((obstacle["center"], obstacle["radius"]))
