from typing import List, Tuple, NewType, Callable
from math import sqrt
from abc import ABC, abstractmethod
from enum import Enum
from .board import Cell, Board


Literal = NewType("Literal", int)
Formula = NewType("Formula", List[List[Literal]])
Range = NewType("Range", Tuple[int, int])


class TranslatorType(Enum):
    """Contains all the existing translators."""

    GameRules = "rules"
    SudokuInstance = "instance"
    SudokuResult = "result"


class Translator(ABC):
    """Common interface for a translator class.

    This is a common interface for a translator class. A translator is a class
    that translate something into an equivalent version of something else.
    """

    @staticmethod
    def create(type: TranslatorType) -> "Translator":
        """Create the desidered translator type.

        Args:
            type (TranslatorType): the type of translator to generate.
        """

        if type == TranslatorType.GameRules:
            return RulesTranslator()
        elif type == TranslatorType.SudokuInstance:
            return InstanceTranslator()
        elif type == TranslatorType.SudokuResult:
            return ResultTranslator()

    @abstractmethod
    def translate(self, obj: object) -> object:
        """Translate the given object into some other equivalent object.

        Args:
            obj (object): object to translate.

        Returns:
            object: the equivalent obj translation.
        """
        pass


class CnfTranslator(Translator):
    """Translator of sudoku boards into CNF formulas.

    This is a Translator of sudoku boards into CNF formulas ready for being
    processed by a sat solver.
    """

    def __init__(self) -> None:
        """Initialize a new BoardTranslator."""

        super().__init__()
        self._board: Board = None
        self.result: Formula = None

    def _coord_to_literal(self, row: int, col: int, value: int) -> Literal:
        """Translate the given coordinates into literal.

        Args:
            row (int): row of the cell.
            col (int): col of the cell.
            value (int): value inside the cell.

        Returns:
            Literal: the equivalent literal.
        """

        col_coefficent = self._board.VALUE_RANGE[1]
        row_coefficent = col_coefficent * self._board.N_COLS
        return value + (col_coefficent * col) + (row_coefficent * row) + 1

    @abstractmethod
    def translate(self, board: Board) -> Formula:
        pass


class RulesTranslator(CnfTranslator):
    """Translator of sudoku rules."""

    def _uniqueness(
        self,
        range_first: Range,
        range_second: Range,
        range_variable: Range,
        map_to_coord: Callable,
    ) -> None:
        """Pattern for the uniqueness.

        Args:
            range_first (Range): range of the first parameter.
            range_second (Range): range of the second parameter.
            range_variable (Range): range of the variable parameter.
            map_to_literal (Callable): function that map the tuple
            (first, second, var) in to the appropriate order for the
            translation into literals.
        """

        for first in range(*range_first):
            for second in range(*range_second):
                # at least one value must be true
                self.result.append(
                    [
                        self._coord_to_literal(*map_to_coord(first, second, var))
                        for var in range(*range_variable)
                    ]
                )

                # only one value must be true
                for i in range(range_variable[0], range_variable[1] - 1):
                    for j in range(i + 1, range_variable[1]):
                        not_first = -self._coord_to_literal(
                            *map_to_coord(first, second, i)
                        )
                        not_second = -self._coord_to_literal(
                            *map_to_coord(first, second, j)
                        )
                        self.result.append([not_first, not_second])

    def _values_uniqueness(self) -> None:
        """Add to the result formula constraints for the uniqueness of every value."""

        args = {
            "range_first": (0, self._board.N_ROWS),
            "range_second": (0, self._board.N_COLS),
            "range_variable": self._board.VALUE_RANGE,
            "map_to_coord": lambda x, y, z: (x, y, z),
        }

        self._uniqueness(**args)

    def _columns_constraints(self) -> None:
        """Add to the result formula constraints for the columns values."""

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_COLS),
            "range_variable": (0, self._board.N_ROWS),
            "map_to_coord": lambda x, y, z: (z, y, x),
        }

        self._uniqueness(**args)

    def _rows_constraints(self) -> None:
        """Add to the result formula constraints for the rows values."""

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_ROWS),
            "range_variable": (0, self._board.N_COLS),
            "map_to_coord": lambda x, y, z: (y, z, x),
        }

        self._uniqueness(**args)

    def _squares_constraints(self) -> None:
        """Add to the result formula constraints for the squares values."""

        n_cells_per_square = (
            self._board.N_ROWS * self._board.N_COLS
        ) // self._board.N_SQUARES
        n_cell_per_side = int(sqrt(n_cells_per_square))
        row = lambda square, cell: (
            ((square // n_cell_per_side) * n_cell_per_side) + (cell // n_cell_per_side)
        )
        col = lambda square, cell: (
            ((square % n_cell_per_side) * n_cell_per_side) + (cell % n_cell_per_side)
        )

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_SQUARES),
            "range_variable": (0, n_cells_per_square),
            "map_to_coord": lambda x, y, z: (row(y, z), col(y, z), x),
        }

        self._uniqueness(**args)

    def translate(self, board: Board) -> Formula:
        """Translate the rules of the given board into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            Formula: a CNF formula equivalent to the rules of the board given.
        """

        self._board = board
        self.result = []

        self._values_uniqueness()
        self._columns_constraints()
        self._rows_constraints()
        self._squares_constraints()

        return self.result


class InstanceTranslator(CnfTranslator):
    """Translator of sudoku instances."""

    def _cell_to_literal(self, cell: Cell) -> Literal:
        """Translate the given cell into literal.

        Args:
            cell (Cell): cell to translate.

        Returns:
            Literal: the equivalent literal.
        """

        return self._coord_to_literal(cell.row, cell.col, cell.value - 1)

    def _translate_instance(self) -> None:
        """Translate all the values already present in the board into constraints."""

        for cell in self._board.get_cells(used=True):
            self.result.append([self._cell_to_literal(cell)])

    def translate(self, board: Board) -> Formula:
        """Translate the given game instance into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            Formula: a CNF formula equivalent to the instance of the board given.
        """

        self._board = board
        self.result = []

        self._translate_instance()

        return self.result


class ResultTranslator(Translator):
    """Translator of sat solver results into sudoku boards."""

    def _literal_to_coord(self, literal: Literal) -> Tuple[int, int, int]:
        """Translate the given literal into matrix coordinates.

        Args:
            literal (Literal): literal to translate.

        Returns:
            Tuple[int, int, int]: the equivalent coordinates.
        """

        literal -= 1
        col_coefficent = Board.VALUE_RANGE[1]
        row_coefficent = Board.N_COLS * col_coefficent

        row = literal // row_coefficent
        col = (literal - (row * row_coefficent)) // col_coefficent
        value = literal - (col * col_coefficent) - (row * row_coefficent)

        return (row, col, value)

    def _translate_sat_result(self) -> List[List[int]]:
        """Translate the sat result into a matrix of numbers.

        Returns:
            List[List[int]]: the matrix equivalent to the sat result given.
        """

        matrix = [list() for _ in range(0, Board.N_ROWS)]
        for i in range(0, len(matrix)):
            matrix[i] = [0 for _ in range(0, Board.N_COLS)]

        for literal in self._result:
            if literal > 0:
                row, col, value = self._literal_to_coord(literal)
                matrix[row][col] = value + 1

        return matrix

    def translate(self, sat_result: List[Literal]) -> Board:
        """Translate the given sat result into the equivalent board.

        Args:
            sat_result (List[Literal]): sat result to translate.

        Returns:
            Board: a board equivalent to the sat result given.
        """

        self._result = sat_result
        self.board = Board.from_matrix(self._translate_sat_result())

        return self.board
