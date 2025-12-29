import requests
import json

from colorama import Fore, Style

from constants import API_URL, Difficulty
from models import BoardObject

def print_in_colour(text: str, colour) -> None:
    print(colour + text + Style.RESET_ALL)
    

def get_sudoku(difficulty: Difficulty = Difficulty.RANDOM) -> BoardObject:
    """
    Fetch Sudoku boards until one matches the requested difficulty.
    Valid difficulties: 'easy', 'medium', 'hard'
    Default is random difficulty
    """
    while True:
        print(f"Sending request for {difficulty.value} game...")

        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()

            new_board = response.json().get("newboard", {})
            game_board: BoardObject = BoardObject(**new_board)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        if difficulty == Difficulty.RANDOM:
            return game_board
        elif game_board.grids.difficulty == difficulty:
            print_in_colour(f"{difficulty.value.upper()} GAME FOUND!", Fore.GREEN)
            return game_board