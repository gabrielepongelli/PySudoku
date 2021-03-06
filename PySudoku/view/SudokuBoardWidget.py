from typing import Optional
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QWidget
from PyQt5.QtGui import QResizeEvent, QMouseEvent
from PyQt5.QtCore import pyqtSignal
import PyQt5.QtCore as qtcore
from .. import model


class SudokuCellWidget(QLabel):
    """Widget that represent a single Sudoku Cell."""

    mousePressed = pyqtSignal()

    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)

        self.setMouseTracking(True)
        self.setFrameShape(QFrame.Shape.Box)
        self.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)
        self.setAutoFillBackground(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        self.mousePressed.emit()  # emit the correspondent signal


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

        self.cells = []

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                cell = SudokuCellWidget("", self)
                layout.addWidget(cell, i, j)
                self.cells.append(cell)
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

        self.squares = []

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                square = SudokuSquareWidget(self)
                layout.addWidget(square, i, j)
                self.squares.append(square)
        self.setLayout(layout)
