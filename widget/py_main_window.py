from configparser import NoSectionError

from PySide2.QtCore import QUrl, Slot
from PySide2.QtWidgets import *

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_pywin32 import PY_Win32
from util.py_shortcuts import ShortCuts
from widget.py_master_widget import MasterWidget
from widget.py_minesched_widget import MineschedWidget
from widget.py_tab_widget import TabWidget
from widget.py_web_widget import WebEngineView
from widget.py_whittle_widget import WhittleWidget


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
        self.mineched_widget = None
        self.minesched_pid = 0
        self.whittle_widget = None
        self.whittle_pid = 0

        # tab_widget界面组件
        self.tab_widget = TabWidget()
        font = self.tab_widget.tabBar().font()
        font.setPointSize(18)
        self.tab_widget.tabBar().setFont(font)

        # 构建web_widget界面组件
        try:
            web_widget_url: str = config.get('web', 'web_url')
            web_widget = WebEngineView(config=config, logger=logger, tabWidget=self.tab_widget)
            web_widget.load(QUrl(web_widget_url))
            web_tag_title = config.get('web', 'web_tag_title')
            web_widget_index = self.tab_widget.add_tab_item(widget=web_widget, item_title=web_tag_title)
            self.tab_widget.tabBar().setTabButton(web_widget_index, QTabBar.RightSide, None)
        except NoSectionError:
            self.logger.debug("No 'Web Section' Configuration")

        # 构建master_widget界面组件
        try:
            self.master_widget = MasterWidget(config=config, logger=logger)
            master_tag_title = config.get('master', 'master_tag_title')
            master_widget_index = self.tab_widget.add_tab_item(widget=self.master_widget, item_title=master_tag_title)
            self.tab_widget.tabBar().setTabButton(master_widget_index, QTabBar.RightSide, None)
        except NoSectionError:
            self.logger.debug("No 'Master Section' Configuration")

        try:
            threejs_widget_url: str = config.get('threejs', 'threejs_url')
            threejs_widget = WebEngineView(config=config, logger=logger, tabWidget=self.tab_widget)
            threejs_widget.load(QUrl(threejs_widget_url))
            threejs_tag_title = config.get('threejs', 'threejs_tag_title')
            threejs_widget_index = self.tab_widget.add_tab_item(widget=threejs_widget, item_title=threejs_tag_title)
            self.tab_widget.tabBar().setTabButton(threejs_widget_index, QTabBar.RightSide, None)
        except NoSectionError:
            self.logger.debug("No 'Threejs Section' Configuration")

        # 生成minesched_widget组件
        try:
            minesched_location = self.config.get('minesched', 'minesched_location')
            self.minesched = MineschedWidget(config=self.config, logger=self.logger)
            self.minesched.startMineSchedDialog.start_minesched_signal.connect(self.star_minesched_listener)
            # 检查minesched路径是否配置正确
            self.minesched_cmd_list = []
            if self.minesched.check_minesched_location_config():
                self.minesched_cmd_list = [minesched_location]
                self.star_minesched_listener(result=self.minesched_cmd_list[0])
            else:
                self.minesched.startMineSchedDialog.set_minescheds(self.short_cuts.get_minesched_cmd_list())
                self.minesched.startMineSchedDialog.show()
        except NoSectionError:
            self.logger.debug("No 'MineSched Section' Configuration")

        # 生成whittle_widget界面组件
        try:
            whittle_location = self.config.get('whittle', 'whittle_location')
            self.whittle = WhittleWidget(config=config, logger=logger)
            self.whittle.startWhittleDialog.start_whittle_signal.connect(self.star_whittle_listener)
            # 检查mwhittle路径是否配置正确
            self.whittle_cmd_list = []
            if self.whittle.check_whittle_location_config():
                self.whittle_cmd_list = [whittle_location]
                self.star_whittle_listener(result=self.whittle_cmd_list[0])
            else:
                self.whittle.startWhittleDialog.set_whittles(self.short_cuts.get_whittle_cmd_list())
                self.whittle.startWhittleDialog.show()
        except NoSectionError:
            self.logger.debug("No 'Whittle Section' Configuration")

        # 指定当前tab
        index_tab = config.getint('default', 'index_tab')
        self.tab_widget.setCurrentIndex(index_tab)

        self.tab_widget.update()

        # 在窗口中央显示tab
        self.setCentralWidget(self.tab_widget)

    @Slot(str)
    def star_minesched_listener(self, result):
        self.minesched_cmd_list = [result]
        self.mineched_widget, self.minesched_pid = self.minesched.build_minesched_widget(cmd=self.minesched_cmd_list[0])
        minesched_tag_title = self.config.get('minesched', 'minesched_tag_title')
        minesched_widget_index = self.tab_widget.add_tab_item(widget=self.mineched_widget,
                                                              item_title=minesched_tag_title)
        self.tab_widget.tabBar().setTabButton(minesched_widget_index, QTabBar.RightSide, None)

    @Slot(str)
    def star_whittle_listener(self, result):
        self.whittle_cmd_list = [result]
        self.whittle_widget, self.whittle_pid = self.whittle.build_whittle_widget(self.whittle_cmd_list[0])
        whittle_tag_title = self.config.get('whittle', 'whittle_tag_title')
        whittle_widget_index = self.tab_widget.add_tab_item(widget=self.whittle_widget, item_title=whittle_tag_title)
        self.tab_widget.tabBar().setTabButton(whittle_widget_index, QTabBar.RightSide, None)

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
