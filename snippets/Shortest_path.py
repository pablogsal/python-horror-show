import collections


def from_id_width(id, width):
    return (id % width, id // width)
# data from main article
DIAGRAM1_WALLS = [from_id_width(id, width=30) for id in [21, 22, 51, 52, 81, 82, 93, 94, 111, 112, 123, 124, 133, 134, 141, 142, 153, 154, 163, 164, 171, 172, 173, 174, 175,
                                                         183, 184, 193, 194, 201, 202, 203, 204, 205, 213, 214, 223, 224, 243, 244, 253, 254, 273, 274, 283, 284, 303, 304, 313, 314, 333, 334, 343, 344, 373, 374, 403, 404, 433, 434]]


# We use a deque because we need the last element that we have added to de
# Queue

class Queue:

    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

##########################################################################


class SquareGrid():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = set()

    def in_bounds(self, id):
        x, y = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        # Very elegant way to yield neightbours !!!!!!!!
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        yield from results

    def _draw_tile(self, id, style, width):
        r = "."
        if 'number' in style and id in style['number']:
            r = "%d" % style['number'][id]
        if 'point_to' in style and style['point_to'].get(id, None) is not None:
            (x1, y1) = id
            (x2, y2) = style['point_to'][id]
            if x2 == x1 + 1:
                r = "\u2192"
            if x2 == x1 - 1:
                r = "\u2190"
            if y2 == y1 + 1:
                r = "\u2193"
            if y2 == y1 - 1:
                r = "\u2191"
        if 'start' in style and id == style['start']:
            r = "A"
        if 'goal' in style and id == style['goal']:
            r = "Z"
        if 'path' in style and id in style['path']:
            r = "@"
        if id in self.walls:
            r = "#" * width
        return r

    def draw(self, width=2, **style):
        for y in range(self.height):
            for x in range(self.width):
                print("%%-%ds" % width %
                      self._draw_tile((x, y), style, width), end="")
            print()


class GridWithWeights(SquareGrid):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

##########################################################################


######## PRIORITY QUEUE ##################

import heapq
import itertools


class PriorityQueue(list):

    def __init__(self, iterable=None):

        self.entries = dict()
        self.counter = itertools.count()

        if iterable is not None:
            for item in iterable:
                self.put(*item)

    def remove(self, key):
        entry = self.entries.pop(key)
        entry[2] = None

    def put(self, item, priority):

        if item in self.entries:
            self.remove(item)

        entry = [priority, next(self.counter), item]
        self.entries[item] = entry
        heapq.heappush(self, entry)

    def get(self):

        while self:
            next_item = heapq.heappop(self)[2]
            if next_item is not None:
                del self.entries[next_item]
                return next_item

        raise KeyError('Pop from an empty priority queue')


####### DIJSTRA ALGORITHM ##############

def dijkstra_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = frontier.get()

        if current == goal:
            break

        for candidate in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, candidate)
            if candidate not in cost_so_far or new_cost < cost_so_far[candidate]:
                cost_so_far[candidate] = new_cost
                priority = new_cost
                frontier.put(candidate, priority)
                came_from[candidate] = current

    return came_from, cost_so_far


######## A* ALGORITHM #########

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    duplicates = collections.Counter()

    while frontier:
        current = frontier.get()

        if current == goal:
            break

        for candidate in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, candidate)
            if candidate not in cost_so_far or new_cost < cost_so_far[candidate]:
                cost_so_far[candidate] = new_cost
                priority = new_cost + heuristic(goal, candidate)
                frontier.put(candidate, priority)
                came_from[candidate] = current

    return came_from, cost_so_far


def a_star_search_no_weights(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    duplicates = collections.Counter()

    while frontier:
        current = frontier.get()

        if current == goal:
            break

        for candidate in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if candidate not in cost_so_far or new_cost < cost_so_far[candidate]:
                cost_so_far[candidate] = new_cost
                priority = new_cost + heuristic(goal, candidate)
                frontier.put(candidate, priority)
                came_from[candidate] = current

    return came_from, cost_so_far

####### RECONSTRUCT PATH #########


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


#####################

if __name__ == '__main__':
    # diagram4 = GridWithWeights(10, 10)
    # diagram4.walls = set([(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)])
    # diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
    #                                        (4, 3), (4, 4), (4, 5), (4, 6),
    #                                        (4, 7), (4, 8), (5, 1), (5, 2),
    #                                        (5, 3), (5, 4), (5, 5), (5, 6),
    #                                        (5, 7), (5, 8), (6, 2), (6, 3),
    #                                        (6, 4), (6, 5), (6, 6), (6, 7),
    #                                        (7, 3), (7, 4), (7, 5)]}
    # came_from, cost_so_far = a_star_search(diagram4, (1, 4), (7, 8))
    # diagram4.draw(width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    # print()
    # diagram4.draw(width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))

    diagram4 = GridWithWeights(30, 15)
    diagram4.walls = set(DIAGRAM1_WALLS)
    came_from, cost_so_far = a_star_search_no_weights(
        diagram4, (1, 4), (24, 3))
    diagram4.draw(width=3, point_to=came_from, start=(1, 4), goal=(24, 3))
    print()
    diagram4.draw(width=3, number=cost_so_far, start=(1, 4), goal=(24, 3))
