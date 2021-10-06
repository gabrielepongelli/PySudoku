from typing import Tuple
from random import shuffle
from pickle import dump, load
import PyQt5.QtCore as qtcore
from ..model import Game, Board, Sudoku


class Controller:
    """Main controller of the application."""

    def __init__(self, model: Game) -> None:
        """Initialize a new controller.

        Args:
            model (Game): model that the new controller will have access to.
        """

        self._model = model
        self._filename = ""
        self._is_saved = True

    def open(self, filename: str = ""):
        """Action to perform when the user whant to load a saved game.

        Args:
            filename (str, optional): name of the file to open. Defaults to "".
        """

        if filename:
            self._filename = filename
            try:
                board = load(open(filename, "rb"))
                self._is_saved = True
                self._model.board = board
            except:
                return
        else:
            if not self._is_saved:
                self._model.not_saved.emit(True)
            self._model.load.emit()

    def save(self, filename: str = ""):
        """Action to perform when the user whant to save the current game.

        Args:
            filename (str, optional): name of the file where to save. Defaults
            to "".
        """

        if filename:
            self._filename = filename

        if self._filename:
            self._is_saved = True
            try:
                dump(self._model.board, open(filename, "wb"))
            except:
                return
        else:
            self._model.not_saved.emit(False)

    def set_difficulty(self, difficulty: str = "") -> None:
        """Action to perform when the user select the difficulty level of the new game.

        Args:
            difficulty (str, optional): level of difficulty chosen. Defaults to "".
        """

        self._model.difficulty = difficulty

    def start_new_game(self, is_difficulty_setted: bool = False) -> None:
        """Action to perform when the user start a new game.

        Args:
            is_difficulty_setted (bool, optional): indicate whether the
            difficulty level is already been setted or not. Defaults to False.
        """

        if not self._is_saved:
            self._model.not_saved.emit(True)
            self._is_saved = True
        if is_difficulty_setted and self._model.difficulty != "":
            self._filename = ""
            self._is_saved = False
            self._model.board = Board.from_matrix(
                Sudoku.generate(self._model.difficulty)
            )
        else:
            self._model.new_game.emit()

    def _calculate_solution(self) -> Board:
        """Calculate the correct solution for the current game.

        Returns:
            Board: the solution.
        """

        initial_board = Board.from_matrix(Board.to_matrix(self._model.board.rows))
        for row, col in self._model.editable_values:
            initial_board.rows[row][col].value = 0
        return Board.from_matrix(Sudoku.solve(Board.to_matrix(initial_board.rows)))

    def _get_solution(self) -> Board:
        """Get the solution of the actual board.

        Get the solution of the actual board. If the solution isn't present,
        it will be calculated.

        Returns:
            Board: the solution of the actual board.
        """

        solution = self._model.solution
        if solution is None:
            solution = self._calculate_solution()
            self._model.solution = solution
        return solution

    def autosolve(self):
        """Action to perform when the user want to know the solution."""

        solution = self._get_solution()
        self._model.board = solution

    def hint(self):
        """Action to perform when the user want an hint."""

        possible_hints = self._model.board.get_cells(used=False)
        shuffle(possible_hints)
        solution = self._get_solution()
        for cell in possible_hints:
            correct_value = solution.rows[cell.row][cell.col].value
            if cell.value != correct_value:
                self.key_pressed(
                    ord(str(correct_value)), Board.coord_to_square(cell.row, cell.col)
                )
                return
        return

    def check(self):
        """Action to perform when the user want to check if his solution is
        correct or not."""

        is_correct = self._get_solution() == self._model.board
        self._model.is_board_correct.emit(is_correct)

    def key_pressed(self, value: int, selected_cell: Tuple[int, int]):
        """Action to perform when the user press a key.

        Args:
            value (int): value of the key pressed.
            selected_cell (Tuple[int, int]): coordinates (square, cell) of the
            cell currently selected.
        """

        if selected_cell is None or self._model.board is None:
            return

        if value == qtcore.Qt.Key_Backspace:  # if canc is pressed
            value = ord("0")

        try:
            value = int(chr(value))
        except ValueError:
            return

        self._is_saved = False
        self._model.change_cell_value(value, selected_cell[0], selected_cell[1])
