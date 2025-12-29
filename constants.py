from enum import Enum

ROW_SEPARATOR  = "  -------+-------+-------"
COLUMNS_HEADER = "   1 2 3   4 5 6   7 8 9 "
NUM_ROWS = 9
NUM_COLUMNS = 9
API_URL = "https://sudoku-api.vercel.app/api/dosuku"
NUM_LIVES = 3

class Difficulty(Enum):
    RANDOM = "random"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @classmethod
    def from_input(cls, value: str) -> "Difficulty":
        return cls(value.strip().lower())