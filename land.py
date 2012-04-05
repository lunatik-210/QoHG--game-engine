import MapGenerator
import numpy

class Land:
    def __init__(self, size, heights, land_id=100, roughness=15.0, debug=False):
        self.heights = heights
        self.map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, debug)
        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)

    def set_land_id(self, land_id):
        self.map_generator.set_seed(land_id)

    def value(self, x,y):
        val = self.land[x][y]
        if val != -1:
            return val
        self.land[x][y] = self.get_block_type_id(self.map_generator.calc(x,y))
        return self.land[x][y]

    def get_size(self):
        return self.lsize

    def get_block_type_id(self, val):
        for i in range(len(self.heights)-1):
            if self.heights[i] <= val <= self.heights[i+1]:
                return i

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass
