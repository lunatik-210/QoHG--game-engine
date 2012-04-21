#!/usr/bin/env python

import numpy
import sys

class MapGenerator():
    def __init__(self, size, debug=False):      
        if not self.is_odd(size):
            size += 1
        self.size = self.correct_size_dimension(size)
        self.grid = self.setup_grid(self.size)
        self.debug = debug

    def clean(self):
        self.grid = setup_grid(self.size)

    def get_size(self):
        return self.size

    def get_map(self):
        return self.grid

    def is_odd(self, dsize):
        return (dsize % 2 == 1)

    def correct_size_dimension(self, dsize):
        temp_dsize = dsize
        while True:
            temp_dsize = (temp_dsize + 1) >> 1
            if not self.is_odd(temp_dsize):
                return self.correct_size_dimension(dsize+2)
            if temp_dsize <= 3:
                return dsize

    def setup_grid(self, size):
        return numpy.zeros((size, size))

    # must be defined by children
    def calc(self, x, y):
        pass

class DiamondSquare(MapGenerator):
    def __init__(self, size, roughness, seed, debug=False):
        MapGenerator.__init__(self, size, debug)

        self.roughness = roughness
        self.seed = seed

        numpy.random.seed(seed)

    def set_seed(self, seed):
        self.seed = seed

    def displace(self, v, blockSize, x, y):
        return (v + (numpy.random.normal(0.5, 0.2) - 0.5) * blockSize * 2 / self.size * self.roughness)

    def calc(self, x, y, v="undef"):
        if v == "undef":
            if x <= 0 or x >= self.size-1 or y <= 0 or y >= self.size-1:
                return 0.0
            if self.grid[x][y] == 0:
                base = 1
                while (x & base) == 0 and (y & base) == 0:
                    base <<= 1
                if (x & base) != 0 and (y & base) != 0:
                    self.square_step(x, y, base)
                else:
                    self.diamond_step(x, y, base)
            return self.grid[x][y]
        else:
            self.grid[x][y] = max(0.0, min(1.0, v))

    def square_step(self, x, y, blockSize):
        if self.grid[x][y] == 0:
            self.calc(x, y, self.displace((self.calc((x-blockSize),(y-blockSize)) + 
                                           self.calc((x+blockSize),(y-blockSize)) + 
                                           self.calc((x-blockSize),(y+blockSize)) + 
                                           self.calc((x+blockSize),(y+blockSize))) / 4, blockSize, x, y))
        
    def diamond_step(self, x, y, blockSize):
        if self.grid[x][y] == 0:
            self.calc(x, y, self.displace((self.calc((x-blockSize), y) + 
                                           self.calc((x+blockSize), y) + 
                                           self.calc(x, (y-blockSize)) + 
                                           self.calc(x, (y+blockSize))) / 4, blockSize, x, y ))
