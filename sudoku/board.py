from typing import List


class SudokuError(Exception):
    """Base exception of the Sudoku package."""

    pass


class InvalidCellValueError(SudokuError, ValueError):
    """Exception raised when trying to set a wrong value to a cell."""

    pass


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

        if new_val < 0 or new_val > 9:
            raise InvalidCellValueError(
                "a cell cannot contains values which are not in [0, 9]."
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

    @classmethod
    def from_matrix(cls, matrix: List[List[int]]) -> "Board":
        """Build a Board from the given matrix.

        Args:
            matrix (List[List[int]]): matrix to convert.

        Returns:
            Board: the board equivalent to the matrix specified.
        """

        result = cls()
        board = result.rows()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                cell.value = matrix[i][j]
        return result

    @classmethod
    def standard_board(cls) -> "Board":
        pass

    def __init__(self, rows: int, col: int) -> None:
        """Initialize a new Board."""

        self.N_ROWS = 9
        self.N_COLS = 9
        self.N_SQUARES = 9
        self.VALUE_RANGE = (0, 9)

        self._rows = []
        self._cols = []
        self._squares = []

        for i in range(0, 9):
            self._rows.append([])
            for j in range(0, 9):
                # rows
                cell = Cell(0, i, j)
                self._rows[i].append(cell)

                # cols
                if i == 0:
                    self._cols.append([])
                self._cols[j].append(cell)

                # squares
                if j % 3 == 0 and i % 3 == 0:
                    self._squares.append([])
                self._squares[(j // 3) * ((i // 3) + 1)].append(cell)

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

    def rows(self) -> List[List[Cell]]:
        """Get all the cells by row.

        Returns:
            List[List[Cell]]: all the cells in the order row[ col ].
        """

        return Board._copy_matrix(self._rows)

    def cols(self) -> List[List[Cell]]:
        """Get all the cells by col.

        Returns:
            List[List[Cell]]: all the cells in the order col[ row ].
        """

        return Board._copy_matrix(self._cols)

    def squares(self) -> List[List[Cell]]:
        """Get all the cells by squares.

        Get all the cells by squares. Each square is in the format row1, row2, row3.

        Returns:
            List[List[Cell]]: all the cells grouped into squares.
        """

        return Board._copy_matrix(self._squares)

    def to_matrix(self) -> List[List[int]]:
        """Get the matrix representation of the board.

        Returns:
            List[List[int]]: the matrix representation.
        """

        result = []
        for row in self._rows:
            result.append([cell.value for cell in row])

        return result

    def __repr__(self) -> str:
        return str(self._rows)
