from socket import *
import pickle
from array import *
import zlib
import sys
from log import *

import config

path = './configs'

network = config.load_network(path+'/network.xml')

class Client(socket):
    """
    Class Client
    TODO: write documentation
    """
    def __init__(self, addr, debug=False):
        self.addr = addr
        self.debug = debug
    
    def __reinitsoc(self):
        socket.__init__(self, AF_INET, SOCK_STREAM)

    def send_request(self, request, waite_for_response=False, is_pickle=False):
        self.__reinitsoc()
        self.connect(self.addr)
        # prcessing request
        self.send(request)
        data = None
        if waite_for_response:
            buffsize = int(self.recv(network['protocol']['response']['buffer_size']))
            data = self.recv(buffsize)
            data = zlib.decompress(data)
            if is_pickle:
                data = pickle.loads(data)
            logging.debug("RESPONSE: %s", str(data))

        self.close()
        return data

class Request:
    """
    Class Request
    TODO: write documentation
    """
    def __init__(self, type, data=None, bytes=network['protocol']['request']['buffer_size']):
        self.type = self.__type_string(type)
        self.data = data
        self.bytes = bytes

    def __type_string(self, type):
        """Return 2 bytes string for correctly sending in request"""
        return "%d%d" % (0, type) if type < 10 else str(type)

    def __add_leading_0(self, data, bytes):
        """
        Function adds leading zeros to number for getting [bytes]bytes number
        For example, incoming data is 'testfoobar'
        We can see, that len('testfoo') is 10
        So the function adds two leading zeros at front: 0010
        FIXME: Maybe there is function in stdlib
        """
        if data:
            string = str(sys.getsizeof(data))
            return (bytes - len(string)) * '0' + string
        else:
            return None

    def form_request(self):
        if not self.data:
            return self.type
        else:
            return "%s%s%s" % (self.type,
                               self.__add_leading_0(self.data, self.bytes),
                               self.data)

if __name__ == '__main__':
    """
    Request class testing
    """
    client = Client(network['addr'], True)

    data1 = '600,600,621,616'
    data2 = '100'

    request0 = Request(0, data1).form_request()
    request1 = Request(1, data2).form_request()
    request2 = Request(2).form_request()
    request3 = Request(3, data1).form_request()

    client.send_request(request0, waite_for_response=True, is_pickle=True)
    client.send_request(request1, waite_for_response=True, is_pickle=True)
    client.send_request(request2, waite_for_response=True)
    client.send_request(request3)
