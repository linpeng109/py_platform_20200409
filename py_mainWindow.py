from PySide2.QtCore import QUrl, Qt
from PySide2.QtWidgets import *

from py_tabWidget import TabWidget
from py_web import WebEngineView
from py_surpac import SurpacProcess
from py_shortcuts import ShortCuts
from py_treeWidget import TreeWidget


# 装配主窗口

class MainWindow(QMainWindow):
    def __init__(self, config, logger):
        super(MainWindow, self).__init__()
        self.config = config
        self.logger = logger
        self.setWindowTitle(config.get('surpac', 'title'))
        self.resize(config.getint('surpac', 'width'), config.getint('surpac', 'height'))
        # 初始化tab
        tabWidget = TabWidget()

        # 首页tabwdg
        webWidget = WebEngineView(config=config, logger=logger, tabWidget=tabWidget)
        webWidget.load(QUrl(config.get('surpac', 'url')))
        tabWidget.addTabItem(widget=webWidget, item_title='首页')

        # Surpac
        # 获取surpac安装列表
        short_cuts = ShortCuts(config=config, logger=logger)
        surpac_cmd_list = short_cuts.getSurpacCmdList()
        # 获取surpac处理进程
        surpac_process = SurpacProcess(config=config, logger=logger)
        # 获取已经在运行的surpac进程id
        pids = surpac_process.getPidsFromPName(pname="surpac2")
        # 终止一组surpac进程
        surpac_process.killProcess(pids=pids)
        # 开始新的surpac进程
        pid = surpac_process.startProcess(cmd=surpac_cmd_list[0])
        # 通过pid获取surpac主窗口句柄
        hwnd = surpac_process.getTheMainWindow(pid=pid, spTitle="Surpac")
        # 通过pid获取surpac对外通讯端口
        ports = surpac_process.getPortsFromPid(pid=pid)
        # 将surpac主窗口句柄转换成Widget
        surpac_widget = surpac_process.convertWndToWidget(hwnd=hwnd)
        # 生成树形目录Widget
        treeWidget = TreeWidget(port=ports[0], config=config, logger=logger)
        treeWidget.expandAll()
        # 生成surpac切换按钮
        surpac_select_button = QPushButton('切换Surpac')
        # 装配右侧
        rightWidget = QWidget()
        right_widget_layout = QHBoxLayout()
        right_widget_layout.setDirection(QHBoxLayout.Direction.TopToBottom)
        right_widget_layout.addWidget(surpac_select_button)
        right_widget_layout.addWidget(treeWidget)
        rightWidget.setLayout(right_widget_layout)
        # 生成一个分割容器
        splitterMain = QSplitter()
        # 设置分割方向
        splitterMain.setOrientation(Qt.Horizontal)
        splitterMain.addWidget(surpac_widget)
        splitterMain.addWidget(rightWidget)
        surpac_tag_title = config.get('surpac', 'surpac_tag_title')
        tabWidget.addTabItem(splitterMain, surpac_tag_title)

        # 指定tab不显示关闭按钮
        tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        # 指定当前tab
        tabWidget.setCurrentIndex(0)
        # 在窗口中央显示tab
        self.setCentralWidget(tabWidget)
