#!/usr/bin/env python

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
from log import *
#################################

######### Game logic ############
from lands.Position import Position
from lands.Land import Land
from lands.DemoLand import DemoLand

import lands.generators.Map as MapGenerator
import config
#################################


path = './configs'

network = config.load_network(path+'/network.xml')

# the approximate size of the map you want (should be large than size of main screen)
# I will try to think how to fix it later
size = 1000
# (change view) roughness, more biggest value will give more filled map
roughness = 20.0
# (change map ) you can think about seed as map number or id
land_id = 1233213

########################################
def pack_data(request_type, data, land):
    ###########################################################
    buffer_size = network['protocol']['response']['buffer_size']
    type = network['requests'][request_type]
    set_front_zeros = lambda s: (buffer_size - len(s)) * '0' + s

    if type == 'get_map':
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
    elif type == 'get_preview':
        size = int(data)
        vector = DemoLand(land, size).get_demo()
        vector = pickle.dumps(vector)
        vector = zlib.compress(vector, 9)
        conn.send(set_front_zeros(str(sys.getsizeof(vector))) + vector)
    ###########################################################
    elif type == 'get_land_size':
        size = zlib.compress("%d" % land.get_size(), 9)
        conn.send(set_front_zeros(str(sys.getsizeof(size))) + size)
    ###########################################################
    elif type == 'update_map':
        x1, y1, x2, y2 = map(int, data.split(','))
        land.update(Position(x1,y1), Position(x2,y2))

def queue_data_handler(**kwargs):
    queue = kwargs['queue']
    land  = kwargs['land']

    while True:
        if queue.empty():
            time.sleep(0.05)
            continue

        conn, addr = queue.get()
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
    type_size = network['protocol']['request']['request_type']
    data_size = network['protocol']['request']['buffer_size']

    request_type = int(conn.recv(type_size))

    if request_type in [0, 1, 3]:
        data_size = int(conn.recv(data_size))
        data = conn.recv(data_size)
        return [request_type, data]
    elif request_type == 2:
        return [request_type, ""]


class Server(socket):
    def __init__(self, addr, debug=False):
        socket.__init__(self, AF_INET, SOCK_STREAM)
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.addr = addr
        # self.debug = debug

    def init(self):
        self.bind((self.addr))
        self.listen(50)
        logging.info('starts listening...')

if __name__ == '__main__':
    # init map generator
    map_generator = MapGenerator.DiamondSquare(size, roughness, land_id, True)
    # init land
    land = Land(map_generator)

    # init queue for storing requests
    queue = Queue()

    # init requests handler
    thread = Thread(target=queue_data_handler, kwargs={'land': land, 'queue': queue})
    thread.daemon = True
    thread.start()

    # init server
    server = Server(network['addr'], True)
    server.init()

    # starting accepting requests loop
    while True:
        # quieue -> connection, address, response (get_map, (x1, y1, x2, y2))
        conn, addr = server.accept()
        item = [conn, addr]
        queue.put(item)
        logging.info('...connected!')

    # terminate server
    server.close()