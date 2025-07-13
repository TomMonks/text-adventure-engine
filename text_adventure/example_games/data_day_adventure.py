# data_day_adventure.py
"""
Data's Day: An Android's Quest
A Star Trek: The Next Generation text adventure game
Based on the episode "Data's Day"
"""

from text_adventure.commands import (
    AddInventoryItemtoHolder, AddLinkToLocation,
    ChangeLocationDescription, RemoveInventoryItem,
    NullCommand, PlayerDeath, QuitGame, SetCurrentRoom,
    ClearInventoryItemActions, AddActionToInventoryItem, 
    AppendToRoomDescription
)
from text_adventure.constants import (
    DEFAULT_VERBS, NORTH, SOUTH, EAST, WEST, 
    GIVE, TOUCH, TALK, QUIT_COMMAND, UP, DOWN
)
from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.actions import (
    BasicInventoryItemAction, ConditionalInventoryItemAction,
    RestrictedInventoryItemAction, RoomSpecificInventoryItemAction
)

# Game Constants
GAME_NAME = "Data's Day: An Android's Quest"
START_INDEX = 0
OPENING_DESC = """Personal's log, Commander Data. Today I have been assigned to assist
Chief O'Brien with his wedding preparations while investigating suspicious
activity involving Ambassador T'Pel. As an android, I find human customs
fascinating yet perplexing. Let the investigation begin."""

# Custom verbs
ANALYZE = 'analyze'
SCAN = 'scan'
DANCE = 'dance'
ACTIVATE = 'activate'
ANSWER = 'answer'

def load_adventure():
    """Load and return the Data's Day adventure."""
    
    # Create rooms
    rooms = create_rooms()
    
    # Create items
    items = create_items()
    
    # Setup world
    adventure = setup_world(rooms)
    
    # Add items to rooms
    setup_room_items(rooms, items)
    
    # Create actions
    setup_actions(rooms, items, adventure)
    
    return adventure

def create_rooms():
    """Create all game rooms."""
    
    # Data's Quarters
    data_quarters = Room("Data's Quarters")
    data_quarters.description = """You are in Data's quarters aboard the USS Enterprise-D.
The room is spartanly furnished with a desk, chair, and several paintings.
Spot the cat is sleeping on the bed. A PADD lies on the desk with today's
schedule. The door leads north to the corridor."""
    
    # Corridor
    corridor = Room("Corridor")
    corridor.description = """A typical Enterprise corridor with the familiar
hum of the warp core. The turbolift is to the north, Data's quarters to the
south, and the Transporter Room lies east."""
    
    # Transporter Room
    transporter = Room("Transporter Room")
    transporter.description = """The main transporter room. The platform
shimmers with residual energy. Chief O'Brien stands at the controls,
looking worried. A tricorder sits on the console. The corridor is west."""
    
    # Turbolift
    turbolift = Room("Turbolift")
    turbolift.description = """You are in the turbolift. The controls allow
you to go to different decks. Available destinations: Ten Forward (east),
Bridge (up), or Corridor (south)."""
    
    # Ten Forward
    ten_forward = Room("Ten Forward")
    ten_forward.description = """Ten Forward, the ship's lounge. Tables and
chairs are arranged for the wedding reception. Keiko sits at a table
looking nervous. A replicator hums in the corner. The turbolift is west."""
    
    # Bridge
    bridge = Room("Bridge")
    bridge.description = """The main bridge of the Enterprise. Captain Picard
sits in the command chair. The viewscreen shows stars at warp. Worf stands
at tactical. The turbolift is down."""
    
    # Holodeck
    holodeck = Room("Holodeck")
    holodeck.description = """Holodeck 3 is currently running a ballroom
dancing program. The room appears as an elegant 18th-century ballroom.
A holographic dance instructor waits patiently. The arch is visible."""
    
    # Security Office
    security = Room("Security Office")
    security.description = """The ship's security office. PADDs with reports
cover the desk. A computer terminal displays recent transporter logs.
The corridor access is south."""
    
    # Setup room connections
    data_quarters.add_exit(corridor, NORTH)
    corridor.add_exit(data_quarters, SOUTH)
    corridor.add_exit(transporter, EAST)
    corridor.add_exit(turbolift, NORTH)
    transporter.add_exit(corridor, WEST)
    turbolift.add_exit(corridor, SOUTH)
    turbolift.add_exit(ten_forward, EAST)
    turbolift.add_exit(bridge, UP)
    ten_forward.add_exit(turbolift, WEST)
    bridge.add_exit(turbolift, DOWN)
    
    return {
        'data_quarters': data_quarters,
        'corridor': corridor,
        'transporter': transporter,
        'turbolift': turbolift,
        'ten_forward': ten_forward,
        'bridge': bridge,
        'holodeck': holodeck,
        'security': security
    }

def create_items():
    """Create all game items."""
    
    # Schedule PADD
    schedule = InventoryItem('schedule', fixed=True)
    schedule.long_description = """Today's schedule:
0800 - Assist Chief O'Brien with wedding preparations
1000 - Investigate Ambassador T'Pel's arrival
1200 - Learn to dance for the wedding
1400 - Wedding ceremony
The schedule seems straightforward, yet I anticipate complications."""
    schedule.add_alias('padd')
    schedule.add_alias('schedule')
    
    # Spot the cat
    spot = InventoryItem('Spot', fixed=True, background=True)
    spot.long_description = """Spot is my pet cat. She is currently sleeping
peacefully on the bed. I have been studying her behavior to better
understand the care of domestic animals."""
    spot.add_alias('cat')
    spot.add_alias('spot')
    
    # Tricorder
    tricorder = InventoryItem('tricorder')
    tricorder.long_description = """A standard Starfleet tricorder. It can
scan for various anomalies and analyze data. The display shows it's
currently set to scan for unusual energy signatures."""
    tricorder.add_alias('tricorder')
    
    # Chief O'Brien
    obrien = InventoryItem("Chief O'Brien", fixed=True, background=True)
    obrien.long_description = """Chief Miles O'Brien, the ship's transporter
chief. He appears anxious about his upcoming wedding and something else
seems to be troubling him."""
    obrien.add_alias('obrien')
    obrien.add_alias('chief')
    obrien.add_alias('miles')
    
    # Keiko
    keiko = InventoryItem('Keiko', fixed=True, background=True)
    keiko.long_description = """Keiko Ishikawa, a botanist and O'Brien's
bride-to-be. She looks nervous about the wedding ceremony."""
    keiko.add_alias('keiko')
    keiko.add_alias('bride')
    
    # Captain Picard
    picard = InventoryItem('Captain Picard', fixed=True, background=True)
    picard.long_description = """Captain Jean-Luc Picard, commanding officer
of the Enterprise. He appears deep in thought about ship's business."""
    picard.add_alias('picard')
    picard.add_alias('captain')
    
    # Worf
    worf = InventoryItem('Worf', fixed=True, background=True)
    worf.long_description = """Lieutenant Worf, the ship's security chief.
He stands alert at his tactical station, monitoring ship's security."""
    worf.add_alias('worf')
    worf.add_alias('lieutenant')
    
    # Dance instructor
    instructor = InventoryItem('dance instructor', fixed=True, background=True)
    instructor.long_description = """A holographic dance instructor dressed
in 18th-century attire. He waits patiently to teach ballroom dancing."""
    instructor.add_alias('instructor')
    instructor.add_alias('teacher')
    
    # Wedding gift
    gift = InventoryItem('wedding gift')
    gift.long_description = """A beautifully wrapped wedding gift for
Chief O'Brien and Keiko. It appears to be a traditional tea set."""
    gift.add_alias('gift')
    gift.add_alias('present')
    
    # Suspicious data
    data_chip = InventoryItem('data chip')
    data_chip.long_description = """A small data chip containing suspicious
transporter patterns. This could be evidence of espionage."""
    data_chip.add_alias('chip')
    data_chip.add_alias('data')
    
    # Replicator
    replicator = InventoryItem('replicator', fixed=True, background=True)
    replicator.long_description = """A food replicator. It can create
various items including wedding gifts if properly programmed."""
    replicator.add_alias('replicator')
    

    # Dance certificate (awarded after learning to dance)
    dance_certificate = InventoryItem('dance skills')
    dance_certificate.long_description = """Your newfound knowledge of ballroom dancing.
Data has successfully learned the Viennese waltz and can now participate
properly in human social ceremonies."""
    dance_certificate.add_alias('skills')
    dance_certificate.add_alias('dancing')
    dance_certificate.add_alias('certificate')

    return {
        'schedule': schedule,
        'spot': spot,
        'tricorder': tricorder,
        'obrien': obrien,
        'keiko': keiko,
        'picard': picard,
        'worf': worf,
        'instructor': instructor,
        'gift': gift,
        'data_chip': data_chip,
        'replicator': replicator,
        'dance_certificate': dance_certificate
    }

def setup_world(rooms):
    """Setup the game world."""
    
    # Create custom verb mapping
    verb_mapping = DEFAULT_VERBS.copy()
    
    # Create the world
    room_list = list(rooms.values())
    adventure = TextWorld(
        name=GAME_NAME,
        rooms=room_list,
        start_index=START_INDEX,
        command_verb_mapping=verb_mapping,
        use_aliases='classic'
    )
    
    # Add custom verbs
    adventure.add_use_command_alias(ANALYZE)
    adventure.add_use_command_alias(SCAN)
    adventure.add_use_command_alias(DANCE)
    adventure.add_use_command_alias(ACTIVATE)
    adventure.add_use_command_alias(TALK)
    adventure.add_use_command_alias(GIVE)
    # answer riddles or choices
    adventure.add_use_command_alias(ANSWER)
    
    # Set opening description
    adventure.opening = OPENING_DESC
    
    return adventure

def setup_room_items(rooms, items):
    """Add items to their starting rooms."""
    
    # Data's Quarters
    rooms['data_quarters'].add_inventory(items['schedule'])
    rooms['data_quarters'].add_inventory(items['spot'])
    
    # Transporter Room
    rooms['transporter'].add_inventory(items['tricorder'])
    rooms['transporter'].add_inventory(items['obrien'])
    
    # Ten Forward
    rooms['ten_forward'].add_inventory(items['keiko'])
    rooms['ten_forward'].add_inventory(items['replicator'])
    
    # Bridge
    rooms['bridge'].add_inventory(items['picard'])
    rooms['bridge'].add_inventory(items['worf'])
    
    # Holodeck
    rooms['holodeck'].add_inventory(items['instructor'])

def setup_actions(rooms, items, adventure):
    """Setup all game actions and puzzles."""
    
    # Puzzle 1: Talk to O'Brien to learn about the problem
    setup_obrien_puzzle(rooms, items, adventure)
    
    # Puzzle 2: Analyze the transporter logs
    setup_transporter_puzzle(rooms, items, adventure)
    
    # Puzzle 3: Get wedding gift from replicator
    setup_replicator_puzzle(rooms, items, adventure)
    
    # Puzzle 4: Learn to dance
    setup_dance_puzzle(rooms, items, adventure)
    
    # Puzzle 5: Expose the spy
    setup_spy_puzzle(rooms, items, adventure)
    
    # Final puzzle: Wedding ceremony
    setup_wedding_puzzle(rooms, items, adventure)

def setup_obrien_puzzle(rooms, items, adventure):
    """Setup the O'Brien conversation puzzle."""
    
    OBRIEN_GREETING = """O'Brien: "Data! Thank goodness you're here. I'm having
problems with the transporter. Ambassador T'Pel's arrival was... unusual.
The energy patterns don't match our records. Could you help me analyze
the logs with your tricorder?\""""
    
    OBRIEN_HELP = """O'Brien: "The transporter patterns are in the main computer.
You'll need to scan them with the tricorder to detect anomalies.\""""
    
    # Talk to O'Brien
    talk_action = BasicInventoryItemAction(
        NullCommand(OBRIEN_GREETING),
        command_text=TALK
    )
    items['obrien'].add_action(talk_action)
    
    # Ask for help
    help_action = ConditionalInventoryItemAction(
        'help',
        BasicInventoryItemAction(NullCommand(OBRIEN_HELP), command_text='answer'),
        BasicInventoryItemAction(NullCommand("O'Brien: \"I'm not sure what you mean.\""), command_text='answer'),
        command_text='answer'
    )
    items['obrien'].add_action(help_action)

def setup_transporter_puzzle(rooms, items, adventure):
    """Setup the transporter analysis puzzle."""
    
    SCAN_SUCCESS = """Tricorder analysis complete. Anomalous pattern detected.
The molecular structure shows signs of Romulan transporter technology.
A data chip materializes with the evidence."""
    
    SCAN_FAILURE = "You need to be in the transporter room to scan the logs."
    
    # Scan tricorder (only works in transporter room)
    scan_cmds = [
        NullCommand(SCAN_SUCCESS),
        AddInventoryItemtoHolder(items['data_chip'], adventure)
    ]
    
    scan_action = RoomSpecificInventoryItemAction(
        adventure,
        rooms['transporter'],
        BasicInventoryItemAction(scan_cmds, command_text=SCAN),
        command_text=SCAN
    )
    items['tricorder'].add_action(scan_action)



def setup_replicator_puzzle(rooms, items, adventure):
    """Setup the replicator puzzle for getting wedding gift."""
    
    REPLICATE_SUCCESS = """The replicator hums to life and produces a beautiful
crystal tea set - the perfect wedding gift for O'Brien and Keiko."""
    
    REPLICATE_FAILURE = "The replicator requires specific programming."
    
    PROMPT_MESSAGE = "Specify what to replicate:"
    
    # Create a 'post-activation' replicator (like treguard2) to update description after use
    replicator_post = InventoryItem('replicator', fixed=True, background=True)
    replicator_post.long_description = """The replicator is cooling down after use."""
    replicator_post.add_alias('replicator')
    
    # Activate action: Prompt the player (mirrors Treguard's talk action)
    activate_cmds = [NullCommand(PROMPT_MESSAGE)]
    activate_action = BasicInventoryItemAction(activate_cmds, command_text=ACTIVATE)
    items['replicator'].add_action(activate_action)
    
    # Conditional action for 'answer' (mirrors Treguard's choice with single expected input)
    success_cmds = [
        NullCommand(REPLICATE_SUCCESS),
        AddInventoryItemtoHolder(items['gift'], adventure),
        RemoveInventoryItem(rooms['ten_forward'], items['replicator']),  # Remove original
        AddInventoryItemtoHolder(replicator_post, rooms['ten_forward'])  # Add updated version
    ]
    success_action = BasicInventoryItemAction(success_cmds, command_text='answer')
    
    failure_action = BasicInventoryItemAction(NullCommand(REPLICATE_FAILURE), command_text='answer')
    
    answer_action = ConditionalInventoryItemAction(
        'gift',  # Expected answer
        success_action,
        failure_action,
        command_text='answer'  # Ties to 'answer' verb
    )
    items['replicator'].add_action(answer_action)



def setup_dance_puzzle(rooms, items, adventure):
    """Setup the dancing lesson puzzle."""
    
    DANCE_LESSON = """The holographic instructor begins the lesson:
"Welcome, Mr. Data. Today we shall learn the Viennese waltz.
Step, step, turn... Very good! You are learning quickly.
Now you are ready for the wedding celebration.\""""
    
    DANCE_COMPLETE = """You have successfully learned to dance! This skill
will be useful at the wedding reception."""
    
    # Talk to instructor
    talk_instructor = BasicInventoryItemAction(
        NullCommand("Instructor: \"Shall we begin your dancing lesson?\""),
        command_text=TALK
    )
    items['instructor'].add_action(talk_instructor)
    
    # Dance lesson - awards the certificate
    dance_action = BasicInventoryItemAction([
        NullCommand(DANCE_LESSON),
        NullCommand(DANCE_COMPLETE),
        # Award the pre-created dance certificate
        AddInventoryItemtoHolder(items['dance_certificate'], adventure),
        AddLinkToLocation(rooms['holodeck'], rooms['bridge'], WEST),
        AppendToRoomDescription(rooms['holodeck'], " The bridge is to the west.")
    ], command_text=DANCE)
    items['instructor'].add_action(dance_action)





def setup_spy_puzzle(rooms, items, adventure):
    """Setup the spy exposure puzzle."""
    
    EXPOSE_SPY = """Data: "Captain, the evidence is conclusive. Ambassador T'Pel
is actually a Romulan spy. The transporter logs show molecular patterns
consistent with Romulan technology."
    
Picard: "Excellent work, Data. We'll handle this diplomatically.
Now, let's focus on the wedding celebration.\""""
    
    # Give evidence to Picard (must have data chip)
    give_evidence = RestrictedInventoryItemAction(
        adventure,
        [
            NullCommand(EXPOSE_SPY),
            RemoveInventoryItem(adventure, items['data_chip']),
            # Use 'east' instead of 'holodeck' as the exit command (your alternative approach)
            AddLinkToLocation(rooms['bridge'], rooms['holodeck'], EAST),
            # Add this line to update the room description
            AppendToRoomDescription(rooms['bridge'], " The way to the Holodeck is now open to the east.")
        ],
        [items['data_chip']],
        "You need evidence to present to the Captain.",
        command_txt=GIVE
    )
    items['picard'].add_action(give_evidence)



def setup_wedding_puzzle(rooms, items, adventure):
    """Setup the final wedding ceremony puzzle."""
    
    WEDDING_SUCCESS = """The wedding ceremony proceeds beautifully. Chief O'Brien
and Keiko exchange vows while you observe the fascinating human ritual of
marriage. Your gift is well-received, and your dancing skills impress
the guests.
    
Mission accomplished, Data. You have successfully:
- Exposed a Romulan spy
- Learned to dance
- Helped with wedding preparations
- Observed human customs
    
A fascinating day indeed."""
    
    WEDDING_FAILURE = """The wedding cannot proceed without proper preparations.
You need both a suitable gift and the social skills to participate properly."""
    
    # Give gift to Keiko (final puzzle) - requires BOTH items
    wedding_action = RestrictedInventoryItemAction(
        adventure,
        [
            NullCommand(WEDDING_SUCCESS),
            QuitGame(adventure, quit_msg="Congratulations! You've completed Data's Day!" \
            "\nDesign: Perplexity Labs\nCoded by Perplexity Labs and TM\nBroken by Grok 4\nFixed by TM and Claude 4.0 Sonnet.")
        ],
        [items['gift'], items['dance_certificate']],  # Reference existing item
        WEDDING_FAILURE,
        command_txt=GIVE
    )
    items['keiko'].add_action(wedding_action)


