'''
A text adventure game where a player can move between Rooms and pick up
and use items.

Classes:
--------

InventoryItem: an item that can be pickup and used in a game.

InventoryItemHolder: encapsualtes functionality for managing and searching
inventory

Room: A location within the game that has a description and exits to other
Rooms

TextWorld: The main game class.  A player can take actions within a game

'''

from .constants import (
    CLASSIC_USE_ALIASES,
    DEFAULT_VERBS,
    DEFAULT_LEGAL_MOVES,
    WARFARE_USE_ALIASES)

from .commands import (
    NullCommand,
    QuitGame,
    ExamineInventoryItem,
    LookAtRoom,
    MoveRoom,
    TransferInventory,
    UseInventoryItem,
    ViewPlayerInventory)

COMMAND_ERROR = "You cannot do that."


class InventoryItem:
    '''
    An item found in a text adventure world that can be picked up
    or dropped.
    '''
    def __init__(self, short_description, fixed=False, background=False):
        '''
        Construct an InventoryItem

        Params:
        ------
        short_description: str
            Displayed when looking at a Room

        fixed: bool, optional (default=False)
            Can the item be picked up or is it fixed in place in the room?

        background: bool, optional (default=False)
            Is this a background item that is hidden from the
            "you can also see" section in the game?
        '''
        self.name = short_description
        self.long_description = ''
        self.fixed = fixed
        self.background = background
        self.aliases = []
        self.actions = []

    def add_alias(self, new_alias):
        '''
        Add an alias (alternative name) to the InventoryItem.
        For example if an inventory item has the short description
        'credit card' then a useful alias is 'card'.

        Parameters:
        -----------
        new_alias: str
            The alias to add.  For example, 'card'

        '''
        self.aliases.append(new_alias)

    def add_action(self, action):
        '''
        Add an action (a sequence of commands) to be executed given a specific
        player interaction with this item.  Potentially affected by location
        or state of game.

        Params:
        -------
        action: InventoryItemAction
        '''
        self.actions.append(action)

    def __eq__(self, other):
        """
        Overrides the default implementation
        Source:
        -------
        https://stackoverflow.com/questions/390250/
        elegant-ways-to-support-equivalence-equality-in-python-classes
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class InventoryHolder:
    '''
    Encapsulates the logic for adding and removing an InventoryItem
    This simulates "picking up" and "dropping" items in a TextWorld
    '''
    def __init__(self):
        '''
        Params:
        ------
        capacity: str or int, optional (default='inf')
            specify a capacity for the holder.
            'inf'=infinite
        '''
        # inventory just held in a list interally
        self.inventory = []

    @property
    def inventory_count(self):
        return len(self.inventory)

    def list_inventory(self):
        '''
        Return a string representation of InventoryItems held.
        '''
        msg = ''
        for item in self.inventory:
            if item.background is False:
                msg += f'{item.name}\n'

        return msg

    def add_inventory(self, item):
        '''
        Add an InventoryItem
        '''
        self.inventory.append(item)

    def get_inventory(self, item_name):
        '''
        Returns an InventoryItem from Room.
        Removes the item from the Room's inventory

        Params:
        ------
        item_name: str
            Key identifying item.

        Returns
        -------
        InventoryItem

        Raises:
        ------
        KeyError
            Raised when an InventoryItem without a matching alias.
        '''
        selected_item, selected_index = self.find_inventory(item_name)

        # remove at index and return (potential bug to delete -1 if none found)
        del self.inventory[selected_index]
        return selected_item

    def find_inventory(self, item_name):
        '''
        Find an inventory item and return it and its index
        in the collection.

        This is a bit clumsy.  Needs improving...
        '''
        selected_item = None
        selected_index = -1
        for index, item in zip(range(len(self.inventory)), self.inventory):
            if item_name in item.aliases:
                selected_item = item
                selected_index = index
                break

        return selected_item, selected_index

    def in_inventory(self, to_find):
        '''
        Returns true of false depending if item or list of items are contained
        in the inventory.

        Params:
        ------
        to_find: InventoryItem or List[InventoryItem]

        Returns:
        --------
        bool
        '''
        count = 0
        if isinstance(to_find, list):
            required_count = len(to_find)
        else:
            required_count = 1
            to_find = [to_find]

        for item in to_find:
            if item in self.inventory:
                count += 1

            if required_count == count:
                return True

        return False


class Room(InventoryHolder):
    '''
    Encapsulates a location/room within a TextWorld.

    A `Room` has a number of exits to other `Room` objects

    A `Room` is-a type of `InventoryHolder`
    '''
    def __init__(self, name, first_enter_msg=''):
        self.name = name
        self.description = ""
        self.exits = {}

        # has the room already been visited?
        self.visited = False

        # additional message on first entry
        self.first_enter_msg = first_enter_msg

        super().__init__()

    def __repr__(self):
        '''
        String representation of the class
        '''
        desc = f"Room(name='{self.name}'"
        desc += f", description='{self.description[:20]}'"
        desc += f', n_exits={len(self.exits)}'
        desc += f', n_items={len(self.inventory)})'
        return desc

    def add_exit(self, room, direction):
        '''
        Add an exit to the room

        Params:
        ------
        room: Room
            a Room object to link

        direction: str
            The str command to access the room
        '''
        self.exits[direction] = room

    def remove_exit(self, direction):
        '''
        Remove an exit in the specified direction

        Params:
        ------
        direction: str
        '''
        self.exits.pop(direction, None)

    def exit(self, direction):
        '''
        Exit the room in the specified direction

        Params:
        ------
        direction: str
            A command string representing the direction.
        '''
        if direction in self.exits:
            return self.exits[direction]
        else:
            raise ValueError()

    def describe(self):
        msg = self.description
        if not self.visited :
            msg = self.first_enter_msg + msg
            self.visited = True

        if len(self.inventory) > 0:
            inv_msg = "\n"
            inv_msg += self.list_inventory()
            if inv_msg != "\n":
                msg += '\nYou can also see:\n' + inv_msg

        return msg


class TextWorld(InventoryHolder):
    '''
    A TextWorld encapsulate the logic and Room objects that comprise the game.

    A `TextWorld` is-a type of `InventoryHolder` although it might be wise to
    to seperate out this logic into a `Player` class and set up a World to have
    one or more players.
    '''
    def __init__(self, name, rooms, start_index=0, legal_exits=None,
                 command_verb_mapping=None, use_aliases='classic'):
        '''
        Constructor method for World

        Parameters:
        ----------
        name: str
            Game name

        rooms: list
            A list of rooms in the world.

        start_index: int, optional (default=0)
            The index of the room where the player begins their adventure.

        legal_exits: None or List, optional (default=None)
            List of exits (e.g. directions) that may be presented to a user
            during a game. If None then ['n', 's', 'e', 'w'].

        command_verb_mapping: None or List, optional (default=None)
            List of commands verbs mapped to game recognised verbs.
            Ordering is strict! When None is specified default is
            ['look', 'inventory', 'get', 'drop', 'ex', 'quit']

        use_aliases: None, str or List.
            None = the game is set up with no aliases for 'use'
            'classic' = the game provides a standard set of simple verb aliases
            'warfare' = classic use verbs + war specific ones.

        '''
        super().__init__()
        self.name = name
        self.rooms = rooms
        self.current_room = self.rooms[start_index]

        # if None then get standard list
        if legal_exits is None:
            self.legal_exits = self.get_vanilla_legal_moves()
        else:
            self.legal_exits = legal_exits

        # self.legal_commands = dict that maps str keywords (e.g. 'look')
        # to functions that create command objects
        # if none then get standard mapping dict
        if command_verb_mapping is None:
            self.legal_verbs = self.get_vanilla_command_verb_mapping()
        else:
            # custom word mapping provided
            self.legal_verbs = \
                    self.custom_command_word_mapping(command_verb_mapping)

        # aliaises for the use
        if use_aliases is None:
            self.use_aliases = ['use']
        elif use_aliases == 'classic':
            # classic game
            self.use_aliases = CLASSIC_USE_ALIASES
        elif use_aliases == 'warfare':
            self.use_aliases = WARFARE_USE_ALIASES
        else:
            # completely custom list
            self.use_aliases = use_aliases

        # record how many actions taken in the game.
        self.n_actions = 0

        # true while the game is active.
        self.active = True

        # game over message
        self.game_over_message = 'Game over.'

    def __repr__(self):
        '''
        String representation of the class
        '''
        desc = f"TextWorld(name='{self.name}', "
        desc += f'n_rooms={len(self.rooms)}, '
        desc += f'legal_exits={self.legal_exits},\n'
        desc += f'\tlegal_commands={self.legal_verbs},\n'
        desc += f'\tcurrent_room={self.current_room})'
        return desc

    def add_use_command_alias(self, alias):
        '''
        Add use alias to the existing set.
        '''
        self.use_aliases.append(alias)

    def take_action(self, command):
        '''
        Take an action in the TextWorld.

        Parameters:
        -----------
        command: str
            A command to parse and execute as a game action

        Returns:
        --------
        str: a string message to display to the player.
        '''
        # no. of actions taken
        self.n_actions += 1

        # handle action to move room
        if command in self.legal_exits:
            cmd = self._create_move_room_command(command)
            return cmd.execute()

        # split user input into list
        parsed_command = command.lower().split()

        # if attempting to use an item.
        if parsed_command[0] in self.use_aliases:
            try:
                cmd = UseInventoryItem(self, item_alias=parsed_command[1],
                                       command_text=parsed_command[0],
                                       parsed_command=parsed_command)
            except IndexError:
                cmd = NullCommand(f"{parsed_command[0]} what?")
            finally:
                return cmd.execute()

        # else lookup the function that will create the command.
        try:
            command_creator = self.legal_verbs[parsed_command[0]]
        except KeyError:
            # handle command error
            return f"I don't know how to {command}"

        cmd = command_creator(parsed_command)
        return cmd.execute()

    def _create_examine_command(self, *args):
        try:
            item_name = args[0][1]
            return ExamineInventoryItem(self, self.current_room, item_name)
        except IndexError:
            return NullCommand("What would you like to examine?")

    def _create_move_room_command(self, *args):
        direction = args[0]
        return MoveRoom(self, direction)

    def _create_transfer_to_player_command(self, *args):
        '''
        Pickup command
        '''
        try:
            item_name = args[0][1]
            return TransferInventory(self.current_room, self, item_name)
        except IndexError:
            return NullCommand("What would you like to pickup?")

    def _create_transfer_to_room_command(self, *args):
        '''
        Drop command
        '''
        try:
            item_name = args[0][1]
            return TransferInventory(self, self.current_room, item_name)
        except IndexError:
            return NullCommand("What would you like to drop?")

    def _create_player_inventory_command(self, *args):
        return ViewPlayerInventory(self)

    def _create_look_at_room_command(self, *args):
        '''
        Refresh display of current room.
        '''
        return LookAtRoom(self.current_room)

    def _create_end_game_command(self, *args):
        return QuitGame(self)

    def get_vanilla_command_verb_mapping(self):
        '''
        Returns a dictionary of vanilla (default) command words
        mapped to functions.
        '''
        return self.custom_command_word_mapping(DEFAULT_VERBS)

    def get_vanilla_legal_moves(self):
        return DEFAULT_LEGAL_MOVES

    def custom_command_word_mapping(self, command_words):
        '''
        Returns a dictionary of user commands mapped to game commands.
        '''
        custom_commands = {}
        command_funcs = [self._create_look_at_room_command,
                        self._create_player_inventory_command,
                        self._create_transfer_to_player_command,
                        self._create_transfer_to_room_command,
                        self._create_examine_command,
                        self._create_end_game_command]

        for user_cmd, mapped_cmd in zip(command_words, command_funcs):
            custom_commands[user_cmd] = mapped_cmd
        return custom_commands