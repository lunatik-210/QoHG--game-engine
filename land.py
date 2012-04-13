
import numpy
import random

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

    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y)

    def __sub__(self, pos):
        return Position(self.x - pos.x, self.y - pos.y)

    def __mod__(self, value):
        return Position(self.x % value, self.y % value)    

    def __div__(self, value):    
        return Position(self.x / value, self.y / value)    

    def left(self):
        return Position(self.x-1, self.y)

    def right(self):
        return Position(self.x+1, self.y)

    def bottom(self):
        return Position(self.x, self.y+1)

    def top(self):
        return Position(self.x, self.y-1)

    def lefttop(self):
        return Position(self.x-1, self.y-1)

    def righttop(self):
        return Position(self.x+1, self.y-1)

    def leftbottom(self):
        return Position(self.x-1, self.y+1)

    def rightbottom(self):
        return Position(self.x+1, self.y+1)

    def value(self):
        return (self.x, self.y)

    def get_neighbors(self):
        return (self.left(), self.top(), self.right(), self.bottom(), 
                self.lefttop(), self.righttop(), self.leftbottom(), self.rightbottom())

class DemoLand:
    def __init__(self, land, size, border = 4):
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
            who = int(random.uniform(0,len(self.monsters)))
            name = 'wolf' * (1-who) + 'pig' * (0+who)
            if self.monsters[name][1] > random.gauss(0.6,0.17):
                self.land[pos.x][pos.y] = self.monsters[name][0]
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

