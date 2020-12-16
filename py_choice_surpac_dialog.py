from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox

from py_config import ConfigFactory
from py_logging import LoggerFactory


class ChoiceSurpacDialog(QDialog):
    # 定义选择信号
    choices_surpac_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str, surpacs: list):
        super(ChoiceSurpacDialog, self).__init__()
        self.config = config
        self.logger = logger

        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.surpacs = surpacs
        self.choice_surpac_button_group = QButtonGroup()
        self.choice_surpac_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for id, choice in enumerate(surpacs):
            surpac_item = QRadioButton(choice)
            self.choice_surpac_button_group.addButton(surpac_item)
            self.choice_surpac_button_group.setId(surpac_item, id)
            if id == 0:
                surpac_item.setChecked(True)
                self.surpac_id = 0
            layout.addWidget(surpac_item)
        self.choice_surpac_button_group.buttonClicked.connect(self.choiceSurpacChange)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def accept(self):
        # 先关闭对话框，然后发送消息
        super(ChoiceSurpacDialog, self).accept()
        self.choices_surpac_signal.emit(self.surpacs[self.surpac_id])
        print("********")

    def choiceSurpacChange(self):
        self.surpac_id = self.choice_surpac_button_group.checkedId()
