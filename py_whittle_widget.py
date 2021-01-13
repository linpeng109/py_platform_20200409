# encoding:utf-8
import os

# 生成whillte工作区widget
from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_pywin32 import PY_Win32
from py_start_whittle_dialog import StartWhittleDialog


class WhittleWidget():
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.logger = logger
        self.config = config
        self.py_win32 = PY_Win32(logger=logger, config=config)

        # 生成版本选择窗口
        self.startWhittleDialog = StartWhittleDialog(config=config, logger=logger, title='请选择Whittle版本')

        # 是否kill当前环境中所有已经启动的whittle进程
        if self.config.get('whittle', 'whittle_kill_other_process'):
            pids = self.py_win32.getPidsFromPName(pname='Whittle', indexName='Whittle.exe', begin=11, end=24)
            self.py_win32.killProcess(pids=pids)

    # 生成Whittle工作区widget
    def build_whittle_widget(self, cmd: str):
        # self.killProcess([self.pid])
        self.whittle_pid = self.py_win32.startProcess(cmd)
        hwnd = self.py_win32.getTheMainWindow(pid=self.whittle_pid, spTitle='Whittle')
        self.whittle_widget = self.py_win32.convertWndToWidget(hwnd=hwnd)
        return self.whittle_widget, self.whittle_pid

    # 检查whittle配置是否正确
    def check_whittle_location_config(self):
        whittle_location = self.config.get('whittle', 'whittle_location')
        return os.path.isfile(whittle_location)
