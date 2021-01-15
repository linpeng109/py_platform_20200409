from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory


class ChoiceLanguageDialog(QDialog):
    # 定义选择信号
    choices_language_dialog_signal = Signal(str)

    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory, title: str, languages: list):
        super(ChoiceLanguageDialog, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.languages = languages
        self.choice_language_button_group = QButtonGroup()
        self.choice_language_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for language_id, language in enumerate(languages):
            # 显示语言提示
            language_item = QRadioButton(language.split(':')[0])
            self.choice_language_button_group.addButton(language_item)
            self.choice_language_button_group.setId(language_item, language_id)
            if language_id == 0:
                language_item.setChecked(True)
                self.language_id = 0
            layout.addWidget(language_item)
        self.choice_language_button_group.buttonClicked.connect(self.language_change)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def accept(self):
        # 先关闭对话框，然后发送消息
        super(ChoiceLanguageDialog, self).accept()
        # 发送语言文件
        language = self.languages[self.language_id].split(':')[1]
        self.choices_language_dialog_signal.emit(language)
        self.config.set_config('master', 'surpac_language_cfg', language)

    def language_change(self):
        self.language_id = self.choice_language_button_group.checkedId()
