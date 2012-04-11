
import numpy
import random

class Land:
    def __init__(self, heights, monsters, grass_area, map_generator):
        self.grass_area = grass_area
        self.monsters = monsters
        self.heights = heights
        self.map_generator = map_generator
        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.objects = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)

    def set_land_id(self, land_id):
        self.map_generator.set_seed(land_id)

    def set_value(self, x, y, value):
        self.land[x][y] = value

    def value(self, x,y):
        val = self.land[x][y]
        if val != -1:
            return val
        val = self.map_generator.calc(x,y)
        self.land[x][y] = self.get_block_id(self.heights, val)
        '''Make desicion about pig or wolf'''
        if self.grass_area[0] < val < self.grass_area[1]:
            who = int(random.uniform(0,len(self.monsters)))
            name = 'wolf' * (1-who) + 'pig' * (0+who)
            if self.monsters[name][1] > random.gauss(0.6,0.17):
                self.land[x][y] = self.monsters[name][0]
        return self.land[x][y]

    def update(self, x1, y1, x2, y2):
        '''-_______- -_______- -_______- -_______- -_______-'''
        '''Not understandable code, I have to fix it        '''
        '''But it really makes monsters move =))))))))))))) '''
        for x in range(x1, x2):
            for y in range(y1, y2):
                for monster in self.monsters:
                    if self.land[x][y] == self.monsters[monster][0]:
                        self.land[x][y] = self.heights['grass'][1]
                        count = 0
                        while count < 5:
                            new_x = int(random.uniform(-2,2)) + x
                            new_y = int(random.uniform(-2,2)) + y
                            if self.land[new_x][new_y] == self.heights['grass'][1]:
                                self.land[new_x][new_y] = self.monsters[monster][0]
                                break
                            count += 1

    def add_player(self, player_id):
        self.player = Position(abs(int(random.gauss(lsize, lsize))),abs(int(random.gauss(lsize, lsize))))
        return self.player

    def get_size(self):
        return self.lsize

    def get_block_id(self, height_map, val):
        for block in height_map:
            if height_map[block][0][0] <= val <= height_map[block][0][1]:
                return height_map[block][1]

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass


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

    def __add__(self,pos):
        self.x, self.y = pos.x, pos.y

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