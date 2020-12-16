from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout

from py_choice_surpac_dialog import ChoiceSurpacDialog
from py_shortcuts import ShortCuts
from py_config import ConfigFactory
from py_logging import LoggerFactory


class ChoicesWidget(QWidget):

    def __init__(self, config: ConfigFactory, logger: LoggerFactory, ports: list):
        super(ChoicesWidget, self).__init__()
        self.config = config
        self.logger = logger
        self.ports = ports

        # language_choice_widget
        language_choice_button = QPushButton('语言')
        language_choice_button.setFixedSize(120, 30)
        language_choice = ['py_surpac_en.yml', 'py_surpac_cn.yml']
        self.language_choice_dialog = ChoiceSurpacDialog(surpacs=language_choice, title='选择语言')
        language_choice_button.clicked.connect(lambda event: self.language_choice_dialog.show())

        # surpac_choice_widget
        surpac_choice_button = QPushButton('Surpac版本')
        surpac_choice_button.setFixedSize(120, 30)
        surpac_choice = ShortCuts(config=config, logger=logger).getSurpacCmdList()
        self.surpac_choice_widget_dialog = ChoiceSurpacDialog(surpacs=surpac_choice, title='选择Surpac版本')
        surpac_choice_button.clicked.connect(lambda event: self.surpac_choice_widget_dialog.show())

        h_layout = QHBoxLayout()
        h_layout.addWidget(surpac_choice_button)
        h_layout.addWidget(language_choice_button)

        self.setLayout(h_layout)
