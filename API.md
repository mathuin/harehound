# Overview
The network API for this app is a contract between the client (the mobile app used to play the game) and the server (a simple network server which accepts TCP connections from clients and exchanges information).

# Known Limitations
Only one game can be played at a time
The game is limited to three players: two hounds and one hare
There is no security!

# API
## Server Status
Clients can contact the server without changing the server's state by sending the word 'PING'.  The server must respond with 'PONG'.
Clients can reset the server state, cancelling any game in progress, by sending the word 'RESET'.  The server must respond with 'OK'.
Note: this is extremely insecure.

## Client Registration
Clients register by sending the word 'NEW' followed by the word 'HARE' or 'HOUND', depending on their roles.  The server must respond to a hare request with one of the following:
* 'OK HARE' if no hare currently exists.
* 'ERR' if a hare has already been accepted.
The server must respond to a hound request with one of the following
* 'OK HOUND-#' with an integer identifying the client.
* 'ERR' if the hound limit has been reached.

Note: No more than one hare can register in any given game.
Note: The game currently begins when one hare and two hounds are registered.

### Examples
Direction | Text
---------------|---------
Client->Server | NEW HARE
Server->Client | OK HARE

Direction | Text
---------------|----------
Client->Server | NEW HOUND
Server->Client | OK HOUND-1

## Client Updates
Clients will send their positions by sending the word 'POS' followed by their tag and their position in decimal degrees during every update.  If positions are unavailable, clients will send 'INVALID POSITION' instead of their position.  The server must respond with one of the following:
* 'OK' if the position is accepted but there is no additional information to send.
* 'POS' followed by one or more lat-long pairs (hounds receive one for the hare, hares receive all hounds)
* 'ERR' if there is a problem with the input.
* 'WIN' followed by the winner ('HARE' or 'HOUND-#') and their location, in the case of a win (see below).

### Examples
Direction | Text
---------------|--------------------------------
Client->Server | POS HOUND-1 44.56714 -123.27902
Server->Client | POS 44.4444 -123.21234

Direction | Text
---------------|--------------------------------
Client->Server | POS HARE 44.56714 -123.27902
Server->Client | POS 43.45432 -123.28932 44.45678 -123.45678

Direction | Text
---------------|--------------------------------
Client->Server | POS HARE 44.56714 -123.27902
Server->Client | WIN HOUND-1 44.56710 -123.27905

## Client Exit
Clients can exit from the game by sending 'EXIT' followed by their tag.  The server will delete the data pertaining to that client.  The server must respond with one of the following:
* 'OK' if the tag exists.
* 'ERR' if the tag does not exist.

# Game End
The game ends when either the hare is caught by a hound or the hare escapes capture for the duration of the game.  At this time, the 'WIN' message will be sent by the server in response to any client updates.

