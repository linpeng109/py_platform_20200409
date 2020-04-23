from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from py_choice_dialog import ChoiceDialog
from py_shortcuts import ShortCuts
from py_surpac_widget import SurpacContainerWidget
from py_tree_widget import TreeWidget


class RightWidget(QWidget):
    def __init__(self, config, logger, ports, surpac_widget: SurpacContainerWidget):
        super(RightWidget, self).__init__()
        self.config = config
        self.logger = logger
        self.ports = ports
        self.surpac_widget = surpac_widget

        # language_choice_widget
        language_choice_button = QPushButton('语言')
        language_choice_button.setFixedSize(120, 30)
        language_choice = ['py_surpac_en.yml', 'py_surpac_cn.yml']
        language_choice_dialog = ChoiceDialog(choices=language_choice, title='选择语言',
                                              callback=self.language_choice_callback_func)
        language_choice_button.clicked.connect(lambda event: language_choice_dialog.show())

        # surpac_choice_widget
        surpac_choice_button = QPushButton('Surpac版本')
        surpac_choice_button.setFixedSize(120, 30)
        surpac_choice = ShortCuts(config=config, logger=logger).getSurpacCmdList()
        surpac_choice_widget_dialog = ChoiceDialog(choices=surpac_choice, title='选择Surpac版本',
                                                   callback=self.surpac_choice_callback_func)
        surpac_choice_button.clicked.connect(lambda event: surpac_choice_widget_dialog.show())

        # tree_widget
        self.tree_widget = TreeWidget(config=config, logger=logger, port=ports[0])
        h_layout = QHBoxLayout()
        h_layout.addWidget(surpac_choice_button)
        h_layout.addWidget(language_choice_button)
        choice_button_group = QWidget()
        choice_button_group.setLayout(h_layout)

        v_layout = QVBoxLayout()
        v_layout.addWidget(choice_button_group)
        v_layout.addWidget(self.tree_widget)

        self.setLayout(v_layout)

    def surpac_choice_callback_func(self, result):
        self.logger.debug(result)
        self.surpac_widget.build_surpac_widget(result)

    def language_choice_callback_func(self, result):
        self.logger.debug(result)
        self.tree_widget.rebuildTreeWidget(surpac_scl_cfg=result, port=self.ports[0])
