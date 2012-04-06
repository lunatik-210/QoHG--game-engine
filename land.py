
import numpy

class Land:
    def __init__(self, heights, map_generator):
        self.heights = heights
        self.map_generator = map_generator
        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)

    def set_land_id(self, land_id):
        self.map_generator.set_seed(land_id)

    def value(self, x,y):
        val = self.land[x][y]
        if val != -1:
            return val
        self.land[x][y] = self.get_block_id(self.heights, self.map_generator.calc(x,y))
        return self.land[x][y]

    def get_size(self):
        return self.lsize

    def get_block_id(self, height_map, val):
        for i in range(len(height_map)-1):
            if height_map[i] <= val <= height_map[i+1]:
                return i

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass
