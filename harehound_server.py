#!/usr/bin/env python

"""
Hounds and Hare server, based on:
ilab.cs.byu.edu/python/socket/echoserver.html
"""

import socket
import re
import sys
import math


# from http://www.johndcook.com/python_longitude_latitude.html
erad = 6373000
def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

def hound_distance(hound):
    """Distance between this particular hound and the hare."""
    try:
        (hare_latitude, hare_longitude) = client_pos['HARE']
        (hound_latitude, hound_longitude) = client_pos[hound]
        hound_distance = distance_on_unit_sphere(hound_latitude, hound_longitude, hare_latitude, hare_longitude) * erad
        print " - - distance between hare and hound is %d meters" % hound_distance
    except ValueError:
        hound_distance = erad
    return hound_distance

# Client position is a dict.
# key: client name (i.e., 'HARE', 'HOUND 1')
# value: tuple of floats (i.e., (47.12345, -123.45678))
client_pos = {}
max_hounds = 2
hound_list = ['HOUND-%d' % (x+1) for x in xrange(max_hounds)]
# Winning distance in meters
win_distance = 15
# If winner is set, all valid responses are replaced with a win notification.
winner = ''
host = ''
if sys.argv == 2:
    port = sys.argv[1]
else:
    port = 50000
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, address = s.accept()
    data = client.recv(size)
    data = data.upper()
    if data:
        output = 'ERR'
        print "Client sent: %s" % data.rstrip()
        words = data.split()
        # PING: is the server up?
        if words[0] == 'PING' and len(words) == 1:
            output = 'PONG'
        # RESET: delete all client positions
        if words[0] == 'RESET' and len(words) == 1:
            print "Client requested position reset."
            client_pos = {}
            output = 'OK'
        # NEW: register a new client
        if words[0] == 'NEW' and len(words) == 2:
            print "Client requested new registration."
            if words[1] == 'HARE':
                print " - Client requested to be the hare!"
                if 'HARE' not in client_pos:
                    print " - - No current hare, client is now the hare!"
                    client_pos['HARE'] = ()
                    output = 'OK HARE'
                else:
                    print " - - Hare already assigned, error returned"
            elif words[1] == 'HOUND':
                print " - Client requested to be a hound!"
                # Find first unassigned hound position.
                success = False
                for hound in hound_list:
                    if hound not in client_pos:
                        print " - - Client is now %s!" % hound
                        client_pos[hound] = ()
                        output = 'OK %s' % hound
                        success = True
                        break
                if not success:
                    print " - - No free hound was found!"
        # POS: exchange position information
        if words[0] == 'POS' and len(words) == 4:
            print "Client requested position information exchange."
            key = words[1]
            latitude = words[2]
            longitude = words[3]
            if key in client_pos:
                if latitude == 'INVALID' and longitude == 'POSITION':
                    print " - Client sent invalid position notification!"
                else:
                    print " - Client sent position!"
                    client_pos[key] = (float(latitude), float(longitude))
                    print " - Client position for %s is " % key, client_pos[key]
                if key == 'HARE':
                    output = 'POS '
                    for hound in hound_list:
                        if hound in client_pos and client_pos[hound] != ():
                            (hound_latitude, hound_longitude) = client_pos[hound]
                            output += '%s %s ' % (hound_latitude, hound_longitude)
                            # Check for win condition!
                            if (hound_distance(hound) < win_distance):
                                winner = hound
                                break
                    if output == 'POS ':
                        output = 'OK'
                elif key in hound_list:
                    try:
                        (hare_latitude, hare_longitude) = client_pos['HARE']
                    except ValueError:
                        output = 'OK'
                    finally:
                        if (hound_distance(key) < win_distance):
                            winner = key
                        else:
                            output = 'POS %.5f %.5f' % (hare_latitude, hare_longitude)

        # Check for victory.
        if winner in client_pos:
            (winner_latitude, winner_longitude) = client_pos[winner]
            output = 'WIN %s %.5f %.5f' % (winner, winner_latitude, winner_longitude)
        # Send output
        print "output = '%s'" % output
        client.send(output.rstrip())
    client.close()
