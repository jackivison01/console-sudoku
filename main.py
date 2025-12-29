import requests
import json
from colorama import Fore, Style
from pick import pick

from constants import ROW_SEPARATOR, COLUMNS_HEADER, NUM_ROWS, NUM_COLUMNS, NUM_LIVES, Difficulty
from services import print_in_colour, get_sudoku
    

class Game:
    def __init__(self, difficulty: Difficulty):
        self.no_lives = NUM_LIVES
        self.game_board = get_sudoku(difficulty)

        self.board_state = self.game_board.grids.value
        self.board_solution = self.game_board.grids.solution

        
    def display_board(self) -> None:
        print(f"DIFFICULTY: {self.game_board.grids.difficulty.value}")
        print("")
        print(COLUMNS_HEADER)
        print("")
        for i in range(NUM_ROWS):
            row_string = ""
            for j in range(NUM_COLUMNS):
                number_separator = " "
                if j % 3 == 0 and j > 0:
                    number_separator = " | "
                row_string += number_separator + str(self.board_state[i][j])
            if i % 3 == 0 and i > 0:
                print(ROW_SEPARATOR)
            print(f"{i+1} {row_string}")


    def get_board_state(self):
        return self.board_state
    
    
    def input_value(self, row, column , val):
        #check correct
        if val != self.board_solution[row][column]:
            self.no_lives -= 1
            print_in_colour("INCORRECT!     |     LIVES REMAINING: " + str(self.no_lives), Fore.RED)
            return

        print_in_colour("CORRECT!", Fore.GREEN)
        self.board_state[row][column] = val


    def check_win(self) -> bool:
        for i in range(NUM_ROWS):
            for j in range(NUM_COLUMNS):
                if self.board_state[i][j] != self.board_solution[i][j]:
                    return False

        print_in_colour("GAME WON!", Fore.GREEN)
        return True


    def check_loss(self) -> bool:
        return self.no_lives == 0
    

    def reset_game(self):
        while True:
            new_game = str(input("Would you like to start a new game? (y/n) "))
            if new_game.lower() not in ("y", "n"):
                print_in_colour("ENTER A VALID INPUT", Fore.RED)
                continue

            if new_game.lower() == "n":
                quit()

            if new_game.lower() == "y":
                return True
            

def difficulty_selection():
    title = "Select game difficulty frm the following options: "
    
    difficulties = list(Difficulty)
    options = [diff.value.upper() for diff in difficulties]

    _, index = pick(options, title, indicator="=>")

    return difficulties[index]

def game_loop():
    selected_difficulty = difficulty_selection()
    game = Game(selected_difficulty)
    game.display_board()

    while True:
        row = int(input("Which row? ")) - 1 #offset for array indices beginning at zero
        column = int(input("Which column? ")) - 1
        value = int(input("What value? "))

        game.input_value(row, column, value)

        if game.check_loss():
            print_in_colour("GAME OVER!", Fore.RED)

            if game.reset_game():
                game_loop()

            break

        game.check_win()

        game.display_board()

if __name__ == "__main__":
    game_loop()