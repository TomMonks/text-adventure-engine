'''
Basic commands

Move
Pick up/drop inventory
Examine inventory
Quit game
View inventory

'''

from abc import ABC, abstractmethod
import os

DEFAULT_MOVE_ERROR = 'You cannot go that way.'
DEFAULT_FAIL_MSG = 'You cannnot do that.'


class Command(ABC):
    '''
    Abstract base class for all commands.  This has a simple interface
    that all commands must implement to work with the parsing game loop.
    '''
    @abstractmethod
    def execute(self) -> str:
        pass


class MoveRoom(Command):
    '''
    Move between two linked Room objects.
    direction must be valid.
    '''
    def __init__(self, game, direction, invalid_msg=DEFAULT_MOVE_ERROR):
        '''
        Params:
        -------
        game: TextWorld
            Current game

        direction: str
            Player specified string representing direction.

        invalid_msg: str, optional (default=DEFAULT_MOVE_ERROR)
            Message displayed if player has specified an incorrect direction.
        '''
        self.game = game
        self.direction = direction
        self.invalid_msg = invalid_msg

    def execute(self) -> str:
        '''
        Execute command to move room.
        '''
        msg = ''
        try:
            self.game.current_room = \
                    self.game.current_room.exit(self.direction)
            # clear terminal or cmd prompt.
            os.system('cls' if os.name == 'nt' else 'clear')
            msg = self.game.current_room.describe()
        except ValueError:
            msg = self.invalid_msg
        finally:
            return msg


class ExamineInventoryItem(Command):
    def __init__(self, game, room, item_name):
        '''
        Parameters:
        -----------
        game: TextWorld
            Current game

        room: Room
            Relevant room object

        item_name: str
            Name of inventory item to examine

        '''
        self.game = game
        self.room = room
        self.description = item_name

    def execute(self) -> str:
        item, _ = self.game.find_inventory(self.description)

        if item is not None:
            return item.long_description

        item, _ = self.room.find_inventory(self.description)

        if item is not None:
            return item.long_description

        return "You can't do that"


class TransferInventory(Command):
    '''
    Transfer an InventoryItem from one InventoryHolder to another.

    Will only succeed if InventoryItem is not fixed to its holder.
    '''
    def __init__(self, holder, reciever, alias):
        self.holder = holder
        self.reciever = reciever
        self.alias = alias

    def execute(self):
        msg = ''
        selected_item, _ = self.holder.find_inventory(self.alias)
        try:
            if selected_item.fixed is False:
                self.reciever.add_inventory(self.holder.get_inventory(self.alias))
                msg = 'Okay.'
            else:
                msg = "You can't do that."
        except AttributeError:
            msg = "You can't do that."
        except KeyError:
            msg = "I'm not sure what you mean."
        return msg


class ViewPlayerInventory(Command):
    '''
    List the inventory items being carried.
    '''
    def __init__(self, player):
        self.player = player

    def execute(self):

        if self.player.inventory_count == 0:
            return "\n[bold red]You are not holding anything." \
                    + "[/bold red] :open_hands:"

        msg = "\n[bold magenta]You are carrying:[/bold magenta] :hand:\n"
        msg += self.player.list_inventory()
        return msg


class LookAtRoom(Command):
    '''
    Description of current room will be displayed.
    '''
    def __init__(self, room):
        self.room = room

    def execute(self):
        # clear terminal or cmd prompt.
        os.system('cls' if os.name == 'nt' else 'clear')
        return self.room.describe()


class QuitGame(Command):
    '''
    Player will quit the game
    '''
    def __init__(self, game):
        self.game = game

    def execute(self):
        self.game.active = False
        return "[bold red]You have quit the game.[/bold red]"


class UseInventoryItem(Command):
    def __init__(self, game, item_name, command_text,
                 fail_message=DEFAULT_FAIL_MSG):
        self.game = game
        self.item_name = item_name
        self.command_text = command_text
        self.fail_message = fail_message

    def execute(self):
        '''
        Search the player and room inventory for item
        try to execute action using given command.
        '''
        msg = ''

        # try players inventory first.
        selected_item, _ = self.game.find_inventory(self.item_name)

        if selected_item is None:
            # try current room
            selected_item, _ = \
                    self.game.current_room.find_inventory(self.item_name)

        try:
            for action in selected_item.actions:
                msg = action.try_to_execute(self.game.current_room,
                                            self.command_text)
        except AttributeError:
            # default if item not in players or room inventory
            msg = self.fail_message

        return msg


class RemoveInventoryItem(Command):
    '''
    Remove an InventoryItem from a InventoryHolder.
    '''
    def __init__(self, holder, to_remove):
        '''
        Constructor

        Params:
        -------
        holder: InventoryItemHolder

        to_remove: InventoryItem
        '''
        self.holder = holder
        self.to_remove = to_remove

    def execute(self):
        _ = self.holder.get_inventory(self.to_remove.name)
        return ""


class RemoveInventoryItemFromPlayerOrRoom(Command):
    '''
    Remove an InventoryItem from the player or the current room.
    '''
    def __init__(self, game, to_remove):
        '''
        Constructor

        Params:
        -------
        game: TextAdventure

        to_remove: InventoryItem
        '''
        self.game = game
        self.to_remove = to_remove

    def execute(self):

        msg = ''
        if self.game.in_inventory(self.to_remove):
             _ = self.game.get_inventory(self.to_remove.name)
        elif self.game.current_room.in_inventory(self.to_remove):
            _ = self.game.current_room.get_inventory(self.to_remove.name)
        else:
            msg = "You can't do that."
        return msg


class NullAction(Command):
    '''
    No command is executed, but a static message is returned.
    '''
    def __init__(self, message):
        self.message = message

    def execute(self):
        return self.message


class AppendToCurrentRoomDescription(Command):
    '''
    Append some text to the long descriptio of the current room
    '''
    def __init__(self, game, to_append, action_text=''):
        '''
        Constructor

        Params:
        ------
        game: TextWorld

        to_append: str
            text to append to game.current_room description

        action_text: str, optional (default='')
            To show user.
        '''
        self.game = game
        self.to_append = to_append
        self.action_text = action_text

    def execute(self) -> str:
        '''
        Append the additonal text.
        '''
        self.game.current_room.description += self.to_append
        return self.action_text

######################## NOT Tested #########################################################

class AppendToRoomDescription(Command):
    '''
    Append some text to a SPECIFIC Room object description.
    '''
    def __init__(self, room, to_append, action_text=''):
        '''
        Constructor

        Params:
        ------
        game: TextWorld

        to_append: str
            text to append to room description

        action_text: str, optional (default='')
            To show user.
        '''
        self.room = room
        self.to_append = to_append
        self.action_text = action_text

    def execute(self) -> str:
        '''
        Append the additonal text.
        '''
        self.room.description += self.to_append
        return self.action_text


class AddLinkToLocation(Command):
    '''
    Add a new exit to the room collection of a context.
    '''
    def __init__(self, context, to_add, direction):
        ''''
        Construtor

        Params:
        -------
        context: Room
            The room that will be modified

        to_add: Room
            room to be added to context

        direction: str
            The direction to naviagate from context to to_add
        '''
        self.context = context
        self.to_add = to_add
        self.direction = direction

    def execute(self) -> str:
        self.context.add_exit(self.to_add, self.direction)
        return ''


class AddInventoryItemtoHolder(Command):
    '''
    Add one or more inventory items to a room or player inventory
    '''
    def __init__(self, items, target):
        '''
        Params:
        ------
        items: List
            List of one or more InventoryItems

        target: InventoryHolder
        '''
        self.items = items
        self.target = target

    def execute(self) -> str:
        for item in self.items:
            self.target.add_inventory(item)

        return ''


class ChangeLocationDescription(Command):
    '''
    Completely change the description of a location
    '''
    def __init__(self, room, new_description, action_text):
        self.room = room
        self.new_description = new_description
        self.action_text = action_text

    def execute(self) -> str:
        self.room.description = self.new_description
        return self.action_text


class PlayerDeath(Command):
    '''
    End of game because player dies!
    '''
    def __init__(self, death_msg, end_game_command):
        self.death_msg = death_msg
        self.end_game_command = end_game_command

    def execute(self) -> str:
        self.end_game_command.execute()
        return self.death_msg


class RemoveLinkToRoom(Command):
    '''
    Remove a link/exit from a room
    '''
    def __init__(self, context, direction_to_remove):
        self.context = context
        self.direction_to_remove = direction_to_remove

    def execute(self) -> str:
        self.context.remove_exit(self.direction_to_remove)
