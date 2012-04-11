
import numpy

from land import Position 

'''
    Here I've implemented A* search algorithm for path finding.
    The idea is to use some heuristic function which is actually
    the estimation distance to the goal from the current location.
    So, every time we try to choose the shortest step to get 
    to the goal, but it doesnt mean that the path is the best one.
'''

# Quick Sort: used in A* algorithm

def quicksort(a, l, r, h):
    if l >= r:
        return
    m = particion(a, l, r, h)
    quicksort(a, l, m-1, h)
    quicksort(a, m+1, r, h)

def particion(a, l, r, h):
    i = l-1
    for j in range(l, r+1):
        if h[a[j].value()] >= h[a[r].value()]:
            i += 1
            a[j], a[i] = a[i], a[j]
    return i

###################################

def get_path(came_from, pos):
    if pos.value() in came_from:
        vector = get_path(came_from, came_from[pos.value()])
        vector.append(pos)
        return vector
    return [pos]

def is_out_of_range(p, land):
    return not ( 0 <= p.x < len(land) and 
                 0 <= p.y < len(land[0]) and 
                 land[p.x][p.y] == 0)

def heuristic(start,goal):
    return numpy.sqrt((start.x-goal.x)**2 + (start.x-goal.y)**2)

def a_star_path_search(start, goal, grid):
    closed = []
    open = [start]
    
    # storing actions for every node to retrieve the path
    came_from = {}

    # g - distance from starting location to current
    g = {}

    # f - g + heuristic
    f = {}

    g[start.value()] = 0
    f[start.value()] = g[start.value()] + heuristic(start, goal)

    while open:

        # getting the step with the shortest f - value
        quicksort(open, 0, len(open)-1, f)
        current_pos = open.pop()

        closed.append(current_pos)

        if current_pos == goal:
            return get_path(came_from, current_pos)

        # for every neighbor of the current calculate f - value
        # and add it to the open list
        for neighbor in current_pos.get_neighbors():
            if is_out_of_range(neighbor, grid):
                continue

            if neighbor in closed:
                continue

            if neighbor not in open:
                g[neighbor.value()] = g[current_pos.value()] + 1
                f[neighbor.value()] = g[neighbor.value()] + heuristic(neighbor, goal)
                came_from[neighbor.value()] = current_pos
                open.append(neighbor)
    return None


''' Some tests '''

def nice_print(data):
    for i in data:
        if i:
            for j in i[:-1]:
                print j, "->",
            print i[-1]
        else:
            print None

if __name__ == '__main__':
    grid1 = [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0]]

    start1 = Position(0,0)
    goal1  = Position(len(grid1)-1, len(grid1[0])-1)

    grid2 = [[0, 0, 0, 0],
             [0, 1, 0, 1],
             [0, 1, 1, 0],
             [0, 1, 1, 0]]

    start2 = Position(0,0)
    goal2  = Position(len(grid2)-1, len(grid2[0])-1)

    # (0, 0) -> (0, 1) -> (0, 2) -> (0, 3) -> (1, 3) -> (2, 3) -> (3, 3) -> (3, 4) -> (4, 4) is the best path
    # (0, 0) -> (1, 0) -> (2, 0) -> (3, 0) -> (4, 0) -> (4, 1) -> (4, 2) -> (3, 2) -> (3, 3) -> (3, 4) -> (4, 4) what algo is find
    #         0  1  2  3  4
    grid3 = [[0, 0, 0, 0, 0], # 0
             [0, 1, 1, 0, 0], # 1
             [0, 1, 1, 0, 1], # 2
             [0, 1, 0, 0, 0], # 3
             [0, 0, 0, 1, 0]] # 4

    start3 = Position(0,0)
    goal3  = Position(len(grid3)-1, len(grid3[0])-1)

    results = (a_star_path_search(start1, goal1, grid1), 
               a_star_path_search(start2, goal2, grid2),
               a_star_path_search(start3, goal3, grid3))
    
    nice_print(results)


