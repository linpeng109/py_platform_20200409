from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from py_choice_dialog import ChoiceDialog
from py_shortcuts import ShortCuts
from py_surpac import Surpac
from py_tree_widget import TreeWidget


class ChoicesWidget(QWidget):

    def __init__(self, config, logger, ports):
        super(ChoicesWidget, self).__init__()
        self.config = config
        self.logger = logger
        self.ports = ports

        # language_choice_widget
        language_choice_button = QPushButton('语言')
        language_choice_button.setFixedSize(120, 30)
        language_choice = ['py_surpac_en.yml', 'py_surpac_cn.yml']
        self.language_choice_dialog = ChoiceDialog(choices=language_choice, title='选择语言')
        language_choice_button.clicked.connect(lambda event: self.language_choice_dialog.show())

        # surpac_choice_widget
        surpac_choice_button = QPushButton('Surpac版本')
        surpac_choice_button.setFixedSize(120, 30)
        surpac_choice = ShortCuts(config=config, logger=logger).getSurpacCmdList()
        self.surpac_choice_widget_dialog = ChoiceDialog(choices=surpac_choice, title='选择Surpac版本')
        surpac_choice_button.clicked.connect(lambda event: self.surpac_choice_widget_dialog.show())

        h_layout = QHBoxLayout()
        h_layout.addWidget(surpac_choice_button)
        h_layout.addWidget(language_choice_button)

        self.setLayout(h_layout)
