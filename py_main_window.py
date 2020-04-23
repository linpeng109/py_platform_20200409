from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import *

from py_choices_widget import RightWidget
from py_shortcuts import ShortCuts
from py_surpac_widget import SurpacContainerWidget
from py_tab_widget import TabWidget
from py_web_widget import WebEngineView


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
        surpac_process = SurpacContainerWidget(config=config, logger=logger)
        short_cuts = ShortCuts(config=config, logger=logger)
        surpac_cmd_list = short_cuts.getSurpacCmdList()
        surpac_widget = surpac_process.build_surpac_widget(surpac_cmd_list[0])
        surpac_ports = surpac_widget.getPortsFromPid(surpac_widget.surpac_pid)

        # right_widget
        right_widget = RightWidget(config=config, logger=logger, ports=surpac_ports, surpac_widget=surpac_widget)

        # work_widget
        work_widget = QSplitter()
        work_widget.setOrientation(Qt.Horizontal)
        work_widget.addWidget(surpac_widget.surpac_widget)
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

    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()
