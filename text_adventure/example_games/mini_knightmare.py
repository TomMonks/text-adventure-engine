'''
An example text adventure.

A mini Knightmare game...

It is comprised of a start room and three simple puzzles. 

'''

from text_adventure.commands import (
    AddActionToInventoryItem,
    AddInventoryItemtoHolder,
    AddLinkToLocation,
    AppendToCurrentRoomDescription,
    ChangeLocationDescription,
    NullAction, 
    RemoveInventoryItem,
    RemoveInventoryItemFromPlayerOrRoom,
    SetCurrentRoom
)
from text_adventure.constants import DEFAULT_CMD_WORDS, NORTH, READ, SOUTH

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
    throne_room.description = "You are stood in the thrown room of Castle" \
        + " Knightmare. Candles scattered around the room bring light" \
            + " and a large fireplace beings warmth." \
            + " In the corner of the room is a portal."

    puzzle1 = Room(name='puzzle1')
    puzzle1.description = """You are in a brightly lit room. There is a door to
    at the far end barred by a portcullis. There are letters scratched into 
    ground. """

    puzzle2 = Room(name='puzzle2')
    puzzle2.description = "You are in room with all stone walls." \
        + " There is an exit to the south. On the north wall is a " \
            + "huge carving of a face."
    
    # store rooms in a list
    rooms_collection = [throne_room, puzzle1, puzzle2]

    # links at the start of the game.
    puzzle2.add_exit(puzzle1, SOUTH)

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
    closed_portal = InventoryItem('a portal', fixed=True, background=True)
    closed_portal.long_description = """The portal to the Dungeon of Deceit. 
    It has a dull glow. Enter at your own risk!"""
    closed_portal.add_alias('portal')

    open_portal = InventoryItem('a portal', fixed=True, background=True)
    open_portal.long_description = """The portal to the Dungeon of Deceit. 
    It is glowing brightly. Enter at your own risk!"""
    open_portal.add_alias('portal')  

    # dungeoneer must wear the helmet    
    throne_room.add_inventory(helmet)
    # initially the portal is closed. 
    throne_room.add_inventory(closed_portal)


    ### Puzzle 1

    # letters on the ground
    letters = InventoryItem('letters', fixed=True, background=True)
    letters.long_description = "The letters N, P, E, and O are engraved in" \
            + " ground."
    letters.add_alias('letters')
    letters.add_alias('letter')
    letters.add_alias('ground')

    letter_o = InventoryItem('the letter o', fixed=True, background=True)
    letter_o.long_description = "The letter O as used in Oscar."
    letter_o.add_alias('the letter o')
    letter_o.add_alias('o')
    letter_o.add_alias('O')

    letter_p = InventoryItem('the letter p', fixed=True, background=True)
    letter_p.long_description = "The letter P as used in Papa."
    letter_p.add_alias('p')
    letter_p.add_alias('P')
    letter_p.add_alias('the letter p')

    letter_e = InventoryItem('the letter e', fixed=True, background=True)
    letter_e.long_description = "The letter E as used in Echo"
    letter_e.add_alias('e')
    letter_e.add_alias('E')
    letter_e.add_alias('the letter e')

    letter_n = InventoryItem('the letter n', fixed=True, background=True)
    letter_n.long_description = "The letter N as used in November"
    letter_n.add_alias('n')
    letter_n.add_alias('N')
    letter_n.add_alias('the letter n')

    puzzle1.add_inventory(letters)
    puzzle1.add_inventory(letter_o)
    puzzle1.add_inventory(letter_p)
    puzzle1.add_inventory(letter_e)
    puzzle1.add_inventory(letter_n)

    ######################## COMMAND WORDS SETUP ##############################

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

    # touch letters
    adventure.add_use_command_alias('touch')

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
    enter_message = NullAction("[red]You step into the bright light of the " \
            + "portal... \n\n[/ red]")
    move_room = SetCurrentRoom(adventure, puzzle1)
    enter_action = BasicInventoryItemAction([enter_message, move_room], 
                                            command_text='enter')
    open_portal.add_action(enter_action)


    # puzzle one.

    # 'touch o'.  This will add an action to 'p' and so on.  'n' opens
    # the portculia and adds a exit.
    # Tip - create the final action first and work backwards when coding...
    
    execute_msg = 'The letter [yellow]glows[/ yellow] briefly and disappears.'
    
    remove_n = RemoveInventoryItem(puzzle1, letter_n)
    open_message = 'The portcullis O.P.E.Ns!'
    p1_solved = """You are in a brightly lit room. There is an open door to
    to the north."""
    new_description = ChangeLocationDescription(puzzle1, p1_solved, 
                                        action_text=open_message)
    open_portcullis = AddLinkToLocation(puzzle1, puzzle2, NORTH)


    letter_n_action = BasicInventoryItemAction([remove_n, new_description, 
                                                open_portcullis],
                                                command_text='touch')

    remove_e = RemoveInventoryItem(puzzle1, letter_e)
    add_n_action = AddActionToInventoryItem(letter_n_action, letter_n, 
                                            execute_msg)
    letter_e_action = BasicInventoryItemAction([remove_e, add_n_action],
                                               command_text='touch')    

    remove_p = RemoveInventoryItem(puzzle1, letter_p)
    add_e_action = AddActionToInventoryItem(letter_e_action, letter_e, 
                                            execute_msg)
    letter_p_action = BasicInventoryItemAction([remove_p, add_e_action],
                                                command_text='touch')                                      
        
    remove_o = RemoveInventoryItem(puzzle1, letter_o)
    add_p_action = AddActionToInventoryItem(letter_p_action, letter_p, 
                                            execute_msg)
    letter_o_action = BasicInventoryItemAction([remove_o, add_p_action],
                                                command_text='touch')    

    # only the first letter has its action added on load...
    letter_o.add_action(letter_o_action)

    adventure.opening = "[yellow]Welcome watcher of illusion to the " \
            + " castle of confusion for this is the time of adventure..." \
            + "\n\nI Treguard issue the challenge.  Beyond this portal lies" \
            + " the dungeon of deceit which I alone have mastered. " \
            + " But you who have crossed time must master it also..." \
            + "\n\n Enter stranger... [/yellow]"
    
    return adventure