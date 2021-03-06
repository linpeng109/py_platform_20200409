import os
import signal
import subprocess
import time

import win32con
import win32gui
import win32process
from PySide2.QtGui import QWindow
from PySide2.QtWidgets import QWidget

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory


class PY_Win32():
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger

    # 启动执行文件返回进程pid
    def startProcess(self, cmd):
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True).pid
        self.pid = pid
        return pid

    # 从指定pid获取窗口句柄（通过回调函数）
    def getHwndFromPid(self, pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    # self.logger.debug(win32gui.GetWindowText(hwnd))
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    # 通过pid获取包含指定窗口特征名的窗口句柄
    def getTheMainWindow(self, pid, spTitle):
        hwnds = []
        while True:
            hwnds = self.getHwndFromPid(pid)
            if (len(hwnds) > 0):
                _title = win32gui.GetWindowText((hwnds[0]))
                if (spTitle in _title):
                    break
            time.sleep(1)
        return hwnds[0]

    # 从指定名称获取进程的pid数组
    def getPidsFromPName(self, pname: str, indexName: str, begin: int, end: int):
        _result = subprocess.Popen("tasklist|findstr " + pname, shell=True, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        _lines = _result.stdout.readlines()
        pids = []
        for pid in _lines:
            _begin = str(pid).index(indexName) + begin
            _end = _begin + end
            pids.append(str(pid)[_begin:_end].strip())
        return pids

    # 根据pid获取运行端口
    def getPortsFromPid(self, pid):
        io = subprocess.Popen("netstat -aon|findstr " + str(pid), shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
        lines = io.stdout.readlines()
        self.ports = []
        for line in lines:
            if 'LISTENING' in str(line):
                begin = str(line).index('0.0.0.0:') + 8
                end = begin + 15
                port = int(str(line)[begin:end].strip())
                self.ports.append(port)
        return self.ports

    # 关闭列出的所有进程id号的进程
    def killProcess(self, pids):
        for pid in pids:
            _pid = int(pid)
            try:
                os.kill(_pid, signal.SIGTERM)
                self.logger.debug('Process(pid=%s) has be killed' % pid)
            except OSError:
                self.logger.debug('no such process(pid=%s)' % pid)

    # 显示窗口
    def showWindow(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    # 隐含窗口
    def hiddenWindow(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # 关闭窗口
    def closeWindow(self, hwnd):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE)

    # 设置窗口样式
    def setNoTitleWindow(self, hwnd):
        ISTYLE = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(hwnd,
                               ISTYLE &
                               ~win32con.WS_CAPTION &
                               win32con.SWP_NOMOVE &
                               win32con.SWP_NOSIZE)

    # 将一个窗口句柄转化为一个标准Widget
    def convertWndToWidget(self, hwnd):
        native_wnd = QWindow.fromWinId(hwnd)
        return QWidget.createWindowContainer(native_wnd)
