from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QDialog, QButtonGroup, QVBoxLayout, QRadioButton, QDialogButtonBox


class ChoiceLanguageDialog(QDialog):
    # 定义选择信号
    choices_language_dialog_signal = Signal(str)

    # 初始化
    def __init__(self, title: str, languages: list):
        super(ChoiceLanguageDialog, self).__init__()
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.languages = languages
        self.choice_language_button_group = QButtonGroup()
        self.choice_language_button_group.setExclusive(True)
        layout = QVBoxLayout()
        for id, language in enumerate(languages):
            language_item = QRadioButton(language)
            self.choice_language_button_group.addButton(language_item)
            self.choice_language_button_group.setId(language_item, id)
            if id == 0:
                language_item.setChecked(True)
                self.language_id = 0
            layout.addWidget(language_item)
        self.choice_language_button_group.buttonClicked.connect(self.languageChange)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def accept(self):
        # 先关闭对话框，然后发送消息
        super(ChoiceLanguageDialog, self).accept()
        self.choices_language_dialog_signal.emit(self.languages[self.language_id])

    def languageChange(self):
        self.language_id = self.choice_language_button_group.checkedId()
