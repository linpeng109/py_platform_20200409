from PySide2.QtCore import QUrl, Qt, Slot
from PySide2.QtWidgets import *

from py_choice_surpac_dialog import ChoiceSurpacDialog
from py_communite import SurpacSocketClient, Tbc_script_thread, Tcl_script_thread, Py_script_thread, Fun_script_worker
from py_shortcuts import ShortCuts
from py_surpac_widget import SurpacWidget
from py_tab_widget import TabWidget
from py_tree_widget import TreeWidget
from py_web_widget import WebEngineView


class Work_Widget(QSplitter):
    def __init__(self, config, logger):
        super(Work_Widget, self).__init__()
        self.logger = logger
        self.config = config
        self.setOrientation(Qt.Horizontal)

        # 从快捷方式中获取所有已经安装的surpac的启动命令
        short_cuts = ShortCuts(config=config, logger=logger)

        # 获取surpac命令行列表
        self.surpac_cmd_list = short_cuts.getSurpacCmdList()

        # 构建surpac界面widget
        self.surpac_widget, self.surpac_ports, self.surpac_pid = \
            self.surpac.build_surpac_widget(self.surpac_cmd_list[0])

        # right_widget配置
        right_widget = QWidget()
        right_widget_layout = QVBoxLayout()

        # 构建tree界面widget
        self.tree_widget = TreeWidget(config=config, logger=logger, port=self.surpac_ports[0])
        right_widget_layout.addWidget(self.tree_widget)
        right_widget.setLayout(right_widget_layout)

        # 在工作区中加入surpac和right组件
        self.addWidget(self.surpac_widget)
        self.addWidget(right_widget)

    # 获取surpac配置地址
    def check_surpac_localtion_config(self):
        surpac_localtion=self.config.get


    # 语言选择信号接收槽
    @Slot(str)
    def change_language_listener(self, result):
        self.logger.debug(result)
        self.tree_widget.treeWidget_load(result)
        surpac_socket_client = SurpacSocketClient(logger=self.logger, config=self.config,
                                                  port=self.surpac_ports[0])
        # surpac_socket_client.sendMsg(result)
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
