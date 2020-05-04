from PySide2.QtCore import QUrl, Qt, Slot
from PySide2.QtWidgets import *
import multiprocessing
from py_choices_widget import ChoicesWidget
from py_shortcuts import ShortCuts
from py_surpac import Surpac
from py_tab_widget import TabWidget
from py_tree_widget import TreeWidget
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
        self.surpac = Surpac(config=config, logger=logger)
        # 销毁所有surpac2名称的进程
        if (config.get('surpac', 'kill_other_surpac_process')):
            pids = self.surpac.getPidsFromPName('surpac2')
            self.surpac.killProcess(pids)
        else:
            pass

        # 从快捷方式中获取所有已经安装的surpac的启动命令
        short_cuts = ShortCuts(config=config, logger=logger)
        surpac_cmd_list = short_cuts.getSurpacCmdList()
        self.surpac_pid = self.surpac.startProcess(surpac_cmd_list[0])
        surpac_hwnd = self.surpac.getTheMainWindow(pid=self.surpac_pid, spTitle='Surpac')
        self.surpac_ports = self.surpac.getPortsFromPid(self.surpac_pid)
        self.surpac_widget = self.surpac.convertWndToWidget(surpac_hwnd)

        # choices_wigdet
        self.choices_widget = ChoicesWidget(config=config, logger=logger, ports=self.surpac_ports)

        # tree_widget
        self.tree_widget = TreeWidget(config=config, logger=logger, port=self.surpac_ports[0])

        # right_widget
        right_widget = QWidget()
        right_widget_layout = QVBoxLayout()
        right_widget_layout.addWidget(self.choices_widget)
        right_widget_layout.addWidget(self.tree_widget)
        right_widget.setLayout(right_widget_layout)

        # work_widget
        self.work_widget = QSplitter()
        self.work_widget.setOrientation(Qt.Horizontal)
        self.work_widget.addWidget(self.surpac_widget)
        self.work_widget.addWidget(right_widget)

        surpac_tag_title = config.get('surpac', 'surpac_tag_title')
        tab_widget.addTabItem(widget=self.work_widget, item_title=surpac_tag_title)

        # 指定tab不显示关闭按钮
        tab_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        tab_widget.tabBar().setTabButton(1, QTabBar.RightSide, None)

        # 指定当前tab
        tab_widget.setCurrentIndex(0)

        # 在窗口中央显示tab
        self.setCentralWidget(tab_widget)

        # 选择语言信号与语言选择接收槽链接
        self.choices_widget.language_choice_dialog.choices_signal.connect(self.language_choices_listener)
        # self.choices_widget.language_choice_dialog.choices_signal.connect(self.tree_widget.treeWidget_load2)

        # Surpac版本选择信号与Surpac版本选择接收槽链接
        self.choices_widget.surpac_choice_widget_dialog.choices_signal.connect(self.surpac_choices_listener)

    # # 语言选择信号接收槽
    @Slot(str)
    def language_choices_listener(self, result):
        self.logger.debug(result)
        self.tree_widget.treeWidget_load2(result)

    # # Surpac版本选择信号接收槽
    @Slot(str)
    def surpac_choices_listener(self, result):
        self.surpac.killProcess([self.surpac_pid])
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(result)
        self.work_widget.replaceWidget(0, self.surpac_widget)

    # 窗口关闭
    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()
