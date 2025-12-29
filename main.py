import requests
import json
from colorama import Fore, Style
from pick import pick

from constants import ROW_SEPARATOR, COLUMNS_HEADER, NUM_ROWS, NUM_COLUMNS, NUM_LIVES, Difficulty
from services import print_in_colour, get_sudoku
from models import CompleteCells
    

class Game:
    def __init__(self, difficulty: Difficulty):
        self.no_lives = NUM_LIVES
        self.game_board = get_sudoku(difficulty)

        self.board_state = self.game_board.grids.value
        self.complete_cells: CompleteCells = [[0 for i in range(NUM_COLUMNS)] for j in range(NUM_ROWS)]
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
                if self.complete_cells[i][j] == 1:
                    row_string += number_separator + Fore.GREEN + str(self.board_state[i][j]) + Style.RESET_ALL
                else:
                    row_string += number_separator + str(self.board_state[i][j])
            if i % 3 == 0 and i > 0:
                print(ROW_SEPARATOR)
            print(f"{i+1} {row_string}")


    def get_board_state(self) -> list[list[int]]:
        return self.board_state
    
    
    def input_value(self, row, column , val) -> None:
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
    

    def reset_game(self) -> bool:
        while True:
            new_game = str(input("Would you like to start a new game? (y/n) "))
            if new_game.lower() not in ("y", "n"):
                print_in_colour("ENTER A VALID INPUT", Fore.RED)
                continue

            if new_game.lower() == "n":
                quit()

            if new_game.lower() == "y":
                return True
            
    
    def check_complete_cells(self):
        #check rows
        for i in range(NUM_ROWS):
            if 0 in self.board_state[i]:
                continue
            for j in range(NUM_COLUMNS):
                self.complete_cells[i][j] = 1
        #check columns
        inverted_board = list(map(list, zip(*self.board_state)))
        for j in range(NUM_COLUMNS):
            if 0 in inverted_board[j]:
                continue
            for i in range(NUM_ROWS):   
                self.complete_cells[i][j] = 1
        #check squares

        #check numbers
        complete_numbers = []
        for i in range(NUM_ROWS):
            for j in range(NUM_ROWS):
                if i not in self.board_state[j]:
                    continue
            complete_numbers.append(i)

        for i in range(NUM_ROWS):
            for j in range(NUM_COLUMNS):
                if self.board_state[i][j] in complete_numbers:
                    self.complete_cells[i][j] = 1

            
        pass
            

def difficulty_selection() -> Difficulty:
    title = "Select game difficulty frm the following options: "
    
    difficulties = list(Difficulty)
    options = [diff.value.upper() for diff in difficulties]

    _, index = pick(options, title, indicator="=>")

    return difficulties[index]

def game_loop():
    selected_difficulty = difficulty_selection()
    game = Game(selected_difficulty)
    game.check_complete_cells()
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
        game.check_complete_cells()
        game.display_board()

if __name__ == "__main__":
    game_loop()