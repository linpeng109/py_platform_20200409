import multiprocessing
import os
import sys

from PySide2.QtWidgets import QApplication

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_mainWindow import MainWindow

if __name__ == '__main__':
    # win环境编译时应用，解决win环境mutilprocess的fork兼容问题
    if os.sys.platform.startswith('win'):
        multiprocessing.freeze_support()
    # 设置配置文件和日志
    config = ConfigFactory(config='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    # 启动应用
    app = QApplication(sys.argv)
    # 启动主窗口
    mainWindow = MainWindow(config=config, logger=logger)
    mainWindow.showMaximized()
    # 结束应用
    sys.exit(app.exec_())