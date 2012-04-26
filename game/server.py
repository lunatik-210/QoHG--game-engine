
########## System libs ##########
from threading import Thread
from Queue import Queue
from socket import *
from array import *

import time
import numpy
import struct
import pickle
import zlib
import sys
#################################

######### Game logic ############
from lands.Position import Position
from lands.Land import Land
from lands.DemoLand import DemoLand

import lands.generators.Map as MapGenerator
import config
#################################


##let's set up some constants
TYPE_SIZE = 2
DATA_SIZE = 5

HOST = ''               #we are the host
PORT = 29877            #arbitrary port not currently in use
ADDR = (HOST, PORT)     #we need a tuple for the address
BUFSIZE = 4096          #reasonably sized buffer for data

'''define constants'''
# the approximate size of the map you want (should be large than size of main screen)
# I will try to think how to fix it later
size = 1000
# (change view) roughness, more biggest value will give more filled map
roughness = 20.0
# (change map ) you can think about seed as map number or id
land_id = 1233213

# terrains are constant
terrains = {
    'water'   : [[0, 0.58],     0],
    'sand'    : [[0.58, 0.60],  1],
    'grass'   : [[0.60, 0.1],   2]
}

# objects may gone
objects = {
    'log'   :  [[0.948, 0.949], 3],
    'stone' :  [[0.949,  0.95], 4],
    'tree'  :  [[0.95, 1.0],    5]
}

# [monster_id, probability]
# wolf, pig
monsters = { 
    'wolf' :  [11, 0.2],
    'pig'  :  [12, 0.3],
    'grass' : [2,  0.5]
}

# grass area
grass_area = [0.8, 0.81]

player_id = 10

########################################
def pack_data(request_type, data, land):
    ###########################################################
    types = {
        0 : 'get_map',
        1 : 'get_preview',
        2 : 'get_land_size',
        3 : 'update_map'
    }
    set_front_zeros = lambda s: (DATA_SIZE - len(s)) * '0' + s

    if types[request_type] == 'get_map':
        x1, y1, x2, y2 = map(int, data.split(','))
        matrix = numpy.zeros((x2-x1, y2-y1))
        ## prepare data ##
        vector = array('f', [])
        for x in range(x2-x1):
            for y in range(y2-y1):
                vector.append(land.value(Position(x+x1, y+y1)))
        ##################
        packed_vector = pickle.dumps(vector)
        compressed_vector = zlib.compress(packed_vector, 9)
        conn.send(set_front_zeros(str(sys.getsizeof(compressed_vector))) + compressed_vector)
    ###########################################################
    elif types[request_type] == 'get_preview':
        size = int(data)
        vector = DemoLand(land, size).get_demo()
        vector = pickle.dumps(vector)
        vector = zlib.compress(vector, 9)
        conn.send(set_front_zeros(str(sys.getsizeof(vector))) + vector)
    ###########################################################
    elif types[request_type] == 'get_land_size':
        size = zlib.compress("%d" % land.get_size(), 9)
        conn.send(set_front_zeros(str(sys.getsizeof(size))) + size)
    ###########################################################
    elif types[request_type] == 'update_map':
        x1, y1, x2, y2 = map(int, data.split(','))
        land.update(Position(x1,y1), Position(x2,y2))

def queue_data_handler(**kwargs):
    queue = kwargs['queue']
    land  = kwargs['land']

    while True:
        if queue.empty():
            time.sleep(0.05)
            continue
        try:
            conn, addr = queue.get()
        except IndexError:
            print "Can't get item[2]"

        request_type, data = request_parser(conn)
        pack_data(request_type, data, land)
        
        conn.close()
        queue.task_done()

def request_parser(conn):
    """
    request_type 0 - 99 [2 bytes]
    data_size 0 - 9999  [5 bytes]
    data                [data_size]
    """
    request_type = int(conn.recv(TYPE_SIZE))

    if request_type == 0 or request_type == 1 or request_type == 3:
        data_size = int(conn.recv(DATA_SIZE))
        data = conn.recv(data_size)
        return [request_type, data]
    elif request_type == 2:
        return [request_type, ""]


class Server(socket):
    def __init__(self, addr, debug = False):
        socket.__init__(self, AF_INET, SOCK_STREAM)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.addr = addr
        self.debug = debug

    def init(self):
        self.bind((self.addr))
        self.listen(50)
        if self.debug: print 'starts listening...'

if __name__ == '__main__':
    # init map generator
    map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, True)
    # init land
    land = Land(config.config, config.player_id, map_generator, config.allowable_list)

    # init queue for storing requests
    queue = Queue()

    # init requests handler
    thread = Thread(target=queue_data_handler, kwargs={'land': land, 'queue': queue})
    thread.daemon = True
    thread.start()

    # init server
    server = Server(ADDR, True)
    server.init()

    # starting accepting requests loop
    while True:
        # quieue -> connection, address, response (get_map, (x1, y1, x2, y2))
        conn, addr = server.accept()
        item = [conn, addr]
        queue.put(item)
        print '...connected!'

    # terminate server
    server.close()