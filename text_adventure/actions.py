'''
Inventory item actions

Actions can be taken with inventory items a TextWorld.  Actions are
at their core a sequence of Command objects that are executed via a specific
key word.  Actions can be:

Restricted to occur only in specific rooms
Restricted to occur only if a player is holding the InventoryItem.

All action classes are subclasses of the Abstract InventoryItemAction
super class.

'''

from abc import ABC, abstractmethod

################# CONSTANTS ###################################################
COMMAND_ERROR = "You cannot do that."


##################### BASE CLASSES ############################################

class InventoryItemAction(ABC):
    '''
    Base class for all inventory item actions
    '''
    @abstractmethod
    def add_command(command):
        pass

    @abstractmethod
    def try_to_execute(command_text, *args):
        pass


################ ACTION SUBCLASSES ############################################

class BasicInventoryItemAction(InventoryItemAction):
    '''
    A basic inventory item action is a sequence of commands.  Each command
    may alter the game state and will return a msg.  The msg is concat and
    returned to the player.
    '''
    def __init__(self, command, command_text='use', invalid_msg=COMMAND_ERROR):
        '''
        Construct a BasicInventoryItemAction

        Params:
        ------
        command: Command
            A command object

        command_text: str, optional (default='use')
            The command text that triggers the action for this item

        invalid_msg: str, optional (default=COMMAND_ERROR)
            The msg to return if the command_text is invalid for this action.
        '''
        if isinstance(command, list):
            self.commands = command
        else:
            self.commands = [command]

        self.command_text = command_text
        self.invalid_msg = invalid_msg

    def add_command(self, command):
        '''
        Add a command to the sequence of commands executed in the action.
        '''
        self.commands.append(command)

    def try_to_execute(self, command_text, **kwargs):
        '''
        Attempt to execute the command using command text.

        May fail and if so returns self.invalid_msg.

        This may not be the best way to implement and probably should be
        implemented in a specialised class makes subclasses actionable
        potential name is `Actionable` or `Interactive`

        '''
        msg = ''

        if self.command_text == command_text:
            for cmd in self.commands:
                msg += cmd.execute()
        else:
            msg = self.invalid_msg

        return msg


class RestrictedInventoryItemAction(InventoryItemAction):
    '''
    The action is restricted to be only actionable by a 'holder' when the
    item or list of items (requirements) are in hand.  i.e. a player or room
    holds all required inventory items.

    Note: if a player is the holder then there is no requirement
    to be in a specific room.
    '''
    def __init__(self, holder, command, requirements, not_holding_msg,
                 command_txt='use'):
        '''
        Constructor

        Params:
        -------

        holder: InventoryItemHolder
            The player or room that is required to hold the items before action
            can be executed.

        command: Command or List
            At least one command is required to be executed.  Pass in a list
            of Command objects if required or use .add_command(cmd) method to
            add commands individually.

        requirements: List
            A list of InventoryItems.  For the action to execute the holder
            must have all InventoryItems in their inventory.

        not_holding_msg: str
            Message to holder if they are not holding all the required items.

        command_txt: str, optional (default='use')
            string to activate action.
        '''
        if isinstance(command, list):
            self.commands = command
        else:
            self.commands = [command]

        self.command_text = command_txt
        self.requirements = requirements
        self.holder = holder
        self.fail_message = not_holding_msg

    def add_command(self, command):
        '''
        Add a new command to the action.  Last in last out.

        Params:
        ------
        command: Command
        '''
        self.commands.append(command)

    def try_to_execute(self, command_text, **kwargs):

        # if correct command issed to trigger action.
        if self.command_text != command_text:
            return "You can't do that."

        if self._requirements_satisifed():
            msg = ''
            for cmd in self.commands:
                msg += cmd.execute()

        else:
            msg = self.fail_message

        return msg

    def _requirements_satisifed(self):
        return self.holder.in_inventory(self.requirements)


class ChoiceInventoryItemAction(InventoryItemAction):
    '''
    Provides a player with a choice between actions based
    on their answer...
    '''
    def __init__(self, choices, command_text='use',
                 invalid_choice="You can't do that."):
        '''
        Provides a player with a choice between two actions.

        Params:
        -------
        choices: dict
            dictionary of str keys representing choices.
            values are InventoryItemActions

        command_text: str, optional (default='use')
        '''
        self.choices = choices
        self.command_text = command_text
        self.invalid_choice = invalid_choice

    def add_command(self, command):
        '''
        Adds to each command in the choices dict.
        '''
        for action in self.choices.values():
            action.add_command(command)

    def try_to_execute(self, command_text, **kwargs):
        '''
        Attempt to execute chosen action.  Invalid actions
        are handled.
        '''
        parsed_command = kwargs['parsed_command']
        if len(parsed_command) < 3:
            return self.command_text + ' ' + parsed_command[1] + ' what?'
        else:
            answer = parsed_command[2]
            try:
                chosen_action = self.choices[answer]
                return chosen_action.try_to_execute(command_text,
                                                    **kwargs)
            except KeyError:
                return self.invalid_choice


class ConditionalInventoryItemAction(InventoryItemAction):
    '''
    Simple if-else conditional action.
    If answer is correct then attempt action a
    Else attempt action y.
    '''
    def __init__(self, correct_answer, action_correct, action_incorrect,
                 command_text='use'):
        self.correct_answer = correct_answer
        self.action_correct = action_correct
        self.action_incorrect = action_incorrect
        self.command_text = command_text

    def add_command(self, command):
        '''
        Add a new command to the action.  Last in last out.
        Note this is added to the correct action only!

        Params:
        ------
        command: Command
        '''
        self.action_correct.add_command(command)

    def try_to_execute(self, command_text, **kwargs):
        parsed_command = kwargs['parsed_command']
        if len(parsed_command) < 3:
            return self.command_text + ' ' + parsed_command[1] + ' what?'
        else:
            answer = parsed_command[2]
            if answer == self.correct_answer:
                return self.action_correct.try_to_execute(command_text,
                                                          **kwargs)
            else:
                return self.action_incorrect.try_to_execute(command_text,
                                                            **kwargs)

########################### Untested code #############################


class RoomSpecificInventoryItemAction(InventoryItemAction):
    '''
    Action with item will only work in specific room
    '''
    def __init__(self, game, context, action, command_text='use'):
        self.game = game
        self.context = context
        self.action = action
        self.command_text = command_text

    def add_command():
        pass

    def try_to_execute(self, command_text, **kwargs):
        msg = ''
        if self.game.current_room == self.context:
            msg = self.action.try_to_execute(command_text)

        return msg



