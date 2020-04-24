import sys

from PySide2.QtWidgets import QDialog, QApplication, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox
from PySide2.QtCore import Qt, Slot, Signal

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_shortcuts import ShortCuts


class ChoiceDialog(QDialog):
    # 定义选择信号
    choices_signal = Signal(str)

    # 初始化
    def __init__(self, title: str, choices: list):
        super(ChoiceDialog, self).__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.choices = choices
        self.choice_button_group = QButtonGroup()
        self.choice_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for id, choice in enumerate(choices):
            rb = QRadioButton(choice)
            self.choice_button_group.addButton(rb)
            self.choice_button_group.setId(rb, id)
            if id == 0:
                rb.setChecked(True)
                self.choice_id = 0
            layout.addWidget(rb)
        self.choice_button_group.buttonClicked.connect(self.choiceChange)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def accept(self):
        self.choices_signal.emit(self.choices[self.choice_id])
        super(ChoiceDialog, self).accept()

    def choiceChange(self):
        self.choice_id = self.choice_button_group.checkedId()
