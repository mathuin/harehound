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
        (hare_latitude, hare_longitude) = player_pos['HARE']
        (hound_latitude, hound_longitude) = player_pos[hound]
        hound_distance = distance_on_unit_sphere(hound_latitude, hound_longitude, hare_latitude, hare_longitude) * erad
        print " - - distance between hare and hound is %d meters" % hound_distance
    except ValueError:
        hound_distance = erad
    return hound_distance

# Player position is a dict.
# key: player name (i.e., 'HARE', 'HOUND 1')
# value: tuple of floats (i.e., (47.12345, -123.45678))
player_pos = {}
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
print 'Starting server now!'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
while 1:
    client, address = s.accept()
    data = client.recv(size)
    data = data.upper()
    if data:
        override_winner = False
        output = 'ERR'
        print "Player sent: %s" % data.rstrip()
        words = data.split()
        # PING: is the server up?
        if words[0] == 'PING' and len(words) == 1:
            output = 'PONG'
        # RESET: delete all player positions
        if words[0] == 'RESET' and len(words) == 1:
            print "Player requested position reset."
            player_pos = {}
            output = 'OK'
        # NEW: register a new player
        if words[0] == 'NEW' and len(words) == 2:
            print "Player requested new registration."
            if words[1] == 'HARE':
                print " - Player requested to be the hare!"
                if 'HARE' not in player_pos:
                    print " - - No current hare, player is now the hare!"
                    player_pos['HARE'] = ()
                    output = 'OK HARE'
                else:
                    print " - - Hare already assigned, error returned"
            elif words[1] == 'HOUND':
                print " - Player requested to be a hound!"
                # Find first unassigned hound position.
                success = False
                for hound in hound_list:
                    if hound not in player_pos:
                        print " - - Player is now %s!" % hound
                        player_pos[hound] = ()
                        output = 'OK %s' % hound
                        success = True
                        break
                if not success:
                    print " - - No free hound was found!"
        # POS: exchange position information
        if words[0] == 'POS' and len(words) == 4:
            print "Player requested position information exchange."
            player = words[1]
            latitude = words[2]
            longitude = words[3]
            if player in player_pos:
                if latitude == 'INVALID' and longitude == 'POSITION':
                    print " - Player sent invalid position notification!"
                else:
                    print " - Player sent position!"
                    player_pos[player] = (float(latitude), float(longitude))
                    print " - Player position for %s is " % player, player_pos[player]
                if player == 'HARE':
                    output = 'POS '
                    for hound in hound_list:
                        if hound in player_pos and player_pos[hound] != ():
                            (hound_latitude, hound_longitude) = player_pos[hound]
                            output += '%s %s ' % (hound_latitude, hound_longitude)
                            # Check for win condition!
                            if (hound_distance(hound) < win_distance):
                                winner = hound
                                break
                    if output == 'POS ':
                        output = 'OK'
                elif player in hound_list:
                    try:
                        (hare_latitude, hare_longitude) = player_pos['HARE']
                    except ValueError:
                        output = 'OK'
                    finally:
                        if (hound_distance(player) < win_distance):
                            winner = player
                        else:
                            output = 'POS %.5f %.5f' % (hare_latitude, hare_longitude)
        # EXIT: player exit from game
        if words[0] == 'EXIT' and len(words) == 2:
            player = words[1]
            override_winner = True
            if player in player_pos:
                del player_pos[player]
                output = 'OK'
        # Check for victory.
        if winner in player_pos and not override_winner:
            (winner_latitude, winner_longitude) = player_pos[winner]
            output = 'WIN %s %.5f %.5f' % (winner, winner_latitude, winner_longitude)
        # Send output
        print "output = '%s'" % output
        client.send(output.rstrip())
    client.close()
