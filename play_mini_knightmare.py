from text_adventure.example_games import mini_knightmare
from rich import print
import os


def show_game_opening(adventure):
    '''
    Display the opening to the game + the first room description.
    '''
    # clear terminal or cmd prompt.
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = os.get_terminal_size()[0]
    print('*' * terminal_width)
    print(adventure.opening, end='\n\n')
    adventure.player_name = input("What is your name stranger? >> ")
    os.system('cls' if os.name == 'nt' else 'clear')
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
    print(f'Your adventure ends here {adventure.player_name}.')


if __name__ == '__main__':
    adventure = mini_knightmare.load_adventure()
    play_text_adventure(adventure)

