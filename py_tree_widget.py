import yaml
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidget

from py_surpac_communite import TbcRunThread, PyRunThread, TclRunThread


class TreeWidget(QTreeWidget):
    # 初始化
    def __init__(self, port, config, logger):
        super(TreeWidget, self).__init__()
        self.config = config
        self.logger = logger
        surpac_scl_cfg = self.config.get('surpac', 'surpac_scl_cfg')
        self.rebuildTreeWidget(surpac_scl_cfg=surpac_scl_cfg, port=port)

    # 重构Tree组件
    def rebuildTreeWidget(self, surpac_scl_cfg, port):
        self.clear()
        self.treeWidget = QTreeWidgetItem(self)
        self.port = port
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.__on_item_clicked)
        menus = self.__build_toplevel_menu(surpac_scl_cfg=surpac_scl_cfg)
        for item in menus:
            self.addTopLevelItem(item)
            self.setItemExpanded(item, True)

    # 处理Tree单击触发
    def __on_item_clicked(self, item):
        if (item.text(2)):
            if ('.tbc' in item.text(2)):
                print('tbc script')
                tbcThread = TbcRunThread(port=self.port, item=item, config=self.config, logger=self.logger)
                tbcThread.start()
                raise ValueError("tbc进程正常终止")

            if ('.tcl' in item.text(2)):
                tclThread = TclRunThread(port=self.port, item=item, config=self.config, logger=self.logger)
                tclThread.start()
                raise ValueError("tcl进程正常终止")

            if ('.py' in item.text(2)):
                pyThread = PyRunThread(port=self.port, item=item, config=self.config, logger=self.logger)
                pyThread.start()
                raise ValueError("py进程正常终止")

    # 构建Tree组件
    def __build_toplevel_menu(self, surpac_scl_cfg: str):
        # Tree递归构建
        def __build_menu_by_recursive(root: QTreeWidgetItem, menu_dict: dict, expand: bool):
            for key in menu_dict:
                item = QTreeWidgetItem()
                # item.setExpanded(expand)
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
                    __build_menu_by_recursive(item, children, True)
                except KeyError:
                    pass
                root.addChild(item)

        surpac_scl_encoding = self.config.get('surpac', 'surpac_scl_encoding')
        menus = []
        with open(file=surpac_scl_cfg, encoding=surpac_scl_encoding) as _f:
            menu_dict = yaml.load(_f, yaml.loader.FullLoader)
            for key in menu_dict:
                menu_toplevel_item = QTreeWidgetItem()
                menu_toplevel_item_font = QFont()
                menu_toplevel_item_font.setPointSize(self.config.getint('surpac', 'root_font_size'))
                try:
                    text = str(menu_dict[key]['text'])
                    menu_toplevel_item.setText(0, text)
                    menu_toplevel_item.setFont(0, menu_toplevel_item_font)
                except KeyError:
                    pass
                try:
                    descript = str(menu_dict[key]['descript'])
                    menu_toplevel_item.setToolTip(0, descript)
                except KeyError:
                    pass
                try:
                    scl = str(menu_dict[key]['scl'])
                    menu_toplevel_item.setText(2, scl)
                except KeyError:
                    pass
                try:
                    children = menu_dict[key]['children']
                    __build_menu_by_recursive(menu_toplevel_item, children, True)
                except KeyError:
                    pass

            # menu_toplevel_item.setExpanded(True)
            menus.append(menu_toplevel_item)

        return menus
