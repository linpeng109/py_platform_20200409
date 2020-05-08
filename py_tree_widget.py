import yaml
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidget


class TreeWidget(QTreeWidget):
    # 树形点击定义消息
    treeItem_tbc_clicked_signal = Signal(str)
    treeItem_tcl_clicked_signal = Signal(str)
    treeItem_py_clicked_signal = Signal(str)
    treeItem_func_clicked_signal = Signal(str)

    # 初始化
    def __init__(self, port, config, logger):
        super(TreeWidget, self).__init__()
        self.config = config
        self.logger = logger
        surpac_scl_cfg = self.config.get('surpac', 'surpac_scl_cfg')
        # self.treeWidget_load(surpac_scl_cfg=surpac_scl_cfg, port=port)
        self.treeWidget_load(surpac_scl_cfg=surpac_scl_cfg)

    # 重构Tree组件
    def treeWidget_load(self, surpac_scl_cfg):
        self.clear()
        self.treeWidget = QTreeWidgetItem(self)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.__on_item_clicked2)
        menus = self.__build_toplevel_menu(surpac_scl_cfg=surpac_scl_cfg)
        for item in menus:
            self.addTopLevelItem(item)
            self.setItemExpanded(item, True)

    # 树形菜单单击处理
    def __on_item_clicked2(self, item):
        msg = item.text(2)
        if (msg):
            if '.tbc' in msg:
                self.treeItem_tbc_clicked_signal.emit(msg)
            elif '.tcl' in msg:
                self.treeItem_tcl_clicked_signal.emit(msg)
            elif '.py' in msg:
                self.treeItem_py_clicked_signal.emit(msg)
            else:
                self.treeItem_func_clicked_signal.emit(msg)

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

            menus.append(menu_toplevel_item)

        return menus
