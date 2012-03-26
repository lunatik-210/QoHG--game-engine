#!/usr/bin/env python

from numpy import *
import random

class MapGenerator():
    def __init__(self, size):      
        if self.isOdd(size) == False:
            size+=1
        self.size = self.correctSizeDimension(size)
        self.grid = self.setupGrid(size)

    def clean(self):
        self.grid = setupGrid()

    def getSize(self):
        return self.size

    def getMap(self):
        return self.grid

    def isOdd(self, dsize):
        return (dsize % 2 == 1)

    def correctSizeDimension(self, dsize):
        temp_dsize = dsize
        while True:
            temp_dsize = (temp_dsize + 1) >> 1
            if self.isOdd(temp_dsize) == False:
                return self.correctSizeDimension(dsize+2)
            if temp_dsize <= 3:
                return dsize

    def setupGrid(self, size):
        return zeros((size, size))

class DiamondSquare(MapGenerator):
    def __init__(self, size, roughness, seed):
        MapGenerator.__init__(self, size)

        self.roughness = roughness
        self.seed = seed
        
        random.seed(seed)

    def displace(self, v, blockSize, x, y):
        return (v + (random.gauss(0.5, 0.2) - 0.5) * blockSize * 2 / self.size * self.roughness)

    def value(self, x, y, v = "undef"):
        size = len(self.grid)
        if v == "undef":
            if x <= 0 or x >= size or y <= 0 or y >= size:
                return 0.0
            if self.grid[x][y] == 0:
                base = 1
                while (((x & base) == 0) and ((y & base) == 0)):
                    base <<= 1
                if (((x & base) != 0) and ((y & base) != 0)):
                    self.squareStep(x, y, base)
                else:
                    self.diamondStep(x, y, base)
            return self.grid[x][y]
        else:
            self.grid[x][y] = max(0.0, min(1.0, v))

    def squareStep(self, x, y, blockSize):
        size = len(self.grid)-1
        if self.grid[x][y] == 0:
            self.value(x, y, self.displace((self.value((x-blockSize),(y-blockSize)) + 
                                            self.value((x+blockSize),(y-blockSize)) + 
                                            self.value((x-blockSize),(y+blockSize)) + 
                                            self.value((x+blockSize),(y+blockSize))) / 4, blockSize, x, y))
        
    def diamondStep(self, x, y, blockSize):
        size = len(self.grid)-1
        if self.grid[x][y] == 0:
            self.value(x, y, self.displace((self.value((x-blockSize), y) + 
                                            self.value((x+blockSize), y) + 
                                            self.value(x, (y-blockSize)) + 
                                            self.value(x, (y+blockSize))) / 4, blockSize, x, y ))
