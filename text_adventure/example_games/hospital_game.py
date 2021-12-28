'''
An example text adventure.

Set in a hospital
'''

from text_adventure.commands import (
    AppendToCurrentRoomDescription,
    NullAction, 
    RemoveInventoryItem,
    RemoveInventoryItemFromPlayerOrRoom
)
from text_adventure.constants import DEFAULT_VERBS

from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.actions import (
    BasicInventoryItemAction, 
    RestrictedInventoryItemAction
)

def load_adventure():
    '''
    Return a basic hospital text world adventure.  Players cna move through
    a reception, corridor, ward and theatre and drop and pick up items.
    
    '''

    ##################### CREATE ROOMS AND LINKS ##############################

    # Let's instantiate some Room objects to represent our network of rooms

    # start fo the game = reception
    reception = Room(name="reception")
    reception.description = """You are stood in the busy hospital reception.
    To the south, east and west are wards with COVID19 restricted areas. 
    To the north is a corridor."""

    corridor = Room(name='corridor')
    corridor.description = """A long corridor branching in three directions. 
    To the north is signposted 'WARD'.  
    The south is  signposted 'RECEPTION'.
    The east is signposted 'THEATRE'"""

    ward = Room(name="ward")
    ward.description = """You are on the general medical ward. There are 10 beds
    and all seem to be full today.  There is a smell of disinfectant. 
    The exit is to the south"""

    theatre = Room(name="theatre")
    theatre.description = """You are in the operating theatre. Its empty today as
    all of the elective operations have been cancelled.
    An exit is to the west."""

    # add the exits by calling the add_exit() method  
    reception.add_exit(corridor, 'n')
    corridor.add_exit(reception, 's')
    corridor.add_exit(ward, 'n')
    corridor.add_exit(theatre, 'e')
    ward.add_exit(corridor, 's')
    theatre.add_exit(corridor, 'w')

    # store rooms in a list
    rooms_collection = [reception, corridor, ward, theatre]
    
    #################### CREATE INVENTORY #####################################

    # Create all the inventory to be used in the game.  Not all of it will be
    # added to the game immediately.

    # add inventory items
    clipboard = InventoryItem('a medical clipboard :clipboard:')
    clipboard.long_description = """It a medical clipboard from the 1980s. 
    It doesn't seem very secure to leave this hanging around."""
    clipboard.add_alias('clipboard')
    clipboard.add_alias('clip')
    clipboard.add_alias('board')
    
    grapes = InventoryItem('a bunch of grapes :grapes:')
    grapes.long_description = """A bunch of juicy red grapes. 
    From Lidl according to the sticker """
    grapes.add_alias('grapes')
    grapes.add_alias('bunch')
    
    ward.add_inventory(grapes)
    reception.add_inventory(clipboard)

    
    # customise the command word set
    hospital_cmd_mapping = DEFAULT_VERBS
    # = ['look', 'inv', 'get', 'drop', 'ex', 'quit']
    # modification = we type 'exit' instead of 'quit' to terminate game.
    hospital_cmd_mapping[-1] = 'exit'
    # modification = we type 'take' instead of 'get' to pick up an item
    hospital_cmd_mapping[2] = 'take'

    # create the game room
    adventure = TextWorld(name='text hospital world', rooms=rooms_collection, 
                          start_index=0, 
                          command_word_mapping=hospital_cmd_mapping,
                          use_aliases='classic')

    # add additional alisas for the word 'use'
    adventure.add_use_command_alias('crush')

    ###### 'Using' the grapes #################################################

    # lets create some interactions with the inventory and world via an Action
    # an action is just a sequence of commands attrached to an InventoryItem.
    # An action is activated by a 'use' keyword alias. e.g. 'eat'
    # For the grapes we will force the player to be holding them using a 
    # RestrictedInventoryItemAction
    # we use two commands with the grapes.  
    #    1. Remove the grapes from the players inventory
    #    2. Output a fun message to the player.
    remove_grapes = RemoveInventoryItem(adventure, grapes)
    eat_message = NullAction(":yum: You ate them ALL.")
    grape_cmds = [remove_grapes, eat_message]

    # The player only needs to be holding the grapes, but this require
    action_requirements = grapes

    # a message if the player is in a room with the grapes, but not holding!
    need_to_pick_up = "You aren't holding any grapes."
    eat_grapes = RestrictedInventoryItemAction(adventure, grape_cmds,
                                               action_requirements, 
                                               need_to_pick_up, 
                                               'eat')
    # finally add the action to the grapes InventoryItem.                                            
    grapes.add_action(eat_grapes)

    # you can also 'crush' the grapes. ('crush' use alias added earlier)
    # the action will remove the `grapes` from the inventory holder (room or
    # player) and add a description of some crushed grapes to the current room.
    remove_grapes = RemoveInventoryItemFromPlayerOrRoom(adventure, 
                                                               grapes)
    crushing_text = ':foot:[bold red] SQUELCH[/ bold red]'
    crushed_append_txt = '\nIt looks like someone has stepped on some ' \
        + 'grapes in this room.'
    update_room = AppendToCurrentRoomDescription(adventure, 
                                                        crushed_append_txt,
                                                        crushing_text)   
    action_cmds = [remove_grapes, update_room]                                                  
    crush_grapes = BasicInventoryItemAction(action_cmds, command_text='crush')
    grapes.add_action(crush_grapes)
    

    # set the legal commands for the game
    # directions a player can move and command they can issue.

    adventure.opening = "[yellow]Welcome to your local hospital!" \
            + " Unfortunatly due to the pandemic most of the hospital" \
            + " is under restrictions today. But there are a few" \
            + " areas where it is safe to visit. [/yellow]"
    
    return adventure