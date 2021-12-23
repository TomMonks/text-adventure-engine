'''
Constants and presets for command words, use aliases and movement commands.

Commands words are:
* 'look' (at room), 
* (list) 'inv'(entory held), 
* 'get' (item)
* 'drop' (item)
* 'ex'(amine) item
* 'quit' game

Notes:
-----
Verbs for using items are specified under use aliases int the TextWorld class.
'''

######################### MOVEMENT ############################################

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'
UP = 'u'
DOWN = 'd'


# List of legal moves.  No mapping is needed here.
DEFAULT_LEGAL_MOVES = [NORTH, SOUTH, EAST, WEST, UP, DOWN]


########################## COMMAND WORDS ######################################
GET_COMMAND = "get";
EXAMINE_COMMAND = "ex";
DROP_COMMAND = "drop";
LOOK_COMMAND = "look";
INVENTORY_COMMAND = "inv";
QUIT_COMMAND = 'quit'

# basic commands for interaction with TextWorld
DEFAULT_CMD_WORDS =  [LOOK_COMMAND, INVENTORY_COMMAND, GET_COMMAND, 
                      DROP_COMMAND, EXAMINE_COMMAND, QUIT_COMMAND]



########################### USE ALIASES #######################################
USE = 'use'
EAT = 'eat'
OPEN = 'open'
CLOSE = 'close'
HIT = 'hit'
BREAK = 'break'
DIG = 'dig'
TALK = 'talk'
THROW = 'throw'
READ = 'read'


SHOOT = 'shoot'
BLAST = 'blast'
FIRE = 'fire'
KILL = 'kill'
PUNCH = 'punch'
EXPLODE = 'explode'


# classic use alias pack
CLASSIC_USE_ALIASES = [USE, 
                       EAT,
                       OPEN,
                       CLOSE,
                       HIT,
                       BREAK,
                       DIG,
                       TALK,
                       THROW,
                       READ]

# warfare pack
WARFARE_USE_ALIASES = CLASSIC_USE_ALIASES \
                        + [SHOOT,
                           BLAST,
                           FIRE,
                           KILL,
                           PUNCH,
                           EXPLODE]




