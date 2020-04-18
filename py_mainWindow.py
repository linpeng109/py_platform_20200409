from PySide2.QtCore import QUrl
from PySide2.QtWidgets import *

from py_tabWidget import TabWidget
from py_web import WebEngineView
from py_surpac import SurpacProcess


class MainWindow(QMainWindow):
    def __init__(self, config, logger):
        super(MainWindow, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(config.get('surpac', 'title'))
        self.resize(config.getint('surpac', 'width'), config.getint('surpac', 'height'))
        # 初始化tab
        tabWidget = TabWidget()

        # 首页tabwdg
        webWidget = WebEngineView(config=config, logger=logger, tabWidget=tabWidget)
        webWidget.load(QUrl(config.get('surpac', 'url')))
        tabWidget.addTabItem(widget=webWidget, item_title='首页')

        # Surpac
        surpac_process = SurpacProcess(config=config, logger=logger)


        # 指定tab不显示关闭按钮
        tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        # 指定当前tab
        tabWidget.setCurrentIndex(0)
        # 在窗口中央显示tab
        self.setCentralWidget(tabWidget)
