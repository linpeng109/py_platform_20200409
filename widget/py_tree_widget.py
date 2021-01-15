import yaml
from PySide2.QtCore import Signal
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QTreeWidgetItem, QTreeWidget

from dialog.py_choice_language_dialog import ChoiceLanguageDialog
from dialog.py_choice_surpac_dialog import ChoiceSurpacDialog
from util.py_path import Path
from util.py_shortcuts import ShortCuts


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
        surpac_scl_cfg = self.config.get('master', 'surpac_language_cfg')
        self.treeWidget_load(surpac_scl_cfg=surpac_scl_cfg)
        self.shortcut = ShortCuts(config=self.config, logger=self.logger)
        surpacs = self.shortcut.get_surpac_cmd_list()
        self.choice_surpac_dialog = ChoiceSurpacDialog(config=self.config, logger=self.logger, title='请选择Surpac版本',
                                                       surpacs=surpacs)
        surpac_languages = str(self.config.get('master', 'surpac_languages')).split(';')
        self.choice_language_dialog = ChoiceLanguageDialog(config=config, logger=logger, title="请选择Surpac语言",
                                                           languages=surpac_languages)

    # 重构Tree组件
    def treeWidget_load(self, surpac_scl_cfg):
        self.clear()
        self.treeWidget = QTreeWidgetItem(self)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.__on_item_clicked)

        # 加入相对路径，处理pyinstaller打包后yml导入错误问题
        self.scl_path = Path.get_resource_path(surpac_scl_cfg)

        # 加入menu菜单配置yml文件
        menus = self.build_toplevel_menu(surpac_scl_cfg=self.scl_path)
        for item in menus:
            self.addTopLevelItem(item)
            self.setItemExpanded(item, True)

    # 树形菜单单击处理
    def __on_item_clicked(self, item):
        #
        print(item.text(2))
        print('==========插入读取软件锁代码============')
        #
        msg = item.text(2)
        if (msg):
            if '.tbc' in msg:
                self.treeItem_tbc_clicked_signal.emit(msg)
            elif '.tcl' in msg:
                self.treeItem_tcl_clicked_signal.emit(msg)
            elif '.py' in msg:
                self.treeItem_py_clicked_signal.emit(msg)
            elif 'choice_surpac' in msg:
                self.choice_surpac_dialog.show()
            elif 'choice_language' in msg:
                self.choice_language_dialog.show()
            else:
                self.treeItem_func_clicked_signal.emit(msg)

    # 构建Tree组件
    def build_toplevel_menu(self, surpac_scl_cfg: str):
        # Tree递归构建
        def build_menu_by_recursive(root: QTreeWidgetItem, menu_dict: dict):
            for key in menu_dict:
                item = QTreeWidgetItem()

                item_font = QFont()
                item_font.setPointSize(self.config.getint('master', 'master_item_font_size'))
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
                    build_menu_by_recursive(item, children)
                except KeyError:
                    pass
                try:
                    expanded = menu_dict[key]['expanded']
                    item.setExpanded(expanded)
                except KeyError:
                    pass

                root.addChild(item)

        surpac_scl_encoding = self.config.get('master', 'surpac_scl_encoding')
        menus = []
        with open(file=surpac_scl_cfg, encoding=surpac_scl_encoding) as _f:
            menu_dict = yaml.load(_f, yaml.loader.FullLoader)
            for key in menu_dict:
                menu_toplevel_item = QTreeWidgetItem()
                menu_toplevel_item_font = QFont()
                menu_toplevel_item_font.setPointSize(self.config.getint('master', 'master_root_font_size'))

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
                    expanded = menu_dict[key]['expanded']
                    menu_toplevel_item.setExpanded(expanded)
                except KeyError:
                    pass

                try:
                    children = menu_dict[key]['children']
                    build_menu_by_recursive(menu_toplevel_item, children)
                except KeyError:
                    pass

            menus.append(menu_toplevel_item)

        return menus
