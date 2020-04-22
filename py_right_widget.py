from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton

from py_choice_dialog import ChoiceDialog
from py_tree_widget import TreeWidget


class RightWidget(QWidget):
    def __init__(self, config, logger, ports, callback_func):
        super(RightWidget, self).__init__()
        self.config = config
        self.logger = logger

        # select_widget
        self.select_widget = QPushButton('切换')
        language_choice = ['en', 'cn']
        # callback_func = lambda id: print(language_choice[id])
        choice_dialog = ChoiceDialog(choices=language_choice, title='选择语言', callback=self.callback_func)
        self.select_widget.clicked.connect(lambda event: choice_dialog.show())

        # tree_widget
        tree_widget = TreeWidget(config=config, logger=logger, port=ports[0])

        layout = QVBoxLayout()
        layout.addWidget(self.select_widget)
        layout.addWidget(tree_widget)

        self.setLayout(layout)

    def callback_func(self, result):
        self.select_widget.setText('aabb')
