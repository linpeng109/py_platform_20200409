import multiprocessing
import os
import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_path import Path
from widget.py_main_window import MainWindow

if __name__ == '__main__':

    # win环境编译时应用，解决win环境mutilprocess的fork兼容问题
    if os.sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_platform.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()

    # 启动应用
    app = QApplication(sys.argv)
    icon = QIcon(Path.get_resource_path('resource/sinomine_logo.ico'))

    app.setWindowIcon(icon)

    # 启动splash窗口
    # splashScreen = QSplashScreen()
    # pixmap = QPixmap(Path.get_resource_path('master_splash.png'))
    # splashScreen.setPixmap(pixmap)
    # splashScreen.resize(pixmap.size())
    # splashScreen.show()
    # splashScreen.showMessage('<h1><font color="green">让每个人都成为大师！</font></h1>', Qt.AlignTop | Qt.AlignCenter, Qt.white)

    # 启动主窗口
    mainWindow = MainWindow(config=config, logger=logger)
    mainWindow.setWindowIcon(icon)
    mainWindow.showMaximized()

    # 关闭splash
    # splashScreen.finish(mainWindow)

    # 结束应用
    sys.exit(app.exec_())
