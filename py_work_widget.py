import os

from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QSplitter, QWidget, QVBoxLayout

from py_communite import SurpacSocketClient, Tbc_script_thread, Tcl_script_thread, Py_script_thread, Fun_script_worker
from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_start_surpac_dialog import StartSurpacDialog
from py_surpac_widget import Surpac
from py_tree_widget import TreeWidget


class WorkWidget(QSplitter):

    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        super(WorkWidget, self).__init__()
        self.logger = logger
        self.config = config
        self.setOrientation(Qt.Horizontal)
        self.surpac_ports = None
        self.tree_widget = None

        # surpac_widget配置
        self.surpac = Surpac(config=config, logger=logger)

        # 销毁所有surpac2名称的进程
        if (config.get('surpac', 'surpac_kill_other_process')):
            pids = self.surpac.getPidsFromPName('surpac2')
            self.surpac.killProcess(pids)

        # 读取配置文件，检查surpac是否已经正确配置
        if (self.check_surpac_location_config()):
            # 如果surpac配置正确，则根据配置文件获取surpac启动命令
            self.surpac_cmd_list = [self.config.get('surpac', 'surpac_location')]
            self.start_surpac_listener(self.surpac_cmd_list[0])
        else:
            # 如果配置不正确，则从系统快捷方式获取surpac命令行列表
            self.surpac_cmd_list = self.surpac.getSurpacCmdList()
            # 弹出对话框选择surpac版本
            self.startSurpacDialog = StartSurpacDialog(logger=self.logger, config=self.config, title='请选择Surpac版本！',
                                                       surpacs=self.surpac_cmd_list)
            self.startSurpacDialog.show()

            # 将启动surpac消息与surpac启动监听器关联
            self.startSurpacDialog.start_surpac_signal.connect(self.start_surpac_listener)

    # 获取surpac配置地址
    def check_surpac_location_config(self):
        surpac_location = self.config.get('surpac', 'surpac_location')
        return os.path.isfile(surpac_location)

    # 语言选择信号接收槽
    @Slot(str)
    def change_language_listener(self, result):
        self.logger.debug(result)
        self.tree_widget.treeWidget_load(result)
        surpac_socket_client = SurpacSocketClient(logger=self.logger, config=self.config,
                                                  port=self.surpac_ports[0])
        surpac_socket_client.closeSocket()

    @Slot(str)
    def start_surpac_listener(self, result):
        # 构建surpac界面widget
        self.surpac_widget, self.surpac_ports, self.surpac_pid = \
            self.surpac.build_surpac_widget(result)

        # right_widget配置
        right_widget = QWidget()
        right_widget_layout = QVBoxLayout()
        right_widget.setLayout(right_widget_layout)

        # 构建tree界面widget
        self.tree_widget = TreeWidget(config=self.config, logger=self.logger, port=self.surpac_ports[0])
        right_widget_layout.addWidget(self.tree_widget)

        # 将改变surpac版本的消息与surpac更改监听器关联
        self.tree_widget.choice_surpac_dialog.choices_surpac_signal.connect(self.change_surpac_listener)

        # 将改变语言的消息与语言改变监听器关联
        self.tree_widget.choice_language_dialog.choices_language_dialog_signal.connect(self.change_language_listener)

        # 在工作区中加入surpac和right组件
        self.addWidget(self.surpac_widget)
        self.addWidget(right_widget)

    # Surpac版本选择信号接收槽
    @Slot(str)
    def change_surpac_listener(self, result):
        self.surpac.killProcess([self.surpac_pid])
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(result)
        self.replaceWidget(0, self.surpac_widget)

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
