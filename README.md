# Hare and Hounds

by Jack Twilley, Jun Xie, and Paul Burris

## What is it?
The application we are writing is a game where one hare is being chased by one or more hounds.  

## What are the goals of the players?
The goal of the hound is to catch the hare while the goal of the hare is to escape capture for the duration of the game.

## What is the connection with Google Maps?  
Throughout the game, the hounds and hare receive position reports of the other players.  The position information for each player is delayed for a short time to provide an additional challenge.  Each hound receives the position of the hare, while the hare receives positions of all the hounds.

## What APIs will be used?
Initially the Location API will be used to gather the positions of the players.  Once that's working, the Google Maps API will be used to plot the positions on the map.

