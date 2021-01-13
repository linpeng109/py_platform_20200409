from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox
from py_config import ConfigFactory
from py_logging import LoggerFactory


class StartMineSchedDialog(QDialog):
    # 定义选择信号

    start_minesched_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str, minescheds: list):
        super(StartMineSchedDialog, self).__init__()
        self.config = config
        self.logger = logger

        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.minescheds = minescheds
        self.start_minesched_button_group = QButtonGroup()
        self.start_minesched_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for id, minesched in enumerate(minescheds):
            minesched_item = QRadioButton(minesched)
            self.start_minesched_button_group.addButton(minesched_item)
            self.start_minesched_button_group.setId(minesched_item, id)
            if id == 0:
                minesched_item.setChecked(True)
                self.minesched_id = 0
            layout.addWidget(minesched_item)
        self.start_minesched_button_group.buttonClicked.connect(self.startMineSchedChange)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    # 如果单击ok按钮
    def accept(self):
        # 先关闭对话框，然后发送消息
        super(StartMineSchedDialog, self).accept()
        self.config.setConfig('minesched', 'minesched_location', self.minescheds[self.minesched_id])
        # 发送surpac启动消息
        self.start_minesched_signal.emit(self.minescheds[self.minesched_id])

    def startMineSchedChange(self):
        self.minesched_id = self.start_minesched_button_group.checkedId()