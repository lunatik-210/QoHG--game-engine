import logging

FORMAT=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
# example:
# server.py[LINE:146]# INFO     [2012-06-02 17:23:32,956]  ...connected!

logging.basicConfig(format=FORMAT, level=logging.DEBUG)