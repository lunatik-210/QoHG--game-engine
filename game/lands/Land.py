
import numpy
import random

from generators.Object import ObjectGenerator
from Position import Position

class Land:
    def __init__(self, terrains, objects, monsters, def_id, grass_area, map_generator):
        self.grass_area = grass_area
        self.monsters = monsters
        self.terrains = terrains
        self.objects = objects
        self.def_id = def_id
        self.map_generator = map_generator
        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)
        self.monster_genearator = ObjectGenerator(monsters)

    def set_land_id(self, land_id):
        self.map_generator.set_seed(land_id)

    def set_value(self, pos, value):
        self.land[pos.x][pos.y] = value

    def get_land(self):
        return self.land

    def value(self, pos):
        val = self.land[pos.x][pos.y]
        if val != -1:
            return val
        val = self.map_generator.calc(pos.x,pos.y)

        self.land[pos.x][pos.y] = self.get_block_id(self.terrains, val)

        if self.land[pos.x][pos.y] == self.def_id:
            self.land[pos.x][pos.y] = self.get_block_id(self.objects, val)
        
        '''Make desicion about pig or wolf'''
        if self.grass_area[0] < val < self.grass_area[1]:
            new_val = self.monster_genearator.generate()
            if new_val is not None:
                self.land[pos.x][pos.y] = new_val

        return self.land[pos.x][pos.y]

    def update(self, p1, p2):
        '''-_______- -_______- -_______- -_______- -_______-'''
        '''Not understandable code, I have to fix it        '''
        '''But it really makes monsters move =))))))))))))) '''
        for x in range(p1.x, p2.x):
            for y in range(p1.y, p2.y):
                for monster in self.monsters:
                    if self.land[x][y] == self.monsters[monster][0]:
                        self.land[x][y] = self.terrains['grass'][1]
                        count = 0
                        while count < 5:
                            new_x = int(random.uniform(-2,2)) + x
                            new_y = int(random.uniform(-2,2)) + y
                            if self.land[new_x][new_y] == self.terrains['grass'][1]:
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
        return self.def_id

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass
