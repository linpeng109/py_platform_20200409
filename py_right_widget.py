from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from py_choice_dialog import ChoiceDialog
from py_tree_widget import TreeWidget
from py_shortcuts import ShortCuts


class RightWidget(QWidget):
    def __init__(self, config, logger, ports):
        super(RightWidget, self).__init__()
        self.config = config
        self.logger = logger

        # language_choice_widget
        language_choice_widget = QPushButton('语言')
        language_choice_widget.setFixedSize(80, 30)
        language_choice = ['en', 'cn']
        language_choice_dialog = ChoiceDialog(choices=language_choice, title='选择语言',
                                              callback=self.callback_func_choice_language)
        language_choice_widget.clicked.connect(lambda event: language_choice_dialog.show())

        # surpac_choice_widget
        surpac_choice_widget = QPushButton('Surpac版本')
        surpac_choice_widget.setFixedSize(80, 30)
        surpac_choice = ShortCuts(config=self.config, logger=self.logger).getSurpacCmdList()
        surpac_choice_dialog = ChoiceDialog(choices=surpac_choice, title='选择Surpac',
                                            callback=self.callback_func_choice_surpac)
        # tree_widget
        tree_widget = TreeWidget(config=config, logger=logger, port=ports[0])

        hlayout = QHBoxLayout()
        hlayout.addWidget(surpac_choice_widget)
        hlayout.addWidget(language_choice_widget)
        choices_widget = QWidget()
        choices_widget.setLayout(hlayout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(choices_widget)
        vlayout.addWidget(tree_widget)

        self.setLayout(vlayout)

    def callback_func_choice_language(self, choiced: str):
        print(choiced)

    def callback_func_choice_surpac(self, choiced: str):
        print(choiced)
