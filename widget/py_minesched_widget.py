# encoding:utf-8
import os

from dialog.py_start_minesched_dialog import StartMineSchedDialog
# 生成minesched工作区widget
from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_pywin32 import PY_Win32
from util.py_shortcuts import ShortCuts


class MineschedWidget():
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.shortCut = ShortCuts(config=config, logger=logger)
        self.py_win32 = PY_Win32(config=config, logger=logger)

        # 生成版本选择窗口
        self.startMineSchedDialog = StartMineSchedDialog(config=config, logger=logger, title='请选择MineSched版本')

        # 是否kill当前环境中所有已经启动的minesched进程
        if self.config.get('minesched', 'minesched_kill_other_process'):
            pids = self.py_win32.getPidsFromPName(pname='MineSched', indexName='MineSched.exe', begin=13, end=22)
            self.py_win32.killProcess(pids=pids)

    # 生成minesched工作区widget
    def build_minesched_widget(self, cmd: str):
        self.minesched_pid = self.py_win32.startProcess(cmd)
        hwnd = self.py_win32.getTheMainWindow(pid=self.minesched_pid, spTitle='MineSched')
        self.minesched_widget = self.py_win32.convertWndToWidget(hwnd=hwnd)
        return self.minesched_widget, self.minesched_pid

    # 检查minesched安装位置
    def check_minesched_location_config(self):
        minesched_location = self.config.get('minesched', 'minesched_location')
        return os.path.isfile(minesched_location)


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='../py_platform.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()

    minesched = MineschedWidget(config=config, logger=logger)
    pids = minesched.getPidsFromPName('MineSched')
    logger.debug(pids)
    minesched.killProcess(pids=pids)
