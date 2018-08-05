from collections import deque

class TODO:
    def __init__(self):
        self.deque = deque()

    def get(self):
        return self.deque.popleft()

    def put(self, x):
        self.deque.append(x)

    def isEmpty(self):
        return len(self.deque) == 0

class Visited:
    def __init__(self):
        self.visited = set()

    def __contains__(self, item):
        if hash(item) in self.visited:
            return True
        else:
            return False

    def add(self, item):
        self.visited.add(hash(item))

    def remove(self, item):
        h = hash(item)
        if h in self:
            self.visited.remove(h)

class BoolenVisited:
