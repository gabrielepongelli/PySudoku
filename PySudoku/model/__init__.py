from typing import Tuple, Set
from PyQt5.QtCore import QObject, pyqtSignal
from .sudoku.board import Board
from .sudoku import Sudoku


DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard", "Extreme"]


class Game(QObject):
    """Model that represents the Sudoku Game."""

    # Emitted when a new board is created
    new_game = pyqtSignal()

    # Emitted when the value of a cell is changed, pass the coordinates
    # (square, cell) of the cell modified
    cell_changed = pyqtSignal(tuple)

    # Emitted when the board is checked, pass the result of the control
    is_board_correct = pyqtSignal(bool)

    # Emitted when the board is not saved, pass whether to ask to the user or not
    not_saved = pyqtSignal(bool)

    # Emitted when a board is loaded from a file
    load = pyqtSignal()

    def __init__(self):
        """Initialize the new model."""

        super().__init__()

        self._board = None
        self._editable_values = set()
        self._difficulty = ""
        self._solution = None

    @property
    def board(self) -> Board:
        return self._board

    @board.setter
    def board(self, value: Board) -> None:
        """Set a new board.

        Set the new board, reset the dictionary of editable values, the
        solution, and notify the view.

        Args:
            value (Board): new board to set.
        """

        self._board = value
        self._editable_values = set()
        self._solution = None
        self._notify_view_new_board()

    @property
    def difficulty(self) -> str:
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: str) -> None:
        self._difficulty = value

    @property
    def solution(self) -> Board:
        return self._solution

    @solution.setter
    def solution(self, value: Board) -> None:
        self._solution = value

    @property
    def editable_values(self) -> Set[Tuple[int, int]]:
        return self._editable_values

    def _notify_view_new_board(self) -> None:
        """Notify the view of the whole board."""

        for i, square in enumerate(self._board.squares):
            for j, cell in enumerate(square):
                if cell.value == 0:
                    self._editable_values.add(Board.coord_to_square(cell.row, cell.col))
                self.cell_changed.emit((i, j))

    def change_cell_value(self, value: int, square: int, cell: int) -> None:
        """Modify the value of the cell specified.

        Modify the value of the cell specified and notify the view of the change.

        Args:
            value (int): new value for the cell.
            square (int): square number of the cell to modify.
            cell (int): cell number of the cell to modify.
        """

        row, col = Board.square_to_coord(square, cell)

        if (square, cell) in self._editable_values:
            self._board.rows[row][col].value = value
            self.cell_changed.emit((square, cell))
        else:
            return
