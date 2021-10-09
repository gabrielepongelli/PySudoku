from abc import ABC, abstractmethod
from enum import Enum
from random import shuffle
from pysat.solvers import Minisat22
from pysat.formula import CNF
from .board import Board
from .translators import TranslatorType, Translator
from .utils import NoSolutionError


class WorkerType(Enum):
    """Contains all the existing workers."""

    Solver = "solver"
    Minimizer = "minimizer"


class Worker(ABC):
    """Worker that has to do the hard work.

    A Worker is a class that has to do the hard job of testing the possible
    solution of a problem in order to find the right one.
    """

    @classmethod
    def create(type: WorkerType, board: Board = None) -> "Worker":
        """Create the desidered worker type.

        Args:
            type (WorkerType): the type of worker to create.
            board (Board): board to work with. If is None an empty board will
            be used. Defaults to None.
        """

        if board is None:
            board = Board.empty_board()

        if type == WorkerType.Solver:
            return Solver(board)
        elif type == WorkerType.Minimizer:
            return Minimizer(board)

    def __init__(self, board) -> None:
        """Initialize a new Worker.

        Args:
            board (Board): board to work with.
        """

        super().__init__()

        self._board = board
        self._sat_solver = Minisat22()

    def _map_sudoku_rules(self) -> CNF:
        """Map the sudoku rules to a valid input for a sat solver.

        Returns:
            CNF: the equivalent input for a sat solver.
        """

        tr = Translator.create(TranslatorType.GameRules)
        return tr.translate(self._board)

    def _map_board_to_sat(self) -> CNF:
        """ "Map the board instance to a valid input for a sat solver.

        Returns:
            CNF: the equivalent input for a sat solver.
        """

        tr = Translator.create(TranslatorType.SudokuInstance)
        return tr.translate(self._board)

    def _map_sat_to_board(self, result) -> Board:
        """Map a sat output to a board.

        Args:
            result: sat result to map.

        Returns:
            Board: the solved board.
        """

        tr = Translator.create(TranslatorType.SudokuResult)
        return tr.translate(result)

    @property
    def solution(self) -> Board:
        return self._board

    @abstractmethod
    def resolve(self) -> Board:
        """Resolve the problem and get the solution.

        Returns:
            Board: the result of the problem resolution.

        Raises:
            NoSolutionError: if the board specified has no solutions.
        """

        pass

    def __del__(self):
        self._sat_solver.delete()


class Solver(Worker):
    """Worker that finds solutions of Sudoku.

    Worker that finds solutions of Sudoku. It is responsable for the generation
    of the solutions of a sudoku board.
    """

    def __init__(self, board: Board) -> None:
        """Initialize a new Solver.

        Args:
            board (Board): board to solve.
        """

        super().__init__(board)

        self._sat_solver.append_formula(self._map_sudoku_rules())
        self._sat_solver.append_formula(self._map_board_to_sat())

    def resolve(self) -> Board:
        if self._sat_solver.solve() == True:
            self._board = self._map_sat_to_board(self._sat_solver.get_model())
            return self._board
        elif self._board == Board.empty_board():
            self.__init__(self._board)
            return self.resolve()
        else:
            raise NoSolutionError("the board specified has no solution.")


class Minimizer(Worker):
    """Worker that minimize a Sudoku board.

    Worker that minimize a Sudoku board. It is responsable for the generation
    of the sudoku board with minimum filled cell number.
    """

    def __init__(self, board: Board) -> None:
        """Initialize a new Minimizer.

        Args:
            board (Board): full board to minimize.
        """

        super().__init__(board)

        self._result_formula = []
        self._sat_solver.append_formula(self._map_sudoku_rules())
        self._forbid_board_solution()

    def _forbid_board_solution(self) -> None:
        """Forbid the full solution of the board."""

        self._result_formula = [
            literal for cong in self._map_board_to_sat() for literal in cong
        ]
        self._sat_solver.add_clause([-literal for literal in self._result_formula])

    def resolve(self) -> Board:
        untested_clues = self._result_formula[:]
        shuffle(untested_clues)

        self._result_formula = []

        # Compute a minimal clueset
        while len(untested_clues):
            test_clue = untested_clues.pop()
            if self._sat_solver.solve(
                assumptions=self._result_formula + untested_clues
            ):
                # Alternate solution exists, keep test_clue
                self._result_formula.append(test_clue)
            else:
                # No alternate solutions, drop test_clue
                core = self._sat_solver.get_core()
                # Remove clues not necessary for deriving unsatisfiability
                untested_clues = [l for l in untested_clues if l in core]

        self._board = self._map_sat_to_board(self._result_formula)
        return self._board
