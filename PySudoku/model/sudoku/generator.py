from random import shuffle
from enum import IntEnum
from .board import Board, BoardTester
from .workers import Worker, WorkerType


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
        self._difficulty = difficulty

    def _wipe_cells(self) -> Board:
        """Remove all the possible cells from a filled board.

        Remove all the cells that can be removed from a filled board in a way
        that the new board will have only one solution.

        Returns:
            Board: the minimized board.
        """

        minimizer = Worker.create(WorkerType.Minimizer, self._board)
        return minimizer.resolve()

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

    def _adapt_to_difficulty(self, minimal_board: Board) -> None:
        """Adapt the minimal board to meet the difficulty specified.

        Args:
            minimal_board (Board): board with the minimum possible number of
            filled cells.
        """

        final_cell_number = self._MIN_NUMBER_OF_VALUES * self._difficulty.value
        n_used_cells = len(minimal_board.get_cells(used=True))
        if final_cell_number > n_used_cells:
            unused_cells = minimal_board.get_cells(used=False)
            shuffle(unused_cells)
            while final_cell_number != n_used_cells:
                cell = unused_cells.pop()
                cell.value = self._board.rows[cell.row][cell.col].value
                minimal_board.rows[cell.row][cell.col].value = cell.value
                n_used_cells += 1

        self._board = minimal_board

    def generate(self) -> Board:
        """Generate a new board ready to be completed.

        Returns:
            Board: the new board to complete.
        """

        self._board = Board.empty_board()
        self._generate_full_board(BoardTester(self._board))
        minimal_board = self._wipe_cells()
        self._adapt_to_difficulty(minimal_board)

        return self._board
