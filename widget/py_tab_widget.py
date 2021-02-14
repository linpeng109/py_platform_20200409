from PySide2.QtWidgets import *

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory


class TabWidget(QTabWidget):
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        super(TabWidget, self).__init__()
        self.config = config
        self.logger = logger
        # 设置所有页签可以被关闭
        self.setTabsClosable(True)
        self.setDocumentMode(True)
        # 设置所有页签可以移动
        self.setMovable(True)
        # 设置tab字体
        font = self.tabBar().font()
        font.setPointSize(self.config.getint('default', 'tab_font_size'))
        self.tabBar().setFont(font)
        # 链接关闭动作函数
        self.tabCloseRequested.connect(self.close_tab_item)

    def add_tab_item(self, widget: QWidget, item_title: str) -> int:
        item_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(50)
        layout.setDirection(QHBoxLayout.LeftToRight)
        layout.addWidget(widget)
        item_widget.setLayout(layout)
        self.addTab(item_widget, item_title)
        self.setCurrentWidget(item_widget)
        return self.indexOf(item_widget)

    def close_tab_item(self, index: int):
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.close()
