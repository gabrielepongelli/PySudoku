from typing import Optional, List
from PyQt5.QtWidgets import (
    QDialog,
    QComboBox,
    QLayout,
    QVBoxLayout,
    QWidget,
    QDialogButtonBox,
)


class DifficultyDialog(QDialog):
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

        self.difficultyComboBox = QComboBox(self)
        self.difficultyComboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.difficultyComboBox.addItems(difficultyLevels)
        self.difficultyComboBox.setCurrentIndex(-1)
        layout.addWidget(self.difficultyComboBox)

        return layout

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

        self._button = QDialogButtonBox()
        self._button.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(self._button)

        return layout
