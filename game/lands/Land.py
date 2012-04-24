
import numpy
import random

from generators.Object import ObjectGenerator
from generators.Map import Humidity
from pathsearch import a_star_path_search as get_path
from Position import Position

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.path = []

    def set_path(self, path):
        self.path = path

    def move(self):
        if len(self.path) != 0:
            step = self.path.pop()
            self.pos = step

class Land:
    def __init__(self, heights, monsters, player_id, grass_area, map_generator, allowable_list):
        self.grass_area = grass_area
        self.monsters = monsters
        self.heights = heights
        self.player_id = player_id
        self.allowable_list = allowable_list

        self.map_generator = map_generator
        self.monster_genearator = ObjectGenerator(monsters)

        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)

        self.humidity = Humidity(self.lsize, self.heights['humidity'])
        self.humidity.build_map()

        self.player = Player(Position(-1, -1))

    def set_land_id(self, land_id):
        self.map_generator.set_seed(land_id)

    ############# for player ##############
    def init_player(self):
        found = False
        pos = None
        s = self.lsize
        while not found:
            pos = Position(abs(int(random.uniform(0, s))),
                           abs(int(random.uniform(0, s))))
            if self.value(pos) == self.heights['default']:
                found = True
        self.player = Player(pos)
        return pos

    def move_player(self):
        self.player.move()

    def add_path_to_player(self, destination):
        path = get_path(self.player.pos, destination, self.get_land(), self.allowable_list)
        if None == path:
            return
        path.reverse()
        self.player.set_path(path)

    #######################################

    def set_value(self, pos, value):
        self.land[pos.x][pos.y] = value

    def get_land(self):
        return self.land

    def value(self, pos):
        if self.player.pos == pos:
            return self.player_id

        val = self.land[pos.x][pos.y]

        if val != -1:
            return val
        val = self.map_generator.calc(pos.x,pos.y)

        self.land[pos.x][pos.y] = self.get_block_id(val, self.humidity.value(pos.x, pos.y ))
        
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
                        self.land[x][y] = self.heights['default']
                        count = 0
                        while count < 5:
                            new_x = int(random.uniform(-2, 2)) + x
                            new_y = int(random.uniform(-2, 2)) + y
                            if self.land[new_x][new_y] == self.heights['default']:
                                self.land[new_x][new_y] = self.monsters[monster][0]
                                break
                            count += 1

    def get_size(self):
        return self.lsize

    def get_block_id(self, val, humidity):
        for block in self.heights[humidity]:
            if block[0][0] <= val <= block[0][1]:
                return block[1]
        return self.heights['default']

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass
