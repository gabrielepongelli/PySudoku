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

        Raises:
            InvalidCellValueError: if value not in [0, 9].
        """
        pass

    @property
    def value(self) -> int:
        """Get the value inside this cell.

        Returns:
            int: the value inside the cell.
        """
        pass

    @value.setter
    def value(self, new_val: int) -> None:
        """Change the value inside the cell.

        Args:
            value (int): new value to put inside this cell. Must be in [0, 9].

        Raises:
            InvalidCellValueError: if value not in [0, 9].
        """
        pass

    def __repr__(self) -> str:
        pass


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

    def __init__(self) -> None:
        """Initialize a new Board."""
        pass

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
        pass

    def rows(self) -> List[List[Cell]]:
        """Get all the cells by row.

        Returns:
            List[List[Cell]]: all the cells in the order row[ col ].
        """
        pass

    def cols(self) -> List[List[Cell]]:
        """Get all the cells by col.

        Returns:
            List[List[Cell]]: all the cells in the order col[ row ].
        """
        pass

    def squares(self) -> List[List[Cell]]:
        """Get all the cells by squares.

        Get all the cells by squares. Each square is in the format row1, row2, row3.

        Returns:
            List[List[Cell]]: all the cells grouped into squares.
        """
        pass

    def to_matrix(self) -> List[List[int]]:
        """Get the matrix representation of the board.

        Returns:
            List[List[int]]: the matrix representation.
        """
        pass

    def __repr__(self) -> str:
        pass


class Solver:
    """Represent a Sudoku Solver.

    This class represent a Sudoku Solver. It is responsable for the generation
    of the solutions of a sudoku board.
    """

    def __init__(self, board: Board) -> None:
        """Initialize a new Solver.

        Args:
            grid (Board): board to solve.
        """
        pass

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
        pass

    def __iter__(self):
        """Iterate through all the possible solutions for the board."""
        pass

    def __repr__(self):
        pass
