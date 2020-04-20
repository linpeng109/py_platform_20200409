from PySide2.QtWidgets import QPushButton
from py_surpac import SurpacProcess

class SurpacButton(QPushButton):
    def __init__(self, config, logger):
        super(SurpacButton, self).__init__()
        self.config=config
        self.logger=logger
        self.connect(self.onclick)

    def onclick(self):

