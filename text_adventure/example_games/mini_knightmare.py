'''
A mini Knightmare text adventure game.
--------------------------------------

Knightmare was a popular TV programme in the early to mid 1990s
shown on ITV in UK.  This game is a text adventure version
of a mini Knightmare quest.  As a text adventure the mechanics
are different from the TV show and it is intended as a fun tribute.

Credits:
-------
The puzzles in this game are partially based on the first episode of
Knightmare.

Rooms in the game:
------------------
* antechamer - the start room where the quest begins
* puzzle1 - where a player must solve an anagram
* puzzle2 - where a player must answer riddles
* puzzle3 - where a player must find a way across a chasm
* puzzle4 - where a player must choose their fate.
'''

from text_adventure.commands import (
    AddActionToInventoryItem,
    AddInventoryItemtoHolder,
    AddLinkToLocation,
    AppendToRoomDescription,
    ChangeLocationDescription,
    ClearInventoryItemActions,
    NullCommand,
    PlayerDeath,
    QuitGame,
    RemoveInventoryItem,
    SetCurrentRoom
)
from text_adventure.constants import (
    DEFAULT_VERBS,
    EAST, GIVE, NORTH,
    QUIT_COMMAND, SOUTH, WEST)

from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.actions import (
    BasicInventoryItemAction,
    ChoiceInventoryItemAction,
    ConditionalInventoryItemAction,
    RestrictedInventoryItemAction,
    RoomSpecificInventoryItemAction
)

# Constants ##################################################################
START_INDEX = 0
GAME_NAME = 'Mini Knightmare'
OPENING_DESC = "[yellow]Welcome watcher of illusion to the " \
    + "castle of confusion for this is the time of adventure..." \
    + "\n\nI Treguard issue the challenge. Beyond this portal lies" \
    + " the Dungeon of Deceit which I alone have mastered. " \
    + " But you who have crossed time must master it also..." \
    + "\n\nEnter stranger... [/yellow]"
SPELLCASTING = 'spellcasting'
ANSWER = 'answer'
ENTER = 'enter'
TOUCH = 'touch'
LIGHT = 'light'


# Procedures to create game logic ############################################
def load_adventure():
    '''
    Return a mini knightmare text world adventure.

    Returns:
    -------
    TextWorld
        The adventure to play.

    '''
    # STEP 1: CREATE ROOMS AND LINKS #########################################

    # Let's instantiate some Room objects to represent our network of rooms

    # start fo the game = antechamber within Castle Knightmare
    antechamber = Room(name="Throne room")
    antechamber.description = "You are stood in an antechamber within Castle" \
        + " Knightmare. Candles scattered around the casts a room dull light" \
        + ", and a large fireplace brings warmth. [green]Treguard[/ green]" \
        + " sits in a great chair. In the corner of the room is a portal."

    puzzle1 = Room(name='puzzle1')
    puzzle1.description = """You are in a brightly lit room. There is a door to
    at the far end barred by a portcullis. There are letters scratched into
    ground. """

    puzzle2 = Room(name='puzzle2')
    puzzle2.description = "You are in room with all stone walls." \
        + " There is an exit to the south. On the north wall is a " \
        + "huge carving of a face."

    puzzle3 = Room(name='chasm')
    puzzle3.description = "You are standing in a large cavern to the south" \
        + " of a deep chasm. On the north side the cavern can be exited via" \
        + " an entrance to a tunnel in the shape of a serpent's head." \
        + " a dark figure stands on the other side of the chasm."

    puzzle4 = Room(name='tunnel')  
    puzzle4.first_enter_msg = "(Treguard's voice whispers in your ears):" \
        + " [italic green]'Caution stranger your time in " \
        + "the dungeon of deceit draws to an end. But danger is still close" \
        + ". Choose your fate. But choose wisely'[/italic green]"
    puzzle4.description = "\n\nYou are standing in a long tunnel." \
        + " To the west a door has two crosses engraved above it." \
        + "  To the east is a door with two upside down crosses engraved" \
        + " above it. Another exit leads South."

    dark_room = Room(name='dark room')
    dark_room.description = "[bold]It is very dark.[/ bold]\n" \
        + "There is a single beam of light penetrating the ceiling" \
        + " and shining in the centre of the chamber. "\
        + "You sense an evil presence in this room."

    light_room = Room(name='light room')
    light_room.description = "[bold]The room is filled with a pure " \
        + "almost blinding white light[/ bold]. In the centre of room "\
        + "the light dims revealing a dark nebulous portal."

    # store rooms in a list
    rooms_collection = [antechamber, puzzle1, puzzle2, puzzle3, puzzle4,
                        dark_room, light_room]

    # link rooms
    puzzle2.add_exit(puzzle1, SOUTH)
    puzzle3.add_exit(puzzle2, EAST)
    puzzle4.add_exit(dark_room, EAST)
    puzzle4.add_exit(light_room, WEST)
    puzzle4.add_exit(light_room, SOUTH)

    # STEP 2. CREATE INVENTORY ###############################################
    # Create all the inventory to be used in the game.  Not all of it will be
    # added to the game immediately.

    # 2.1 Antechamber inventory ##############################################
    helmet, closed_portal, open_portal, treguard, treguard2 = \
        create_antechamber_inventory()

    # dungeoneer must wear the helmet
    antechamber.add_inventory(helmet)
    # initially the portal is closed.
    antechamber.add_inventory(closed_portal)
    antechamber.add_inventory(treguard)

    # 2.2 Puzzle 1 inventory #################################################
    # letters on the ground
    letters, letter_o, letter_p, letter_e, letter_n = \
        create_puzzle1_inventory()

    puzzle1.add_inventory(letters)
    puzzle1.add_inventory(letter_o)
    puzzle1.add_inventory(letter_p)
    puzzle1.add_inventory(letter_e)
    puzzle1.add_inventory(letter_n)

    # 2.2 Puzzle 2 inventory: olgarth of legend ##############################
    olgarth, olgarth2a, olgarth2b = create_puzzle2_inventory()
    puzzle2.add_inventory(olgarth)

    # 2.3 Puzzle 3 inventory: Lilith #########################################
    lilith = create_puzzle_3_inventory()
    puzzle3.add_inventory(lilith)

    # 2.4 Puzzle 4: beam of light and dark portal
    light_beam, dark_portal = create_puzzle_4_inventory()
    dark_room.add_inventory(light_beam)
    light_room.add_inventory(dark_portal)

    # 2.5 MISC Inventory #####################################################
    # spell
    spell, ruby, lamp = create_misc_inventory()

    # STEP 3. SETUP ADVRENTURE OBJECT + COMMANDS #############################
    adventure = setup_adventure(rooms_collection)

    # 3.1 ANTECHAMBER ACTIONS ################################################
    # wear helment (if in inventory)
    # enter portal (if wearing helmet)
    create_antechamber_actions(antechamber, puzzle1, helmet, closed_portal,
                               open_portal, adventure)

    # talk to treguard
    # 'answer' treguard and choose either a lamp or ruby
    create_treguard_actions(antechamber, treguard, treguard2, ruby,
                            lamp, adventure)

    # 3.2 PUZZLE 1: letters ##################################################
    # Player must 'touch' the letters in the correct order.
    create_puzzle1_actions(puzzle1, puzzle2, letter_o, letter_p, letter_e,
                           letter_n)

    # 3.4 PUZZLE 2: olgarth of legend ########################################
    # Olgarth asks 2 riddles
    # 0 correct - death
    # 1 correct - open way ahead (puzzle 3)
    # 2 correct - open + bridge spell.
    # 'answer olgarth <answer>'
    create_puzzle2_actions(puzzle2, puzzle3, olgarth, olgarth2a, olgarth2b,
                           spell, adventure)

    # 3.5 PUZZLE 3: LILITH & THE CHASM #######################################
    # Lilith and the chasm
    # Cast Bridge spell by-passes lilith
    # Give Lilith ruby - she creates bridge.
    create_puzzle3_actions(puzzle3, puzzle4, lilith, spell, ruby, adventure)

    # 3.6 PUZZLE 5: Choose your fate.#########################################
    # If the dungeoneer chooses the dark room they must have the lamp 
    # The other room is the 'light' room and they suvive no matter what.
    create_dark_room_actions(dark_room, light_room, light_beam, lamp, 
                             adventure)
    create_light_room_actions(dark_portal, adventure)
    
    return adventure

def create_light_room_actions(dark_portal, adventure):
    ENTER_PORTAL = 'You step forward into the darkness ...'
    ENDING = '\n\nYou find yourself once again in a warm antechamber of ' \
        + 'Castle Knightmare. Treguard stands before you and as he lifts ' \
        + 'the Helmet of Justice from your head you realise he is smiling.' \
        + "\n\n[italic green]'Well stranger, you have remained true to your "\
        + "quest and survived the Dungeon of Deceit. This in itself is your " \
        + "reward. As for me I have only one remaining task...'" \
        + "\n\n'Spellcasting D.I.M.I.S.S.' [/ italic green]"

    GAME_OVER_MSG = "Well done adventurer. You have completed Knightmare."
    end_cmd = QuitGame(adventure, quit_msg=ENTER_PORTAL + ENDING, 
                       game_over_msg=GAME_OVER_MSG)
    touch_portal_action = BasicInventoryItemAction(end_cmd, ENTER)
    dark_portal.add_action(touch_portal_action)

def create_dark_room_actions(dark_room, light_room, light_beam, lamp, adventure):
    TOUCH_BEAM_MSG = "In the corner of your eye you catch a brief"\
        + " glimpse of a many legs rushing towards you before a great pain "\
        + "fills your chest..."
    TREGUARD_BAD_END = "\n\nAs the final light fades from your eyes you " \
        + "hear Treguard speak for one last time:\n[italic green]'Oooh "\
        + "NASTY. I thought the symbol might provide you a clue. " \
        + "But fear not stranger your time is not"\
        + " yet at an end. You have many centuries of time to ponder your " \
        + "mistakes in your after-life service of Shelob...[/ italic green]"
    LIGHT_LAMP_MSG = "Light from the lamp floods the room and reveals a " \
        + "monsterous spider like creature looming down on you. Centuries old"\
        + " eyes peer down at you revealing the beast's hidden thirst, but"\
        + " the creature cowers away from the light. A solitary exit lies to" \
        + " the north."
    TREGUARD_LAMP = "\n\nTreguard speaks: [italic green]'Caution.. you have "\
        + "entered the domain of Shelob the Enslaver. You were wise to "\
        + "light your lamp. But do not linger adventurer, make your escape "\
        + "quickly' [/italic green]"

    # enter light beam
    player_death = PlayerDeath(TOUCH_BEAM_MSG + TREGUARD_BAD_END,
                               QuitGame(adventure))
    death_action = BasicInventoryItemAction(player_death, command_text=ENTER)                           
    light_beam.add_action(death_action)

    # light lamp
    remove_lamp = RemoveInventoryItem(adventure, lamp)
    room_desc = ChangeLocationDescription(dark_room, LIGHT_LAMP_MSG)
    add_link = AddLinkToLocation(dark_room, light_room, NORTH)
    tre_warning = NullCommand('\n' + LIGHT_LAMP_MSG + TREGUARD_LAMP)
    cmds = [remove_lamp, room_desc, add_link, tre_warning]
    light_action = RestrictedInventoryItemAction(adventure, cmds, [lamp],
                                                 '', LIGHT)
    lamp.add_action(light_action)

def create_puzzle_4_inventory():
    light_beam = InventoryItem('A beam of light', fixed=True, background=True)
    light_beam.long_description = "A singlular thin beam of light penetrates "\
        + " the ceiling of the chamber from an unknown source. The beam "\
        + "illuminates the centre of the room and is just wide enough " \
        + "to step into"
    light_beam.add_alias("light")
    light_beam.add_alias("beam")

    # the dark portal (final item to end the game)
    dark_portal = InventoryItem('dark portal', fixed=True, background=True)
    dark_portal.long_description = "Treguard speaks [italic green]'"\
        + "This portal is the end of your journey adventurer. Don't give up" \
        + " now; take the final step.' [/italic green]"
    dark_portal.add_alias('dark')
    dark_portal.add_alias('portal')

    return light_beam, dark_portal


def create_misc_inventory():
    '''
    Create misc inventory that is used within the game.  These might
    be relevant (or obtained and then used across) multiple puzzles
    '''
    spell = InventoryItem('The bridge spell')
    spell.long_description = "Cast me if you wish to avoid the depths"
    spell.add_alias("bridge")

    # ruby
    ruby = InventoryItem('ruby')
    ruby.long_description = "A beautiful and valuable ruby. " \
        + "It might come in useful!"
    ruby.add_alias('ruby')

    # lamp
    lamp = InventoryItem('lamp')
    lamp.long_description = "The lamp has two crosses engraved on it." \
        + " It might come in useful!"
    lamp.add_alias('lamp')

    return spell, ruby, lamp


def create_antechamber_inventory():
    '''
    The antechamber is the beginning of the game and is where
    Treguard resides.

    Returns:
    -------
    tuple: (helmet, closed_portal, open_portal, treguard, treguard2)
    '''
    helmet = InventoryItem('The Helmet of Justice')
    helmet.long_description = """The fabled helmet of justice!
    The helmet protects a dungeoneer just like a standard helmet, but also
    protects them from Dungeon of Deciet's potent illusions."""
    helmet.add_alias('helmet')
    helmet.add_alias('justice')

    # portal - this is fixed to the inventory of the room. (can't be picked up)
    closed_portal = InventoryItem('portal', fixed=True, background=True)
    closed_portal.long_description = """The portal to the Dungeon of Deceit.
    It has a dull glow. Enter at your own risk!"""
    closed_portal.add_alias('portal')

    open_portal = InventoryItem('portal', fixed=True, background=True)
    open_portal.long_description = """The portal to the Dungeon of Deceit.
    It is glowing brightly. Enter at your own risk!"""
    open_portal.add_alias('portal')

    # treguard offers the player a ruby or lantern
    treguard = InventoryItem('treguard', fixed=True, background=True)
    treguard.long_description = "Treguard of Dunshelm, the dungeon master." \
        + "He stars unflinchingly at you.  His eyes feel like they pierce" \
        + " your very soul."
    treguard.add_alias("treguard")
    treguard.add_alias("tre")

    # treguard after choosing the item.
    treguard2 = InventoryItem('treguard', fixed=True, background=True)
    treguard2.long_description = "Treguard of Dunshelm, the dungeon master." \
        + "He stars unflinchingly at you.  His eyes feel like they pierce" \
        + " your very soul."
    treguard2.add_alias("treguard")
    treguard.add_alias("tre")

    return helmet, closed_portal, open_portal, treguard, treguard2


def create_puzzle1_inventory():
    '''
    Puzzle 1 is a simple anagrame. Players need to spell open by touching
    the letters in the correct order.  There is also a general letters item
    that describes the scene.

    Returns:
    -------
    tuple: (letters, letter_o, letter_p, letter_e, letter_n)
    '''
    letters = InventoryItem('letters', fixed=True, background=True)
    letters.long_description = "The letters N, P, E, and O are engraved in" \
        + " ground."
    letters.add_alias('letters')
    letters.add_alias('letter')
    letters.add_alias('ground')

    HIDE_LETTERS = True
    letter_o = InventoryItem('the letter o', fixed=True,
                             background=HIDE_LETTERS)
    letter_o.long_description = "The letter O as used in Oscar."
    letter_o.add_alias('the letter o')
    letter_o.add_alias('o')
    letter_o.add_alias('O')

    letter_p = InventoryItem('the letter p', fixed=True,
                             background=HIDE_LETTERS)
    letter_p.long_description = "The letter P as used in Papa."
    letter_p.add_alias('p')
    letter_p.add_alias('P')
    letter_p.add_alias('the letter p')

    letter_e = InventoryItem('the letter e', fixed=True,
                             background=HIDE_LETTERS)
    letter_e.long_description = "The letter E as used in Echo"
    letter_e.add_alias('e')
    letter_e.add_alias('E')
    letter_e.add_alias('the letter e')

    letter_n = InventoryItem('the letter n', fixed=True,
                             background=HIDE_LETTERS)
    letter_n.long_description = "The letter N as used in November"
    letter_n.add_alias('n')
    letter_n.add_alias('N')
    letter_n.add_alias('the letter n')

    return letters, letter_o, letter_p, letter_e, letter_n


def create_puzzle2_inventory():
    '''
    Puzzle 2 inventory.
    Olgarth of legends.

    There are three olgarth objects.  olgarth is replaced either by
    olgarth2a (correct answer) or olgarth2b (incorrect answer)

    Returns:
    -------
    Tuple (olgarth, olgarth2a, olgarth2b)
    '''
    olgarth = InventoryItem("Olgarth", fixed=True, background=True)
    olgarth.long_description = "A creature appears to live within the wall" \
        + " itself and is manifested as a giant face."
    olgarth.add_alias("olgarth")
    olgarth.add_alias("face")
    olgarth.add_alias("creature")
    olgarth.add_alias("carving")

    # olgarth for second riddle... first answer correct.
    olgarth2a = InventoryItem("Olgarth", fixed=True, background=True)
    olgarth2a.long_description = "A creature appears to live within the wall" \
        + " itself and is manifested as a giant face."
    olgarth2a.add_alias("olgarth")
    olgarth2a.add_alias("face")
    olgarth2a.add_alias("creature")
    olgarth2a.add_alias("carving")

    # olgarth for second riddle... first answer correct incorrect.
    olgarth2b = InventoryItem("Olgarth", fixed=True, background=True)
    olgarth2b.long_description = "A creature appears to live within the wall" \
        + " itself and is manifested as a giant face."
    olgarth2b.add_alias("olgarth")
    olgarth2b.add_alias("face")
    olgarth2b.add_alias("creature")
    olgarth2b.add_alias("carving")
    return olgarth, olgarth2a, olgarth2b


def create_puzzle_3_inventory():
    '''
    Puzzle 3 inventory. Lilith.

    Returns:
    -------
    InventoryItem (lilith)
    '''
    lilith = InventoryItem("Lilith", fixed=True, background=True)
    lilith.long_description = "A mysterious figure in a dark hood."
    lilith.add_alias('lilith')
    lilith.add_alias('figure')
    return lilith


def setup_adventure(rooms_collection):
    '''
    create adventure object and setup command interface.
    '''
    # customise the command verb set
    knightmare_verb_mapping = DEFAULT_VERBS
    # = ['look', 'inv', 'get', 'drop', 'ex', 'quit']

    # create the game room
    adventure = TextWorld(name=GAME_NAME, rooms=rooms_collection,
                          start_index=START_INDEX,
                          command_verb_mapping=knightmare_verb_mapping,
                          use_aliases='classic')

    # custom game over message
    adventure.game_over_message = 'Your adventure ends here stranger.'

    # add additional alisas for the word 'use' - classic knightmare spellcast
    adventure.add_use_command_alias(SPELLCASTING)

    # enter portal
    adventure.add_use_command_alias(ENTER)

    # touch letters
    adventure.add_use_command_alias(TOUCH)

    # answer riddles or choices
    adventure.add_use_command_alias(ANSWER)

    # light lamp
    adventure.add_use_command_alias(LIGHT)

    # Adventure opening line.
    adventure.opening = OPENING_DESC
    return adventure


def create_antechamber_actions(antechamber, puzzle1, helmet, closed_portal,
                               open_portal, adventure):
    '''
    Antechamber actions

    The dungeoneer must posess the helmet and wear it.  This activates
    portal to the Dungeon of Deciet.

    Wear helmet
    1. Remove the helmet from the players inventory
    2. Output a fun message to the player.
    3. Replace the closed_portal object with open_portal.

    The open portal can be entered. This moves the player to puzzle 1.
    '''
    # WEAR THE HELMET ########################################################
    remove_helmet = RemoveInventoryItem(adventure, helmet)
    wear_message = NullCommand("You place the Helmet of Justice on your head.")
    remove_closed_portal = RemoveInventoryItem(antechamber, closed_portal)
    add_open_portal = AddInventoryItemtoHolder([open_portal], antechamber)
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
    failed_entry_msg = NullCommand("It is not safe to enter yet.")
    fail_entry = BasicInventoryItemAction(failed_entry_msg,
                                          command_text='enter')
    closed_portal.add_action(fail_entry)

    # ENTER the open portal
    enter_message = NullCommand("[red]You step into the bright light of the "
                                + "portal...\n\n[/ red]")
    move_room = SetCurrentRoom(adventure, puzzle1)
    enter_action = BasicInventoryItemAction([enter_message, move_room],
                                            command_text='enter')
    open_portal.add_action(enter_action)


def create_treguard_actions(antechamber, treguard, treguard2, ruby, lamp,
                            adventure):
    '''
    TALK TO TREGUARD and CHOOSE a ruby or lamp
    '''
    TRE_SPEACH = "[italic green]'Welcome stranger...To help you on " \
        + "your quest I can offer you a precious 'ruby' or the 'lamp of the" \
        + " cross' \nAnswer me...which do you choose?'[/ italic green]"
    TRE2_SPEACH = "[italic green]'The dungeon awaits you.'[/ italic green]"
    TRE_UNIMPRESSED = 'Treguard looks unimpressed with your choice.'
    CHOOSE_RUBY = "Treguard hands you a ruby." \
        + "[italic green]\n'A rare and precious gem." \
        + " Let us hope its value is of value in the dungeon'" \
        + "[/ italic green]"
    CHOOSE_LAMP = "Treguard hands you a lamp." \
        + "[italic green]\n'The dungeon is a dark place" \
        + " Let this lamp light your path in your darkest hour.'" \
        + "[/ italic green]"

    talk_tre = BasicInventoryItemAction(NullCommand(TRE_SPEACH),
                                        command_text="talk")
    treguard.add_action(talk_tre)

    # answer treguard lamp or answer tregaurd ruby
    add_ruby = AddInventoryItemtoHolder(ruby, adventure)
    tre_talk2 = NullCommand(CHOOSE_RUBY)
    remove_tre = RemoveInventoryItem(antechamber, treguard)
    add_tre2 = AddInventoryItemtoHolder(treguard2, antechamber)
    cmds1 = [add_ruby, tre_talk2, remove_tre, add_tre2]
    ruby_action = BasicInventoryItemAction(cmds1, command_text='answer')

    add_lamp = AddInventoryItemtoHolder(lamp, adventure)
    tre_talk2 = NullCommand(CHOOSE_LAMP)
    cmds2 = [add_lamp, tre_talk2, remove_tre, add_tre2]
    lamp_action = BasicInventoryItemAction(cmds2, command_text='answer')

    action_choices = {'ruby': ruby_action,
                      'lamp': lamp_action}

    tre_choice = ChoiceInventoryItemAction(action_choices, 'answer',
                                           TRE_UNIMPRESSED)

    treguard.add_action(tre_choice)

    talk_tre2 = BasicInventoryItemAction(NullCommand(TRE2_SPEACH), 'talk')
    treguard2.add_action(talk_tre2)


def create_puzzle2_actions(puzzle2, puzzle3, olgarth, olgarth2a, olgarth2b,
                           spell, adventure):
    '''
    Answer Olgarth of legends riddles.
    '''
    CORRECT_ANSWER = "[bold italic red]'Truth accepted'[/ bold italic red]"
    ONE_INCORRECT_ANSWER = 'You do not speak the truth.'
    DEATH_MSG = "[bold red]'I FEED UPON YOU.'[/ bold red]" \
        + "\nAs the world fades to black Treguard speaks:"\
        + "\n[italic green]'Oohh nasty! Your soul has been consumed" \
        + " by Olgarth. Your bones will remain" \
        + " in the dungeon of deciet for all eternity.'"
    SPELL_MSG = "[italic green] I grant you the spell " \
        + "BRIDGE. [/ italic green]"
    ANSWER_1 = 'stone'
    ANSWER_2 = 'arthur'

    RIDDLE_1 = "\nRiddle: 1 [italic yellow]'Of earth I was born. Deep fires" \
        + " tempered me. Mountains slept on me. My father was younger" \
        + " than I and a sculptor gave me my face. " \
        + " What am I made of?'[/ italic yellow]"

    RIDDLE_2 = "\nRiddle 2: [italic yellow]'Once by magic I was cleft." \
        + " Deep in my chest a sword was left. 10 years of pain" \
        + " I endured. then came a prince who pulled it forth.  " \
        + " Name him now and gain reward.'[/ italic yellow]"

    OLGARTH_INTRO = "[italic green]'I am Olgarth of legend. " \
        + " I have riddles of different times of different legends." \
        + " Two riddles I have and seek answers. Answer one correctly" \
        + " and the way ahead is opened.  Answer two correctly and" \
        + " help I shall provide. Fail both and I feed upon you.'" \
        + "[/italic green]"

    # OLGARTH: RIDDLE 2 ######################################################
    # response to talk olgarth
    riddle_text = NullCommand(RIDDLE_2)
    talk_olgarth2 = BasicInventoryItemAction(riddle_text, command_text='talk')
    olgarth2a.add_action(talk_olgarth2)

    # These command issued no matter what with 2a
    # Link to puzzle 3
    link_puz3 = AddLinkToLocation(puzzle2, puzzle3, WEST)
    # Add the link as descriptive text
    extra_desc = \
        AppendToRoomDescription(puzzle2, " The way forward is to the West.")

    # 2a CORRECRT answer 2
    # action = remove olgarth, give player spell, show text, link p3
    remove_o2 = RemoveInventoryItem(puzzle2, olgarth2a)
    add_spell = AddInventoryItemtoHolder([spell], adventure)
    response_txt = NullCommand(CORRECT_ANSWER)
    spell_output = NullCommand(SPELL_MSG)
    correct_action = BasicInventoryItemAction([remove_o2, add_spell,
                                               response_txt,
                                               spell_output,
                                               link_puz3, extra_desc],
                                              'answer')

    # 2a INCORRECT answer.
    # remove olgarth, show text, link p3, add link as txt
    incorrect_txt = NullCommand(ONE_INCORRECT_ANSWER)
    incorrect_action = \
        BasicInventoryItemAction([incorrect_txt, link_puz3, extra_desc],
                                 'answer')
    olgarth_qa = ConditionalInventoryItemAction(ANSWER_2,
                                                correct_action,
                                                incorrect_action,
                                                command_text='answer')
    olgarth2a.add_action(olgarth_qa)

    # OLGARTH ACTIONS - AFTER 1 INCORRECT ANSWER #############################
    # add riddle - command word 'talk'
    olgarth2b.add_action(talk_olgarth2)

    # correct answer action = remove, output text, link p3, add desc to room.
    correct_action = BasicInventoryItemAction([remove_o2, response_txt,
                                               link_puz3, extra_desc],
                                              'answer')

    # incorrect answer = Death and game over ...
    player_death = PlayerDeath(DEATH_MSG,
                               QuitGame(adventure, quit_msg='Game over'))
    incorrect_action = \
        BasicInventoryItemAction(player_death, 'answer')
    olgarth_qa = ConditionalInventoryItemAction(ANSWER_2,
                                                correct_action,
                                                incorrect_action,
                                                command_text='answer')
    olgarth2b.add_action(olgarth_qa)

    # OLGARTH RIDDLE 1 ACTIONS ###############################################
    olgarth_response = NullCommand(OLGARTH_INTRO + RIDDLE_1)
    talk_olgarth = BasicInventoryItemAction(olgarth_response,
                                            command_text='talk')
    olgarth.add_action(talk_olgarth)

    remove_o1 = RemoveInventoryItem(puzzle2, olgarth)
    add_o2a = AddInventoryItemtoHolder([olgarth2a], puzzle2)
    output = NullCommand(CORRECT_ANSWER)
    correct_action = BasicInventoryItemAction([remove_o1, add_o2a, output],
                                              'answer')

    add_o2b = AddInventoryItemtoHolder([olgarth2b], puzzle2)
    output = NullCommand(ONE_INCORRECT_ANSWER)
    incorrect_action = \
        BasicInventoryItemAction([remove_o1, add_o2b, output], 'answer')
    olgarth_qa = ConditionalInventoryItemAction(ANSWER_1,
                                                correct_action,
                                                incorrect_action,
                                                command_text='answer')
    olgarth.add_action(olgarth_qa)


def create_puzzle1_actions(puzzle1, puzzle2, letter_o, letter_p, letter_e,
                           letter_n):
    '''
    PUZZLE 1: touch letters in correct order
    and manage response when letters touched out of order
    '''
    wrong_order = BasicInventoryItemAction(NullCommand("Nothing happens."),
                                           command_text="touch")
    letter_p.add_action(wrong_order)
    letter_e.add_action(wrong_order)
    letter_n.add_action(wrong_order)

    # 'touch o'.  This will add an action to 'p' and so on.  'n' opens
    # the portculia and adds a exit.
    # Tip - create the final action first and work backwards when coding...

    execute_msg = 'The letter [yellow]glows[/ yellow] briefly and disappears.'

    remove_n = RemoveInventoryItem(puzzle1, letter_n)
    open_message = 'The portcullis O.P.E.Ns!'
    p1_solved = """You are in a brightly lit room. There is an open door to
    to the north."""
    new_description = ChangeLocationDescription(puzzle1, p1_solved,
                                                open_message)
    open_portcullis = AddLinkToLocation(puzzle1, puzzle2, NORTH)
    letter_n_action = BasicInventoryItemAction([remove_n, new_description,
                                                open_portcullis],
                                               command_text='touch')

    clear_n = ClearInventoryItemActions(letter_n)
    remove_e = RemoveInventoryItem(puzzle1, letter_e)
    add_n_action = AddActionToInventoryItem(letter_n_action, letter_n,
                                            execute_msg)
    letter_e_action = BasicInventoryItemAction([clear_n, remove_e,
                                                add_n_action],
                                               command_text='touch')

    clear_e = ClearInventoryItemActions(letter_e)
    remove_p = RemoveInventoryItem(puzzle1, letter_p)
    add_e_action = AddActionToInventoryItem(letter_e_action, letter_e,
                                            execute_msg)
    letter_p_action = BasicInventoryItemAction([clear_e, remove_p,
                                                add_e_action],
                                               command_text='touch')

    clear_p = ClearInventoryItemActions(letter_p)
    remove_o = RemoveInventoryItem(puzzle1, letter_o)
    add_p_action = AddActionToInventoryItem(letter_p_action, letter_p,
                                            execute_msg)
    letter_o_action = BasicInventoryItemAction([clear_p, remove_o,
                                                add_p_action],
                                               command_text='touch')

    # only the first letter has its action added on load...
    letter_o.add_action(letter_o_action)


def create_puzzle3_actions(puzzle3, puzzle4, lilith, spell, ruby, adventure):
    '''
    Puzzle 3: Lilith and the Chasm
    Either use B.R.I.D.G.E spell or give ruby to Lilith to cross the chasm.
    '''
    LIL_SPEAK = "[italic yellow]'No master, but a mistress rules here. " \
        + "I am called Lilith and this is my domain. " \
        + "The only way beyond is through the serpent's mouth." \
        + "You must leave. Kindly use the alternative exit. " \
        + "For some small consideration I might just spare you " \
        + "and allow you to leave through the serpent's mouth. " \
        + "Have you anything that might interest me?'[/ italic yellow] :snake:"

    SPELLCAST = "[italic pink] spellcasting: B.R.I.D.G.E [/ italic pink]"
    BRIDGE_APPEAR = "\nA bridge magically appears across the chasm."
    LIL_ACCEPT = "[italic yellow]'I accept your offering'[/ italic yellow]"\
        + ":snake:"
    LIL_LEAVE = "\n(Lilith fades into nothingness)"
    UPDATE_DESC = "You are standing in a large cavern on the south side" \
        + " of a [bold]bridge[/bold] crossing a deep chasm. On the north" \
        + " side the cavern can be exited via an entrance to a tunnel" \
        + "  in the shape of a serpent's head."
    NO_RUBY = "Its probably best not to offer her something you don't have."
    NO_SPELL = "you don't have a spell"
    # Talk to lilith #########################################################
    talk_lil = BasicInventoryItemAction(NullCommand(LIL_SPEAK),
                                        command_text="talk")
    lilith.add_action(talk_lil)

    # SPELLCASTING ###########################################################
    spellcast_cmd = NullCommand(SPELLCAST)
    remove_spell = RemoveInventoryItem(adventure, spell)
    remove_lil = RemoveInventoryItem(puzzle3, lilith)
    add_tunnel = AddLinkToLocation(puzzle3, puzzle4, 'n')
    new_desc = \
        ChangeLocationDescription(puzzle3, UPDATE_DESC,
                                  BRIDGE_APPEAR + "\n" + LIL_LEAVE)
    cmds = [spellcast_cmd, remove_spell, remove_lil, add_tunnel, new_desc]
    reqs = [spell]
    command_txt = 'spellcasting'
    spell_action = RestrictedInventoryItemAction(adventure, cmds, reqs,
                                                 NO_SPELL,
                                                 command_txt=command_txt)
    spell_p3_action = RoomSpecificInventoryItemAction(adventure, puzzle3,
                                                      spell_action,
                                                      command_text=command_txt)

    spell.add_action(spell_p3_action)

    # Give ruby to lilith ####################################################
    remove_ruby = RemoveInventoryItem(adventure, ruby)
    lil_give_txt = NullCommand(LIL_ACCEPT)
    cmds = [remove_ruby, remove_lil, lil_give_txt, add_tunnel, new_desc]
    reqs = [ruby]
    ruby_action = RestrictedInventoryItemAction(adventure, cmds, reqs,
                                                NO_RUBY,
                                                command_txt=GIVE)
    ruby_p3_action = RoomSpecificInventoryItemAction(adventure, puzzle3,
                                                     ruby_action,
                                                     command_text=GIVE)
    ruby.add_action(ruby_p3_action)
