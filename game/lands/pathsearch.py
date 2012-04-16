
import numpy

from Position import Position 

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

####### fast_insert (logn) is faster than quick_sort (nlogn) #######
def fast_insert(element, h, list):
    l = len(list)
    val = h[element.value()]

    if l == 0:
        list.append(element)
        return True
    
    if l == 1:
        if h[list[0].value()] > val:
            list.append(element)
        else: 
            list.insert(0,element)
        return True

    if l == 2 and h[list[0].value()] < val < h[list[1].value()]:
        list.insert(1, element)
        return True

    if h[list[0].value()] < val:
        list.insert(0,element)
        return True
    if h[list[-1].value()] > val:
        list.append(element)
        return True

    return __fast_insert(element, h, list, 0, len(list)-1)

def __fast_insert(element, h, list, l, r):
    c = (r + l) >> 1
    val = h[element.value()]
    if not 1 <= c <= len(list)-2:
        return False
    if h[list[c-1].value()] < val < h[list[c].value()]:
        list.insert(c+1, element)
        return True
    if h[list[c].value()] < val < h[list[c+1].value()]:
        list.insert(c, element)
        return True
    if h[list[c-1].value()] < val:
        return __fast_insert(element, h, list, l, c-1)
    if h[list[c+1].value()] > val:
        return __fast_insert(element, h, list, c+1, r)
    return False

#################################################################

def get_path(came_from, pos):
    if pos.value() in came_from:
        vector = get_path(came_from, came_from[pos.value()])
        vector.append(pos)
        return vector
    return [pos]

def is_out_of_range(p, land, allowed_id):
    return not (0 <= p.x < len(land) and 
                0 <= p.y < len(land[0]) and 
                land[p.x][p.y] == allowed_id)

def heuristic(start,goal):
    return numpy.sqrt((start.x-goal.x)**2 + (start.y-goal.y)**2)

def a_star_path_search(start, goal, grid, allowed_id):
    if grid[goal.x][goal.y] != allowed_id:
        return None

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

    steps = 0

    while open:
        if steps > 500:
            return None
        steps += 1
        # getting the step with the shortest f - value
        #quicksort(open, 0, len(open)-1, f)
        current_pos = open.pop()

        closed.append(current_pos)

        if current_pos == goal:
            return get_path(came_from, current_pos)

        # for every neighbor of the current calculate f - value
        # and add it to the open list
        for neighbor in current_pos.get_neighbors():
            if is_out_of_range(neighbor, grid, allowed_id):
                continue

            if neighbor in closed:
                continue

            new_g = g[current_pos.value()] + 1
            update_pos = False
            insert = False

            if neighbor not in open:
                insert = True
                update_pos = True
            elif new_g < g[neighbor.value()]:
                update_pos = True

            if update_pos:
                g[neighbor.value()] = new_g
                f[neighbor.value()] = g[neighbor.value()] + heuristic(neighbor, goal)
                came_from[neighbor.value()] = current_pos
            
            if insert:
                fast_insert(neighbor,f, open)
                #open.append(neighbor)

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

    grid3 = [[0, 0, 0, 0, 0], # 0
             [0, 1, 1, 0, 0], # 1
             [0, 1, 1, 0, 1], # 2
             [0, 1, 0, 0, 0], # 3
             [0, 0, 0, 1, 0]] # 4

    start3 = Position(0,0)
    goal3  = Position(len(grid3)-1, len(grid3[0])-1)

    grid4 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # 0
             [0, 1, 1, 1, 1, 0, 0, 0, 0], # 1
             [0, 1, 1, 0, 1, 1, 1, 0, 0], # 2
             [0, 1, 0, 0, 0, 0, 1, 0, 0], # 3
             [0, 1, 0, 1, 0, 0, 0, 0, 0]] # 4

    start4 = Position(0,0)

    goal4  = Position(2,3)

    results = (a_star_path_search(start1, goal1, grid1, 0), 
               a_star_path_search(start2, goal2, grid2, 0),
               a_star_path_search(start3, goal3, grid3, 0),
               a_star_path_search(start4, goal4, grid4, 0))
    
    nice_print(results)
