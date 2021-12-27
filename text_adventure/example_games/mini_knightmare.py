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
    AppendToRoomDescription,
    ChangeLocationDescription,
    ClearInventoryItemActions,
    NullAction,
    PlayerDeath,
    QuitGame,
    RemoveInventoryItem,
    RemoveInventoryItemFromPlayerOrRoom,
    SetCurrentRoom
)
from text_adventure.constants import DEFAULT_CMD_WORDS, EAST, GIVE, NORTH, SOUTH, WEST

from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.actions import (
    BasicInventoryItemAction,
    ChoiceInventoryItemAction,
    ConditionalInventoryItemAction,
    RestrictedInventoryItemAction,
    RoomSpecificInventoryItemAction
)

START_INDEX = 0


def load_adventure():
    '''
    Return a mini knightmare text world adventure.

    '''
    ##################### CREATE ROOMS AND LINKS ##############################

    # Let's instantiate some Room objects to represent our network of rooms

    # start fo the game = antechamber within Castle Knightmare
    antechamber = Room(name="Throne room")
    antechamber.description = "You are stood in an antechamber within Castle" \
        + " Knightmare. Candles scattered around the room dull light" \
        + " and a large fireplace beings warmth. Treguard sits in a great" \
        + "chair. In the corner of the room is a portal."

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
        + " of a deep chasm.  On the north side the cavern can be exited via" \
        + " an entrance to a tunnel in the shape of a serpent's head." \
        + " a dark figure stands on the other side of the chasm."

    puzzle4 = Room(name='tunnel')
    puzzle4.description = "You are standing in a long tunnel." \
        + " To the west a door has two crosses engraved above it." \
        + "  To the east is a door with two upside down crosses engaved" \
        + " above it.  Another exit leads South."

    dark_room = Room(name='dark room')
    dark_room.description = "[bold]It is very dark.[/ bold]\n" \
        + "There is a single beam of light penetrating the ceiling" \
        + " and shining in the centre of the chamber.\n"\
        + "You sense an evil presence in this room."

    # links at the start of the game.
    puzzle2.add_exit(puzzle1, SOUTH)
    puzzle3.add_exit(puzzle2, EAST)
    puzzle4.add_exit(puzzle3, SOUTH)

    # store rooms in a list
    rooms_collection = [antechamber, puzzle1, puzzle2, puzzle3, puzzle4,
                        dark_room]

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

    # dungeoneer must wear the helmet
    antechamber.add_inventory(helmet)
    # initially the portal is closed.
    antechamber.add_inventory(closed_portal)
    # treguard
    antechamber.add_inventory(treguard)

    ### Puzzle 1

    # letters on the ground
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

    puzzle1.add_inventory(letters)
    puzzle1.add_inventory(letter_o)
    puzzle1.add_inventory(letter_p)
    puzzle1.add_inventory(letter_e)
    puzzle1.add_inventory(letter_n)

    # Puzzle 2: olgarth of legend
    # 2 riddles
    # 0 correct = death
    # 1 correct = open door
    # 2 correct = open door + spell
    olgarth = InventoryItem("Olgarth", fixed=True, background=True)
    olgarth.long_description = "A creature appears to live within the wall" \
        + " itself and is manifested as a giant face."
    olgarth.add_alias("olgarth")
    olgarth.add_alias("face")
    olgarth.add_alias("creature")
    olgarth.add_alias("carving")

    puzzle2.add_inventory(olgarth)

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

    # Puzzle 3
    lilith = InventoryItem("Lilith", fixed=True, background=True)
    lilith.long_description = "A mysterious figure in a dark hood."
    lilith.add_alias('lilith')
    lilith.add_alias('figure')

    puzzle3.add_inventory(lilith)

    # spell
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
    lamp.long_description = 'The lamp has two crosses engraved on it." \
        + " It might come in useful!'
    lamp.add_alias('light')
    lamp.add_alias('lamp')

    ######################## COMMAND WORDS SETUP ##############################

    # customise the command word set
    knightmare_cmd_mapping = DEFAULT_CMD_WORDS
    # = ['look', 'inv', 'get', 'drop', 'ex', 'quit']

    # create the game room
    adventure = TextWorld(name='mini knightmare', rooms=rooms_collection,
                          start_index=START_INDEX,
                          command_word_mapping=knightmare_cmd_mapping,
                          use_aliases='classic')

    # add additional alisas for the word 'use' - classic knightmare spellcast
    adventure.add_use_command_alias('spellcasting')

    # enter portal
    adventure.add_use_command_alias('enter')

    # touch letters
    adventure.add_use_command_alias('touch')

    # answer riddles or choices
    adventure.add_use_command_alias('answer')

    # ANTECHAMBER ACTIONS ####################################################
    # wear helment (if in inventory)
    # enter portal (if wearing helmet)
    create_antechamber_actions(antechamber, puzzle1, helmet, closed_portal,
                               open_portal, adventure)

    # talk to treguard
    # 'answer' treguard and choose either a lamp or ruby
    create_treguard_actions(antechamber, treguard, treguard2, ruby,
                            lamp, adventure)

    # PUZZLE 1: letters ######################################################
    # Player must 'touch' the letters in the correct order.
    create_puzzle1_actions(puzzle1, puzzle2, letter_o, letter_p, letter_e,
                           letter_n)

    # PUZZLE 2: olgarth of legend ############################################
    # Olgarth asks 2 riddles
    # 0 correct - death
    # 1 correct - open way ahead (puzzle 3)
    # 2 correct - open + bridge spell.
    # 'answer olgarth <answer>'
    create_puzzle2_actions(puzzle2, puzzle3, olgarth, olgarth2a, olgarth2b,
                           spell, adventure)

    # PUZZLE 3: LILITH & THE CHASM ###########################################
    # Lilith and the chasm
    # Cast Bridge spell by-passes lilith
    # Give Lilith ruby - she creates bridge.
    create_puzzle3_actions(puzzle3, puzzle4, lilith, spell, ruby, adventure)

    # GAME OPENING INFO ######################################################

    adventure.opening = "[yellow]Welcome watcher of illusion to the " \
        + " castle of confusion for this is the time of adventure..." \
        + "\n\nI Treguard issue the challenge.  Beyond this portal lies" \
        + " the dungeon of deceit which I alone have mastered. " \
        + " But you who have crossed time must master it also..." \
        + "\n\nEnter stranger... [/yellow]"

    return adventure

def create_antechamber_actions(antechamber, puzzle1, helmet, closed_portal, open_portal, adventure):
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
    wear_message = NullAction("You place the Helmet of Justice on your head.")
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
    failed_entry_msg = NullAction("It is not safe to enter yet.")
    fail_entry = BasicInventoryItemAction(failed_entry_msg,
                                          command_text='enter')
    closed_portal.add_action(fail_entry)

    # ENTER the open portal
    enter_message = NullAction("[red]You step into the bright light of the "
                               + "portal... \n\n[/ red]")
    move_room = SetCurrentRoom(adventure, puzzle1)
    enter_action = BasicInventoryItemAction([enter_message, move_room],
                                            command_text='enter')
    open_portal.add_action(enter_action)

def create_treguard_actions(antechamber, treguard, treguard2, ruby, lamp, adventure):
    '''
    TALK TO TREGUARD and CHOOSE a ruby or lamp
    '''
    TRE_SPEACH = "[italic green]'Welcome stranger...To help you on " \
        + "your quest I can offer you a precious 'ruby' or the 'lamp of the" \
        + "cross'\nAnswer me...which do you choose?'[/ italic green]"
    TRE2_SPEACH = "[italic green]'The dungeon awaits you.'[/ italic green]"
    TRE_UNIMPRESSED = 'Treguard looks unimpressed with your choice.'
    CHOOSE_RUBY = "Treguard hands you a ruby." \
        + "[italic green]\n'A rare and precious gem." \
        + "Let us hope its value is of value in the dungeon'" \
        + "[/ italic green]"
    CHOOSE_LAMP = "Treguard hands you a lamp." \
        + "[italic green]\n'The dungeon is a dark place" \
        + "Let this lamp light your path in your darkest hour.'" \
        + "[/ italic green]"

    talk_tre = BasicInventoryItemAction(NullAction(TRE_SPEACH),
                                        command_text="talk")
    treguard.add_action(talk_tre)

    # answer treguard lamp or answer tregaurd ruby
    add_ruby = AddInventoryItemtoHolder(ruby, adventure)
    tre_talk2 = NullAction(CHOOSE_RUBY)
    remove_tre = RemoveInventoryItem(antechamber, treguard)
    add_tre2 = AddInventoryItemtoHolder(treguard2, antechamber)
    cmds1 = [add_ruby, tre_talk2, remove_tre, add_tre2]
    ruby_action = BasicInventoryItemAction(cmds1, command_text='answer')

    add_lamp = AddInventoryItemtoHolder(lamp, adventure)
    tre_talk2 = NullAction(CHOOSE_LAMP)
    cmds2 = [add_lamp, tre_talk2, remove_tre, add_tre2]
    lamp_action = BasicInventoryItemAction(cmds2, command_text='answer')

    action_choices = {'ruby': ruby_action,
                      'lamp': lamp_action}

    tre_choice = ChoiceInventoryItemAction(action_choices, 'answer',
                                           TRE_UNIMPRESSED)

    treguard.add_action(tre_choice)

    talk_tre2 = BasicInventoryItemAction(NullAction(TRE2_SPEACH), 'talk')
    treguard2.add_action(talk_tre2)

def create_puzzle2_actions(puzzle2, puzzle3, olgarth, olgarth2a, olgarth2b, spell, adventure):
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

    OLGARTH_INTRO = "[italic green] 'I am Olgarth of legend. " \
        + " I have riddles of different times of different legends." \
        + " Two riddles I have and seek answers. Answer one correctly" \
        + " and the way ahead is opened.  Answer two correctly and" \
        + "help I shall provide.  Fail both and I feed upon you.'" \
        + "[/italic green]"

    ################### OLGARTH: RIDDLE 2 #####################################
    # response to talk olgarth
    riddle_text = NullAction(RIDDLE_2)
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
    response_txt = NullAction(CORRECT_ANSWER)
    spell_output = NullAction(SPELL_MSG)
    correct_action = BasicInventoryItemAction([remove_o2, add_spell,
                                               response_txt,
                                               spell_output,
                                               link_puz3, extra_desc],
                                              'answer')

    # 2a INCORRECT answer.
    # remove olgarth, show text, link p3, add link as txt
    incorrect_txt = NullAction(ONE_INCORRECT_ANSWER)
    incorrect_action = \
        BasicInventoryItemAction([incorrect_txt, link_puz3, extra_desc],
                                 'answer')
    olgarth_qa = ConditionalInventoryItemAction(ANSWER_2,
                                                correct_action,
                                                incorrect_action,
                                                command_text='answer')
    olgarth2a.add_action(olgarth_qa)

    ################### OLGARTH ACTIONS - AFTER 1 INCORRECT ANSWER ####################
    # olgarth2b

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

    ####################### OLGARTH RIDDLE 1 ACTIONS ###############################
    olgarth_response = NullAction(OLGARTH_INTRO + RIDDLE_1)
    talk_olgarth = BasicInventoryItemAction(olgarth_response,
                                            command_text='talk')
    olgarth.add_action(talk_olgarth)

    remove_o1 = RemoveInventoryItem(puzzle2, olgarth)
    add_o2a = AddInventoryItemtoHolder([olgarth2a], puzzle2)
    output = NullAction(CORRECT_ANSWER)
    correct_action = BasicInventoryItemAction([remove_o1, add_o2a, output],
                                              'answer')

    add_o2b = AddInventoryItemtoHolder([olgarth2b], puzzle2)
    output = NullAction(ONE_INCORRECT_ANSWER)
    incorrect_action = \
        BasicInventoryItemAction([remove_o1, add_o2b, output], 'answer')
    olgarth_qa = ConditionalInventoryItemAction(ANSWER_1,
                                                correct_action,
                                                incorrect_action,
                                                command_text='answer')
    olgarth.add_action(olgarth_qa)

def create_puzzle1_actions(puzzle1, puzzle2, letter_o, letter_p, letter_e, letter_n):
    ############ PUZZLE 1: touch letters in correct order ##################Ç
    # manage response when letters touched out of order

    wrong_order = BasicInventoryItemAction(NullAction("Nothing happens."),
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
    LIL_SPEAK = "[italic yellow] 'No master, but a mistress rules here. " \
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
    # talk to lilith
    talk_lil = BasicInventoryItemAction(NullAction(LIL_SPEAK),
                                        command_text="talk")
    lilith.add_action(talk_lil)

    # SPELLCASTING
    spellcast_cmd = NullAction(SPELLCAST)
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


    # Give ruby to lilith
    remove_ruby = RemoveInventoryItem(adventure, ruby)
    lil_give_txt = NullAction(LIL_ACCEPT)
    cmds = [remove_ruby, remove_lil, lil_give_txt, add_tunnel, new_desc]
    reqs = [ruby]
    ruby_action = RestrictedInventoryItemAction(adventure, cmds, reqs,
                                                NO_RUBY,
                                                command_txt=GIVE)
    ruby_p3_action = RoomSpecificInventoryItemAction(adventure, puzzle3,
                                                     ruby_action,
                                                     command_text=GIVE)
    ruby.add_action(ruby_p3_action)
