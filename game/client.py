##client.py
from socket import *
import pickle
from array import *
import zlib
import sys

class Client(socket):
    def __init__(self, addr, buffsize, debug=False):
        self.addr = addr
        self.buffsize = buffsize
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
            self.buffsize = int(self.recv(5))
            data = self.recv(self.buffsize)
            data = zlib.decompress(data)
            if is_pickle:
                data = pickle.loads(data)
            if self.debug:
                print "RESPONSE: ", (data)

        self.close()
        return data

class Request:
    def __init__(self, type, data=None, bytes=5):
        self.type = self._type_string(type)
        self.data = data
        self.bytes = bytes

    def _type_string(self, type):
        if type < 10:
            return "%d%d" % (0, type)
        else:
            return str(type)

    def _add_leading_0(self, data, bytes):
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
        """
        Form request by pattern:
            [REQUESTTYPE (?:BUFSIZE DATA)?]
            REQUESTTYPE: 2b
            BUFSIZE:     5b
            DATA:        15b (or less)
        There are 4 request types at this moment:
            0 -> get_map
            1 -> get_preview
            2 -> get_land_size
            3 -> update_map
        """
        if not self.data:
            return self.type
        else:
            return "%s%s%s" % (self.type,
                               self._add_leading_0(self.data, self.bytes),
                               self.data)

if __name__ == '__main__':
    client = Client(ADDR, BUFSIZE, True)

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
