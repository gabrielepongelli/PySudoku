class SudokuError(Exception):
    """Base exception of the Sudoku package."""

    pass


class InvalidCellValueError(SudokuError, ValueError):
    """Exception raised when trying to set a wrong value to a cell."""

    pass
