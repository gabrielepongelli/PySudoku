import sys
import platform
import ctypes
from PyQt5.QtWidgets import QApplication
from .view import MainWindow, QIcon
from .controller import Controller
from .model import Game


APP_NAME = "PySudoku"


class PySudoku(QApplication):
    """Represent the application itself."""

    def __init__(self, sys_argv, config):
        super().__init__(sys_argv)

        self.model = Game()
        self.controller = Controller(self.model)
        self.main_view = MainWindow(config.app_name, self.model, self.controller)

        icon_path = (
            config.app_icon["path"]
            + config.app_icon["name"]
            + config.app_icon["extension"]
        )

        # Necessary in order to make the app icon work prperly on windows
        if platform.system() == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                u"gabrielepongelli.pysudoku.pysudoku.1"
            )

        self.setWindowIcon(QIcon(icon_path))
        self.main_view.setWindowIcon(QIcon(icon_path))

        self.main_view.show()


def main(config):
    """Main funtion to execute in order to run the game."""

    app = PySudoku(sys.argv, config)
    sys.exit(app.exec())
