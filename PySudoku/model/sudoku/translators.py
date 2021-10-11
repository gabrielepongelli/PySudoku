from typing import List, Tuple, NewType, Callable, Set
from abc import ABC, abstractmethod
from enum import Enum
from random import shuffle
from pysat.formula import CNF
from pysat.card import CardEnc
from .board import Cell, Board


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

    __literal_tr = None

    @classmethod
    def create(cls, type: TranslatorType) -> "Translator":
        """Create the desidered translator type.

        Args:
            type (TranslatorType): the type of translator to generate.
        """

        if Translator.__literal_tr is None:
            Translator.__literal_tr = LiteralTranslator()

        if type == TranslatorType.GameRules:
            return RulesTranslator(Translator.__literal_tr)
        elif type == TranslatorType.SudokuInstance:
            return InstanceTranslator(Translator.__literal_tr)
        elif type == TranslatorType.SudokuResult:
            return ResultTranslator(Translator.__literal_tr)

    @abstractmethod
    def translate(self, obj: object) -> object:
        """Translate the given object into some other equivalent object.

        Args:
            obj (object): object to translate.

        Returns:
            object: the equivalent obj translation.
        """
        pass


class LiteralTranslator(Translator):
    """Translator between Board values and Literal values."""

    def __init__(self) -> None:
        """Initialize a new LiteralTranslator."""

        self._all_values = self._calculate_all_possible_values()
        self._randomized_matrix = []

    def _calculate_all_possible_values(self) -> List[int]:
        """Calculate all the possible values of a literal.

        Returns:
            List[int]: the list of all the possible values that a literal can
            assume in ascending order.
        """

        return [
            value + 1
            for value in range(Board.N_ROWS * Board.N_COLS * Board.VALUE_RANGE[1])
        ]

    @property
    def randomized_matrix(self) -> List[List[List[int]]]:
        return self._randomized_matrix

    @property
    def max_problem_variable(self) -> int:
        """Get the max value that a literal can assume."""

        return self._all_values[-1]

    def randomize_values(self) -> None:
        """Randomize every cell value.

        Randomize the literal values assigned to every cell.
        """

        values = self._all_values[:]
        shuffle(values)

        self._randomized_matrix = []
        for i in range(Board.N_ROWS):
            col = []
            for j in range(Board.N_COLS):
                start_index = j * Board.VALUE_RANGE[1] + (
                    i * Board.N_COLS * Board.VALUE_RANGE[1]
                )
                cell = values[start_index : (start_index + Board.VALUE_RANGE[1])]
                col.append(cell)
            self._randomized_matrix.append(col)

    def _cell_to_literal(self, cell: Cell) -> int:
        """Map the given cell into literal.

        Args:
            cell (Cell): cell to map.

        Returns:
            int: the equivalent literal value.
        """

        assert len(self._randomized_matrix) != 0

        return self._randomized_matrix[cell.row][cell.col][cell.value - 1]

    def _literal_to_value(self, row: int, col: int, valid_values: Set[int]) -> int:
        """Map the given cell into a valid matrix value.

        Args:
            row (int): row of the cell.
            col (int): col of the cell.
            valid_values (Set[int]): list of positive literal values for the board.

        Returns:
            int: the equivalent matrix value.
        """

        cell = self._randomized_matrix[row][col]
        trues = [
            value + 1 for value, literal in enumerate(cell) if literal in valid_values
        ]

        if len(trues) == 0:
            return 0
        else:
            return trues[0]

    def translate(self, cell: Cell, valid_values: Set[int] = None) -> int:
        """Perform the translation between literal and cell value.

        Args:
            cell (Cell): cell to translate.
            valid_values (Set[int], optional): contains all the positive
            values of the board. If specified will be performed the translation
            literal->cell and, in this case, the value property of the
            parameter cell wouldn't be considered. Defaults to None.

        Returns:
            int: represent the result of the translation.
        """

        if valid_values is None:
            return self._cell_to_literal(cell)
        else:
            return self._literal_to_value(cell.row, cell.col, valid_values)


class CnfTranslator(Translator):
    """Translator of sudoku boards into CNF formulas.

    This is a Translator of sudoku boards into CNF formulas ready for being
    processed by a sat solver.
    """

    def __init__(self, literal_tr: LiteralTranslator) -> None:
        """Initialize a new BoardTranslator.

        Args:
            literal_tr (LiteralTranslator): trasnslator for literal values to use.
        """

        super().__init__()
        self._literal_tr = literal_tr
        self._board: Board = None
        self.result = CNF()

    @abstractmethod
    def translate(self, board: Board) -> CNF:
        pass


class RulesTranslator(CnfTranslator):
    """Translator of sudoku rules."""

    def __init__(self, literal_tr: LiteralTranslator) -> None:
        super().__init__(literal_tr)

        self._max_literal_value = self._literal_tr.max_problem_variable
        self._literal_tr.randomize_values()

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
            (first, second, var) in to the appropriate order to create a cell.
        """

        for first in range(*range_first):
            for second in range(*range_second):
                # at least one value must be true
                formula = [
                    self._literal_tr.translate(Cell(*map_to_coord(first, second, var)))
                    for var in range(*range_variable)
                ]
                self.result.append(formula)

                # only one value must be true
                card = CardEnc.atmost(
                    lits=formula, top_id=self._max_literal_value, bound=1
                )
                self.result.extend(card.clauses)
                self._max_literal_value = card.nv

    def _values_uniqueness(self) -> None:
        """Add to the result formula constraints for the uniqueness of every value."""

        args = {
            "range_first": (0, self._board.N_ROWS),
            "range_second": (0, self._board.N_COLS),
            "range_variable": self._board.VALUE_RANGE,
            "map_to_coord": lambda x, y, z: (z, x, y),
        }

        self._uniqueness(**args)

    def _columns_constraints(self) -> None:
        """Add to the result formula constraints for the columns values."""

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_COLS),
            "range_variable": (0, self._board.N_ROWS),
            "map_to_coord": lambda x, y, z: (x, z, y),
        }

        self._uniqueness(**args)

    def _rows_constraints(self) -> None:
        """Add to the result formula constraints for the rows values."""

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_ROWS),
            "range_variable": (0, self._board.N_COLS),
            "map_to_coord": lambda x, y, z: (x, y, z),
        }

        self._uniqueness(**args)

    def _squares_constraints(self) -> None:
        """Add to the result formula constraints for the squares values."""

        n_cell_per_side = self._board.N_CELLS_PER_SQUARE_SIDE
        row = lambda square, cell: self._board.square_to_coord(square, cell)[0]
        col = lambda square, cell: self._board.square_to_coord(square, cell)[1]

        args = {
            "range_first": self._board.VALUE_RANGE,
            "range_second": (0, self._board.N_SQUARES),
            "range_variable": (0, n_cell_per_side * n_cell_per_side),
            "map_to_coord": lambda x, y, z: (x, row(y, z), col(y, z)),
        }

        self._uniqueness(**args)

    def translate(self, board: Board) -> CNF:
        """Translate the rules of the given board into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            CNF: a CNF formula equivalent to the rules of the board given.
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

    def _translate_instance(self) -> None:
        """Translate all the values already present in the board into constraints."""

        for cell in self._board.get_cells(used=True):
            self.result.append([self._literal_tr.translate(cell)])

    def translate(self, board: Board) -> CNF:
        """Translate the given game instance into the equivalent CNF formula.

        Args:
            board (Board): board to translate.

        Returns:
            CNF: a CNF formula equivalent to the instance of the board given.
        """

        self._board = board
        self.result = CNF()

        self._translate_instance()

        return self.result


class ResultTranslator(Translator):
    """Translator of sat solver results into sudoku boards."""

    def __init__(self, literal_tr: LiteralTranslator) -> None:
        """Initialize a new ResultTranslator.

        Args:
            literal_tr (LiteralTranslator): trasnslator for literal values to use.
        """

        super().__init__()

        self._literal_tr = literal_tr

    def _translate_sat_result(self) -> List[List[int]]:
        """Translate the sat result into a matrix of numbers.

        Returns:
            List[List[int]]: the matrix equivalent to the sat result given.
        """

        valid_values = [
            value
            for value in self._result
            if value > 0 and value <= self._literal_tr.max_problem_variable
        ]
        valid_values = set(valid_values)

        matrix = []
        for i in range(Board.N_ROWS):
            col = []
            for j in range(Board.N_COLS):
                col.append(self._literal_tr.translate(Cell(0, i, j), valid_values))
            matrix.append(col)

        return matrix

    def translate(self, sat_result: List[int]) -> Board:
        """Translate the given sat result into the equivalent board.

        Args:
            sat_result (List[int]): sat result to translate.

        Returns:
            Board: a board equivalent to the sat result given.
        """

        self._result = sat_result
        self.board = Board.from_matrix(self._translate_sat_result())

        return self.board
