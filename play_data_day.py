
from text_adventure.example_games import data_day_adventure
from rich import print
import os

TITLE = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    DATA'S DAY: AN ANDROID'S QUEST                        ║
║                   A Star Trek: TNG Text Adventure                        ║
║                                                                          ║
║                     "Today I have observed..."                           ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

def show_game_opening(adventure):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(TITLE)
    print('*' * 78)
    print(adventure.opening)
    print('*' * 78)
    print(adventure.current_room.describe())

def play_text_adventure(adventure):
    show_game_opening(adventure)
    while adventure.active:
        user_input = input("\nWhat do you want to do? >>> ")
        response = adventure.take_action(user_input)
        print(response)
    print(adventure.game_over_message)

if __name__ == '__main__':
    adventure = data_day_adventure.load_adventure()
    play_text_adventure(adventure)
