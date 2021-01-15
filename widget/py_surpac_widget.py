# encoding:utf-8
import os

from dialog.py_start_surpac_dialog import StartSurpacDialog
# 生成surpac工作区
from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_pywin32 import PY_Win32
from util.py_shortcuts import ShortCuts


class Surpac():
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.logger = logger
        self.config = config
        self.surpac_pid = -1
        self.shortcuts = ShortCuts(config=config, logger=logger)
        self.py_win32 = PY_Win32(config=config, logger=logger)

        # 生成surpac不同版本选择窗口
        self.startSurpacDialog = StartSurpacDialog(config=config, logger=logger, title='请选择Surpac版本')

        # 清理旧surpac进程
        if self.config.get('master', 'surpac_kill_other_process'):
            pids = self.py_win32.getPidsFromPName(pname='surpac', indexName='surpac2.exe', begin=11, end=24)
            self.py_win32.killProcess(pids=pids)

    # 生成surpac工作区widget
    def build_surpac_widget(self, cmd: str):
        self.surpac_pid = self.py_win32.startProcess(cmd)
        hwnd = self.py_win32.getTheMainWindow(pid=self.surpac_pid, spTitle='Surpac')
        self.surpac_ports = self.py_win32.getPortsFromPid(pid=self.surpac_pid)
        self.surpac_widget = self.py_win32.convertWndToWidget(hwnd=hwnd)
        return self.surpac_widget, self.surpac_ports, self.surpac_pid

    # 获取surpac配置地址
    def check_surpac_location_config(self):
        surpac_location = self.config.get('master', 'surpac_location')
        return os.path.isfile(surpac_location)
