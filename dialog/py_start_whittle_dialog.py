from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory


class StartWhittleDialog(QDialog):
    # 定义选择信号
    start_whittle_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str):
        super(StartWhittleDialog, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.start_whittle_button_group = QButtonGroup()
        self.start_whittle_button_group.setExclusive(True)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

    # 设置Whittle不同版本列表
    def setWhittles(self, whittles: list):
        self.whittles = whittles
        for id, whittle in enumerate(self.whittles):
            whittle_item = QRadioButton(whittle)
            self.start_whittle_button_group.addButton(whittle_item)
            self.start_whittle_button_group.setId(whittle_item, id)
            if id == 0:
                whittle_item.setChecked(True)
                self.whittle_id = 0
            self.layout.addWidget(whittle_item)
        self.start_whittle_button_group.buttonClicked.connect(self.startWhittleChange)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    # 如果单击ok按钮
    def accept(self):
        # 先关闭对话框，然后发送消息
        super(StartWhittleDialog, self).accept()
        self.config.setConfig('whittle', 'whittle_location', self.whittles[self.whittle_id])
        # 发送surpac启动消息
        self.start_whittle_signal.emit(self.whittles[self.whittle_id])

    def startWhittleChange(self):
        self.whittle_id = self.start_whittle_button_group.checkedId()
