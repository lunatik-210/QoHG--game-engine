import numpy
import random

from generators.Object import ObjectGenerator
from generators.Map import Humidity
from pathsearch import a_star_path_search as get_path
from Position import Position

import config

path = './configs'

items = config.load_items(path+'/items.xml')
bioms = config.load_bioms(path+'/bioms.xml', items)

class Player:
    """
    Player can move on the land - user just let him do it by clicking on the stage.
    """
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
    """
    TODO: write documentation
    """
    def __init__(self, map_generator):
        self.map_generator = map_generator

        self.lsize = self.map_generator.get_size()
        self.land = numpy.empty((self.lsize,self.lsize))
        self.land.fill(-1)

        self.humidity = Humidity(self.lsize, bioms['humidity'])
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
            if self.value(pos) == items['default'] and bioms['prairie'] == self.humidity.value(pos.x, pos.y):
                found = True
        self.player = Player(pos)
        return pos

    def move_player(self):
        self.player.move()

    def add_path_to_player(self, destination):
        path = get_path(self.player.pos, destination, self.get_land(), items['walkable_objects'])
        if path is None:
            return
        path.reverse()
        self.player.set_path(path)

    #######################################

    def set_value(self, pos, value):
        self.land[pos.x][pos.y] = value

    def get_land(self):
        return self.land

    def value(self, pos):
        pos %= self.lsize

        if self.player.pos == pos:
            return items['monsters']['player']

        val = self.land[pos.x][pos.y]

        if val != -1:
            return val
        
        val = self.map_generator.calc(pos.x,pos.y)
        biom = self.humidity.value(pos.x, pos.y)

        self.land[pos.x][pos.y] = self.get_block_id(val, biom)
        monsters = bioms[biom]['monsters']

        # choose monster
        if (monsters is not None) and (self.land[pos.x][pos.y] in items['walkable_objects']):
            new_val = ObjectGenerator(monsters).generate()
            if new_val is not None:
                self.land[pos.x][pos.y] = new_val

        return self.land[pos.x][pos.y]

    def update(self, p1, p2):
        """
            Not understandable code, I have to fix it
            But it really makes monsters move =)))))))))))))
        """
        # FIXME: try to refactor this not understandable piece of sh!t T_T
        monsters = items['monsters']
        for x in range(p1.x, p2.x):
            for y in range(p1.y, p2.y):
                x %= self.lsize
                y %= self.lsize
                for monster in monsters:
                    if self.land[x][y] == monsters[monster]:
                        self.land[x][y] = bioms[self.humidity.value(x,y)]['default']
                        count = 0
                        while count < 5:
                            new_x = (int(random.uniform(-2, 2)) + x) % self.lsize
                            new_y = (int(random.uniform(-2, 2)) + y) % self.lsize
                            if self.land[new_x][new_y] in items['walkable_objects']:
                                self.land[new_x][new_y] = monsters[monster]
                                break
                            count += 1

    def get_size(self):
        return self.lsize

    def get_block_id(self, val, biom):
        for block in bioms[biom]['objects']:
            if block[0][0] <= val <= block[0][1]:
                return block[1]
        return bioms[biom]['default']

    # Here we should use some data base
    def save(self, name):
        pass

    def load(self, name):
        pass
