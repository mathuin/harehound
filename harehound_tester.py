#!/usr/bin/env python

"""
Testing the hounds and hare server!
"""

import socket
import sys

if len(sys.argv) == 2:
    print 'host is %s' % sys.argv[1]
    host = sys.argv[1]
else:
    host = ''
port = 50000
size = 1024

def test_server(datain, dataout, host=host, port=port, size=size):
    print "Sending '%s', expecting '%s'" % (datain, dataout)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(datain)
    data = s.recv(size)
    s.close()
    if data == dataout:
        print " Success!"
    else:
        print " Failure!"

test_server('RESET', 'OK')
test_server('NEW HARE', 'OK HARE')
test_server('NEW HARE', 'ERR')
test_server('NEW HOUND', 'OK HOUND 1')
test_server('NEW HOUND', 'OK HOUND 2')
test_server('NEW HOUND', 'ERR')
test_server('ping', 'PONG')

