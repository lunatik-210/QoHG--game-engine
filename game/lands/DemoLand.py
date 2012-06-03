import numpy

from Position import Position

class DemoLand:
    """
    TODO: write documentation
    """
    def __init__(self, land, size, border=4):
        self.land = land
        self.size = size
        self.border = border
        self.demo_land = numpy.zeros((self.size,self.size))
        
        self.init_demo()

    def init_demo(self):
        d = self.land.get_size() / self.size
        for x in range(self.border, self.size-self.border):
            for y in range(self.border, self.size-self.border):
                self.demo_land[x][y] = self.land.value(Position(x * d, y * d))

    def get_demo(self):
        return self.demo_land

    def get_size(self):
        return self.size

    def get_border(self):
        return self.border

    def get_local_pos(self, global_pos, surface_size):
        return global_pos / (self.land.get_size()/surface_size)