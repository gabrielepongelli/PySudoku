import sys
from PyQt5.QtWidgets import QApplication
from .view import MainWindow
from .controller import Controller
from .model import Game


APP_NAME = "PySudoku"


class PySudoku(QApplication):
    """Represent the application itself."""

    def __init__(self, sys_argv):
        super().__init__(sys_argv)

        self.model = Game()
        self.controller = Controller(self.model)
        self.main_view = MainWindow(APP_NAME, self.model, self.controller)
        self.main_view.show()


def main():
    """Main funtion to execute in order to run the game."""

    app = PySudoku(sys.argv)
    sys.exit(app.exec())
