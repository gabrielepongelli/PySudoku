from typing import Optional, List
from PyQt5.QtWidgets import (
    QDialog,
    QComboBox,
    QLabel,
    QLayout,
    QVBoxLayout,
    QWidget,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
)
import PyQt5.QtCore as qtcore


class SingleOKButtonDialog(QDialog):
    """Generic dialog with a single OK button."""

    def _initButton(self, layout: QLayout = None) -> QLayout:
        """Generate the button that will form this dialog.

        Generate the button that will form this dialog and insert
        it inside a layout.

        Args:
            layout (QLayout): layout in which to place the button. If is None
            will be created a new QVBoxLayout. Defaults to None.

        Returns:
            QLayout: the resulting layout.
        """

        if layout is None:
            layout = QVBoxLayout()

        self._button = QDialogButtonBox(self)
        self._button.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(self._button)

        return layout


class DifficultyDialog(SingleOKButtonDialog):
    """Dialog that allows to choose the difficulty level of the new game."""

    def __init__(
        self, title: str, diffficultyLevels: List[str], parent: Optional[QWidget] = None
    ) -> None:
        """Initialize the new widget.

        Args:
            title (str): title of the dialog.
            diffficultyLevels (List[str]): list that contains all the name of
            difficulty levels to generate.
            parent (Optional[QWidget], optional): parent widget. Defaults to None.
        """

        super().__init__(parent)

        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self._initComboBox(diffficultyLevels, layout)
        self._initButton(layout)
        self.setLayout(layout)

        self._button.accepted.connect(self.accept)

    def _initComboBox(
        self, difficultyLevels: List[str], layout: QLayout = None
    ) -> QLayout:
        """Generate the combobox that will form this dialog.

        Generate the combobox that will form this dialog and insert
        it inside a layout.

        Args:
            difficultyLevels (List[str]): list that contains all the name of
            difficulty levels that the combobox will contain.
            layout (QLayout): layout in which to place the combobox. If is
            None will be created a new QVBoxLayout. Defaults to None.

        Returns:
            QLayout: the resulting layout.
        """

        if layout is None:
            layout = QVBoxLayout()

        frame = QFrame(self)
        hblayout = QHBoxLayout(frame)
        self.label = QLabel("Choose the difficulty: ", frame)

        self.difficultyComboBox = QComboBox(frame)
        self.difficultyComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.difficultyComboBox.addItems(difficultyLevels)
        self.difficultyComboBox.setCurrentIndex(-1)

        hblayout.addWidget(self.label)
        hblayout.addWidget(self.difficultyComboBox)
        frame.setLayout(hblayout)

        layout.addWidget(frame)

        return layout


class ResultDialog(SingleOKButtonDialog):
    """Dialog that communicate whether the sudoku has been solved or not."""

    def __init__(
        self, title: str, result: bool, parent: Optional[QWidget] = None
    ) -> None:
        """Initialize the new widget.

        Args:
            title (str): title of the dialog.
            result (bool): indicate whether the sudoku has been solved or not.
            parent (Optional[QWidget], optional): parent widget. Defaults to None.
        """

        super().__init__(parent)

        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self._initResult(result, layout)
        self._initButton(layout)
        self.setLayout(layout)

        self._button.accepted.connect(self.accept)

    def _initResult(self, result: bool, layout: QLayout = None) -> QLayout:
        """Generate the label containing the result.

        Generate the label containing the result and insert it inside a layout.

        Args:
            result (bool): indicate whether the sudoku has been solved or not.
            layout (QLayout): layout in which to place the combobox. If is
            None will be created a new QVBoxLayout. Defaults to None.

        Returns:
            QLayout: the resulting layout.
        """

        if layout is None:
            layout = QVBoxLayout()

        self.label = QLabel(self)
        if result:
            self.label.setText("Congratulations, you have solved the sudoku!")
        else:
            self.label.setText("Maybe you did something wrong.. better double check.")
        layout.addWidget(self.label)

        return layout


class WannaSaveDialog(QDialog):
    """Dialog that let the user choose whether to save the game or not."""

    def __init__(self, title: str, parent: Optional[QWidget] = None) -> None:
        """Initialize the new widget.

        Args:
            title (str): title of the dialog.
            parent (Optional[QWidget], optional): parent widget. Defaults to None.
        """

        super().__init__(parent)

        self.setWindowTitle(title)
        layout = QVBoxLayout()
        self._initText(layout)
        self._initButtons(layout)
        self.setLayout(layout)

        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

    def _initText(self, layout: QLayout = None) -> QLayout:
        """Generate the label containing the text.

        Generate the label containing the tex and insert it inside a layout.

        Args:
            layout (QLayout): layout in which to place the combobox. If is
            None will be created a new QVBoxLayout. Defaults to None.

        Returns:
            QLayout: the resulting layout.
        """

        if layout is None:
            layout = QVBoxLayout()

        self.label = QLabel("Do you want to save the game?", self)
        self.label.setAlignment(qtcore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        return layout

    def _initButtons(self, layout: QLayout = None) -> QLayout:
        """Generate the buttons that will form this dialog.

        Generate the buttons that will form this dialog and insert
        them inside a layout.

        Args:
            layout (QLayout): layout in which to place the button. If is None
            will be created a new QVBoxLayout. Defaults to None.

        Returns:
            QLayout: the resulting layout.
        """

        if layout is None:
            layout = QVBoxLayout()

        self._buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.No,
            self,
        )

        layout.addWidget(self._buttonBox)

        return layout
