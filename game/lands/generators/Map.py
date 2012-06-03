#!/usr/bin/env python

import numpy
import sys
import math
import random

class Humidity:
    """
    TODO: write documentation
    """
    def __init__(self, size, height):
        self.height = height
        self.size = int(numpy.log2(size))
        self.scale = int(size / self.size)
        self.map = numpy.zeros((self.size, self.size))

    def build_map(self):
        for x in range(self.size):
            for y in range(self.size):
                self.map[x][y] = self.get_block_id(random.uniform(0,1))
        return self.map

    def value(self, x, y):
        x = int(x/self.scale) % self.size
        y = int(y/self.scale) % self.size
        return self.map[x][y]

    def get_block_id(self, val):
        for block in self.height:
            if block[0][0] <= val <= block[0][1]:
                return block[1]
        print 'Error: cannt define Humidity block: ', val
        return None

class MapGenerator:
    """
    TODO: write documentation
    """
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
        return (dsize & 1)

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
    """
    TODO: write documentation
    """
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

class Perling(MapGenerator):
    """
    TODO: write documentation
    """
    def __init__(self, size, octaves=6, persistence=0.2, debug=False):
        MapGenerator.__init__(self, size, debug)
        self.octaves = octaves
        self.persistence = persistence

    def noise(self, x, y):
        n = x + y * 57
        n = (n<<13) ^ n
        return ( 1.0 - ( (n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

    def lin_interpolate(self, a, b, x):
        return  a*(1-x) + b*x

    def cos_interpolate(self, a, b, x):
        ft = x * 3.1415927
        f = (1 - math.cos(ft)) * .5
        return  a*(1-f) + b*f

    def smooth_noise(self, x, y):
        corners = ( self.noise(x-1, y-1)+self.noise(x+1, y-1)+self.noise(x-1, y+1)+self.noise(x+1, y+1) ) / 16
        sides   = ( self.noise(x-1, y)  +self.noise(x+1, y)  +self.noise(x, y-1)  +self.noise(x, y+1) ) /  8
        center  =  self.noise(x, y) / 4
        return corners + sides + center

    def interpolated_noise(self, x, y, interpolate):
        integer_X    = int(x)
        fractional_X = x - 1
        integer_Y    = int(y)
        fractional_Y = y - 1
        v1 = self.smooth_noise(integer_X,     integer_Y)
        v2 = self.smooth_noise(integer_X + 1, integer_Y)
        v3 = self.smooth_noise(integer_X,     integer_Y + 1)
        v4 = self.smooth_noise(integer_X + 1, integer_Y + 1)
        i1 = interpolate(v1 , v2 , fractional_X)
        i2 = interpolate(v3 , v4 , fractional_X)
        return interpolate(i1 , i2 , fractional_Y)

    def calc(self, x, y):
        val = 0.0
        for i in range(self.octaves):
            val += self.interpolated_noise(x * (2**i), y * (2**i), self.cos_interpolate) * self.persistence**i
        return val