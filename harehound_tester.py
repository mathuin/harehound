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
        print " Failure -- got '%s' instead!" % data

test_server('ping', 'PONG')
test_server('RESET', 'OK')
test_server('NEW HARE', 'OK HARE')
test_server('NEW HARE', 'ERR')
test_server('NEW HOUND', 'OK HOUND-1')
test_server('NEW HOUND', 'OK HOUND-2')
test_server('NEW HOUND', 'ERR')
test_server('POS HOUND-3 47.12345 -123.12345', 'ERR')
test_server('POS HARE INVALID POSITION', 'OK')
test_server('POS HARE 45.12345 -123.12345', 'OK')
test_server('POS HOUND-2 44.12345 -123.45678', 'POS 45.12345 -123.12345')
test_server('POS HOUND-1 46.12345 -123.45678', 'POS 45.12345 -123.12345')
test_server('POS HARE 44.56753 -123.27911', 'POS 46.12345 -123.45678 44.12345 -123.45678')
test_server('POS HOUND-1 44.56747 -123.27897', 'WIN HOUND-1 44.56747 -123.27897')
test_server('POS HOUND-2 44.12345 -123.45678', 'WIN HOUND-1 44.56747 -123.27897')
test_server('EXIT HOUND-2', 'OK')
test_server('EXIT HOUND-2', 'ERR')

