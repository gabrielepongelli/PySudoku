from typing import Optional, Dict, List, NewType
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)


Section = NewType("Section", List[str])
Menu = NewType("Menu", Dict[str, Section])


class CommandWidget(QWidget):
    """Widget that contain all the UI elements that trigger commands."""

    def __init__(
        self,
        commands: Menu,
        parent: Optional["QWidget"] = None,
    ) -> None:
        """Initialize the widget.

        Args:
            commands (Menu): menu that will be transformed into buttons.
            parent (Optional[, optional): parent widget. Defaults to None.
        """

        super().__init__(parent)

        self._commands = commands
        layout = self._generateButtons()
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)
        self.setLayout(layout)

    def _generateButtons(self) -> QVBoxLayout:
        """Generate all the buttons that will form this widget.

        Generate all the buttons that will form this widget and insert
        them inside a vertical box layout.

        Returns:
            QVBoxLayout: the resulting layout.
        """

        self.command_buttons = {}
        verticalLayout = QVBoxLayout()

        for n, section in enumerate(self._commands.values()):
            for name in section:
                button = QPushButton(name, self)
                verticalLayout.addWidget(button)
                self.command_buttons[name] = button
            if n != len(self._commands) - 1:
                separator = QFrame(self)
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                verticalLayout.addWidget(separator)

        return verticalLayout
