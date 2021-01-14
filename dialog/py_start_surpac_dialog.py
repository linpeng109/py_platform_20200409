from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory


class StartSurpacDialog(QDialog):
    # 定义选择信号
    start_surpac_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str):
        super(StartSurpacDialog, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.start_surpac_button_group = QButtonGroup()
        self.start_surpac_button_group.setExclusive(True)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

    # 设置Surpac不同版本列表
    def setSurpacs(self, surpacs: list):
        self.surpacs = surpacs
        for id, surpac in enumerate(surpacs):
            surpac_item = QRadioButton(surpac)
            self.start_surpac_button_group.addButton(surpac_item)
            self.start_surpac_button_group.setId(surpac_item, id)
            if id == 0:
                surpac_item.setChecked(True)
                self.surpac_id = 0
            self.layout.addWidget(surpac_item)
        self.start_surpac_button_group.buttonClicked.connect(self.startSurpacChange)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    # 如果单击ok按钮
    def accept(self):
        # 先关闭对话框，然后发送消息
        super(StartSurpacDialog, self).accept()
        self.config.setConfig('master', 'surpac_location', self.surpacs[self.surpac_id])
        # 发送surpac启动消息
        self.start_surpac_signal.emit(self.surpacs[self.surpac_id])

    def startSurpacChange(self):
        self.surpac_id = self.start_surpac_button_group.checkedId()
