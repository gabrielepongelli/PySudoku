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

    def __init__(self, difficulty: Difficulty) -> None:
        """Initialize a new Generator.

        Initialize a new Generator in order to generate boards with the given
        difficulty level.

        Args:
            difficulty (Difficulty): the difficulty level of the boards that
            will be generated.
        """

        pass

    def _wipe_cells(self) -> None:
        """Remove some cells from a filled board.

        Remove some cells from a filled board in a way that the new board will
        have only one solution.
        """

        pass

    def _generate_full_board(self, tester: BoardTester) -> bool:
        """Generate a new filled board.

        Args:
            tester (BoardTester): tester that will be used to test the
            correctness of every new cell values.

        Returns:
            bool: True when the board is full.
        """

        pass

    def generate(self) -> Board:
        """Generate a new board ready to be completed.

        Returns:
            Board: the new board to complete.
        """

        pass
