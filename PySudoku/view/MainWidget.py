from typing import Optional
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from .SudokuBoardWidget import SudokuBoardWidget
from .CommandWidget import CommandWidget, Menu


class MainWidget(QWidget):
    """Main widget of the application."""

    APP_MIN_SIZE = (526, 400)

    def __init__(
        self,
        title: str,
        menu: Menu,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the new widget.

        Args:
            title (str): title of the window.
            menu (Menu): menu that contains all the sections of button titles
            to generate.
            parent (Optional[QWidget], optional): parent widget. Defaults to None.
        """
        super().__init__(parent)

        self._title = title
        self.setMinimumSize(*self.APP_MIN_SIZE)
        self._fill_widget(menu)

    def setup(self, mainWindow: QMainWindow) -> None:
        """Setup this widget and the main window that will contain it.

        Args:
            mainWindow (QMainWindow): main window that will contain this widget.
        """

        mainWindow.setWindowTitle(self._title)
        mainWindow.setCentralWidget(self)

    def _fill_widget(self, menu: Menu) -> None:
        """Generate the content of this widget.

        Args:
            menu (Menu): menu that contains all the sections of button titles
            to generate.
        """

        self.horizontalLayout = QHBoxLayout(self)

        self.commands = CommandWidget(menu, self)
        self.horizontalLayout.addWidget(self.commands)

        self.board = SudokuBoardWidget(self)
        self.horizontalLayout.addWidget(self.board)

        self.horizontalLayout.setStretch(1, 3)
        self.setLayout(self.horizontalLayout)
