import sys

from PySide2.QtWidgets import QDialog, QApplication, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox
from PySide2.QtCore import Qt

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_shortcuts import ShortCuts


class ChoiceDialog(QDialog):
    def __init__(self, title: str, choices: list, callback):
        super(ChoiceDialog, self).__init__()
        self.setWindowTitle(title)
        self.callback = callback
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
        super(ChoiceDialog, self).accept()
        self.callback(self.choice_id)

    def choiceChange(self):
        self.choice_id = self.choice_button_group.checkedId()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    config = ConfigFactory(config='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    short_cuts = ShortCuts(config=config, logger=logger)
    surpac_choice = short_cuts.getSurpacCmdList()

    # 定义回调函数
    def callback_func(id):
        print(surpac_choice[id])


    surpac_choice_dialog = ChoiceDialog(choices=surpac_choice, title='选择surpac版本', callback=callback_func)
    surpac_choice_dialog.show()

    sys.exit(app.exec_())
