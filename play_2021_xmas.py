from text_adventure.example_games import mini_knightmare
from rich import print
import os
import sys

TITLE_ART_PATH = 'text_adventure/example_games/mini_knightmare_title_art.txt'

def print_title(file_path=TITLE_ART_PATH):
    '''
    Print the title...
    '''
    file1 = open(file_path, 'r')
    lines = file1.readlines()

    for line in lines:
        print(line.rstrip())


def show_game_opening(adventure):
    '''
    Display the opening to the game + the first room description.
    '''
    # clear terminal or cmd prompt.
    os.system('cls' if os.name == 'nt' else 'clear')
    print_title()
    terminal_width = os.get_terminal_size()[0]
    print('*' * terminal_width)
    print(adventure.opening, end='\n\n')
    print('*' * terminal_width)
    print(adventure.current_room.describe())


def play_text_adventure(adventure):
    '''
    Play your text adventure!
    '''
    show_game_opening(adventure)
    while adventure.active:
        user_input = input("\nWhat do you want to do? >>> ")
        response = adventure.take_action(user_input)
        print(response)
    print(adventure.game_over_message)


if __name__ == '__main__':
    adventure = mini_knightmare.load_adventure()
    play_text_adventure(adventure)

