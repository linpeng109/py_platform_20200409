import yaml
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidget

from py_thread import TbcRunThread, PyRunThread, TclRunThread


class TreeWidget(QTreeWidget):
    def __init__(self, port, config, logger):
        super(TreeWidget, self).__init__()
        self.config = config
        self.logger = logger
        self.treeWidget = QTreeWidgetItem(self)
        self.port = port
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.onItemClicked)
        self.menus = self.buildMenus()
        self.addTopLevelItem(self.menus)

    def onItemClicked(self, item):
        if (item.text(2)):
            if ('.tbc' in item.text(2)):
                print('tbc script')
                tbcThread = TbcRunThread(port=self.port, item=item)
                tbcThread.start()
                raise ValueError("tbc进程正常终止")
                tbcThread.join()

            if ('.tcl' in item.text(2)):
                tclThread = TclRunThread(port=self.port, item=item)
                tclThread.start()
                raise ValueError("tcl进程正常终止")
                tclThread.join()

            if ('.py' in item.text(2)):
                pyThread = PyRunThread(port=self.port, item=item)
                pyThread.start()
                raise ValueError("py进程正常终止")
                pyThread.join()

    def recursiveBuildMenu(self, root: QTreeWidgetItem, menu_dict: dict):
        for key in menu_dict:
            item = QTreeWidgetItem()
            item_font = QFont()
            item_font.setPointSize(self.config.getint('surpac', 'item_font_size'))
            try:
                text = str(menu_dict[key]['text'])
                item.setText(0, text)
                item.setFont(0, item_font)
            except KeyError:
                pass
            try:
                descript = str(menu_dict[key]['descript'])
                item.setToolTip(0, descript)
            except KeyError:
                pass
            try:
                scl = str(menu_dict[key]['scl'])
                item.setText(2, scl)
            except KeyError:
                pass
            try:
                children = menu_dict[key]['children']
                self.recursiveBuildMenu(item, children)
            except KeyError:
                pass
            root.addChild(item)

    def buildMenus(self):
        surpac_scl_cfg = self.config.get('surpac', 'surpac_scl_cfg')
        surpac_scl_title = self.config.get('surpac', 'surpac_scl_title')
        surpac_scl_encoding = self.config.get('surpac', 'surpac_scl_encoding')
        root = QTreeWidgetItem(self)
        root.setText(0, surpac_scl_title)
        root_font = QFont()
        root_font.setPointSize(self.config.getint('surpac', 'root_font_size'))
        root.setFont(0, root_font)
        root.setExpanded(1)
        with open(file=surpac_scl_cfg, encoding=surpac_scl_encoding) as _f:
            data = yaml.load(_f, yaml.loader.FullLoader)
            self.recursiveBuildMenu(root=root, menu_dict=data)
        return root