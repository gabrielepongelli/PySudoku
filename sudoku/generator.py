from random import shuffle
from enum import IntEnum
from .board import Board, BoardTester
from .solver import Solver


class Difficulty(IntEnum):
    """Contains all the existing difficulty levels."""

    Easy = 4
    Medium = 3
    Hard = 2
    Extreme = 1


class Generator:
    """Represent a Sudoku Generator.

    This class represent a Sudoku Generator. It is responsable for the
    generation of the initial incomplete board that will be filled by the
    player.
    """

    _MIN_NUMBER_OF_VALUES = 17

    def __init__(self, difficulty: Difficulty) -> None:
        """Initialize a new Generator.

        Initialize a new Generator in order to generate boards with the given
        difficulty level.

        Args:
            difficulty (Difficulty): the difficulty level of the boards that
            will be generated.
        """

        self._board = None
        self._solver = None
        self._difficulty = difficulty

    def _wipe_cells(self) -> None:
        """Remove some cells from a filled board.

        Remove some cells from a filled board in a way that the new board will
        have only one solution.
        """

        non_empty_squares = self._board.get_cells(used=True)
        shuffle(non_empty_squares)
        non_empty_squares_count = len(non_empty_squares)
        final_cell_number = self._MIN_NUMBER_OF_VALUES * self._difficulty.value
        while non_empty_squares_count > final_cell_number:
            # if there aren't other cells to remove exit
            try:
                cell = non_empty_squares.pop()
            except IndexError:
                return

            removed_value = cell.value
            non_empty_squares_count -= 1
            cell.value = 0
            n_solutions = 0
            self._solver = Solver.create(self._board)

            # if there is more than one solution...
            # put the last removed cell back into the board
            for _ in self._solver:
                n_solutions += 1
                if n_solutions > 1:
                    break
            else:
                continue

            cell.value = removed_value
            non_empty_squares_count += 1

    def _generate_full_board(self, tester: BoardTester) -> bool:
        """Generate a new filled board.

        Args:
            tester (BoardTester): tester that will be used to test the
            correctness of every new cell values.

        Returns:
            bool: True when the board is full.
        """

        values = [val for val in range(*self._board.VALUE_RANGE)]
        n_cells = self._board.N_ROWS * self._board.N_COLS
        for cell in range(0, n_cells):
            row = cell // self._board.N_COLS
            col = cell % self._board.N_ROWS

            # find next empty cell
            if self._board.rows[row][col].value == 0:
                shuffle(values)
                for v in values:
                    if tester.is_cell_correct(row, col, v + 1):
                        self._board.rows[row][col].value = v + 1
                        if not self._board.get_cells(used=False):
                            return True
                        else:
                            if self._generate_full_board(tester):
                                # if the board is full
                                return True
                break
        # if none of the possible values can be stored backtrack
        self._board.rows[row][col].value = 0
        return False

    def generate(self) -> Board:
        """Generate a new board ready to be completed.

        Returns:
            Board: the new board to complete.
        """

        self._board = Board.empty_board()
        self._generate_full_board(BoardTester(self._board))
        self._wipe_cells()

        return self._board
