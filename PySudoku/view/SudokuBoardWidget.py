from typing import Optional
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QWidget
import PyQt5.QtCore as qtcore
from .. import model


class SudokuCellWidget(QLabel):
    def __init__(self, text: str = "", parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)

        self.setMouseTracking(True)
        self.setFrameShape(QFrame.Shape.Box)
        self.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)


class SudokuSquareWidget(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.Box)
        self._initGrid()

    def _initGrid(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                layout.addWidget(SudokuCellWidget(), i, j)
        self.setLayout(layout)


class SudokuBoardWidget(QFrame):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self._initGrid()

    def _initGrid(self) -> None:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for i in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
            for j in range(model.Board.N_CELLS_PER_SQUARE_SIDE):
                layout.addWidget(SudokuSquareWidget(), i, j)
        self.setLayout(layout)
