from PySide2.QtCore import QUrl
from PySide2.QtWidgets import *

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_master_widget import MasterWidget
from py_minesched_widget import MineschedWidget
from py_shortcuts import ShortCuts
from py_tab_widget import TabWidget
from py_web_widget import WebEngineView
from py_whittle_widget import WhittleWidget


# 装配主窗口
class MainWindow(QMainWindow):
    # 初始化
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        super(MainWindow, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(config.get('default', 'title'))
        self.resize(self.config.getint('default', 'width'), self.config.getint('default', 'height'))

        # tab_widget界面组件
        tab_widget = TabWidget()

        # 构建index_widget界面组件
        index_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        index_widget.load(QUrl(config.get('index', 'index_url')))
        index_tag_title = config.get('index', 'index_tag_title')
        tab_widget.addTabItem(widget=index_widget, item_title=index_tag_title, index=0)
        tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # 构建master_widget界面组件
        self.master_widget = MasterWidget(config=config, logger=logger)
        master_tag_title = config.get('surpac', 'surpac_tag_title')
        tab_widget.addTabItem(widget=self.master_widget, item_title=master_tag_title, index=1)
        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # treejs_widget
        treejs_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        treejs_widget.load(QUrl(config.get('threejs', 'threejs_url')))
        threejs_tag_title = config.get('threejs', 'threejs_tag_title')
        tab_widget.addTabItem(widget=treejs_widget, item_title=threejs_tag_title, index=2)
        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(2, QTabBar.RightSide, None)

        # short_cuts = ShortCuts(config=config, logger=logger)

        # minesched_widget
        self.minesched = MineschedWidget(config=config, logger=logger)
        # minesched_cmd_list = short_cuts.getMineSchedCmdList()
        minesched_cmd_list = []
        minesched_cmd_list.append(config.get('minesched', 'minesched_location'))
        self.minesched_widget, self.minesched_pid = self.minesched.build_minesched_widget(minesched_cmd_list[0])
        minesched_tag_title = config.get('minesched', 'minesched_tag_title')
        tab_widget.addTabItem(widget=self.minesched_widget, item_title=minesched_tag_title, index=3)
        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(3, QTabBar.RightSide, None)

        # whittle_widget
        self.whittle = WhittleWidget(config=config, logger=logger)
        # whittle_cmd_list = short_cuts.getWhittleCmdList()
        whittle_cmd_list = []
        whittle_cmd_list.append(config.get('whittle', 'whittle_location'))
        self.whittle_widget, self.whittle_pid = self.whittle.build_whittle_widget(whittle_cmd_list[0])
        whittle_tag_title = config.get('whittle', 'whittle_tag_title')
        tab_widget.addTabItem(widget=self.whittle_widget, item_title=whittle_tag_title, index=4)
        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(4, QTabBar.RightSide, None)

        # 指定当前tab
        index_tab = config.getint('default', 'index_tab')
        tab_widget.setCurrentIndex(index_tab)

        # 在窗口中央显示tab
        self.setCentralWidget(tab_widget)

    # 窗口关闭
    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            # 获取surpac进程id
            surpac_id = self.master_widget.surpac.surpac_pid
            # 如果surpac已经启动，则清除surpac进程
            if surpac_id > 0:
                self.master_widget.surpac.killProcess([surpac_id])
            if self.whittle_pid > 0:
                self.whittle.killProcess([self.whittle_pid])
            if self.minesched_pid > 0:
                self.minesched.killProcess([self.minesched_pid])
            super().closeEvent(event)
        else:
            event.ignore()
