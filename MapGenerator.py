
from numpy import *
import random

def is_odd(dsize):
    return (dsize % 2 == 1)

def correct_as_odd(dsize):
    if is_odd(dsize) == False:
        return dsize+1
    return dsize

def correct_dimension_size(dsize):
    temp_dsize = dsize
    while True:
        temp_dsize = (temp_dsize + 1) >> 1
        if is_odd(temp_dsize) == False:
            return correct_dimension_size(dsize+2)
        if temp_dsize <= 3:
            return dsize

def setup_grid(dsize):
    return zeros((dsize, dsize))

def displace(h):
    return random.uniform(-h, h)

def square(grid, dsize, sideLength, displs):
    halfSide = sideLength >> 1
    x = 0        
    while x<dsize-1:
        y = 0
        while y<dsize-1:
            avg = ( grid[x][y] + 
                grid[x+sideLength][y] + 
                grid[x][y+sideLength] + 
                grid[x+sideLength][y+sideLength] )
            avg *= 0.25
            avg += displs
            grid[x+halfSide][y+halfSide] = avg
            y += sideLength
        x += sideLength
    return grid

def diamond(grid, dsize, sideLength, displs):
    halfSide = sideLength >> 1
    x = 0
    while x<dsize-1:
        y = (x + halfSide) % sideLength
        while y<dsize-1:
            avg = ( grid[(x-halfSide+dsize-1)%(dsize-1)][y] + 
                    grid[(x+halfSide)%(dsize-1)][y] + 
                    grid[x][(y-halfSide+dsize-1)%(dsize-1)] + 
                    grid[x][(y+halfSide)%(dsize-1)] )
            avg *= 0.25
            avg += displs
            grid[x][y] = avg
            if x == 0:
                grid[dsize-1][y] = avg
            if y == 0:
                grid[x][dsize-1] = avg
            y += sideLength
        x+=halfSide    
    return grid

def diamond_square(grid, dsize, h):
    seed = h
    random.seed(seed)

    grid[0][0] = displace(h)
    grid[0][dsize-1] = displace(h)
    grid[dsize-1][0] = displace(h)
    grid[dsize-1][dsize-1] = displace(h)       

    sideLength = dsize-1

    while sideLength >=2:
        displs = displace(h)
        grid = square(grid, dsize, sideLength, displs)
        grid = diamond(grid, dsize, sideLength, displs)
        sideLength >>= 1
        h >>= 1

    return grid

def generate_map(dsize, h):
    dsize = correct_as_odd(dsize)
    dsize = correct_dimension_size(dsize)
    grid = setup_grid(dsize)
    grid = diamond_square(grid, dsize, h)
    return grid, dsize
