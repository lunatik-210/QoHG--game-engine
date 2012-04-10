
import numpy

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __eq__(self, pos):
        return ( self.x == pos.x and 
                 self.y == pos.y )

    def __repr__(self):
        return "(%d,%d)" % (self.x, self.y)

    def left(self):
        return Position(self.x-1, self.y)

    def right(self):
        return Position(self.x+1, self.y)

    def bottom(self):
        return Position(self.x, self.y+1)

    def top(self):
        return Position(self.x, self.y-1)

    def value(self):
        return (self.x, self.y)

    def get_neighbors(self):
        return (self.left(), self.top(), self.right(), self.bottom())

def a_star_path_search(start, goal, grid):

    def particion(a, l, r, h):
        i = l-1
        for j in range(l,r+1):
            if h[a[j].value()] >= h[a[r].value()]:
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

    def is_out_of_range(p):
        return not ( neighbor.x >= 0 and neighbor.x < len(grid) and 
                     neighbor.y >= 0 and neighbor.y < len(grid[0]) and 
                     grid[neighbor.x][neighbor.y] == 0)

    def heuristic(start,goal):
        return numpy.sqrt((start.x-goal.x)**2 + (start.x-goal.y)**2)

    def get_path(came_from, pos):
        if pos.value() in came_from:
            vector = get_path(came_from, came_from[pos.value()])
            vector.append(pos)
            return vector
        return [pos]

    closedset = []
    openset = [start]
    came_from = {}

    g = {}
    h = {}
    f = {}

    g[start.value()] = 0
    h[start.value()] = heuristic(start, goal)
    f[start.value()] = g[start.value()] + h[start.value()]

    iteration = 0

    while openset:
        iteration += 1
        quicksort(openset, 0, len(openset)-1, f)
        current_pos = openset.pop()
        closedset.append(current_pos)

        if current_pos == goal:
            return get_path(came_from, current_pos)

        for neighbor in current_pos.get_neighbors():
            if is_out_of_range(neighbor):
                continue

            if neighbor in closedset:
                continue

            if neighbor not in openset:
                h[neighbor.value()] = heuristic(neighbor, goal)
                g[neighbor.value()] = g[current_pos.value()] + 1
                f[neighbor.value()] = g[neighbor.value()] + h[neighbor.value()]
                came_from[neighbor.value()] = current_pos
                openset.append(neighbor)
    return None

if __name__ == '__main__':
    grid1 = [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0]]

    start1 = Position(0,0)
    goal1  = Position(len(grid1)-1,len(grid1[0])-1)

    grid2 = [[0, 0, 0, 0],
             [0, 1, 0, 1],
             [0, 1, 1, 0],
             [0, 1, 1, 0]]

    start2 = Position(0,0)
    goal2  = Position(len(grid2)-1,len(grid2[0])-1)

    results = (a_star_path_search(start1, goal1, grid1), 
               a_star_path_search(start2, goal2, grid2))
    
    print results
