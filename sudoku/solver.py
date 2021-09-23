import pysat.solvers as pysat
from .board import Board
from .translators import Formula, TranslatorType, Translator
from .utils import NoSolutionError


class Solver:
    """Represent a Sudoku Solver.

    This class represent a Sudoku Solver. It is responsable for the generation
    of the solutions of a sudoku board.
    """

    @classmethod
    def create(cls, board: Board) -> "Solver":
        """Create a new Solver that will solve the given board.

        Args:
            board (Board): board to assign to the new Solver.

        Returns:
            Solver: the new solver created.
        """

        if not hasattr(cls, "_rules_formula"):
            cls._rules_formula = cls._map_sudoku_rules(board)

        return cls(board, pysat.Minisat22(bootstrap_with=cls._rules_formula))

    @classmethod
    def _map_sudoku_rules(cls, board: Board) -> Formula:
        """Map the sudoku rules to a valid input for a sat solver.

        Args:
            board (Board): board that contains the rules to map.

        Returns:
            Formula: the equivalent input for a sat solver.
        """

        tr = Translator.create(TranslatorType.GameRules)
        formula = tr.translate(board)
        return formula

    def __init__(self, board: Board, solver: pysat.Solver) -> None:
        """Initialize a new Solver.

        Args:
            board (Board): board to solve.
            solver (pysat.Solver): sat solver to use.
        """

        self._sat_solver = solver
        self._board = board
        self._map_board_to_sat()

    def _map_board_to_sat(self):
        """Map the board instance to a valid input for a sat solver."""

        tr = Translator.create(TranslatorType.SudokuInstance)
        formula = tr.translate(self._board)
        self._sat_solver.append_formula(formula)

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

    def __del__(self):
        self._sat_solver.delete()
