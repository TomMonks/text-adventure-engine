## text_adventure

The `text_adventure` package is a Python framework designed to create interactive text-based adventure games in the style of classic 1980s adventures. It provides a structured approach to building games with rooms, items, characters, and complex puzzle mechanics.

### Key Features

- **Room-based navigation** with directional movement
- **Inventory management** system for items and objects
- **Interactive NPCs** with conversation and action systems
- **Puzzle mechanics** including conditional actions and item requirements
- **Flexible command parsing** with customizable verbs and aliases
- **Rich text output** support using the Rich library
- **Extensible architecture** for creating custom game mechanics

## Package Structure

The framework consists of several core modules:

### Core Components

- **`world.py`** - Contains `TextWorld`, `Room`, and `InventoryItem` classes
- **`actions.py`** - Defines action classes for game interactions
- **`commands.py`** - Implements game commands and state changes
- **`constants.py`** - Defines default verbs and navigation constants

### Key Classes

- **`TextWorld`** - Main game controller managing rooms, inventory, and command processing
- **`Room`** - Represents game locations with descriptions and exits
- **`InventoryItem`** - Represents interactive objects, characters, and items
- **Action Classes** - Handle player interactions (BasicInventoryItemAction, ConditionalInventoryItemAction, etc.)

## Environment Setup

### Creating the Conda Environment

The package includes an `environment.yml` file for setting up the required dependencies:

```bash
# Create the conda environment
conda env create -f environment.yml

# Activate the environment
conda activate text-adventure-engine
```

### Manual Installation

If you prefer manual setup:

```bash
# Create a new conda environment
conda create -n text-adventure-engine python=3.8

# Activate the environment
conda activate text-adventure-engine

# Install required packages
pip install rich
```

## Running Example Games

### Mini Knightmare Example

The package includes a complete example game called "Mini Knightmare" based on the classic TV show:

```bash
# Navigate to the project directory
cd text-adventure-engine

# Run the example game
python play_mini_knightmare.py
```

### Game Structure

The `mini_knightmare.py` example demonstrates the framework's capabilities:

- **Multiple rooms** with interconnected puzzles
- **Character interactions** (Treguard, Olgarth, Lilith)
- **Item-based puzzles** requiring specific objects
- **Conditional progression** based on player choices
- **Rich narrative** with atmospheric descriptions

## Creating Your Own Games

### Basic Game Structure

Every game follows this pattern:

1. **Create Rooms** - Define locations and their connections
2. **Create Items** - Define interactive objects and characters
3. **Setup World** - Initialize the game engine with custom commands
4. **Add Actions** - Define how players interact with items
5. **Return Adventure** - Package everything into a playable game

### Example Game Template

```python
from text_adventure.world import TextWorld, Room, InventoryItem
from text_adventure.commands import *
from text_adventure.constants import *
from text_adventure.actions import *

def load_adventure():
    # Create rooms
    start_room = Room("Starting Room")
    start_room.description = "You are in the starting room."
    
    # Create items
    key = InventoryItem('key')
    key.long_description = "A rusty old key."
    
    # Setup world
    adventure = TextWorld(
        name="My Adventure",
        rooms=[start_room],
        start_index=0,
        command_verb_mapping=DEFAULT_VERBS,
        use_aliases='classic'
    )
    
    # Add items to rooms
    start_room.add_inventory(key)
    
    return adventure
```

### Running Custom Games

Create a launcher script similar to `play_mini_knightmare.py`:

```python
from text_adventure.example_games import your_game_module
from rich import print
import os

def play_text_adventure(adventure):
    while adventure.active:
        user_input = input("\nWhat do you want to do? >>> ")
        if not user_input.strip():
            print("Please enter a command.")
            continue
        response = adventure.take_action(user_input)
        print(response)
    print(adventure.game_over_message)

if __name__ == '__main__':
    adventure = your_game_module.load_adventure()
    play_text_adventure(adventure)
```

## Command System

### Default Commands

The framework provides standard text adventure commands:

- **Navigation**: `north`, `south`, `east`, `west`, `up`, `down`
- **Inventory**: `get [item]`, `drop [item]`, `inv` (inventory)
- **Examination**: `look`, `examine [item]`
- **Interaction**: `use [item]`, `give [item] [character]`
- **System**: `quit`, `help`

### Custom Commands

Add custom verbs using the `add_use_command_alias()` method:

```python
adventure.add_use_command_alias('dance')
adventure.add_use_command_alias('scan')
adventure.add_use_command_alias('activate')
```

## Puzzle Design Patterns

### Basic Interactions

```python
# Simple action that displays text
talk_action = BasicInventoryItemAction(
    NullCommand("Hello, adventurer!"),
    command_text="talk"
)
character.add_action(talk_action)
```

### Conditional Puzzles

```python
# Action that checks for specific input
riddle_action = ConditionalInventoryItemAction(
    'correct answer',
    success_action,
    failure_action,
    command_text='answer'
)
```

### Item Requirements

```python
# Action requiring specific items in inventory
restricted_action = RestrictedInventoryItemAction(
    adventure,
    [success_commands],
    [required_item],
    "You need the key first!",
    command_text='unlock'
)
```

## Best Practices

### Game Design

- **Progressive difficulty** - Start simple and build complexity
- **Clear feedback** - Always respond to player actions
- **Logical puzzles** - Ensure solutions make thematic sense
- **Multiple paths** - Offer different approaches when possible

### Code Organization

- **Separate concerns** - Keep room creation, item creation, and action setup in different functions
- **Consistent naming** - Use clear, descriptive names for rooms and items
- **Modular design** - Create reusable components for common patterns

### Testing

- **Test all paths** - Verify both success and failure conditions
- **Edge cases** - Handle empty input and invalid commands
- **Sequence testing** - Ensure puzzles work in the intended order

## Troubleshooting

### Common Issues

- **IndexError on empty input** - Add input validation in your launcher
- **Missing exits** - Ensure room connections are bidirectional when needed
- **Action not triggering** - Check that custom verbs are registered with `add_use_command_alias()`
- **Items not appearing** - Verify items are added to rooms or inventory correctly

### Debug Tips

- Use `look` frequently to check room state
- Check inventory with `inv` before attempting item-based actions
- Examine items with `examine [item]` for detailed descriptions
- Test puzzle sequences in the intended order