import pysat.solvers as pysat
from board import Board


class Solver:
    """Represent a Sudoku Solver.

    This class represent a Sudoku Solver. It is responsable for the generation
    of the solutions of a sudoku board.
    """

    def __init__(self, board: Board) -> None:
        """Initialize a new Solver.

        Args:
            board (Board): board to solve.
        """

        self._sat_solver = None
        self.board = board

    def _map_board_to_sat(self):
        """Map the board to a valid input for a sat solver."""
        pass

    def _map_sat_to_board(self) -> Board:
        """Map a sat output to a board.

        Returns:
            Board: the solved board.
        """
        pass

    def solve(self) -> Board:
        """Solve the board and get the first solution.

        Returns:
            Board: the solved board.
        """

        self._sat_solver = pysat.Solver()
        self._map_board_to_sat()

    def __iter__(self):
        """Iterate through all the possible solutions for the board."""
        pass

    def __repr__(self):
        pass
