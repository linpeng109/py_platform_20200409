from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import *

from py_surpac import SurpacProcess
from py_tab_widget import TabWidget
from py_tree_widget import TreeWidget
from py_web import WebEngineView
from py_shortcuts import ShortCuts


# 装配主窗口
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
        pids = surpac_process.getPidsFromPName(pname='Surpac')
        surpac_process.killProcess(pids=pids)
        short_cuts = ShortCuts(config=config, logger=logger)
        surpac_cmd_list = short_cuts.getSurpacCmdList()
        surpac_pid = surpac_process.startProcess(surpac_cmd_list[0])
        hwnd = surpac_process.getTheMainWindow(pid=surpac_pid, spTitle='Surpac')
        surpac_widget = surpac_process.convertWndToWidget(hwnd)
        surpac_ports = surpac_process.getPortsFromPid(pid=surpac_pid)

        # Tree
        tree_widget = TreeWidget(config=config, logger=logger, port=surpac_ports[0])
        select_surpac_widget = QPushButton('切换')

        # rightWidget
        right_widget = QWidget()
        right_widget_layout = QVBoxLayout()
        right_widget_layout.addWidget(select_surpac_widget)
        right_widget_layout.addWidget(tree_widget)
        right_widget.setLayout(right_widget_layout)

        # work Widget
        workWidget = QSplitter()
        workWidget.setOrientation(Qt.Horizontal)
        workWidget.addWidget(surpac_widget)
        workWidget.addWidget(right_widget)
        surpac_tag_title = config.get('surpac', 'surpac_tag_title')
        tabWidget.addTabItem(widget=workWidget, item_title=surpac_tag_title)

        # 指定tab不显示关闭按钮
        tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        tabWidget.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # 指定当前tab
        tabWidget.setCurrentIndex(0)

        # 在窗口中央显示tab
        self.setCentralWidget(tabWidget)

    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()
