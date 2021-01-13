from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QSplitter, QWidget, QVBoxLayout

from py_communite import Surpac_changelanguage_worker
from py_communite import Tbc_script_worker, Tcl_script_worker, Py_script_worker, Fun_script_worker
from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_shortcuts import ShortCuts
from py_surpac_widget import Surpac
from py_tree_widget import TreeWidget


class MasterWidget(QSplitter):

    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        super(MasterWidget, self).__init__()
        self.logger = logger
        self.config = config
        self.setOrientation(Qt.Horizontal)
        self.surpac_ports = None
        self.tree_widget = None
        self.short_cuts = ShortCuts(config=config, logger=logger)

        # 生成surpac_widget界面组件
        self.surpac = Surpac(config=config, logger=logger)
        self.surpac.startSurpacDialog.start_surpac_signal.connect(self.start_surpac_listener)
        # 读取配置文件，检查surpac是否已经正确配置
        self.surpac_cmd_list = []
        if (self.surpac.check_surpac_location_config()):
            self.surpac_cmd_list = [self.config.get('master', 'surpac_location')]
            self.start_surpac_listener(self.surpac_cmd_list[0])
        else:
            # 如果配置不正确，则从系统快捷方式获取surpac命令行列表
            self.surpac.startSurpacDialog.setSurpacs(self.short_cuts.getSurpacCmdList())
            self.surpac.startSurpacDialog.show()

    # 语言选择信号接收槽
    @Slot(str)
    def change_language_listener(self, result):
        self.tree_widget.treeWidget_load(result)
        # 命令与执行脚本对应(待优化)
        if ('_cn' in result):
            client = Surpac_changelanguage_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0],
                                                  msg='test_language_cn.tcl')
            client.start()
        elif ('_en' in result):
            client = Surpac_changelanguage_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0],
                                                  msg='test_language_en.tcl')
            client.start()

    # Surpac启动信号接收槽
    @Slot(str)
    def start_surpac_listener(self, result):
        # 构建surpac界面widget
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(result)

        # Menu_widget配置
        menu_widget = QWidget()
        menu_widget_layout = QVBoxLayout()
        menu_widget.setLayout(menu_widget_layout)

        # 构建tree界面widget
        self.tree_widget = TreeWidget(config=self.config, logger=self.logger, port=self.surpac_ports[0])
        menu_widget_layout.addWidget(self.tree_widget)

        # 将改变surpac版本的消息与surpac更改监听器关联
        self.tree_widget.choice_surpac_dialog.choices_surpac_signal.connect(self.change_surpac_listener)

        # 将改变语言的消息与语言改变监听器关联
        self.tree_widget.choice_language_dialog.choices_language_dialog_signal.connect(self.change_language_listener)
        self.tree_widget.treeItem_func_clicked_signal.connect(self.treeItem_func_clicked_listener)
        self.tree_widget.treeItem_tcl_clicked_signal.connect(self.treeItem_tcl_clicked_listener)
        self.tree_widget.treeItem_tbc_clicked_signal.connect(self.treeItem_tbc_clicked_listener)
        self.tree_widget.treeItem_py_clicked_signal.connect(self.treeItem_py_clicked_listener)

        # 在工作区中加入surpac和menu组件
        self.addWidget(self.surpac_widget)
        self.addWidget(menu_widget)

    # Surpac版本选择信号接收槽
    @Slot(str)
    def change_surpac_listener(self, result):
        self.surpac.py_win32.killProcess([self.surpac_pid])
        self.surpac_widget, self.surpac_ports, self.surpac_pid = self.surpac.build_surpac_widget(result)
        self.replaceWidget(0, self.surpac_widget)

    # 运行func类脚本
    @Slot(str)
    def treeItem_func_clicked_listener(self, result):
        client = Fun_script_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()

    # 运行tcl类脚本
    @Slot(str)
    def treeItem_tcl_clicked_listener(self, result):
        client = Tcl_script_worker(config=self.config, logger=self.logger, port=self.surpac_ports[0], msg=result)
        client.start()

    # 运行tbc类脚本
    @Slot(str)
    def treeItem_tbc_clicked_listener(self, result):
        client = Tbc_script_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()

    # 运行py类脚本
    @Slot(str)
    def treeItem_py_clicked_listener(self, result):
        client = Py_script_worker(logger=self.logger, config=self.config, port=self.surpac_ports[0], msg=result)
        client.start()
