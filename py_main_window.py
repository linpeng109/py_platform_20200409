from PySide2.QtCore import QUrl
from PySide2.QtWidgets import *

from py_tab_widget import TabWidget
from py_web_widget import WebEngineView
from py_work_widget import WorkWidget
from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_minesched_widget import MineschedWidget
from py_whittle_widget import Whittle
from py_shortcuts import ShortCuts

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
        index_widget.load(QUrl(config.get('index', 'url')))
        tab_widget.addTabItem(widget=index_widget, item_title='紫金矿业')

        # 构建work_widget界面组件
        self.work_widget = WorkWidget(config=config, logger=logger)
        work_tag_title = config.get('surpac', 'surpac_tag_title')
        tab_widget.addTabItem(widget=self.work_widget, item_title=work_tag_title)

        # treejs_widget
        treejs_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        treejs_widget.load(QUrl(config.get('threejs', 'url')))
        tab_widget.addTabItem(widget=treejs_widget, item_title='三维模型')

        short_cuts = ShortCuts(config=config, logger=logger)

        # minesched_widget
        self.minesched = MineschedWidget(config=config, logger=logger)
        minesched_cmd_list = short_cuts.getMineSchedCmdList()
        self.minesched_widget, self.minesched_pid = self.minesched.build_minesched_widget(minesched_cmd_list[0])
        tab_widget.addTabItem(widget=self.minesched_widget, item_title='MineSched')

        # whittle_widget
        self.whittle = Whittle(config=config, logger=logger)
        whittle_cmd_list = short_cuts.getWhittleCmdList()
        self.whittle_widget, self.whittle_pid = self.whittle.build_whittle_widget(whittle_cmd_list[0])
        tab_widget.addTabItem(widget=self.whittle_widget, item_title='Whittle')

        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        tab_widget.tabBar().setTabButton(1, QTabBar.RightSide, None)

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
            surpac_id = self.work_widget.surpac.surpac_pid
            # 如果surpac已经启动，则清除surpac进程
            if surpac_id > 0:
                self.work_widget.surpac.killProcess([surpac_id])
            super().closeEvent(event)
        else:
            event.ignore()
