from typing import List, Tuple, NewType
from math import sqrt
from abc import ABC, abstractmethod
from enum import Enum
from board import Cell, Board


Literal = NewType("Literal", int)
Formula = NewType("Formula", List[List[Literal]])
Range = NewType("Range", Tuple[int, int])


class TranslatorType(Enum):
    """Contains all the existing translators."""

    GameRules = "rules"
    SudokuInstance = "instance"


class Translator(ABC):
    """Common interface for a translator class.

    This is a common interface for a translator class. A translator is a class
    that translate something into CNF formulas ready for being processed by a
    sat solver.
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

    @abstractmethod
    def translate(self, obj: object) -> Formula:
        """Translate the given object into the equivalent CNF formula.

        Args:
            obj (object): object to translate.

        Returns:
            Formula: a CNF formula equivalent to the object given.
        """
        pass


class BoardTranslator(Translator):
    """Translator of sudoku boards."""

    def __init__(self) -> None:
        """Initialize a new BoardTranslator."""

        super().__init__()
        self._board = None
        self.result = None

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
        return value + (col_coefficent * col) + (row_coefficent * row)


class RulesTranslator(BoardTranslator):
    """Translator of sudoku rules."""

    def _uniqueness(
        self,
        range_first: Range,
        range_second: Range,
        range_variable: Range,
        map_to_coord: function,
    ) -> None:
        """Pattern for the uniqueness.

        Args:
            range_first (Range): range of the first parameter.
            range_second (Range): range of the second parameter.
            range_variable (Range): range of the variable parameter.
            map_to_literal (function): function that map the tuple
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
                    for j in range(i + 1, range_variable[0]):
                        not_first = -self._coord_to_literal(
                            map_to_coord(first, second, i)
                        )
                        not_second = -self._coord_to_literal(
                            map_to_coord(first, second, j)
                        )
                        self.result.append([not_first, not_second])

    def _values_uniqueness(self) -> None:
        """Add to the result formula constraints for the uniqueness of every value."""

        args = {
            "range_first": (0, self._board.N_ROWS),
            "range_second": (0, self._board.N_COLS),
            "range_variable": (
                self._board.VALUE_RANGE[0] + 1,
                self._board.VALUE_RANGE[1] + 1,
            ),
            "map_to_coord": lambda x, y, z: (x, y, z),
        }

        self._uniqueness(**args)

    def _columns_constraints(self) -> None:
        """Add to the result formula constraints for the columns values."""

        args = {
            "range_first": (
                self._board.VALUE_RANGE[0] + 1,
                self._board.VALUE_RANGE[1] + 1,
            ),
            "range_second": (0, self._board.N_COLS),
            "range_variable": (0, self._board.N_ROWS),
            "map_to_coord": lambda x, y, z: (z, y, x),
        }

        self._uniqueness(**args)

    def _rows_constraints(self) -> None:
        """Add to the result formula constraints for the rows values."""

        args = {
            "range_first": (
                self._board.VALUE_RANGE[0] + 1,
                self._board.VALUE_RANGE[1] + 1,
            ),
            "range_second": (0, self._board.N_ROWS),
            "range_variable": (0, self._board.N_COLS),
            "map_to_coord": lambda x, y, z: (y, z, x),
        }

        self._uniqueness(**args)

    def _squares_constraints(self) -> None:
        """Add to the result formula constraints for the squares values."""

        n_cells_per_square = self._board.N_SQUARES / self._board.N_ROWS
        row = lambda square: square // sqrt(n_cells_per_square)
        col = lambda square: square % sqrt(n_cells_per_square)

        args = {
            "range_first": (
                self._board.VALUE_RANGE[0] + 1,
                self._board.VALUE_RANGE[1] + 1,
            ),
            "range_second": (0, self._board.N_SQUARES),
            "range_variable": (0, n_cells_per_square),
            "map_to_coord": lambda x, y, z: (
                row(y) + (z // n_cells_per_square),
                col(z) + (z % n_cells_per_square),
                x,
            ),
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


class InstanceTranslator(BoardTranslator):
    """Translator of sudoku instances."""

    def _cell_to_literal(self, cell: Cell) -> Literal:
        """Translate the given cell into literal.

        Args:
            cell (Cell): cell to translate.

        Returns:
            Literal: the equivalent literal.
        """

        return self._coord_to_literal(cell.row, cell.col, cell.value)

    def _translate_instance(self) -> None:
        """Translate all the values already present in the board into constraints."""

        for cell in self._board.get_cells():
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
