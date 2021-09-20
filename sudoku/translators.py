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
        pass

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
        pass

    def _coord_to_literal(self, row: int, col: int, value: int) -> Literal:
        """Translate the given coordinates into literal.

        Args:
            row (int): row of the cell.
            col (int): col of the cell.
            value (int): value inside the cell.

        Returns:
            Literal: the equivalent literal.
        """
        pass


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
        pass

    def _values_uniqueness(self) -> None:
        """Add to the result formula constraints for the uniqueness of every value."""
        pass

    def _columns_constraints(self) -> None:
        """Add to the result formula constraints for the columns values."""
        pass

    def _rows_constraints(self) -> None:
        """Add to the result formula constraints for the rows values."""
        pass

    def _squares_constraints(self) -> None:
        """Add to the result formula constraints for the squares values."""
        pass

    def translate(self, board: Board) -> Formula:
        """Translate the rules of the given board into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            Formula: a CNF formula equivalent to the rules of the board given.
        """
        pass


class InstanceTranslator(BoardTranslator):
    """Translator of sudoku instances."""

    def _cell_to_literal(self, cell: Cell) -> Literal:
        """Translate the given cell into literal.

        Args:
            cell (Cell): cell to translate.

        Returns:
            Literal: the equivalent literal.
        """
        pass

    def _translate_instance(self) -> None:
        """Translate all the values already present in the board into constraints."""
        pass

    def translate(self, board: Board) -> Formula:
        """Translate the given game instance into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            Formula: a CNF formula equivalent to the instance of the board given.
        """
        pass
