from PySide2.QtCore import QUrl, Qt, Slot
from PySide2.QtWidgets import *

from py_choices_widget import ChoicesWidget
from py_communite import SurpacSocketClient, Tbc_script_thread, Tcl_script_thread, Py_script_thread, Fun_script_worker
from py_minesched import Minesched
from py_whittle import Whittle
from py_shortcuts import ShortCuts
from py_surpac import Surpac
from py_tab_widget import TabWidget
from py_tree_widget import TreeWidget
from py_web_widget import WebEngineView


# 装配主窗口
class MainWindow(QMainWindow):
    # 初始化
    def __init__(self, config, logger):
        super(MainWindow, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(config.get('default', 'title'))
        self.resize(config.getint('default', 'width'), config.getint('default', 'height'))

        # tab_widget
        tab_widget = TabWidget()

        # index_widget
        index_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        index_widget.load(QUrl(config.get('index', 'url')))
        tab_widget.addTabItem(widget=index_widget, item_title='紫金矿业')

        # treejs_widget
        treejs_widget = WebEngineView(config=config, logger=logger, tabWidget=tab_widget)
        treejs_widget.load(QUrl(config.get('threejs', 'url')))
        tab_widget.addTabItem(widget=treejs_widget, item_title='三维模型')

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
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(surpac_cmd_list[0])

        # minesched_widget
        self.minesched = Minesched(config=config, logger=logger)
        minesched_cmd_list = short_cuts.getMineSchedCmdList()
        self.minesched_widget, self.minesched_pid = self.minesched.build_minesched_widget(minesched_cmd_list[0])
        tab_widget.addTabItem(widget=self.minesched_widget, item_title='MineSched')

        # whittle_widget
        self.whittle = Whittle(config=config, logger=logger)
        whittle_cmd_list = short_cuts.getWhittleCmdList()
        self.whittle_widget, self.whittle_pid = self.whittle.build_whittle_widget(whittle_cmd_list[0])
        tab_widget.addTabItem(widget=self.whittle_widget, item_title='Whittle')

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
        index_tab = config.getint('default', 'index_tab')
        tab_widget.setCurrentIndex(index_tab)

        # 在窗口中央显示tab
        self.setCentralWidget(tab_widget)

        # 选择语言信号与语言选择接收槽链接
        self.choices_widget.language_choice_dialog.choices_signal.connect(self.change_language_listener)

        # Surpac版本选择信号与Surpac版本选择接收槽链接
        self.choices_widget.surpac_choice_widget_dialog.choices_signal.connect(self.change_surpac_listener)

        # 向surpac发送指令
        self.tree_widget.treeItem_func_clicked_signal.connect(self.treeItem_func_clicked_listener)
        self.tree_widget.treeItem_tcl_clicked_signal.connect(self.treeItem_tcl_clicked_listener)
        self.tree_widget.treeItem_tbc_clicked_signal.connect(self.treeItem_tbc_clicked_listener)
        self.tree_widget.treeItem_py_clicked_signal.connect(self.treeItem_py_clicked_listener)

    # 语言选择信号接收槽
    @Slot(str)
    def change_language_listener(self, result):
        self.logger.debug(result)
        self.tree_widget.treeWidget_load(result)
        surpac_socket_client = SurpacSocketClient(logger=self.logger, config=self.config,
                                                  port=self.surpac_ports[0])
        # surpac_socket_client.change_language_script_worker(result)
        surpac_socket_client.closeSocket()

    # Surpac版本选择信号接收槽
    @Slot(str)
    def change_surpac_listener(self, result):
        self.surpac.killProcess([self.surpac_pid])
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(result)
        self.work_widget.replaceWidget(0, self.surpac_widget)

    # func
    @Slot(str)
    def treeItem_func_clicked_listener(self, result):
        client = Fun_script_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()

    # tcl
    @Slot(str)
    def treeItem_tcl_clicked_listener(self, result):
        client = Tcl_script_thread(config=self.config, logger=self.logger, port=self.surpac_ports[0], msg=result)
        client.start()

    # tbc
    @Slot(str)
    def treeItem_tbc_clicked_listener(self, result):
        client = Tbc_script_thread(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()

    # py
    @Slot(str)
    def treeItem_py_clicked_listener(self, result):
        client = Py_script_thread(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()

    # 窗口关闭
    def closeEvent(self, event):
        replay = QMessageBox.question(self, '操作提示', '是否退出应用？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if replay == QMessageBox.Yes:
            event.accept()
            super().closeEvent(event)
        else:
            event.ignore()
