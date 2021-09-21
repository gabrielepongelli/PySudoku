import pysat.solvers as pysat
from .board import Board
from .translators import TranslatorType, Translator
from .utils import NoSolutionError


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

        self._sat_solver = pysat.Solver()
        self._board = board

    def _map_board_to_sat(self):
        """Map the board to a valid input for a sat solver."""

        tr = Translator.create(TranslatorType.GameRules)
        formula = tr.translate(self._board)
        tr = Translator.create(TranslatorType.SudokuInstance)
        formula += tr.translate(self._board)

        for prep in formula:
            self._sat_solver.add_clause(prep)

    def _map_sat_to_board(self, result) -> Board:
        """Map a sat output to a board.

        Args:
            result: sat result to map.

        Returns:
            Board: the solved board.
        """

        tr = Translator.create(TranslatorType.SudokuResult)
        return tr.translate(result)

    def solve(self) -> Board:
        """Solve the board and get the first solution.

        Returns:
            Board: the solved board.

        Raises:
            NoSolutionError: if the board specified has no solutions.
        """

        self._map_board_to_sat()

        if self._sat_solver.solve() == True:
            self._board = self._map_sat_to_board(self._sat_solver.get_model())
            return self._board
        else:
            raise NoSolutionError("the board specified has no solution.")

    @property
    def solution(self) -> Board:
        return self._board

    def __iter__(self):
        """Iterate through all the possible solutions for the board."""

        for solution in self._sat_solver.enum_models():
            yield self._map_sat_to_board(solution)
