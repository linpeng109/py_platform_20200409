import multiprocessing
import os
import sys

from PySide2.QtGui import QIcon, Qt, QPixmap
from PySide2.QtWidgets import QApplication, QSplashScreen

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_main_window import MainWindow
from py_minesched_widget import MineschedWidget
from py_whittle_widget import Whittle
from py_path import Path

if __name__ == '__main__':

    # win环境编译时应用，解决win环境mutilprocess的fork兼容问题
    if os.sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()

    # 启动应用
    app = QApplication(sys.argv)
    icon = QIcon(Path.resource_path('sinomine_logo.ico'))

    app.setWindowIcon(icon)

    # 启动splash窗口
    splashScreen = QSplashScreen()
    pixmap = QPixmap(Path.resource_path('master_splash.png'))
    splashScreen.setPixmap(pixmap)
    splashScreen.resize(pixmap.size())
    splashScreen.show()
    # splashScreen.showMessage('<h1><font color="green">让每个人都成为大师！</font></h1>', Qt.AlignTop | Qt.AlignCenter, Qt.white)

    # 启动主窗口
    mainWindow = MainWindow(config=config, logger=logger)
    mainWindow.setWindowIcon(icon)
    mainWindow.showMaximized()

    # 关闭splash
    splashScreen.finish(mainWindow)

    # 结束应用
    sys.exit(app.exec_())
