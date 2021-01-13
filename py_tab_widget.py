from PySide2.QtWidgets import *


class TabWidget(QTabWidget):
    def __init__(self):
        super(TabWidget, self).__init__()
        # 设置所有页签可以被关闭
        self.setTabsClosable(True)
        self.setDocumentMode(True)
        # 设置所有页签可以移动
        self.setMovable(True)
        # 链接关闭动作函数
        self.tabCloseRequested.connect(self.closeTabItem)

    def addTabItem(self, widget: QWidget, item_title: str, index=-1):
        item_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(50)
        layout.setDirection(QHBoxLayout.LeftToRight)
        layout.addWidget(widget)
        item_widget.setLayout(layout)
        self.addTab(item_widget, item_title)
        self.setCurrentWidget(item_widget)

    def closeTabItem(self, index: int):
        if self.count() > 1:
            self.removeTab(index)
        else:
            self.close()
