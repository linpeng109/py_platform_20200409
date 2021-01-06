# encoding:utf-8
import ctypes
import winreg
from configparser import ConfigParser
from logging import Logger

from py_config import ConfigFactory
from py_logging import LoggerFactory


class WinRegist():
    def __init__(self, config: ConfigParser, logger: Logger):
        self.config = config
        self.logger = logger

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def getHKeyHandle(self, reg_root, reg_sub: str):
        # 连接注册表根键
        reg_root = winreg.ConnectRegistry(None, reg_root)
        # 获得指定键的操作句柄
        reg_handle = winreg.OpenKey(reg_root, reg_sub)
        return reg_handle

    def getHKeyValue(self, reg_root, reg_sub, key: str):
        # 连接注册表根键
        reg_root = winreg.ConnectRegistry(None, reg_root)
        # 获得指定键的操作句柄
        reg_handle = winreg.OpenKey(reg_root, reg_sub)
        # 获取键值
        result = winreg.QueryValueEx(reg_handle, key)[0]
        # 关闭键
        winreg.CloseKey(reg_handle)
        winreg.CloseKey(reg_root)
        # 返回
        return result

    def getStartMenu(self):
        reg_root = winreg.HKEY_LOCAL_MACHINE
        reg_sub = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Backup'
        key = r'Start Menu'
        result = self.getHKeyValue(reg_root=reg_root, reg_sub=reg_sub, key=key)
        return result

    def getSurpacList(self):
        reg_root = winreg.HKEY_LOCAL_MACHINE
        reg_sub = r'SOFTWARE\Gemcom Software\Surpac'
        result = self.getHKeyHandle(reg_root=reg_root, reg_sub=reg_sub)

        return result


if __name__ == '__main__':
    config = ConfigFactory(config='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    reg = WinRegist(config=config, logger=logger)
    # start_menu_path = reg.getStartMenu()
    result = reg.getSurpacList()
    reg.logger.debug(result)
