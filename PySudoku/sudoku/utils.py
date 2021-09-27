class SudokuError(Exception):
    """Base exception of the Sudoku package."""

    pass


class InvalidCellValueError(SudokuError, ValueError):
    """Exception raised when trying to set a wrong value to a cell."""

    pass


class NoSolutionError(SudokuError):
    """Exception raised when a board has no solutions."""

    pass


class InvalidDifficultyError(SudokuError, ValueError):
    """Exception raised when trying to create a new board with a wrong difficulty."""

    pass


class InvalidMatrixError(SudokuError, ValueError):
    """Exception raised when trying to solve a malformed matrix."""

    pass
