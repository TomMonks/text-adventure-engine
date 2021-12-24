'''
An example text adventure.

A mini Knightmare game...
'''

from text_adventure.commands import (
    AddInventoryItemtoHolder,
    AppendToCurrentRoomDescription,
    NullAction, 
    RemoveInventoryItem,
    RemoveInventoryItemFromPlayerOrRoom,
    SetCurrentRoom
)
from text_adventure.constants import DEFAULT_CMD_WORDS

from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.actions import (
    BasicInventoryItemAction, 
    RestrictedInventoryItemAction
)

def load_adventure():
    '''
    Return a mini knightmare text world adventure.  
    
    '''

    ##################### CREATE ROOMS AND LINKS ##############################

    # Let's instantiate some Room objects to represent our network of rooms

    # start fo the game = reception
    throne_room = Room(name="Throne room")
    throne_room.description = """You are stood in the thrown room of Castle 
    Knightmare.  Candles scattered around the room bring light and a
    a large fireplace beings warmth."""

    puzzle1 = Room(name='puzzle1')
    puzzle1.description = """A long corridor branching in three directions. 
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
    #reception.add_exit(corridor, 'n')
    #corridor.add_exit(reception, 's')
    #corridor.add_exit(ward, 'n')
    #corridor.add_exit(theatre, 'e')
    #ward.add_exit(corridor, 's')
    #theatre.add_exit(corridor, 'w')

    # store rooms in a list
    rooms_collection = [throne_room, puzzle1]
    
    #################### CREATE INVENTORY #####################################

    # Create all the inventory to be used in the game.  Not all of it will be
    # added to the game immediately.

    # add inventory items
    helmet = InventoryItem('The Helmet of Justice')
    helmet.long_description = """The fabled helmet of justice! 
    The helmet protects a dungeoneer just like a standard helmet, but also 
    protects them from Dungeon of Deciet's potent illusions."""
    helmet.add_alias('helmet')
    helmet.add_alias('justice')

    # portal - this is fixed to the inventory of the room. (can't be picked up)
    closed_portal = InventoryItem('a portal', fixed=True)
    closed_portal.long_description = """The portal to the Dungeon of Deceit. 
    It has a dull glow. Enter at your own risk!"""
    closed_portal.add_alias('portal')

    open_portal = InventoryItem('a portal', fixed=True)
    open_portal.long_description = """The portal to the Dungeon of Deceit. 
    It is glowing brightly. Enter at your own risk!"""
    open_portal.add_alias('portal')

    # dungeoneer must wear the helmet    
    throne_room.add_inventory(helmet)
    # initially the portal is closed. 
    throne_room.add_inventory(closed_portal)

    # customise the command word set
    knightmare_cmd_mapping = DEFAULT_CMD_WORDS
    # = ['look', 'inv', 'get', 'drop', 'ex', 'quit']

    # create the game room
    adventure = TextWorld(name='mini knightmare', rooms=rooms_collection, 
                          start_index=0, 
                          command_word_mapping=knightmare_cmd_mapping,
                          use_aliases='classic')

    # add additional alisas for the word 'use' - classic knightmare spellcast
    adventure.add_use_command_alias('spellcasting')

    # enter portal
    adventure.add_use_command_alias('enter')

    # I am Olgarth of legend.  I ahve riddles of different times of different legends.  Three riddles I have and seek answers. 
    # Fail all three and I feed on you... (PlayerDeath)
    # 
    # Of earth I was born deep fires tempered me, mountains slept on me. My farther was younger than I and a sculptor gave me my face.  What am I made of? 
    # A: stone.  "Truth accepted"
    # Made like me the mountains stand. The tallest object in our land.  Give name to him.
    # A: Ben Nevis!
    # Once by magoic I was cleft.  Depp in my chest a sword was left.  10 years of pain I endured. then came a prince who pulled it forth. Name him now and gain reward. 
    # A: Arthor.
    # open the door...


    ## Lilith
    ## No master, but a mistress rules here.  I am called Lillith and this is my domain. The only 
    # way beyond is through the serpents mouth.  You must leave.  Kindly use the alternative exit.
    # For some small consideration I might just spare you and allow you to leave through the serpent's mouth.
    # have you anything that might interest me?

    # summon the courseway.
    ## Spellcasting bridge

    # magic lamp - includes a symbol.  This helps choose the right door...
    # Death if not carrying the

 

    ###### 'wear' the helmet #################################################

    # The dungeoneer must posess the helmet and wear it.  This activates 
    # portal to the Dungeon of Deciet.

    # we use two commands with the grapes.  
    #    1. Remove the helmet from the players inventory
    #    2. Output a fun message to the player.
    #    3. Replace the closed_portal object with open_portal.
    remove_helmet = RemoveInventoryItem(adventure, helmet)
    wear_message = NullAction("You place the Helmet of Justice on your head.")
    remove_closed_portal = RemoveInventoryItem(throne_room, closed_portal)
    add_open_portal = AddInventoryItemtoHolder([open_portal], throne_room)

    wear_cmds = [remove_helmet, wear_message, remove_closed_portal, 
                 add_open_portal]

    # The player only needs to be holding the helmet
    action_requirements = helmet

    # a message if the player is in a room with the grapes, but not holding!
    need_to_pick_up = "You aren't holding a helmet."
    wear_helmet = RestrictedInventoryItemAction(adventure, wear_cmds,
                                               action_requirements, 
                                               need_to_pick_up, 
                                               'wear')
    # finally add the action to the grapes InventoryItem.                                            
    helmet.add_action(wear_helmet)

    # attempt to enter the closed portal
    failed_entry_msg = NullAction("It is not safe to enter yet.")
    fail_entry = BasicInventoryItemAction(failed_entry_msg, 
                                          command_text='enter')
    closed_portal.add_action(fail_entry)


    # ENTER the open portal
    enter_message = NullAction("You step into the bright light of the portal.")
    move_room = SetCurrentRoom(adventure, puzzle1)
    enter_action = BasicInventoryItemAction([enter_message, move_room], 
                                            command_text='enter')
    open_portal.add_action(enter_action)


    # set the legal commands for the game
    # directions a player can move and command they can issue.

    adventure.opening = "[yellow]Welcome watcher of illusion to the " \
            + " castle of confusion for this is the time of adventure..." \
            + "\n\nI Treguard issue the challenge.  Beyond this portal lies" \
            + " the dungeon of deceit which I alone have mastered. " \
            + " But you who have crossed time must master it also..." \
            + "\n\n Enter stranger... [/yellow]"
    
    return adventure