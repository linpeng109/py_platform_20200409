from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox
from py_config import ConfigFactory
from py_logging import LoggerFactory


class StartSurpacDialog(QDialog):
    # 定义选择信号
    start_surpac_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str, surpacs: list):
        super(StartSurpacDialog, self).__init__()
        self.config = config
        self.logger = logger

        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.surpacs = surpacs
        self.start_surpac_button_group = QButtonGroup()
        self.start_surpac_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for id, surpac in enumerate(surpacs):
            surpac_item = QRadioButton(surpac)
            self.start_surpac_button_group.addButton(surpac_item)
            self.start_surpac_button_group.setId(surpac_item, id)
            if id == 0:
                surpac_item.setChecked(True)
                self.surpac_id = 0
            layout.addWidget(surpac_item)
        self.start_surpac_button_group.buttonClicked.connect(self.startSurpacChange)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    # 如果单击ok按钮
    def accept(self):
        # 先关闭对话框，然后发送消息
        super(StartSurpacDialog, self).accept()
        self.config.setConfig('surpac', 'surpac_location', self.surpacs[self.surpac_id])
        # 发送surpac启动消息
        self.start_surpac_signal.emit(self.surpacs[self.surpac_id])

    def startSurpacChange(self):
        self.surpac_id = self.start_surpac_button_group.checkedId()
