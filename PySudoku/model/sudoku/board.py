from typing import List, Sequence, Tuple
from math import sqrt
from .utils import InvalidCellValueError


class Cell:
    """Represent a cell of the Sudoku board.

    This class represents a cell of the Sudoku board. It is responsable of the
    control of the value present inside the cell.
    """

    def __init__(self, value: int, row: int, col: int) -> None:
        """Initialize a new Cell.

        Args:
            value (int): new value to put inside this cell. Must be in [0, 9].
            row (int): row number of this cell.
            col (int): col number of this cell.

        Raises:
            InvalidCellValueError: if value not in [0, 9].
        """

        self.value = value
        self.row = row
        self.col = col

    @property
    def value(self) -> int:
        """Get the value inside this cell.

        Returns:
            int: the value inside the cell.
        """

        return self._value

    @value.setter
    def value(self, new_val: int) -> None:
        """Change the value inside the cell.

        Args:
            value (int): new value to put inside this cell. Must be in [0, 9].

        Raises:
            InvalidCellValueError: if value not in [0, 9].
        """

        if new_val < Board.VALUE_RANGE[0] or new_val > Board.VALUE_RANGE[1]:
            raise InvalidCellValueError(
                f"a cell cannot contains values which are not in [{Board.VALUE_RANGE[0]}, {Board.VALUE_RANGE[1]}]."
            )
        else:
            self._value = new_val

    def __eq__(self, other: "Cell") -> bool:
        return self.row == other.row and self.col == other.col

    def __repr__(self) -> str:
        return repr(self._value)


class Board:
    """Represent a sudoku board.

    This class represent a sudoku board. It is responsible for the creation of
    a well defined sudoku board and provides useful methods to access cells.
    A well defined sudoku board is a grid of 9x9 cells.
    """

    N_ROWS = 9
    N_COLS = 9
    N_SQUARES = 9
    VALUE_RANGE = (0, 9)
    N_CELLS_PER_SQUARE_SIDE = int(sqrt((N_ROWS * N_COLS) // N_SQUARES))

    @classmethod
    def from_matrix(cls, matrix: List[List[int]]) -> "Board":
        """Build a Board from the given matrix.

        Args:
            matrix (List[List[int]]): matrix to convert.

        Returns:
            Board: the board equivalent to the matrix specified.
        """

        result = cls()
        board = result.rows
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                cell.value = matrix[i][j]
        return result

    @classmethod
    def empty_board(cls) -> "Board":
        """Build an empty Board.

        Returns:
            Board: the new Board created.
        """

        return cls()

    def __init__(self) -> None:
        """Initialize a new Board."""

        self._rows = []
        self._cols = []
        self._squares = []

        col_per_square = row_per_square = self.N_CELLS_PER_SQUARE_SIDE

        for i in range(0, self.N_ROWS):
            self._rows.append([])
            for j in range(0, self.N_COLS):
                # rows
                cell = Cell(0, i, j)
                self._rows[i].append(cell)

                # cols
                if i == 0:
                    self._cols.append([])
                self._cols[j].append(cell)

                # squares
                if j % col_per_square == 0 and i % row_per_square == 0:
                    self._squares.append([])
                self._squares[
                    (j // col_per_square) + ((i // row_per_square) * col_per_square)
                ].append(cell)

    def get_cells(
        self, used: bool = True, row: int = None, col: int = None
    ) -> List[Cell]:
        """Get some cells of the board.

        Get the used/unused cells of the board. If row or col is specified, the
        cells returned are only those of the specified row/col.

        Args:
            used (bool, optional): specifies whether to obtain all the used
            (True), or unused (False) cells. Defaults to True.
            row (int, optional): filter the used cells to a specific row.
            Defaults to None.
            col (int, optional): filter the used cells to a specific col.
            Defaults to None.

        Returns:
            List[Cell]: the specified cells of this board.
        """

        result = None
        if row is not None:
            result = list(self._rows[row])

        if col is not None:
            if result is not None:
                result = [cell for cell in result if cell.col == col]
            else:
                result = list(self._cols[col])

        test = lambda x: (x.value != 0) if used else (x.value == 0)
        if result is not None:
            result = [cell for cell in result if test(cell)]
        else:
            result = [cell for col in self._rows for cell in col if test(cell)]

        return result

    @staticmethod
    def _copy_matrix(matrix: List[List[object]]) -> List[List[object]]:
        """Create a new matrix."""

        result = []
        for item in matrix:
            result.append(list(item))

        return result

    @property
    def rows(self) -> List[List[Cell]]:
        """Get all the cells by row.

        Returns:
            List[List[Cell]]: all the cells in the order row[ col ].
        """

        return Board._copy_matrix(self._rows)

    @property
    def cols(self) -> List[List[Cell]]:
        """Get all the cells by col.

        Returns:
            List[List[Cell]]: all the cells in the order col[ row ].
        """

        return Board._copy_matrix(self._cols)

    @property
    def squares(self) -> List[List[Cell]]:
        """Get all the cells by squares.

        Get all the cells by squares. Each square is in the format row1, row2, row3.

        Returns:
            List[List[Cell]]: all the cells grouped into squares.
        """

        return Board._copy_matrix(self._squares)

    @staticmethod
    def square_to_coord(square: int, cell: int) -> Tuple[int, int]:
        """Convert a square and a cell number into (row, col) coordinates.

        Args:
            square (int): square number to convert.
            cell (int): cell number inside the square to convert.

        Returns:
            Tuple[int, int]: a pair (row, col) equivalent to the square and
            cell numbers given.
        """

        row = (
            (square // Board.N_CELLS_PER_SQUARE_SIDE) * Board.N_CELLS_PER_SQUARE_SIDE
        ) + (cell // Board.N_CELLS_PER_SQUARE_SIDE)
        col = (
            (square % Board.N_CELLS_PER_SQUARE_SIDE) * Board.N_CELLS_PER_SQUARE_SIDE
        ) + (cell % Board.N_CELLS_PER_SQUARE_SIDE)

        return (row, col)

    @staticmethod
    def coord_to_square(row: int, col: int) -> Tuple[int, int]:
        """Convert (row, col) coordinates into the equivalent (square, cell) couple.

        Args:
            row (int): row to convert.
            col (int): col to convert.

        Returns:
            Tuple[int, int]: square number and cell number equivalent to the
            pair (row, col) given.
        """

        square = (
            (row // Board.N_CELLS_PER_SQUARE_SIDE) * Board.N_CELLS_PER_SQUARE_SIDE
        ) + (col // Board.N_CELLS_PER_SQUARE_SIDE)

        cell = (
            (row % Board.N_CELLS_PER_SQUARE_SIDE) * Board.N_CELLS_PER_SQUARE_SIDE
        ) + (col % Board.N_CELLS_PER_SQUARE_SIDE)

        return (square, cell)

    @staticmethod
    def to_matrix(board: List[List[Cell]]) -> List[List[int]]:
        """Get the matrix representation of the board.

        Args:
            board (List[List[Cell]]): board to be converted into matrix.

        Returns:
            List[List[int]]: the matrix representation.
        """

        result = []
        for row in board:
            result.append([cell.value for cell in row])

        return result

    def __repr__(self) -> str:
        return repr(self._rows)


class BoardTester:
    """Test whether the board specified satisfy all the sudoku rules or not."""

    def __init__(self, board: Board) -> None:
        """Initialize a new BoardTester.

        Args:
            board (Board): board to be tested.
        """

        self.board = board

    @staticmethod
    def _is_cell_value_present(cell: Cell, seq: Sequence[Cell]) -> bool:
        """Check if the cell value is already present in the sequence.

        Args:
            cell (Cell): cell to control.
            seq (Sequence[Cell]): sequence of cell to use for the control.

        Returns:
            bool: True if the cell value is found in seq.
        """

        for c in seq:
            if c.value == cell.value:
                return True
            else:
                continue

        return False

    def _is_val_used_in_row(self, cell: Cell) -> bool:
        """Check whether the cell value is already used in its row or not.

        Args:
            cell (Cell): cell that has to be controlled.

        Returns:
            bool: True if the cell value has been used in its row.
        """

        return BoardTester._is_cell_value_present(cell, self.board.rows[cell.row])

    def _is_val_used_in_column(self, cell: Cell) -> bool:
        """Check whether the cell value is already used in its col or not.

        Args:
            cell (Cell): cell that has to be controlled.

        Returns:
            bool: True if the cell value has been used in its col.
        """

        return BoardTester._is_cell_value_present(cell, self.board.cols[cell.col])

    def _is_val_used_in_square(self, cell: Cell) -> bool:
        """Check whether the cell value is already used in its square or not.

        Args:
            cell (Cell): cell that has to be controlled.

        Returns:
            bool: True if the cell value has been used in its square.
        """

        return BoardTester._is_cell_value_present(
            cell, self.board.squares[self.board.coord_to_square(cell.row, cell.col)[0]]
        )

    def is_cell_correct(self, row: int, col: int, value: int) -> bool:
        """Check whether the cell specified follow the sudoku rules or not.

        Args:
            row (int): row of the cell that has to be controlled.
            col (int): col of the cell that has to be controlled.
            value (int): value of the cell that has to be controlled.

        Returns:
            bool: True if the cell follow the sudoku rules, False otherwise.
        """

        cell = Cell(value, row, col)

        if self._is_val_used_in_row(cell):
            return False
        elif self._is_val_used_in_column(cell):
            return False
        elif self._is_val_used_in_square(cell):
            return False
        return True
