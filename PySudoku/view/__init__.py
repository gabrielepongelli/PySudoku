from typing import Optional, Dict, Tuple, Callable
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QPalette
from .MainWidget import MainWidget
from .DialogWidgets import DifficultyDialog, ResultDialog, WannaSaveDialog
from ..controller import Controller
from ..model import Game, DIFFICULTY_LEVELS


def get_menu_options(controller: Controller) -> Dict:
    """Create a menu containing all the options to show.

    Create a menu containing all the options to show using the actions of the
    controller specified.

    Args:
        controller (Controller): controller to use.

    Returns:
        Menu: the new menu to use.
    """

    menuOptions = {
        "File": {
            "New": controller.start_new_game,
            "Save": controller.save,
            "Open": controller.open,
        },
        "Play": {
            "Hint": controller.hint,
            "Auto-solve": controller.autosolve,
            "Check": controller.check,
        },
    }

    return menuOptions


class MainWindow(QMainWindow):
    """Widget that represent the main window of the application."""

    # Emitted when a key is pressed, pass the code of the key pressed
    keyPressed = pyqtSignal(int)

    # Emitted when a file where to save the game is chosen, pass the file path
    save = pyqtSignal(str)

    # Emitted when a file to load the game is chosen, pass the file path
    load = pyqtSignal(str)

    def __init__(
        self,
        name: str,
        model: Game,
        controller: Controller,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the main window.

        Args:
            name (str): name of the window.
            model (Game): object that model the sudoku game.
            controller (Controller): ibject that manages the user actions.
            parent (Optional[QWidget], optional): parent widget. Defaults to None.
        """

        super().__init__(parent)

        self._model = model
        self._controller = controller
        menu = get_menu_options(self._controller)
        menu_voices = {
            key: [name for name in value.keys()] for key, value in menu.items()
        }
        self._ui = MainWidget(name, menu_voices)
        self._ui.setup(self)
        self._ui.commands.command_buttons["Hint"].setEnabled(False)
        self._ui.commands.command_buttons["Auto-solve"].setEnabled(False)
        self._ui.commands.command_buttons["Check"].setEnabled(False)
        self._cell_selected = None

        menu_commands = {
            key: val for section in menu.values() for key, val in section.items()
        }
        self._connect_signals(menu_commands)

    def _connect_signals(self, menu: Dict[str, Callable]) -> None:
        """Connect all the signals to the appropriate slots.

        Args:
            menu (Dict[str, Callable]): dictionary that contains all the
            button names and the relative action to perform when pressed.
        """

        #### Controller
        # Buttons
        for name, action in menu.items():
            self._ui.commands.command_buttons[name].clicked.connect(action)

        # Cells
        for i, square in enumerate(self._ui.board.squares):
            for j, cell in enumerate(square.cells):
                cell.mousePressed.connect(
                    lambda square=i, cell=j: self.on_cell_clicked(square, cell)
                )

        self.keyPressed.connect(
            lambda value: self._controller.key_pressed(value, self._cell_selected)
        )

        self.save.connect(self._controller.save)
        self.load.connect(self._controller.open)

        #### Model
        self._model.new_game.connect(self.spawn_difficulty_dialog)
        self._model.cell_changed.connect(self.on_cell_changed)
        self._model.is_board_correct.connect(self.spawn_result_dialog)
        self._model.not_saved.connect(self.spawn_save_dialog)
        self._model.load.connect(self.on_load_saved_file)

    def _to_cell_value(self, value: int) -> str:
        """Convert the integer value to the correspondent string.

        Convert the integer value to the correspondent string. If the value is
        0 it will be an empty string, otherwise it will be the value
        represented as a string.

        Args:
            value (int): value to convert. It must be in [0, 9].

        Returns:
            str: the correspondent string representation.
        """

        if value == 0:
            return ""
        else:
            return str(value)

    def _set_cell_color(
        self, square: int, cell: int, selected: bool, editable: bool = False
    ) -> None:
        """Change the cell background color.

        Args:
            square (int): square number of the cell to modify.
            cell (int): cell number of the cell to modify.
            selected (bool): indicate whether the cell specified is selected or not.
            editable (bool, optional): indicate whether the cell specified is
            editable or not. Defaults to False.
        """

        cell = self._ui.board.squares[square].cells[cell]
        palette = cell.palette()
        if selected:  # Selected cell color
            color = palette.highlight().color()
        else:
            if editable:  # Unselected editable cell color
                color = self._ui.palette().window().color()
            else:  # Unselected non-editable cell color
                color = palette.dark().color()

        palette.setColor(QPalette.Background, color)
        cell.setPalette(palette)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self.keyPressed.emit(event.key())  # Emit the correspondent signal

    @pyqtSlot()
    def spawn_difficulty_dialog(self) -> None:
        """Slot that spawn the difficulty dialog.

        Slot that spawn a dialog that let the user choose the difficulty level
        for the new game.
        """

        dialog = DifficultyDialog("Choose difficulty", DIFFICULTY_LEVELS, self)
        dialog.difficultyComboBox.currentTextChanged.connect(
            self._controller.set_difficulty
        )
        dialog.accepted.connect(
            lambda chosen=True: self._controller.start_new_game(chosen)
        )
        dialog.exec()

    @pyqtSlot()
    def on_cell_clicked(self, square: int, cell: int) -> None:
        """Slot that select the cell that was clicked.

        Args:
            square (int): square number of the cell to select.
            cell (int): cell number of the cell to select.
        """

        if self._cell_selected is not None:
            was_editable = self._cell_selected in self._model.editable_values
            self._set_cell_color(*self._cell_selected, False, was_editable)
        self._cell_selected = (square, cell)
        self._set_cell_color(square, cell, True)

    @pyqtSlot(tuple)
    def on_cell_changed(self, coord: Tuple[int, int]) -> None:
        """Slot that update the cell text when its value changes.

        Args:
            coord (Tuple[int, int]): couple of coord (square, cell) of the
            square to update.
        """

        if self._model.board is not None:
            self._ui.commands.command_buttons["Hint"].setEnabled(True)
            self._ui.commands.command_buttons["Auto-solve"].setEnabled(True)
            self._ui.commands.command_buttons["Check"].setEnabled(True)

        square, cell = coord
        self.on_cell_clicked(square, cell)
        self._ui.board.squares[square].cells[cell].setText(
            self._to_cell_value(self._model.board.squares[square][cell].value)
        )

    @pyqtSlot(bool)
    def spawn_result_dialog(self, is_correct: bool) -> None:
        """Slot that spawn the result dialog.

        Slot that spawn a dialog that inform the user if the solution is
        correct or not.

        Args:
            is_correct (bool): indicate whether the solution is correct or not.
        """

        dialog = ResultDialog("Result", is_correct, self)
        dialog.exec()

    @pyqtSlot(bool)
    def spawn_save_dialog(self, spawn: bool) -> None:
        """Slot that spawn the save dialog.

        Slot that spawn a dialog that let the user choose whether to save the
        current game or not and, if yes let it choose the filename and position.

        Args:
            spawn (bool): indicate if the save dialog have to be spawned (True)
            or if the user must directly choose the filename and position
            (False).
        """

        if spawn:
            dialog = WannaSaveDialog("Saving", self)
            dialog.accepted.connect(self.on_select_file_to_save)
            dialog.exec()
        else:
            self.on_select_file_to_save()

    @pyqtSlot()
    def on_select_file_to_save(self) -> None:
        """Slot that let the user choose the filename and position where to
        save the current match."""

        filename = QFileDialog.getSaveFileName(self, "Save", "", "*.sudoku")
        if filename[0]:
            self.save.emit(filename[0])
        else:
            return

    @pyqtSlot()
    def on_load_saved_file(self) -> None:
        """Slot that let the user choose the file to load."""

        filename = QFileDialog.getOpenFileName(self, "Open", "", "*.sudoku")
        if filename[0]:
            self.load.emit(filename[0])
        else:
            return
