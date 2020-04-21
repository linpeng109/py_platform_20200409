from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import *

from py_right_widget import RightWidget
from py_shortcuts import ShortCuts
from py_surpac import SurpacProcess
from py_tab_widget import TabWidget
from py_web import WebEngineView


# 装配主窗口
class MainWindow(QMainWindow):
    def __init__(self, config, logger):
        super(MainWindow, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(config.get('surpac', 'title'))
        self.resize(config.getint('surpac', 'width'), config.getint('surpac', 'height'))

        # tab_widget
        tab_widget = TabWidget()

        # web_widget
        web_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        web_widget.load(QUrl(config.get('surpac', 'url')))
        tab_widget.addTabItem(widget=web_widget, item_title='首页')

        # surpac_widget
        surpac_process = SurpacProcess(config=config, logger=logger)
        pids = surpac_process.getPidsFromPName(pname='Surpac')
        surpac_process.killProcess(pids=pids)
        short_cuts = ShortCuts(config=config, logger=logger)
        surpac_cmd_list = short_cuts.getSurpacCmdList()
        surpac_pid = surpac_process.startProcess(surpac_cmd_list[0])
        hwnd = surpac_process.getTheMainWindow(pid=surpac_pid, spTitle='Surpac')
        surpac_widget = surpac_process.convertWndToWidget(hwnd)
        surpac_ports = surpac_process.getPortsFromPid(pid=surpac_pid)

        # right_widget
        right_widget = RightWidget(config=config, logger=logger, ports=surpac_ports, callback_func=self.callback_func)

        # work_widget
        work_widget = QSplitter()
        work_widget.setOrientation(Qt.Horizontal)
        work_widget.addWidget(surpac_widget)
        work_widget.addWidget(right_widget)
        surpac_tag_title = config.get('surpac', 'surpac_tag_title')
        tab_widget.addTabItem(widget=work_widget, item_title=surpac_tag_title)

        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        tab_widget.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # 指定当前tab
        tab_widget.setCurrentIndex(0)

        # 在窗口中央显示tab
        self.setCentralWidget(tab_widget)

    def callback_func(self, id):
        print(id)

    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()
