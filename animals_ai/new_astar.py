
import numpy

grid = [[0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 0]]

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        print "(%d, %d)" % (self.x, self.y)

    def __eq__(self, pos):
        return ( self.x == pos.x and 
                 self.y == pos.y )

    def left(self):
        return Position(self.x-1, self.y)

    def right(self):
        return Position(self.x+1, self.y)

    def bottom(self):
        return Position(self.x, self.y+1)

    def top(self):
        return Position(self.x, self.y-1)

    def get_neighbors(self):
        return (self.left(), self.top(), self.right(), self.bottom())

def particion(a, l, r, h):
    i = l-1
    for j in range(l,r+1):
        if h[a[j]] >= h[a[r]]:
            i += 1
            temp = a[j]
            a[j] = a[i]
            a[i] = temp
    return i

def quicksort(a, l, r, h):
    if l >= r:
        return
    m = particion(a, l, r, h)
    quicksort(a, l, m-1, h)
    quicksort(a, m+1, r, h)

def heuristic(start,goal):
    return numpy.sqrt((start.x-goal.x)**2 + (start.x-goal.y)**2)

def astarpathsearch(start, goal, map, heuristic):
    closedset = []
    openset = [start]
    came_from = [] 



def astarpathsearch(start, goal, map, heuristic):
    closedset = []
    openset = [start]
    came_from = []

    g = {}
    h = {}
    f = {}

    g[start] = 0
    h[start] = heuristic(start, goal)
    f[start] = g[start] + h[start]

    while openset:
        quicksort(openset, 0, len(openset)-1, f)
        current_pos = openset.pop()
        closedset.append(current_pos)

        if current_pos == goal:
            return get_path(came_from, current_pos)

        for neighbor in current_pos.get_neighbors():
            if not (neighbor.x >= 0 and neighbor.x < len(map) and neighbor.y >= 0 and neighbor.y < len[map[0]]):
                continue

            if neighbor in closedset:
                continue

            tentaive_is_better = False

            if neighbor not in openset:
                openset.append(neighbor)
                h[neighbor] = heuristic(neighbor, goal)
                tentaive_is_better = True
            elif g[current_pos] + 1 < g[neighbor]:
                tentaive_is_better = True

            if tentaive_is_better:
                came_from[neighbor] = current_pos
                g[neighbor] = g[current_pos] + 1
                f[neighbor] = g[neighbor] + h[neighbor]

    return False

def get_path(came_from, pos):
    if pos in came_from:
        vector = get_path(came_from, came_from[pos])
        vector.append(pos)
        return vector
    return pos

start = Position(0,0)
goal  = Position(5,4)

path = astarpathsearch(start, goal, grid, heuristic)
print path