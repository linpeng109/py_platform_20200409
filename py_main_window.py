from PySide2.QtCore import QUrl, Slot
from PySide2.QtWidgets import *

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_master_widget import MasterWidget
from py_minesched_widget import MineschedWidget
from py_pywin32 import PY_Win32
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
        self.py_win32 = PY_Win32(logger=logger, config=config)
        self.short_cuts = ShortCuts(logger=logger, config=config)

        # tab_widget界面组件
        self.tab_widget = TabWidget()
        font = self.tab_widget.tabBar().font()
        font.setPointSize(18)
        self.tab_widget.tabBar().setFont(font)

        # 构建web_widget界面组件
        web_widget = WebEngineView(config=config, logger=logger, tabWidget=self.tab_widget)
        web_widget.load(QUrl(config.get('web', 'web_url')))
        web_tag_title = config.get('web', 'web_tag_title')
        self.tab_widget.addTabItem(widget=web_widget, item_title=web_tag_title, index=0)
        self.tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # 构建master_widget界面组件
        self.master_widget = MasterWidget(config=config, logger=logger)
        master_tag_title = config.get('master', 'master_tag_title')
        self.tab_widget.addTabItem(widget=self.master_widget, item_title=master_tag_title, index=1)
        # 指定tab不显示关闭按钮
        self.tab_widget.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # threejs_widget
        threejs_widget = WebEngineView(config=config, logger=logger, tabWidget=self.tab_widget)
        threejs_widget.load(QUrl(config.get('threejs', 'threejs_url')))
        threejs_tag_title = config.get('threejs', 'threejs_tag_title')
        self.tab_widget.addTabItem(widget=threejs_widget, item_title=threejs_tag_title, index=2)
        # 指定tab不显示关闭按钮
        self.tab_widget.tabBar().setTabButton(2, QTabBar.RightSide, None)

        # 生成minesched_widget组件
        self.minesched = MineschedWidget(config=self.config, logger=self.logger)
        self.minesched.startMineSchedDialog.start_minesched_signal.connect(self.star_minesched_listener)
        # 检查minesched路径是否配置正确
        self.minesched_cmd_list = []
        if self.minesched.check_minesched_location_config():
            self.minesched_cmd_list = [self.config.get('minesched', 'minesched_location')]
            self.star_minesched_listener(result=self.minesched_cmd_list[0])
        else:
            self.minesched.startMineSchedDialog.setMinescheds(self.short_cuts.getMineSchedCmdList())
            self.minesched.startMineSchedDialog.show()

        # 生成whittle_widget界面组件
        self.whittle = WhittleWidget(config=config, logger=logger)
        self.whittle.startWhittleDialog.start_whittle_signal.connect(self.star_whittle_listener)
        # 检查mwhittle路径是否配置正确
        self.whittle_cmd_list = []
        if self.whittle.check_whittle_location_config():
            self.whittle_cmd_list = [self.config.get('whittle', 'whittle_location')]
            self.star_whittle_listener(result=self.whittle_cmd_list[0])
        else:
            self.whittle.startWhittleDialog.setWhittles(self.short_cuts.getWhittleCmdList())
            self.whittle.startWhittleDialog.show()

        # 指定当前tab
        index_tab = config.getint('default', 'index_tab')
        self.tab_widget.setCurrentIndex(index_tab)

        self.tab_widget.update()

        # 在窗口中央显示tab
        self.setCentralWidget(self.tab_widget)

    @Slot(str)
    def star_minesched_listener(self, result):
        self.minesched_cmd_list = [result]
        self.mineched_widget, self.minesched_pid = self.minesched.build_minesched_widget(self.minesched_cmd_list[0])
        minesched_tag_title = self.config.get('minesched', 'minesched_tag_title')
        self.tab_widget.addTabItem(widget=self.mineched_widget, item_title=minesched_tag_title, index=3)
        self.tab_widget.tabBar().setTabButton(3, QTabBar.RightSide, None)

    @Slot(str)
    def star_whittle_listener(self, result):
        self.whittle_cmd_list = [result]
        self.whittle_widget, self.whittle_pid = self.whittle.build_whittle_widget(self.whittle_cmd_list[0])
        whittle_tag_title = self.config.get('whittle', 'whittle_tag_title')
        self.tab_widget.addTabItem(widget=self.whittle_widget, item_title=whittle_tag_title, index=4)
        self.tab_widget.tabBar().setTabButton(4, QTabBar.RightSide, None)

    # 窗口关闭
    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            # 获取surpac进程id
            surpac_id = self.master_widget.surpac.surpac_pid
            # 如果surpac已经启动，则清除surpac进程
            if surpac_id > 0:
                self.py_win32.killProcess([surpac_id])
            if self.whittle_pid > 0:
                self.py_win32.killProcess([self.whittle_pid])
            if self.minesched_pid > 0:
                self.py_win32.killProcess([self.minesched_pid])
            super().closeEvent(event)
        else:
            event.ignore()
