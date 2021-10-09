from random import shuffle
from enum import IntEnum
from .board import Board
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

    def _generate_full_board(self) -> None:
        """Generate a new filled board."""

        solver = Worker.create(WorkerType.Solver, board=None)
        self._board = solver.resolve()

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

        self._generate_full_board()
        minimal_board = self._wipe_cells()
        self._adapt_to_difficulty(minimal_board)

        return self._board
