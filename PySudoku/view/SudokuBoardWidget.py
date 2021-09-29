from typing import Optional
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QResizeEvent
import PyQt5.QtCore as qtcore
from .. import model


class SudokuCellWidget(QLabel):
    """Widget that represent a single Sudoku Cell."""

    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)

        self.setMouseTracking(True)
        self.setFrameShape(QFrame.Shape.Box)
        self.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)


class SudokuSquareWidget(QFrame):
    """Widget that represent a square of n*n Sudoku Cells."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.Box)
        self._initGrid()

    def _initGrid(self) -> None:
        """Generate all the Sudoku Cells that will form this widget.

        Generate all the Sudoku Cells that will form this widget and insert
        them inside a grid layout.
        """

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                layout.addWidget(SudokuCellWidget("", self), i, j)
        self.setLayout(layout)


class SudokuBoardWidget(QFrame):
    """Widget that represent a Sudoku Board."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setMinimumSize(100, 100)
        self._initGrid()

    def resizeEvent(self, event: QResizeEvent):
        """Overloaded resizeEvent to make the board a square."""

        new_size = qtcore.QSize(self.minimumWidth(), self.minimumWidth())
        new_size.scale(event.size(), qtcore.Qt.KeepAspectRatio)
        self.resize(new_size)

    def _initGrid(self) -> None:
        """Generate all the squares of Sudoku Cells that will form this widget.

        Generate all the Sudoku Cells that will form this widget and insert
        them inside a grid layout.
        """

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                layout.addWidget(SudokuSquareWidget(self), i, j)
        self.setLayout(layout)
